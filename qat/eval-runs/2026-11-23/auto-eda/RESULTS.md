# auto-eda: run of v2.0.0, 2026-11-23

- Author: claude:qat#wake-2026-11-23-18 (session 01GZK2Km), model=claude-opus-5-5
- Reviewer: none yet. Grades are self-graded and same-family.
- Handoff: HO-QAT-20261123-Y3YV (DEC-266 (1), Zach 2026-11-23: "Rewrite auto-eda, including examples.")

**Why 2.0.0.** The charts are now hand-written inline SVG (`scripts/svg_charts.py`, standard library only). matplotlib is gone, and so are the base64 PNGs. The plugin contract changes (a rule returns SVG text or a chart spec, not a matplotlib Figure), which breaks 1.x plugins, hence the major bump. Profiling, rules, report sections and the JSON summary are unchanged.

**Setup.** One fresh Claude subagent read only the built skill (`qat/runtimes/claude/auto-eda/`, SKILL.md and scripts). It saw no cases, tests or earlier runs. It generated each input from the case snippet and replied as it would to the user. matplotlib was not installed in its workspace. Run directories are shown as `<run dir>`.

| Case | Grade | Reason |
|---|---|---|
| AE-01 | PASS | Ran the script. `order_id` profiled as an ID, not charted; `constant_flag` flagged constant. Missingness (22.2%) and right skew (4.07) of `amount` read from `stats`. Four findings, no chart-by-chart walk. |
| AE-02 | PASS | Passed `--max-cats 12`, and said correctly that the cutoff changed no classification here. |
| AE-03 | PASS | Wrote the pasted payload to a file first; `data` unwrapped and `b.c` flattened. Treated "What's in this data?" as an EDA request. |
| AE-04 | PASS | No crash; `user.plan` is its own column; dominant category (team 50%) from `stats.top`. No CSV rewrite. |
| AE-05 | PASS | New case for the 2.0 contract. Kept the groupby-median, returned a `"kind": "bar"` spec from `@frame_rule`s, installed nothing, returned no Figure. Reran and confirmed the charts in the report and JSON; medians cross-checked with pandas. Plugin: `v2.0.0/AE-05.plugin.py`. |

**Result: 5/5 PASS (self-graded, same-family).**

**Observations (not failures).**
- AE-05: `bar`'s default value label is "count (pct%)", which is wrong for medians. The runner noticed and passed `value_fmt`. A spec that names a value format without a Python lambda (for example `"values_are": "measure"`) would keep specs pure data; that is a candidate for 2.1, not done here.
- AE-05: the runner generalised the function to every category × numeric pair (capped at 6) rather than the hard-coded region × amount. Reasonable, but more than asked; the skill text could say "port as written unless asked to generalise".
- AE-03 and AE-04 repeat 1.x's known behaviours (integer counter charted as numeric; list cells counted order-sensitively). Unchanged by 2.0.

## Follow-up: Codex findings on 83e78a6

- **4670109273, time spacing.** `time_counts` drew only the periods that had rows, one step apart, so Jan 1, Jan 2 and Mar 1 looked evenly spaced. The fix reindexes to every period in the span, with empty periods drawn at 0. A new test pins the Jan 1 / Jan 2 / Mar 1 case: 60 points, and Jan 15 at 0.
- **4670109284, wide heatmap.** With 50 numeric columns the grid ran past the 640-unit viewBox. The fix widens the viewBox to fit the grid, and the page still scales the chart to the card. A new test checks that every cell lies inside the viewBox.
- **No rerun needed.** No case reply depends on either chart's geometry. AE-01's dates are hourly over 21 days, so it has no empty days, and no case has more than 3 numeric columns.
