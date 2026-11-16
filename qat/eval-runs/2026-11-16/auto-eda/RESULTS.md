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

**Not run here:** AE-02 (passing a stated threshold) and AE-03 (pasted connector JSON). Neither path changed in this commit.

**Observation (not a failure).** AE-04 shows a limit of the list-as-text choice. `["a","b"]` and `["b","a"]` count as different values. The runner noticed, said so, and gave its own unordered count, labelled as its own. Whether lists should be profiled order-free (sorted, or exploded per element) is a design choice for a later version. It is left as is here.
