# selective-self-distillation: baseline run, 2026-11-16

- Author: claude:qat (wake 2026-11-16 22:09Z, session 01GZK2Kn6Qgge9Tv3qByL4kB), model=claude-opus-5-5
- Reviewer: none yet (Kate asked for a cross-family review in HO-QAT-20261116-9ANR)

**What this is.** The first cases for the standalone skill (`qat/cases/selective-self-distillation.cases.md`, 6 cases) and a baseline run against the **unchanged** skill text, v1.0.0. The skill is not edited in this change. CONTRIBUTING.md says a spec with no cases gets cases before its first change; this is that step, so the next change to the skill has something to be gated against.

**Setup**
- Text under test: `qat/tools/selective-self-distillation.skill.md` v1.0.0, copied verbatim.
- Runners: two fresh Claude subagents (same model family as the author), three cases each. Each saw only the skill text and the case inputs: no Must/Must not lines, no repo, no other case file. Each transcript was run as "a pasted single conversation", so the corpus file (Output item 6) was skipped.
- Inputs: constructed, no personal material.

**Grading.** Graded by claude:qat, who also wrote the cases. The grades are **self-graded and same-family**, so provisional until an independent grader re-grades them.

| Case | Rule under test | Grade | Reason |
|---|---|---|---|
| paste-delimiter | Paste delimiter | PASS | Forum text sits in its own "Not his: pasted third-party claim" row; mulch is Adopted with "Fine, mulch the sandy rows." quoted. |
| silence-not-adoption | Silence is not adoption | PASS | Template and 1-5 score both AI proposal; 3:15 Adopted with "3:15 it is."; neither proposal appears in the reconstruction. |
| coinage-drift | Coinage drift | PASS | Idea Direct (L2); "pivot index" credited to the model, and his later use of the name is called provisional, not his coinage. |
| relay | Relays | PASS | Relayed sentence labelled "Not his", rejected by him; his framing ("goes too far", one a quarter) is Direct; not counted as a change of mind. |
| change-of-mind | Track changes of mind | PASS | One change, monthly (L2) → fortnightly (L14), both quoted with lines; current position fortnightly with his reason; "What's On" stays AI proposal. |
| inverted-roles | Inverted roles | PASS | Setup turn recognised; L5 and L11 excluded as model text; reports no positions to reconstruct and why. |

**Result: 6/6 PASS (self-graded).**

**Observations (not failures)**
- The extraction script flags neither relays nor role inversion. Both runners caught them in step 2 (screen) as the skill directs. The script's flags are a first pass, and these cases show the manual screen carrying the weight. A later case with an undelimited pasted model reply (the `likely_paste` heuristic, 250+ words) would test the script's own flag; it is not in this set, to keep the inputs short.
- Every runner verified its quotes and reported the count (step 7).
- These cases are easy for a strong model. Their job is a regression floor for the next change to the skill, not a hard benchmark.
