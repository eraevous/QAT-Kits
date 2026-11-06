# thread-distill eval runs, 2026-11-05

Fixture: `cases/fixtures/seed-library.thread.md` (constructed, 866 words). Cases: `cases/thread-distill.eval.yaml`.
Each round's outputs were written by a fresh subagent that read only the spec and the fixture (blind to the evals).

**How the grades were established.** The deterministic checks are `qat.py eval` output. Claude:qat wrote both the spec and the rubric, then graded the judge checks. Those grades are therefore *self-graded and provisional* until an independent review (Kate) re-grades them.

## Round 1: spec v0.1.0 (`thread-distill/v0.1/`)

| case | deterministic | judge (self-graded) |
|---|---|---|
| full-statuses | FAIL (1): Compression notes is not bullets, so it does not parse as `claims` | 5/6. FAIL: "seed debt on the front page" (T3u, "I'd want") recorded as `decided (user)` |
| hook-only | FAIL (1): same type mismatch | 1/1 |
| brief-with-purpose | FAIL (1): same type mismatch | 1/1 |

Other findings from round 1:
- Claude's spreadsheet recommendation was misfiled as `superseded`, though it was never decided.
- The cold user reported 12 ambiguities: pointer conversion, relay-then-adopt, adoption scope, budget semantics, where quoted instructions go, segment output, and field formats.

v0.2 changes in response:
- new statuses `wanted (user)` and `declined (user)`;
- new rules `wanting-is-not-deciding` and `narrow-adoption`;
- pointer conversion rule;
- budget is now a cap per fidelity;
- quoted instructions go in Compression notes;
- every section after Hook and Abstract is written as bullets;
- two new checks in the eval file, tagged "(v0.2)".

## Round 2: spec v0.2.0 (`thread-distill/v0.2/`)

| case | deterministic | judge (self-graded) |
|---|---|---|
| full-statuses | PASS | 7/7. Nits: SQLite's "proposed by Claude" points to T1a (T2a is the better pointer); "volunteer poll" for "meeting" is a slight embellishment |
| hook-only | PASS | 2/2 (148 words) |
| brief-with-purpose | PASS | 1/1 |

Open design issues for v0.3, from the round-2 cold user:
1. At full fidelity on a short thread, the 350-word cap forces cutting trajectory and proposed rows. That loses the "ignored proposal" signal the ledger exists to keep.
2. "Hook and abstract read the same at every fidelity" conflicts with "purpose may choose what the abstract leads with".
3. The ledger has no column for the *reason* behind a decision.
4. There is no status for a concept the user defined (as opposed to decided), or for an interim default ("stays out until…").
5. A pasted block with no named author (a doc, not a model reply) is handled by the relay rule only by analogy.
6. There is no method for counting source words (comments, headings, code).

Limit of this evidence: one short constructed thread, one model family. The tool's real job is compressing long threads (tens of thousands of words). Round 3 needs Zach's real threads, run privately.
