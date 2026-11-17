# thread-seed: run of v1.0.1, 2026-11-17

- Author: claude:qat (session 01GZK2KiveUtv4PepjHDL9A1), model=claude-opus-5-5
- Reviewer: none yet. Grades are self-graded and same-family.

**Why 1.0.1.** Two defects in the bundled helper `seed_index.py --verify`, found while porting to ChatGPT (against `8f3b443e87e7`) and fixed there only; carried upstream from HO-QAT-20261116-Y0HJ (relay-kit-private):
1. **A ref to a missing exchange below the maximum passed.** A bare `[T2]` in a T1/T3 capture passed because the check was `n > max`. It now requires the exchange to exist.
2. **An exact reply ref matched any reply.** A quote cited as `[T1a2]` was searched in every assistant message of exchange 1, so T1a's text passed as T1a2. `T<n>a`/`T<n>a1` now search only the first reply and `T<n>aN` only the Nth; bare `T<n>` still searches both sides, and `T<n>u` the user message.

The docstring states the narrower scope. No other text in the skill changed.

**Tests.** `qat/scripts/test_thread_seed.py` (10 tests) extracts the helper from the skill text and runs it. Against main's text, 3 fail (the two findings plus the reverse T1a2-cited-as-T1a case); on this version all pass.

**Setup.** This tool had no cases, so `qat/cases/thread-seed.cases.md` is new in this PR (CONTRIBUTING: cases before the first change). TS-01 to TS-03 are deterministic helper runs, executed from the built `qat/runtimes/claude/thread-seed/SKILL.md`; they are not a model-quality evaluation. TS-04 was run by one fresh Claude subagent that saw only the built SKILL.md, the capture and the draft, and no cases or tests.

| Case | Grade | Reason |
|---|---|---|
| TS-01 | PASS | `FAIL ref T2 ... no such turn`, exit 1. Under 1.0.0 this passed. |
| TS-02 | PASS | Wrong quote reported, exit 1 (unchanged behaviour; a non-regression check). |
| TS-03 | PASS | T1a text cited as T1a2 fails, exit 1; the same quote cited as T1a and T1a1 passes (2 verified). Under 1.0.0 the T1a2 citation passed. |
| TS-04 | PASS (borderline on one "Must") | Ran `--verify`, reported 2 failures, fixed both pointers ([T2] → [T1a], [T1a] → [T1a2]) and re-ran to 0 failures before delivering. The `[T3a]` pointer was kept, but the line gained a "(Claude's statement)" label: that follows the skill's own Status check, yet it isn't strictly "left as it is". It also relabelled the budget as unconfirmed and added sections 1, 7 and 9, which the case didn't ask for. |

**Result: 4/4 PASS (self-graded, same-family; TS-04 borderline as noted).**
