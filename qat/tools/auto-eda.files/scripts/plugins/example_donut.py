"""
Example plugin: a donut chart, written as SVG with auto-eda's helper.

The plugin contract (auto-eda 2.0): a rule takes (series, profile) and returns one of
  - SVG text: a single <svg> element, as here (build it with svg_doc() for the title,
    aria-label and sizing every chart shares), or
  - a chart spec the helper draws, e.g.
        {"kind": "bar", "title": "...", "labels": [...], "values": [...]}
    with kind one of svg_charts.CHART_KINDS (bar, histogram, line, heatmap), or
  - None, to skip the column.
A matplotlib Figure is refused with an error that names this contract.

Porting from your own viz repo: keep the function's data work, and replace the drawing
with a chart spec if one of the built-in kinds fits, or with SVG as below.

Profile fields available: name, dtype, kind, n, n_null, n_unique, null_pct, notes
kind is one of: low_cat, high_cat, numeric, datetime, boolean, id, text, constant, empty
"""
import math

from auto_eda import rule, PALETTE
from svg_charts import FG, MUTED, esc, svg_doc


@rule("donut: share of total", lambda p: p.kind == "low_cat" and p.n_unique <= 5)
def donut(s, p):
    counts = s.astype("string").fillna("(missing)").value_counts()
    total = int(counts.sum())
    cx, cy, r_out, r_in = 120, 140, 95, 58
    marks, start = [], -math.pi / 2          # 12 o'clock, clockwise
    for i, (label, n) in enumerate(counts.items()):
        sweep = 2 * math.pi * n / total
        end = start + sweep
        if sweep >= 2 * math.pi - 1e-9:      # one slice: a full ring
            path = (f"M{cx - r_out},{cy} a{r_out},{r_out} 0 1,0 {2 * r_out},0 a{r_out},{r_out} 0 1,0 {-2 * r_out},0 "
                    f"M{cx - r_in},{cy} a{r_in},{r_in} 0 1,1 {2 * r_in},0 a{r_in},{r_in} 0 1,1 {-2 * r_in},0Z")
        else:
            big = 1 if sweep > math.pi else 0
            pt = lambda r, a: f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}"
            path = (f"M{pt(r_out, start)} A{r_out},{r_out} 0 {big},1 {pt(r_out, end)} "
                    f"L{pt(r_in, end)} A{r_in},{r_in} 0 {big},0 {pt(r_in, start)}Z")
        pct = 100 * n / total
        color = PALETTE[i % len(PALETTE)]
        marks.append(f'<path d="{path}" fill-rule="evenodd" style="fill:{color};stroke:var(--card, #fff);stroke-width:2">'
                     f"<title>{esc(label)}: {n:,} ({pct:.0f}%)</title></path>")
        y = 70 + i * 24                       # legend
        marks.append(f'<rect x="250" y="{y - 11}" width="12" height="12" style="fill:{color}"/>'
                     f'<text x="268" y="{y}" style="fill:{FG}">{esc(label)}</text>'
                     f'<text x="380" y="{y}" style="fill:{MUTED}">{n:,} ({pct:.0f}%)</text>')
        start = end
    marks.append(f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" font-size="14" style="fill:{FG}">{total:,}</text>')
    return svg_doc(f"{p.name} — share", 250, "".join(marks))
