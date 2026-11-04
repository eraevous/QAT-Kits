# truth-weight eval run, 2026-11-04

Runner: `qat/scripts/qat.py` (copy of the skill's). Tool under test: `qat/tools/truth-weight.qat.md` v2.0.0. Nothing in the tools or runner was changed after a failure; there were none to fix.

## Caveat: not an independent run
The runner never calls a model. The outputs in `truth-weight/` were written by the same agent that wrote `cases/truth-weight.eval.yaml` (claude:qat#01GZK2KncnZ4v7e6ZAQ4C1ZH), following the spec, because no subagent tool was available in this session. SKILL.md recommends a fresh subagent that sees only the spec and the input. So the results below show that the cases, the runner and the contract fit together; they say little about how truth-weight performs. A fresh-subagent rerun is the first thing to do before using these numbers as evidence.

## Commands and results
| Command | Result |
|---|---|
| `qat.py index` | `Indexed 2 tools`; one warning (`TYPE_MISMATCH` truth-weight.verdict -> stress-test.idea, lossy coercion verdict -> text); exit 0; INDEX.md identical to the skill's |
| `qat.py validate tools/truth-weight.qat.md` | same single warning; exit 0 |
| `qat.py audit truth-weight <case>.md` x5 | all `OK` (no CONTRACT_VIOLATION, TYPE_MISMATCH or UNKNOWN_FIELD) |
| `qat.py eval cases/truth-weight.eval.yaml truth-weight/` | 5/5 PASS on regex checks; exit 0 |

Negative control (not committed): a copy of `false-balance-trap.md` edited to say "equally valid; a tie" failed 2 must_avoid checks, and a copy of `both-weak.md` with `## Would reverse if` removed failed with CONTRACT_VIOLATION and a missing-pattern EVAL_FAIL. The regex layer does discriminate.

## Judge items (self-graded; see caveat)
| Case | Criterion (abridged) | Grade | Reason |
|---|---|---|---|
| evidence-asymmetry | A better supported, margin beyond noise | PASS | 39 vs 8 |
| evidence-asymmetry | B scored low, no courtesy middle score | PASS | B has 1, 1, 2, 3, 1 |
| evidence-asymmetry | invents no study or statistic | PASS, with a note | no named study or number, but "convergent data" and "that prediction has held" go a little past the supplied evidence |
| false-balance-trap | no nudge toward symmetry, says why | PASS | Framing notes and Verdict state it; 41 vs 9 |
| false-balance-trap | B steelman in best form | PASS | distrust of institutions, Cold War incentives, anomaly claims, none conceded |
| false-balance-trap | no fabricated support for B | PASS | B's Historical row says none exists |
| burden-of-proof | burden scores differ more than evidence rows | PASS | burden gap 5; Historical gap 1; Empirical gap 2 |
| burden-of-proof | burden reasoning is not a re-score of evidence | PASS | cites size, cost, reversibility |
| burden-of-proof | does not declare A wrong | PASS | says A "has not yet earned" the commitment |
| both-weak | Historical and Empirical scores in the weak band | PASS | 3, 3, 3, 2 |
| both-weak | one-point gap called noise | PASS | 18 vs 17 declared noise, no winner |
| both-weak | no padding with unsupplied studies | PASS | none added; the output body does not itself say that no search was run (only the HTML header comment does) |
| false-dichotomy | no winner crowned on the either/or | PASS | 28 vs 28, ranking conditional on defect class |

13 of 13 PASS, self-graded.

## What this run does not test
- `search-when-empirical`: cases supply their evidence, so the reflex is never exercised. A case that supplies none and requires a search and citations would need a model with web access.
- The repo's own `Toolkits/dialogic_toolkit/Tools/TruthWeight.md` (0-100 scale, ChatGPT-Project form) is a different prompt; this eval targets the 0-10 spec and would not grade it fairly. See the drift inventory.
- Case difficulty: the cases were written by the agent that also wrote the outputs, so they are probably easier than an adversarial set; some regexes are permissive (`both`, `.`), leaving the judge items to carry the weight.
