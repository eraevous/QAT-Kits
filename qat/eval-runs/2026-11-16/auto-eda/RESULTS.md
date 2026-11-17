# auto-eda: run of v1.1.0, 2026-11-16

- Author: claude:qat (session 01GZK2Kn6Qgge9Tv3qByL4kB), model=claude-opus-5-5
- Reviewer: none yet. Grades are self-graded and same-family.

**Why 1.1.0.** These changes answer Copilot's two findings on #20, and Codex's two matching P2 findings.
- **Nested JSONL is now flattened like JSON.** `load()` reads the records and calls `json_normalize`, so a nested JSONL file no longer crashes the run.
  - Under 1.0.0, `pd.read_json(lines=True)` left dict cells, and `profile_column()` raised `TypeError: unhashable type: 'dict'` before any report was written. This was reproduced on a two-line file.
  - List cells are now profiled as JSON text (`make_hashable`).
- **The JSON summary now carries the measurements behind the charts.**
  - Each profile has `stats`: numeric count, mean, std, min, p25, median, p75, max and skew; categorical `top` values with count and %; datetime min and max.
  - The summary has `correlations`: numeric pairs with Pearson r, strongest first.
  - Workflow step 4 says to read findings from that file, and it can now be done.
- Tests: `qat/scripts/test_auto_eda.py` (3 tests, OK locally). They skip in CI, where pandas is not installed.

**Setup.** One fresh Claude subagent read only the built skill (`qat/runtimes/claude/auto-eda/`, SKILL.md and scripts). It saw no cases or tests. It generated each input from the case snippet and replied as it would to the user. Run directories are shown as `<run dir>`.

| Case | Grade | Reason |
|---|---|---|
| AE-01 | PASS | Ran the script. `order_id` was profiled as an ID; `constant_flag` was flagged as constant. Missingness (22.2%) and the right skew of `amount` (skew 4.07, median 18.28 vs mean 29.28) come from the summary's new `stats`, which 1.0.0 could not support. Four findings were given. One extra "Also" line restates the rest of the profile: borderline against "2-4 findings", but not a chart-by-chart walk. |
| AE-04 | PASS | No crash. `user.plan` is its own flattened column. The dominant category (team 50%) is read from `stats.top`. No CSV rewrite. |

| AE-02 | PASS | Passed `--max-cats 12` to the script. It also said, correctly, that the cutoff changed no classification here (`region` has 4 values; `qty` has 39). Findings come from `stats` and `correlations`. |
| AE-03 | PASS | Wrote the pasted payload to a file before running the script. `{"data": [...]}` was unwrapped and `b` flattened to `b.c`, which passes through the new `make_hashable` step unharmed. Treated "What's in this data?" as an EDA request. |

**AE-02 and AE-03 were added after Codex's review** (finding 4592970450 on #21). The first commit left them out on the grounds that their paths were unchanged. That did not hold: both pass through the changed summary code, and AE-03 also goes through `make_hashable`. A second fresh subagent ran them against the same built skill, with the same blind setup.

**Result: 4/4 PASS (self-graded, same-family).**

Note for AE-03, not a failure: the runner said, rightly, that the 0-29 counter `a` is charted as numeric. That is the known integer-ID behaviour recorded in the cases file under AE-01.

**Observation (not a failure).** AE-04 shows a limit of the list-as-text choice. `["a","b"]` and `["b","a"]` count as different values. The runner noticed, said so, and gave its own unordered count, labelled as its own. Whether lists should be profiled order-free (sorted, or exploded per element) is a design choice for a later version. It is left as is here.

## Follow-up: category percentages (Codex 4592993932 on ef5c867)

- **Bug:** categorical `stats.top` percentages used non-null rows as the denominator. The bar chart uses all rows and shows a "(missing)" bar. With 90 missing values, 6 A and 4 B, the summary said A was 60% while the chart showed 6%.
- **Fix:** `pct` is now a share of all rows. Low-cardinality and boolean columns list "(missing)" as a value, as their chart does. High-cardinality columns carry `missing_count`. Each categorical `stats` says `"pct_of": "all rows"`. A new test pins the 6% case.
- **Rerun not needed:** none of the four cases has missing values in a categorical column. Their recorded outputs and grades hold as they are; the only differences are the added `pct_of` field and `(missing)` rows that would have a count of 0.

## Follow-up: non-finite statistics (Copilot 4593532067)

- **Bug:** `inf` in a numeric column, or a finite value that overflows when rounded to 4 significant figures (`1.7976931348623157e308`), reached the summary as a bare `Infinity` token. Strict JSON parsers reject that token.
- **Fix:** rounded statistics that are not finite are now written as `null`.
- **Test:** a new test parses the summary strictly. It failed before the fix and passes after it.
- **Rerun not needed:** none of the four cases has non-finite values, so their outputs and grades hold.
