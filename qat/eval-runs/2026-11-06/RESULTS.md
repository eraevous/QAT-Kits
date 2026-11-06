# effort-cost eval runs, 2026-11-06

**Setup**
- Fixtures: `cases/fixtures/lit-analysis.thread.md` and `cases/fixtures/recall.thread.md` (both constructed).
- Cases: `cases/effort-cost.eval.yaml`.
- Text under test: the ChatGPT paste block (`runtimes/chatgpt/effort-cost.paste.md`).

**Each round**
- A fresh subagent played ChatGPT.
- It read only the paste block and the fixtures, so it was blind to the evals and the spec.
- It is Claude, not ChatGPT, so a real ChatGPT run is still owed.

**Grading**
- Deterministic checks come from `qat.py eval`.
- claude:qat wrote the tool and the rubric and graded the judge checks. Those grades are **self-graded and provisional** until an independent grader re-grades them.

## Round 1: v0.1.0 (`effort-cost/v0.1/`)

| Case | Deterministic | Judge (self-graded) | Lean given |
|---|---|---|---|
| lit-high | FAIL (3 sections written as prose, contract says bullets) | 5/5 | bump for this message only |
| recall-pro | FAIL (same) | 3/3 | stay |
| lit-unknown | FAIL (same) | 2/2 | bump for this message only |

The cold user reported 9 ambiguities. The material ones:
- Product names (Thinking, standard, High) did not map to the effort rows.
- The "default" setting was undefined. The runner assumed "fast", which shrank the lit-unknown result.
- "Floor" had two readings, a roughly 5× swing in the Pro case.
- 9:40 pm fit no time band.
- The ranges for the difference row were unspecified.
- It was unclear whether the word limit counts the table.

## Round 2: v0.2.0 (`effort-cost/v0.2/`)

| Case | Deterministic | Judge (self-graded) | Lean given |
|---|---|---|---|
| lit-high | PASS | 5/5 | bump for this message only |
| recall-pro | PASS | 3/3 | stay |
| lit-unknown | PASS | 2/2 | bump for this message only |

Worked example (lit-high), from the runner. Setting: standard → High, about 1,500 tokens, Chicago, 9:40 pm.

- **Difference, next answer:**
  - energy: about 14 Wh (4.5–38)
  - carbon: about 6 g CO2e (2–17)
  - water: about 41 mL (4.5–190)
- **In everyday terms:**
  - about 80 minutes of a 10 W LED bulb
  - about 0.9 of a phone charge
- **Next 5 answers at High:**
  - energy: about 120 Wh (40–310)
  - carbon: about 53 g

## Open for v0.3 (from the round-2 cold user)

1. **The floor rule overstates short reasoning answers.** A 150-token factual reply at medium is costed at the full 1,000-token figure. Reasoning on easy questions is shorter too.
   - Candidate fix: a floor of half the table value for short answers.
2. **Follow-up turns are assumed to be the same length as the next answer.** For the lit thread that likely overstates the 5-turn row.
   - Candidate fix: follow-ups default to a paragraph unless the request says otherwise.
3. **The carbon windows leave 3–4 pm unassigned.** Also, "US" should mean the user's local time zone.
4. **"Answer quickly" conflicts with the required arithmetic.** Keep the check itself on the current setting, but drop "quickly".
5. **The context add-on bands have no central value.** The runner used the midpoint.

Missing evidence:
- No real ChatGPT run yet, so it is unknown whether ChatGPT knows its own effort setting.
- No independent grader yet.
