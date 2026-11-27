#!/usr/bin/env python3
"""Tests for replay.py (stdlib unittest). Run from qat/: python3 -I scripts/test_replay.py

They check the properties the study design depends on: every grader sees every item
once; never the same item in both arms; the two graders see complementary arms; each
grader's arms are balanced overall and within each stratum; packets never show the arm;
the adjudication queue holds exactly the items where graders split on the key."""

import json
import shutil
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import replay  # noqa: E402

REAL_STUDY = replay.DEFAULT_STUDY


class ReplayTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for sub in ("items", "keys"):
            shutil.copytree(REAL_STUDY / sub, self.tmp / sub)
        self.out = replay.assign(self.tmp, seed=158)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _strata(self, tool):
        items = json.loads((self.tmp / "items" / f"{tool}.items.json").read_text())["items"]
        return {it["id"]: it["stratum"] for it in items}

    def test_counterbalance(self):
        for tool in replay.TOOLS:
            strata = self._strata(tool)
            g = self.out["tools"][tool]["graders"]
            seen = {gr: {r["item"]: r["arm"] for r in rows} for gr, rows in g.items()}
            for gr, rows in g.items():
                self.assertEqual(len(rows), len(strata), f"{tool}/{gr} sees every item")
                self.assertEqual(set(seen[gr]), set(strata), f"{tool}/{gr} sees each item once")
                arms = Counter(r["arm"] for r in rows)
                self.assertEqual(arms["A"], arms["B"], f"{tool}/{gr} arms balanced")
                for s in set(strata.values()):
                    per = Counter(r["arm"] for r in rows if strata[r["item"]] == s)
                    self.assertLessEqual(abs(per["A"] - per["B"]), 1, f"{tool}/{gr}/{s} balanced")
            for item in strata:
                self.assertNotEqual(seen["claude"][item], seen["kate"][item], f"{tool}/{item} complementary")

    def test_opaque_ids_hide_arm_and_item(self):
        for tool in replay.TOOLS:
            for rows in self.out["tools"][tool]["graders"].values():
                oids = [r["oid"] for r in rows]
                self.assertEqual(len(oids), len(set(oids)))
                for r in rows:
                    self.assertNotIn(r["item"], r["oid"])

    def test_deterministic(self):
        again = replay.assign(self.tmp, seed=158)
        self.assertEqual(self.out, again)

    def test_packet_needs_cards_and_hides_arm(self):
        with self.assertRaises(SystemExit):
            replay.packet(self.tmp, "claude", "kind-check")
        for arm in replay.ARMS:
            d = self.tmp / "runs" / "kind-check" / "cards" / arm
            d.mkdir(parents=True)
            for item in self._strata("kind-check"):
                (d / f"{item}.md").write_text("- Disposition: no action\n")
        text = replay.packet(self.tmp, "claude", "kind-check")
        self.assertNotIn("arm", text.lower().replace("charm", ""))
        self.assertNotIn("seen_in_design", text)
        self.assertEqual(text.count("**Response card:**"), 20)

    def test_tally_queue(self):
        tool = "real-problem"
        (self.tmp / "grades").mkdir()
        g = self.out["tools"][tool]["graders"]
        split_item = g["claude"][0]["item"]
        for grader, rows in g.items():
            lines = []
            for r in rows:
                key = "dispute" if (grader == "kate" and r["item"] == split_item) else "agree"
                lines.append(json.dumps({"oid": r["oid"], "defensible": "yes", "corrections": 0,
                                         "incorrect_commitment": False, "unnecessary_action": False,
                                         "missed_abstention": False, "invented_detail": False,
                                         "key": key, "key_note": "", "arm_guess": "unsure"}))
            (self.tmp / "grades" / f"{grader}.{tool}.jsonl").write_text("\n".join(lines) + "\n")
        res = replay.tally(self.tmp, tool)
        self.assertEqual([q["item"] for q in res["adjudication_queue"]], [split_item])
        self.assertEqual(res["arms"]["A"]["graded"] + res["arms"]["B"]["graded"], 40)
        self.assertEqual(res["problems"], [])
        self.assertEqual(res["blinding"], {"unsure": 40})
        res2 = replay.tally(self.tmp, tool, exclude_seen=True)
        self.assertEqual(res2["arms"]["A"]["graded"] + res2["arms"]["B"]["graded"], 40 - 2 * 6)

    def test_tally_rejects_invalid_grades(self):
        tool = "real-problem"
        (self.tmp / "grades").mkdir()
        graders = self.out["tools"][tool]["graders"]
        invalids = {
            ("claude", 0): ("key_note", None),
            ("claude", 1): ("corrections", "0"),
            ("kate", 0): ("incorrect_commitment", "false"),
            ("kate", 1): ("defensible", "maybe"),
        }
        for grader, rows in graders.items():
            lines = []
            for index, row in enumerate(rows):
                grade = {"oid": row["oid"], "defensible": "yes", "corrections": 0,
                         "incorrect_commitment": False, "unnecessary_action": False,
                         "missed_abstention": False, "invented_detail": False,
                         "key": "agree", "key_note": "", "arm_guess": "unsure"}
                invalid = invalids.get((grader, index))
                if invalid:
                    field, value = invalid
                    if value is None:
                        grade.pop(field)
                    else:
                        grade[field] = value
                lines.append(json.dumps(grade))
            (self.tmp / "grades" / f"{grader}.{tool}.jsonl").write_text("\n".join(lines) + "\n")
        res = replay.tally(self.tmp, tool)
        self.assertEqual(res["arms"]["A"]["graded"] + res["arms"]["B"]["graded"], 36)
        self.assertEqual(sum("invalid grade:" in problem for problem in res["problems"]), 4)
        self.assertTrue(any("missing key_note" in problem for problem in res["problems"]))
        self.assertTrue(any("corrections must be 0, 1, or 2" in problem for problem in res["problems"]))
        self.assertTrue(any("incorrect_commitment must be a boolean" in problem for problem in res["problems"]))
        self.assertTrue(any("defensible must be one of yes, partly, no" in problem for problem in res["problems"]))

    def _write_grades(self, tool, extra=None):
        (self.tmp / "grades").mkdir(exist_ok=True)
        for grader, rows in self.out["tools"][tool]["graders"].items():
            lines = [json.dumps({"oid": r["oid"], "defensible": "yes", "corrections": 0,
                                 "incorrect_commitment": False, "unnecessary_action": False,
                                 "missed_abstention": False, "invented_detail": False,
                                 "key": "agree", "key_note": "", "arm_guess": "unsure"}) for r in rows]
            lines += (extra or {}).get(grader, [])
            (self.tmp / "grades" / f"{grader}.{tool}.jsonl").write_text("\n".join(lines) + "\n")

    def test_tally_duplicate_grade_counts_neither(self):
        # A second line for the same opaque id used to replace the first silently,
        # so an appended grade could flip the tally with no problem reported.
        tool = "real-problem"
        first = self.out["tools"][tool]["graders"]["claude"][0]["oid"]
        flipped = json.dumps({"oid": first, "defensible": "no", "corrections": 2,
                              "incorrect_commitment": True, "unnecessary_action": False,
                              "missed_abstention": False, "invented_detail": False,
                              "key": "dispute", "key_note": "changed", "arm_guess": "tool"})
        self._write_grades(tool, {"claude": [flipped]})
        res = replay.tally(self.tmp, tool)
        self.assertEqual(res["arms"]["A"]["graded"] + res["arms"]["B"]["graded"], 39)
        self.assertNotIn("defensible_no", res["arms"]["A"])
        self.assertNotIn("defensible_no", res["arms"]["B"])
        self.assertTrue(any(f"duplicate grade for {first}" in p for p in res["problems"]))
        self.assertTrue(any(f"missing grade {first}" in p for p in res["problems"]))

    def test_non_utf8_inputs_are_reported_not_raised(self):
        tool = "real-problem"
        self._write_grades(tool)
        (self.tmp / "grades" / f"kate.{tool}.jsonl").write_bytes(b"\xff\xfe not text\n")
        res = replay.tally(self.tmp, tool)
        self.assertTrue(any(f"cannot read kate.{tool}.jsonl" in p for p in res["problems"]))
        self.assertEqual(res["arms"]["A"]["graded"] + res["arms"]["B"]["graded"], 20)
        (self.tmp / "keys" / f"{tool}.key.json").write_bytes(b"\xff")
        with self.assertRaises(SystemExit) as cm:
            replay.tally(self.tmp, tool)
        self.assertIn("cannot read", str(cm.exception.code))
        for arm in replay.ARMS:
            d = self.tmp / "runs" / "kind-check" / "cards" / arm
            d.mkdir(parents=True)
            for item in self._strata("kind-check"):
                (d / f"{item}.md").write_bytes(b"\xff")
        with self.assertRaises(SystemExit) as cm:
            replay.packet(self.tmp, "claude", "kind-check")
        self.assertIn("cannot read", str(cm.exception.code))


if __name__ == "__main__":
    unittest.main(verbosity=2)
