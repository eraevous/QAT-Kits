"""Regression tests for ThreadSeed's helper, seed_index.py, as embedded in qat/tools/thread-seed.skill.md.

The helper lives inside the skill text, so the tests extract the ```python block under "## seed_index.py"
and run it as a script, the way the skill tells a model to. Standard library only.
Run: python3 -I qat/scripts/test_thread_seed.py -v

The three cases come from the ChatGPT port findings carried upstream in HO-QAT-20261116-Y0HJ
(relay-kit-private): a nonexistent T2 in a T1/T3 capture, a wrong quote, and T1a text cited as T1a2.
"""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "tools" / "thread-seed.skill.md"


def extract_helper(dest: Path) -> Path:
    text = SKILL.read_text(encoding="utf-8")
    m = re.search(r"^## seed_index\.py\s*\n+```python\n(.*?)^```", text, re.S | re.M)
    if not m:
        raise AssertionError("no ```python block under '## seed_index.py' in " + str(SKILL))
    script = dest / "seed_index.py"
    script.write_text(m.group(1), encoding="utf-8")
    return script


def capture(turns):
    """turns: list of (n, role, [message texts])."""
    return {"turns": [{"n": n, "role": role, "label": "User" if role == "user" else "Claude",
                       "messages": [{"text": t, "ts": "2026-11-17T10:00"} for t in texts]}
                      for n, role, texts in turns]}


# A T1/T3 capture: exchange 2 is missing. T1 has two replies.
GAPPED = capture([
    (1, "user", ["Please keep the seed short and cite every claim you carry over."]),
    (1, "assistant", ["First reply: we agreed the budget stays at three pages for the successor.",
                      "Second reply: the reviewer is chosen by Zach, not by the lane."]),
    (3, "user", ["Thanks, now draft the open decisions section for the successor thread."]),
    (3, "assistant", ["Open decisions wait on Zach; the lane only proposes them."]),
])


class VerifyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.script = extract_helper(cls.tmp)
        cls.cap = cls.tmp / "capture.json"
        cls.cap.write_text(json.dumps(GAPPED), encoding="utf-8")

    def verify(self, seed_text):
        seed = self.tmp / "SEED.md"
        seed.write_text(seed_text, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(self.script), str(self.cap), "--verify", str(seed)],
                           capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    # Finding 1: a nonexistent turn below the maximum passed reference validation.
    def test_bare_ref_to_missing_exchange_fails(self):
        code, out = self.verify("Budget was settled earlier [T2].\n")
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL ref T2", out)

    def test_suffixed_ref_to_missing_exchange_fails(self):
        for ref in ("T2u", "T2a"):
            code, out = self.verify(f"See [{ref}].\n")
            self.assertEqual(code, 1, ref + ": " + out)
            self.assertIn(f"FAIL ref {ref}", out)

    def test_existing_refs_pass(self):
        code, out = self.verify("See [T1], [T1u], [T1a], [T1a1], [T1a2], [T3] and [T3a].\n")
        self.assertEqual(code, 0, out)

    def test_ref_beyond_max_still_fails(self):
        code, out = self.verify("See [T4].\n")
        self.assertEqual(code, 1, out)

    # Wrong quotes fail.
    def test_wrong_quote_fails(self):
        code, out = self.verify('"the budget stays at five pages for the successor" [T1a]\n')
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL quote", out)

    def test_quote_cited_to_missing_exchange_fails(self):
        code, out = self.verify('"the budget stays at three pages for the successor" [T2]\n')
        self.assertEqual(code, 1, out)

    # Finding 2: an exact assistant-reply reference could match a different reply.
    def test_first_reply_text_cited_as_second_reply_fails(self):
        code, out = self.verify('"the budget stays at three pages for the successor" [T1a2]\n')
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL quote", out)

    def test_second_reply_text_cited_as_first_reply_fails(self):
        for ref in ("T1a", "T1a1"):
            code, out = self.verify(f'"the reviewer is chosen by Zach, not by the lane" [{ref}]\n')
            self.assertEqual(code, 1, ref + ": " + out)

    def test_exact_reply_refs_pass(self):
        code, out = self.verify(
            '"the budget stays at three pages for the successor" [T1a]\n'
            '"the budget stays at three pages for the successor" [T1a1]\n'
            '"the reviewer is chosen by Zach, not by the lane" [T1a2]\n')
        self.assertEqual(code, 0, out)
        self.assertIn("verified 3 quotes; 0 failures", out)

    def test_bare_and_user_refs_keep_their_scope(self):
        code, out = self.verify(
            '"the reviewer is chosen by Zach, not by the lane" [T1]\n'
            '"keep the seed short and cite every claim" [T1u]\n')
        self.assertEqual(code, 0, out)
        code, out = self.verify('"keep the seed short and cite every claim" [T1a]\n')
        self.assertEqual(code, 1, out)

    # API Kate's coverage asks (reply 18acfb147f91 on HO-QAT-20261116-Y0HJ).
    def test_ref_to_missing_reply_fails(self):
        code, out = self.verify("See [T3a2].\n")  # exchange 3 has one reply
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL ref T3a2", out)

    def test_reply_text_cited_as_user_fails(self):
        code, out = self.verify('"the budget stays at three pages for the successor" [T1u]\n')
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL quote", out)


if __name__ == "__main__":
    unittest.main()
