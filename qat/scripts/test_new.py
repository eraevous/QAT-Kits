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
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
