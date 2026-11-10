#!/usr/bin/env python3
"""Tests for scripts/new.py (the QAT tool scaffold).

Run from qat/:  python3 -I -m unittest discover -s scripts -p "test_*.py"
             or python3 -I scripts/test_new.py

Every test writes into a fresh temporary directory (--root), so the repo is never
touched. What is tested, and why it matters:
  - a default scaffold validates under the unchanged runner (the whole point);
  - every runtime stub carries the spec's headings verbatim (the lesson from the
    first two tools, whose first cold runs failed on exactly this);
  - refusals write nothing (bad name, bad description, existing file);
  - --json is parseable and carries the fields an agent needs.
"""

import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import new  # noqa: E402  (the module under test, imported from this directory)


def run(*argv):
    """Run new.main() with argv; return (exit code, stdout)."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = new.main(list(argv))
    return code, buf.getvalue()


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def files(self):
        return sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*") if p.is_file())

    def test_default_scaffold_validates(self):
        code, out = run("demo-tool", "--root", str(self.root))
        self.assertEqual(code, 0, out)
        self.assertIn("validate OK", out)
        self.assertEqual(self.files(), [
            "cases/demo-tool.eval.yaml",
            "cases/fixtures/demo-tool.example.md",
            "tools/demo-tool.qat.md",
        ])

    def test_all_options(self):
        code, out = run("demo-tool", "--root", str(self.root), "--design",
                        "--runtime", "chatgpt", "--runtime", "skill",
                        "--description", "Demonstrates every scaffold option for the tests.")
        self.assertEqual(code, 0, out)
        self.assertIn("tools/demo-tool.DESIGN.md", self.files())
        self.assertIn("runtimes/chatgpt/demo-tool.paste.md", self.files())
        self.assertIn("runtimes/claude/demo-tool/SKILL.md", self.files())

    def test_runtime_stubs_name_every_heading_and_format(self):
        run("demo-tool", "--root", str(self.root), "--runtime", "chatgpt", "--runtime", "skill")
        for rel in ("runtimes/chatgpt/demo-tool.paste.md", "runtimes/claude/demo-tool/SKILL.md"):
            text = (self.root / rel).read_text()
            for _, _, heading, fmt in new.DEFAULT_OUTPUTS:
                self.assertIn(f"`## {heading}`: {fmt}", text, rel)

    def test_eval_stub_is_yaml_and_names_the_tool(self):
        import yaml
        run("demo-tool", "--root", str(self.root))
        data = yaml.safe_load((self.root / "cases/demo-tool.eval.yaml").read_text())
        self.assertEqual(data["tool"], "demo-tool")
        self.assertEqual([c["id"] for c in data["cases"]], ["ordinary", "failure-mode-1"])

    def test_bad_name_refused_and_nothing_written(self):
        code, out = run("Bad_Name", "--root", str(self.root))
        self.assertEqual(code, 2)
        self.assertIn("REFUSED", out)
        self.assertEqual(self.files(), [])

    def test_short_description_refused(self):
        code, _ = run("demo-tool", "--root", str(self.root), "--description", "too short")
        self.assertEqual(code, 2)
        self.assertEqual(self.files(), [])

    def test_existing_file_refused_and_nothing_overwritten(self):
        spec = self.root / "tools" / "demo-tool.qat.md"
        spec.parent.mkdir(parents=True)
        spec.write_text("mine")
        code, out = run("demo-tool", "--root", str(self.root), "--design")
        self.assertEqual(code, 2)
        self.assertIn("already exists", out)
        self.assertEqual(spec.read_text(), "mine")
        self.assertEqual(self.files(), ["tools/demo-tool.qat.md"])  # all or nothing

    def test_yaml_scalar_names_remain_strings_in_every_template(self):
        import yaml
        for name in ("true", "false", "null", "123", "0123", "yes", "no", "on", "off"):
            with self.subTest(name=name):
                root = self.root / name
                code, out = run(name, "--root", str(root), "--runtime", "skill", "--json")
                self.assertEqual(code, 0, out)
                for relative, key in ((f"tools/{name}.qat.md", "name"),
                                      (f"cases/{name}.eval.yaml", "tool"),
                                      (f"runtimes/claude/{name}/SKILL.md", "name")):
                    text = (root / relative).read_text()
                    document = text.split("---", 2)[1] if text.startswith("---") else text
                    self.assertEqual(yaml.safe_load(document)[key], name)

    def test_dangling_target_symlinks_refused_without_outside_writes(self):
        targets = new.plan(self.root, "demo-tool", "description", ["chatgpt", "skill"], True)
        with tempfile.TemporaryDirectory() as outside:
            for index, target in enumerate(targets):
                with self.subTest(target=str(target.relative_to(self.root))):
                    destination = Path(outside) / str(index)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.symlink_to(destination)
                    code, out = run("demo-tool", "--root", str(self.root), "--design",
                                    "--runtime", "chatgpt", "--runtime", "skill", "--json")
                    self.assertEqual(code, 2, out)
                    res = json.loads(out)
                    self.assertEqual(res["created"], [])
                    self.assertIn("already exists", res["error"])
                    self.assertTrue(target.is_symlink())
                    self.assertFalse(destination.exists())
                    self.assertEqual(self.files(), [])
                    target.unlink()

    def test_blocked_directories_refused_before_any_writes(self):
        for relative in ("tools", "cases", "cases/fixtures", "runtimes/chatgpt",
                         "runtimes/claude/demo-tool"):
            with self.subTest(directory=relative), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                blocker = root / relative
                blocker.parent.mkdir(parents=True, exist_ok=True)
                blocker.write_text("mine")
                code, out = run("demo-tool", "--root", str(root), "--design",
                                "--runtime", "chatgpt", "--runtime", "skill", "--json")
                self.assertEqual(code, 2, out)
                res = json.loads(out)
                self.assertEqual(res["created"], [])
                self.assertIsNone(res["validate"])
                self.assertIn(relative, res["error"])
                self.assertEqual(blocker.read_text(), "mine")
                self.assertEqual([p for p in root.rglob("*") if p.is_file()], [blocker])

    def test_symlink_directories_refused_without_outside_writes(self):
        for relative in ("tools", "cases/fixtures", "runtimes/claude/demo-tool"):
            for dangling in (False, True):
                with self.subTest(directory=relative, dangling=dangling), \
                        tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
                    root = Path(temp)
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    destination = Path(outside) / "missing" if dangling else Path(outside)
                    target.symlink_to(destination, target_is_directory=True)
                    code, out = run("demo-tool", "--root", str(root), "--design",
                                    "--runtime", "chatgpt", "--runtime", "skill", "--json")
                    self.assertEqual(code, 2, out)
                    res = json.loads(out)
                    self.assertEqual(res["created"], [])
                    self.assertIsNone(res["validate"])
                    self.assertIn(relative, res["error"])
                    self.assertEqual(list(Path(outside).iterdir()), [])
                    self.assertFalse(any(p.is_file() for p in root.rglob("*")))

    def test_non_directory_root_refused_as_json(self):
        root = self.root / "blocked"
        root.write_text("mine")
        code, out = run("demo-tool", "--root", str(root), "--json")
        self.assertEqual(code, 2, out)
        self.assertEqual(json.loads(out)["created"], [])
        self.assertEqual(root.read_text(), "mine")

    def test_write_failure_rolls_back_files_and_new_directories(self):
        original_open = Path.open

        def fail_fixture(path, *args, **kwargs):
            if path.name.endswith(".example.md"):
                raise PermissionError("injected fixture write failure")
            return original_open(path, *args, **kwargs)

        with patch.object(Path, "open", fail_fixture):
            code, out = run("demo-tool", "--root", str(self.root), "--json")
        self.assertEqual(code, 2, out)
        res = json.loads(out)
        self.assertEqual(res["created"], [])
        self.assertIn("injected fixture write failure", res["error"])
        self.assertEqual(list(self.root.iterdir()), [])

    def test_exclusive_create_preserves_late_target(self):
        original_open = Path.open
        target = self.root / "cases/fixtures/demo-tool.example.md"

        def add_late_target(path, *args, **kwargs):
            if path == target and args and args[0] == "x":
                with original_open(path, "w") as output:
                    output.write("created by someone else")
            return original_open(path, *args, **kwargs)

        with patch.object(Path, "open", add_late_target):
            code, out = run("demo-tool", "--root", str(self.root), "--json")
        self.assertEqual(code, 2, out)
        res = json.loads(out)
        self.assertEqual(res["created"], [])
        self.assertEqual(self.files(), ["cases/fixtures/demo-tool.example.md"])
        self.assertEqual(target.read_text(), "created by someone else")

    def test_partial_write_failure_removes_incomplete_file(self):
        original_open = Path.open

        def fail_after_partial_write(path, *args, **kwargs):
            output = original_open(path, *args, **kwargs)
            if path.name.endswith(".example.md"):
                def write(text):
                    output.buffer.write(b"partial")
                    raise OSError("injected disk-full failure")
                output.write = write
            return output

        with patch.object(Path, "open", fail_after_partial_write):
            code, out = run("demo-tool", "--root", str(self.root), "--json")
        self.assertEqual(code, 2, out)
        self.assertIn("injected disk-full failure", json.loads(out)["error"])
        self.assertEqual(list(self.root.iterdir()), [])

    def test_json_result_for_agents(self):
        code, out = run("demo-tool", "--root", str(self.root), "--json")
        self.assertEqual(code, 0)
        res = json.loads(out)
        self.assertTrue(res["ok"])
        self.assertTrue(res["validate"]["ok"])
        self.assertEqual(len(res["created"]), 3)
        self.assertIsNone(res["error"])
        self.assertTrue(res["next"])

    def test_json_refusal(self):
        code, out = run("Nope", "--root", str(self.root), "--json")
        self.assertEqual(code, 2)
        res = json.loads(out)
        self.assertFalse(res["ok"])
        self.assertIn("lowercase", res["error"])

    def test_control_characters_in_names_refused_without_writes(self):
        for name in ("demo-tool\n", "demo-tool\r\n", "demo\ntool", "demo-tool\t"):
            with self.subTest(name=repr(name)):
                code, out = run(name, "--root", str(self.root), "--json")
                self.assertEqual(code, 2, out)
                result = json.loads(out)
                self.assertFalse(result["ok"])
                self.assertEqual(result["created"], [])
                self.assertIsNone(result["validate"])
                self.assertIn("lowercase", result["error"])
                self.assertEqual(list(self.root.iterdir()), [])

    def test_argument_parser_refusals_return_json_without_writes(self):
        cases = [
            ("demo-tool", "--runtime", "invalid-runtime"),
            ("demo-tool", "--bogus"),
            (),
            ("demo-tool", "--runtime"),
            ("demo-tool", "--d"),
        ]
        for args in cases:
            for json_args in (("--json", *args), (*args, "--json")):
                with self.subTest(args=json_args):
                    err = io.StringIO()
                    with redirect_stderr(err):
                        code, out = run("--root", str(self.root), *json_args)
                    self.assertEqual(code, 2, out)
                    result = json.loads(out)
                    self.assertFalse(result["ok"])
                    self.assertEqual(result["created"], [])
                    self.assertIsNone(result["validate"])
                    self.assertEqual(result["next"], [])
                    self.assertTrue(result["error"])
                    self.assertEqual(err.getvalue(), "")
                    self.assertEqual(list(self.root.iterdir()), [])

    def test_json_parser_refusals_work_through_cli_argv(self):
        for flag in ("--json", "--js", "--json=false"):
            with self.subTest(flag=flag):
                result = subprocess.run([sys.executable, "-I", "-B", str(Path(new.__file__)),
                                         "--root", str(self.root), "demo-tool",
                                         "--runtime", "invalid-runtime", flag],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertFalse(json.loads(result.stdout)["ok"])
                self.assertEqual(result.stderr, "")
                self.assertEqual(list(self.root.iterdir()), [])

    def test_parser_refusal_without_json_retains_argparse_behavior(self):
        err = io.StringIO()
        out = io.StringIO()
        with redirect_stderr(err), redirect_stdout(out), self.assertRaises(SystemExit) as raised:
            new.main(["demo-tool", "--runtime", "invalid-runtime"])
        self.assertEqual(raised.exception.code, 2)
        self.assertEqual(out.getvalue(), "")
        self.assertIn("usage:", err.getvalue())
        self.assertIn("invalid choice", err.getvalue())

    def test_json_after_option_terminator_is_only_a_name(self):
        code, out = run("--root", str(self.root), "--", "--json")
        self.assertEqual(code, 2)
        self.assertTrue(out.startswith("REFUSED"), out)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_help_remains_normal_successful_help(self):
        out = io.StringIO()
        with redirect_stdout(out), self.assertRaises(SystemExit) as raised:
            new.main(["--json", "--help"])
        self.assertEqual(raised.exception.code, 0)
        self.assertIn("usage:", out.getvalue())


if __name__ == "__main__":
    unittest.main()
