"""Tests for auto-eda's companion script (qat/tools/auto-eda.files/scripts/auto_eda.py).

Needs pandas (and numpy, which pandas brings); skips when it is missing (the qat-skills CI job
does not install it). matplotlib is not needed: since 2.0 the charts are inline SVG.
Run: python3 -I qat/scripts/test_auto_eda.py -v
"""
import importlib.util
import json
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "auto-eda.files" / "scripts" / "auto_eda.py"
HAVE_DEPS = importlib.util.find_spec("pandas") is not None


def load_module():
    spec = importlib.util.spec_from_file_location("auto_eda", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["auto_eda"] = mod  # dataclasses look the module up while it loads
    for name in [n for n in sys.modules if n.startswith("auto_eda_plugin_")]:
        del sys.modules[name]       # plugins register into this fresh module, not the last one
    spec.loader.exec_module(mod)
    return mod


@unittest.skipUnless(HAVE_DEPS, "pandas not installed")
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

    def test_summary_is_strict_json_with_infinite_values(self):
        # Copilot 4593532067: inf, and a finite max that overflows when rounded, must not
        # reach the file as bare Infinity tokens.
        rows = ["v,w"] + [f"{i},{i}" for i in range(20)] + ["inf,1.7976931348623157e308"]
        self.run_on("inf.csv", "\n".join(rows))
        text = (self.tmp / "out" / "inf_eda.json").read_text()
        json.loads(text, parse_constant=lambda c: self.fail(f"non-finite token {c} in summary"))
        stats = {p["name"]: p["stats"] for p in json.loads(text)["profiles"]}
        self.assertIsNone(stats["v"]["max"])
        self.assertIsNone(stats["w"]["max"])


    # --- 2.0: charts are inline SVG (DEC-266 (1)) -------------------------------------------

    def report(self, name, text):
        self.run_on(name, text)
        return (self.tmp / "out" / f"{Path(name).stem}_eda.html").read_text()

    def svgs(self, html_text):
        return re.findall(r"<svg\b.*?</svg>", html_text, flags=re.S)

    def chart(self, html_text, label_start):
        hits = [s for s in self.svgs(html_text) if re.search(r'aria-label="' + re.escape(label_start), s)]
        self.assertEqual(len(hits), 1, f"expected one chart labelled {label_start!r}")
        return hits[0]

    def test_report_has_svg_charts_and_no_images(self):
        rows = ["region,amount,when,score"] + [
            f"{'NNSEW'[i % 5]},{(i * 7) % 50 if i % 9 else ''},2026-01-{1 + i % 28:02d},{(i * 13) % 17}"
            for i in range(80)]
        html_text = self.report("r.csv", "\n".join(rows))
        self.assertNotIn("<img", html_text)
        self.assertNotIn("base64", html_text)
        self.assertNotIn("matplotlib", html_text)
        summary = json.loads((self.tmp / "out" / "r_eda.json").read_text())
        self.assertEqual(len(self.svgs(html_text)), len(summary["charts"]))
        for svg in self.svgs(html_text):   # accessible: role, label and a <title> first
            self.assertIn('role="img"', svg)
            self.assertRegex(svg, r'aria-label="[^"]+"')
            self.assertRegex(svg, r"^<svg[^>]*><title>[^<]+</title>")
            ET.fromstring(svg)              # well-formed XML on its own

    def test_bar_chart_text_and_counts(self):
        vals = ["A"] * 6 + ["B"] * 3 + ["C"] * 1
        svg = self.chart(self.report("b.csv", "g\n" + "\n".join(vals)), "g — 3 categories")
        self.assertEqual(svg.count('class="bar"'), 3)
        for lab, txt in (("A", "6 (60%)"), ("B", "3 (30%)"), ("C", "1 (10%)")):
            self.assertIn(f"<title>{lab}: {txt}</title>", svg)
        self.assertLess(svg.index(">A<"), svg.index(">C<"))      # largest first, as before

    def test_top_n_missingness_histogram_time_heatmap(self):
        rows = ["city,x,y,when"] + [
            f"c{i % 20},{i if i % 10 else ''},{2 * i},2026-02-{1 + i % 20:02d}" for i in range(200)]
        html_text = self.report("m.csv", "\n".join(rows))
        top = self.chart(html_text, "city — top 15 of 20 (other: 50 rows)")
        self.assertEqual(top.count('class="bar"'), 15)
        miss = self.chart(html_text, "Missing values by column")
        self.assertIn("<title>x: 10.0%</title>", miss)
        self.assertIn("% of rows missing", miss)
        hist = self.chart(html_text, "y — median")
        self.assertIn('class="box"', hist)
        bins = re.findall(r"<title>[^<]* to [^<]*: ([\d,]+) rows</title>", hist)
        self.assertEqual(sum(int(b.replace(",", "")) for b in bins), 200)
        line = self.chart(html_text, "when — rows per day (2026-02-01 → 2026-02-20)")
        self.assertIn("<polyline", line)
        self.assertIn("<title>2026-02-01: 10</title>", line)
        heat = self.chart(html_text, "Pearson correlation")
        self.assertIn("x × y: r = 1.00", heat)

    def test_time_chart_keeps_empty_periods(self):
        # Codex 4670109273: Jan 1, Jan 2 and Mar 1 must not be drawn equally spaced.
        days = ["2026-01-01"] * 3 + ["2026-01-02"] * 2 + ["2026-03-01"] * 4
        line = self.chart(self.report("t.csv", "when\n" + "\n".join(days)), "when — rows per day")
        self.assertIn("<title>2026-01-01: 3</title>", line)
        self.assertIn("<title>2026-01-15: 0</title>", line)       # a gap day, plotted at zero
        self.assertEqual(line.count("<circle"), 60)               # Jan 1 .. Mar 1, every day

    def test_wide_heatmap_fits_its_viewbox(self):
        # Codex 4670109284: 50 columns must not run past the right edge.
        import svg_charts as sc
        k = 50
        labels = [f"c{i}" for i in range(k)]
        svg = sc.heatmap("wide", labels, [[1.0 if i == j else 0.1 for j in range(k)] for i in range(k)])
        vb_w = float(re.search(r'viewBox="0 0 ([\d.]+) ', svg).group(1))
        right = max(float(x) + float(w) for x, w in re.findall(r'<rect x="([\d.]+)" y="[\d.]+" width="([\d.]+)"', svg))
        self.assertLessEqual(right, vb_w)
        self.assertEqual(svg.count("<rect"), k * k)

    def test_ticks_keep_tiny_scales(self):
        # Codex 4670109298: rounding ticks to 12 places turned 1e-15..9e-15 into zeros.
        import svg_charts as sc
        ticks = sc.nice_ticks(1e-15, 9e-15, 6)
        self.assertEqual(len(set(ticks)), len(ticks))
        self.assertTrue(all(1e-15 <= t <= 9e-15 for t in ticks), ticks)
        self.assertEqual([sc.fmt(t) for t in sc.nice_ticks(0, 1, 5)], ["0", "0.2", "0.4", "0.6", "0.8", "1"])

    def test_narrow_range_labels_stay_distinct(self):
        # Codex 4670146296: 1000.1..1000.9 printed every tick and bin edge as "1e+03".
        import svg_charts as sc
        ticks = sc.nice_ticks(1000.1, 1000.9, 6)
        labels = [sc.fmt(t, ticks[1] - ticks[0]) for t in ticks]
        self.assertEqual(len(set(labels)), len(labels), labels)
        self.assertIn("1,000.2", labels)
        svg = sc.histogram("h", [1, 2], [1000.1, 1000.5, 1000.9])
        self.assertIn("1,000.1 to 1,000.5: 1 rows", svg)
        self.assertEqual(sc.fmt(0.5, 0.1), "0.5")
        self.assertEqual(sc.fmt(2e-15, 1e-15), "2e-15")   # tiny scales stay scientific

    def test_labels_from_data_are_escaped(self):
        svg = self.chart(self.report("e.csv", "g\n" + "\n".join(["<b>&x"] * 3 + ["y"] * 2)), "g — 2 categories")
        self.assertIn("&lt;b&gt;&amp;x", svg)
        self.assertNotIn("<b>", svg)

    def test_plugin_contract(self):
        ae = self.ae
        self.assertIsNone(ae.to_svg(None))
        spec = {"kind": "bar", "title": "T", "labels": ["a", "b"], "values": [2, 1]}
        self.assertIn('aria-label="T"', ae.to_svg(spec))
        self.assertTrue(ae.to_svg('<svg role="img"></svg>').startswith("<svg"))
        with self.assertRaisesRegex(ValueError, "unknown chart kind"):
            ae.to_svg({"kind": "pie"})
        with self.assertRaisesRegex(TypeError, "not an <svg>"):
            ae.to_svg("<div>")

        class FakeFigure:          # what a pre-2.0 plugin returns
            def savefig(self, *a):
                pass
        with self.assertRaisesRegex(TypeError, "matplotlib Figure"):
            ae.to_svg(FakeFigure())

    def test_example_donut_plugin_draws_svg(self):
        html_text = self.report("d.csv", "g\n" + "\n".join(["p"] * 3 + ["q"]))
        donut = self.chart(html_text, "g — share")
        self.assertEqual(donut.count("<path"), 2)
        self.assertIn("<title>p: 3 (75%)</title>", donut)
        ints = self.chart(self.report("d1.csv", "h\n" + "\n".join(str(i % 3) for i in range(6))), "h — share")
        self.assertIn("<title>0: 2 (33%)</title>", ints)   # small-range integers count as categories


if __name__ == "__main__":
    unittest.main()
