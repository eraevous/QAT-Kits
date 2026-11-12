#!/usr/bin/env python3
"""Tests for scripts/skills.py (generated Claude skills, staleness check, gates, packaging).

Run from qat/:  python3 -I -m unittest discover -s scripts -p "test_*.py"

Each test copies qat/ into a fresh temporary git repository and runs the copied script there,
so the real repo is never touched. What is tested, and why it matters:
  - the committed generated files are current (the same check CI runs);
  - a generated file edited by hand, or a source edited without a rebuild, is reported STALE;
  - the stamp carries the version, the source's sha256 and the source path;
  - a changed spec needs a version bump and a recorded eval run (DEC-193 eval gate);
  - changed skills need a bundle version bump;
  - packaging is deterministic and carries the plugin manifest.
"""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

QAT = Path(__file__).resolve().parent.parent


def sh(cwd, *args, check=True):
    return subprocess.run(list(args), cwd=cwd, capture_output=True, text=True, check=check)


class SkillsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        shutil.copytree(QAT, self.repo / "qat", ignore=shutil.ignore_patterns("__pycache__"))
        # Stable synthetic fixtures, so the tests don't depend on any real skill's version, cases or
        # wording, or on the real bundle version.
        (self.repo / "qat/tools/zz-fixture.skill.md").write_text(
            '---\nname: "zz-fixture"\nversion: 1.0.0\ndescription: "Synthetic test skill."\n---\n\n# FixtureWord\n')
        (self.repo / "qat/runtimes/claude/BUNDLE_VERSION").write_text("5.0.0\n")
        sh(self.repo, sys.executable, "-I", "qat/scripts/skills.py", "build")
        for args in (["init", "-q"], ["config", "user.email", "t@example.invalid"], ["config", "user.name", "t"],
                     ["add", "-A"], ["commit", "-qm", "base"], ["tag", "base"]):
            sh(self.repo, "git", *args)

    def tearDown(self):
        self.tmp.cleanup()

    def run_skills(self, *args):
        r = sh(self.repo, sys.executable, "-I", "qat/scripts/skills.py", *args, check=False)
        return r.returncode, r.stdout + r.stderr

    def edit(self, rel, old, new):
        p = self.repo / rel
        text = p.read_text()
        self.assertIn(old, text)
        p.write_text(text.replace(old, new, 1))

    def append(self, rel, text):
        p = self.repo / rel
        p.write_text(p.read_text() + text)

    def commit(self):
        sh(self.repo, "git", "add", "-A")
        sh(self.repo, "git", "commit", "-qm", "change")

    def test_committed_files_are_current(self):
        code, out = self.run_skills("check")
        self.assertEqual(code, 0, out)

    def test_stamp(self):
        src = self.repo / "qat/tools/zz-fixture.skill.md"
        gen = (self.repo / "qat/runtimes/claude/zz-fixture/SKILL.md").read_text()
        self.assertTrue(gen.startswith("---\nname:"))
        self.assertNotIn("\nversion:", gen.split("\n---\n", 1)[0])   # frontmatter stays name + description
        self.assertIn("from qat/tools/zz-fixture.skill.md", gen)
        self.assertIn("version: 1.0.0", gen)
        self.assertIn(hashlib.sha256(src.read_bytes()).hexdigest(), gen)

    def test_hand_edit_is_stale(self):
        self.edit("qat/runtimes/claude/zz-fixture/SKILL.md", "FixtureWord", "FixtureWordX")
        code, out = self.run_skills("check")
        self.assertEqual(code, 1)
        self.assertIn("STALE qat/runtimes/claude/zz-fixture/SKILL.md", out)

    def test_source_edit_without_build_is_stale_then_build_fixes(self):
        self.edit("qat/tools/zz-fixture.skill.md", "FixtureWord", "FixtureWordX")
        code, out = self.run_skills("check")
        self.assertEqual(code, 1)
        self.assertIn("STALE", out)
        self.assertEqual(self.run_skills("build")[0], 0)
        self.assertEqual(self.run_skills("check")[0], 0)

    def test_runner_file_change_is_stale(self):
        self.append("qat/tools/stress-test.qat.md", "\nTest-only line.\n")
        code, out = self.run_skills("check")
        self.assertEqual(code, 1)
        self.assertIn("STALE qat/runtimes/claude/qat/tools/stress-test.qat.md", out)

    def test_gate_requires_version_bump_and_eval(self):
        self.edit("qat/tools/zz-fixture.skill.md", "FixtureWord", "FixtureWordX")
        self.run_skills("build")
        self.commit()
        code, out = self.run_skills("check", "--base", "base")
        self.assertEqual(code, 1)
        self.assertIn("VERSION_NOT_BUMPED qat/tools/zz-fixture.skill.md", out)
        self.assertIn("EVAL_NOT_RECORDED qat/tools/zz-fixture.skill.md", out)
        self.assertIn("has no cases yet", out)
        self.assertIn("BUNDLE_NOT_BUMPED", out)

    def test_gate_passes_with_bump_and_recorded_eval(self):
        self.edit("qat/tools/zz-fixture.skill.md", "FixtureWord", "FixtureWordX")
        self.edit("qat/tools/zz-fixture.skill.md", "version: 1.0.0", "version: 1.1.0")
        (self.repo / "qat/runtimes/claude/BUNDLE_VERSION").write_text("5.1.0\n")
        run = self.repo / "qat/eval-runs/2026-12-01/zz-fixture/RESULTS.md"
        run.parent.mkdir(parents=True)
        run.write_text("synthetic case: PASS\n")
        self.run_skills("build")
        self.commit()
        code, out = self.run_skills("check", "--base", "base")
        self.assertEqual(code, 0, out)

    def test_eval_for_another_tool_does_not_count(self):
        self.edit("qat/tools/zz-fixture.skill.md", "version: 1.0.0", "version: 1.1.0")
        (self.repo / "qat/runtimes/claude/BUNDLE_VERSION").write_text("5.1.0\n")
        run = self.repo / "qat/eval-runs/2026-12-01/truth-weight/RESULTS.md"
        run.parent.mkdir(parents=True)
        run.write_text("x\n")
        self.run_skills("build")
        self.commit()
        code, out = self.run_skills("check", "--base", "base")
        self.assertIn("EVAL_NOT_RECORDED qat/tools/zz-fixture.skill.md", out)

    def test_deleted_eval_run_does_not_count(self):
        run = self.repo / "qat/eval-runs/2026-12-01/zz-fixture/RESULTS.md"
        run.parent.mkdir(parents=True)
        run.write_text("old run\n")
        self.commit()
        sh(self.repo, "git", "tag", "-f", "base")
        self.edit("qat/tools/zz-fixture.skill.md", "version: 1.0.0", "version: 1.1.0")
        (self.repo / "qat/runtimes/claude/BUNDLE_VERSION").write_text("5.1.0\n")
        run.unlink()
        self.run_skills("build")
        self.commit()
        code, out = self.run_skills("check", "--base", "base")
        self.assertEqual(code, 1, out)
        self.assertIn("EVAL_NOT_RECORDED qat/tools/zz-fixture.skill.md", out)

    def test_gate_applies_to_qat_specs(self):
        self.append("qat/tools/stress-test.qat.md", "\nTest-only line.\n")
        (self.repo / "qat/runtimes/claude/BUNDLE_VERSION").write_text("5.0.1\n")
        self.run_skills("build")
        self.commit()
        code, out = self.run_skills("check", "--base", "base")
        self.assertIn("VERSION_NOT_BUMPED qat/tools/stress-test.qat.md", out)
        self.assertIn("EVAL_NOT_RECORDED qat/tools/stress-test.qat.md", out)
        self.assertIn("qat.py eval", out)

    def test_removed_source_drops_generated_dir(self):
        (self.repo / "qat/tools/zz-fixture.skill.md").unlink()
        self.assertEqual(self.run_skills("check")[0], 1)
        self.run_skills("build")
        self.assertFalse((self.repo / "qat/runtimes/claude/zz-fixture").exists())
        self.assertTrue((self.repo / "qat/runtimes/claude/kind-check/SKILL.md").exists())  # hand-written, untouched
        self.assertEqual(self.run_skills("check")[0], 0)

    def test_invalid_version_refused(self):
        self.edit("qat/tools/zz-fixture.skill.md", "version: 1.0.0", "version: one")
        code, out = self.run_skills("check")
        self.assertEqual(code, 1)
        self.assertIn("SPEC_INVALID", out)

    def test_semver_precedence(self):
        sys.path.insert(0, str(self.repo / "qat/scripts"))
        try:
            import skills
        finally:
            sys.path.pop(0)
        order = ["1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha.beta", "1.0.0-beta", "1.0.0-beta.2",
                 "1.0.0-beta.11", "1.0.0-rc.1", "1.0.0-rc.9", "1.0.0-rc.10", "1.0.0", "1.0.1", "1.10.0"]
        self.assertEqual(sorted(order, key=skills.version_key), order)
        self.assertLess(skills.version_key("0.1.0-reconstruction"), skills.version_key("0.1.0"))

    def test_runner_carries_runtime_tables(self):
        files = json.loads((self.repo / "qat/runtimes/claude/skills.lock.json").read_text())["skills"]["qat"]["files"]
        self.assertIn("runtimes/chatgpt/effort-cost.paste.md", files)
        self.assertIn("runtimes/chatgpt/effort-cost.card.md", files)
        paste = (self.repo / "qat/runtimes/claude/qat/runtimes/chatgpt/effort-cost.paste.md").read_text()
        self.assertIn("TABLE D.", paste)

    def test_package_is_deterministic(self):
        outs = []
        for i in range(2):
            d = self.repo / f"dist{i}"
            code, out = self.run_skills("package", str(d))
            self.assertEqual(code, 0, out)
            outs.append((d / "SHA256SUMS").read_text())
        self.assertEqual(outs[0], outs[1])
        bundle = (self.repo / "qat/runtimes/claude/BUNDLE_VERSION").read_text().strip()
        with zipfile.ZipFile(self.repo / "dist0" / f"qat-kit-{bundle}.zip") as z:
            names = set(z.namelist())
            manifest = json.loads(z.read(".claude-plugin/plugin.json"))
        self.assertEqual(manifest["version"], bundle)
        self.assertIn("skills/truth-weight/SKILL.md", names)
        self.assertIn("skills/qat/scripts/qat.py", names)
        with zipfile.ZipFile(self.repo / "dist0/zz-fixture-1.0.0.zip") as z:
            self.assertEqual(z.namelist(), ["zz-fixture/SKILL.md"])

    def test_package_refuses_nonempty_out_dir(self):
        d = self.repo / "dist"
        d.mkdir()
        (d / "old-1.0.0.zip").write_bytes(b"stale")
        code, out = self.run_skills("package", str(d))
        self.assertEqual(code, 1)
        self.assertIn("not empty", out)

    def test_checksums_match_release_asset_names(self):
        d = self.repo / "dist"
        self.assertEqual(self.run_skills("package", str(d))[0], 0)
        for line in (d / "SHA256SUMS").read_text().splitlines():
            name = line.split("  ", 1)[1]
            self.assertNotIn("/", name)            # release assets are flat; `sha256sum -c` must work on them
            self.assertTrue((d / name).is_file())

    def test_package_refuses_stale(self):
        self.edit("qat/tools/zz-fixture.skill.md", "FixtureWord", "FixtureWordX")
        code, out = self.run_skills("package", str(self.repo / "dist"))
        self.assertEqual(code, 1)
        self.assertFalse((self.repo / "dist").exists())


if __name__ == "__main__":
    unittest.main()
