"""Tests for auto-eda's companion script (qat/tools/auto-eda.files/scripts/auto_eda.py).

Needs pandas and matplotlib; skips when they are missing (the qat-skills CI job installs neither).
Run: python3 -I qat/scripts/test_auto_eda.py -v
"""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "auto-eda.files" / "scripts" / "auto_eda.py"
HAVE_DEPS = all(importlib.util.find_spec(m) for m in ("pandas", "matplotlib"))


def load_module():
    spec = importlib.util.spec_from_file_location("auto_eda", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["auto_eda"] = mod  # dataclasses look the module up while it loads
    spec.loader.exec_module(mod)
    return mod


@unittest.skipUnless(HAVE_DEPS, "pandas and matplotlib not installed")
class AutoEdaTest(unittest.TestCase):
    def setUp(self):
        self.ae = load_module()
        self.tmp = Path(tempfile.mkdtemp())

    def run_on(self, name, text):
        src = self.tmp / name
        src.write_text(text)
        out = self.tmp / "out"
        self.ae.run(src, out, None)
        return json.loads((out / f"{src.stem}_eda.json").read_text())

    def test_nested_jsonl_is_flattened_not_crashing(self):
        lines = [json.dumps({"a": i, "b": {"c": "xy"[i % 2]}, "tags": ["t", str(i % 3)]}) for i in range(30)]
        summary = self.run_on("nested.jsonl", "\n".join(lines) + "\n")
        names = [p["name"] for p in summary["profiles"]]
        self.assertIn("b.c", names)                      # flattened, as the .json branch does
        self.assertNotIn("b", names)
        tags = next(p for p in summary["profiles"] if p["name"] == "tags")
        self.assertEqual(tags["n_unique"], 3)            # list cells profiled as JSON text

    def test_nested_json_and_jsonl_agree(self):
        recs = [{"a": i, "b": {"c": "xy"[i % 2]}} for i in range(20)]
        j = self.run_on("p.json", json.dumps({"data": recs}))
        jl = self.run_on("p2.jsonl", "\n".join(json.dumps(r) for r in recs))
        self.assertEqual([p["name"] for p in j["profiles"]], [p["name"] for p in jl["profiles"]])

    def test_summary_carries_stats_and_correlations(self):
        rows = ["x,y,region"] + [f"{i},{2 * i + (i % 3)},{'NNS'[i % 3]}" for i in range(1, 61)]
        summary = self.run_on("t.csv", "\n".join(rows))
        prof = {p["name"]: p for p in summary["profiles"]}
        self.assertEqual(set(prof["x"]["stats"]),
                         {"count", "mean", "std", "min", "p25", "median", "p75", "max", "skew"})
        self.assertEqual(prof["x"]["stats"]["max"], 60)
        top = prof["region"]["stats"]["top"]
        self.assertEqual((top[0]["value"], top[0]["count"], top[0]["pct"]), ("N", 40, 66.7))
        self.assertEqual(prof["region"]["stats"]["pct_of"], "all rows")
        self.assertEqual(summary["correlations"][0]["a"], "x")
        self.assertGreater(summary["correlations"][0]["r"], 0.99)

    def test_category_pct_matches_chart_denominator(self):
        # Codex 4592993932: 90 missing, 6 A, 4 B -> A is 6% of rows (as the bar chart shows), not 60%.
        vals = [""] * 90 + ["A"] * 6 + ["B"] * 4
        summary = self.run_on("m.csv", "g,n\n" + "\n".join(f"{v},{i}" for i, v in enumerate(vals)))
        top = {d["value"]: d for d in next(p for p in summary["profiles"] if p["name"] == "g")["stats"]["top"]}
        self.assertEqual(top["A"]["pct"], 6.0)
        self.assertEqual(top["(missing)"]["count"], 90)


if __name__ == "__main__":
    unittest.main()
