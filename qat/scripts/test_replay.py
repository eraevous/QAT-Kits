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
                                         "key": key, "arm_guess": "unsure"}))
            (self.tmp / "grades" / f"{grader}.{tool}.jsonl").write_text("\n".join(lines) + "\n")
        res = replay.tally(self.tmp, tool)
        self.assertEqual([q["item"] for q in res["adjudication_queue"]], [split_item])
        self.assertEqual(res["arms"]["A"]["graded"] + res["arms"]["B"]["graded"], 40)
        self.assertEqual(res["problems"], [])
        self.assertEqual(res["blinding"], {"unsure": 40})
        res2 = replay.tally(self.tmp, tool, exclude_seen=True)
        self.assertEqual(res2["arms"]["A"]["graded"] + res2["arms"]["B"]["graded"], 40 - 2 * 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
