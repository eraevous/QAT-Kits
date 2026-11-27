---
name: auto-eda
version: 2.0.0
description: Generate a rule-driven EDA companion report (HTML with inline SVG charts + JSON summary) for any tabular data — a CSV, Excel, JSON or parquet file, a query result, a connector export, or a table Claude just produced. Use whenever Zach shares or receives a dataset and wants a look at it, asks for EDA, profiling, "what's in this data", distributions, or category breakdowns, or says "run auto-eda" — even if he doesn't ask for charts explicitly.
---

# Auto-EDA

Produces a repeatable EDA file for a dataset by running `scripts/auto_eda.py`. The script profiles every column, classifies it, and fires every chart rule whose condition matches. Rules are deterministic, so the same data always gets the same report.

It needs pandas. The charts are hand-written inline SVG (`scripts/svg_charts.py`, standard library only), so no plotting library is needed. Each chart has a title, an `aria-label` and per-bar hover values, and its colours follow the page's light or dark theme.

## Built-in rules

| Column kind | Condition | Chart |
|---|---|---|
| `low_cat` | ≤ 8 distinct values (also small-range integers) | Horizontal bar with counts and % |
| `low_cat` | ≤ 5 distinct values (example plugin) | Donut |
| `boolean` | two yes/no-style values | Bar |
| `high_cat` | > 8 distinct, not ID-like | Top-15 bar + "other" count |
| `numeric` | numeric, not few-valued int | Histogram with box strip |
| `datetime` | dtype or ≥90% parseable strings | Rows per day/week/month |
| `id`, `text` | > 95% unique | Profiled, not charted |
| `constant` | one distinct value | Flagged in the profile table, not charted |
| dataset | any missing values | Missingness by column |
| dataset | ≥ 2 numeric columns | Correlation grid (red positive, blue negative) |

## Workflow

1. **Get the data into a file.** If the data came back from a tool or connector rather than as a file, write it out first (CSV for flat rows, JSON/JSONL for nested records — the script flattens nested JSON and JSONL with `json_normalize`, and turns list values into text, and unwraps `{"data": [...]}`-style payloads).
2. **Copy the skill's scripts** into the working directory so plugins resolve, then run:
   ```bash
   cp -r <skill_dir>/scripts ./auto_eda_scripts
   python auto_eda_scripts/auto_eda.py DATA_FILE --out eda_out [--max-cats 8] [--top-n 15] [--title "..."]
   ```
   The script prints a JSON line with the output paths, row/column counts, and how many columns fell into each kind.
3. **Deliver** `eda_out/<stem>_eda.html` with SendUserFile (display: render). Keep `<stem>_eda.json` for your own follow-up reasoning; send it only if asked.
4. **Reply briefly**: the 2–4 most notable things the report shows (a dominant category, heavy missingness, a skewed numeric, a strong correlation) — read them from the JSON summary, not by guessing. Each profile there carries `stats` (numeric: count, mean, std, min, p25, median, p75, max, skew; categorical: `top` values with count and % of all rows, missing included, as in the charts; datetime: min and max), and `correlations` lists Pearson r for numeric pairs, strongest first. Don't describe every chart.

Respect a threshold the user states ("use 12 categories") via `--max-cats`.

## Adding rules (porting from a viz repo)

Each rule is a function `(series, profile) -> chart | None` plus a condition on the profile. A chart is one of:

- **a chart spec**, a dict the helper draws: `{"kind": "bar", "title": ..., "labels": [...], "values": [...]}`. Kinds are `bar`, `histogram` (`counts`, `edges`, optional `box`), `line` (`labels`, `values`) and `heatmap` (`labels`, `matrix`); the keys are the arguments of the same-named function in `scripts/svg_charts.py`;
- **SVG text**, a single `<svg>` element, for a chart the kinds don't cover. Build it with `svg_doc(title, height, body)` from `svg_charts` so it gets the title, `aria-label` and sizing the others have, escape data text with `esc()`, and colour with `PALETTE` (CSS variables with fallbacks) so it follows the theme. `scripts/plugins/example_donut.py` is a worked example;
- `None`, to skip.

Plugins are executable Python code; install only reviewed, trusted plugins. Their returned SVG is embedded without sanitisation. Built-in chart rendering escapes data text; plugins returning raw SVG must handle escaping themselves. The generated HTML/SVG report is provider-neutral. Plugins and callable spec fields require Python; raw SVG itself does not.

A matplotlib Figure (the pre-2.0 contract) is refused with an error naming this contract: in the column's Notes for a column rule, as a stderr warning for a dataset rule. To add a rule, put a `.py` file in `scripts/plugins/`:

```python
from auto_eda import rule, frame_rule

@rule("top values by share", lambda p: p.kind == "high_cat")
def my_chart(s, p):
    counts = s.value_counts().head(10)
    return {"kind": "bar", "title": f"{p.name} — top 10", "labels": counts.index, "values": counts.values}
```

`@frame_rule("name")` registers a dataset-level chart taking `(df, profiles)`.

When porting a function from Zach's GitHub repo:
- Keep the function's data work (filtering, grouping, binning) and replace only the drawing: return a chart spec when a built-in kind fits, otherwise SVG built with `svg_doc`.
- Don't add a plotting library to get a chart drawn; if the chart truly needs one, say so to the user instead of installing it.
- Pick the trigger condition from what the function actually needs (column kind, cardinality, null rate). Functions that need two columns (e.g. numeric-by-category) belong in a `@frame_rule` that loops over qualifying pairs — cap the pair count so wide tables don't explode.
- Run the script on a small sample afterward to confirm the plugin loads and its chart appears (a failure shows in the profile table's Notes column).

Profile fields: `name, dtype, kind, n, n_null, n_unique, null_pct, notes`. Kinds: `low_cat, high_cat, numeric, datetime, boolean, id, text, constant, empty`. Tunables live in `CFG` at the top of `auto_eda.py`.
