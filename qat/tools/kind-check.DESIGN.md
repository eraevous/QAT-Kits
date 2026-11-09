# kind-check: design notes

Kit-owned and ungoverned (Telosmith governs the creation machinery, not tools).

## Why it exists
- Proposed by the Claude QAT lane with Kate (ChatGPT), 2026-11-06 (DEC-145), adopted by the owner as DEC-158 on 2026-11-07: a governance-object classifier (type, purpose, status, destination, smallest next action). Kate ranked it second by attention saved.
- The recurring failures it targets: a proposal recorded as if adopted; an item in the wrong ledger; a message bundling several acts handled as one; items that needed no record getting one.
- Separate from **real-problem**: kind-check says what an item is and where it goes; real-problem decides what to do about a challenge. Handoff from kind-check to real-problem when the item is a challenge; optional.

## Choices and the alternatives rejected
- **Seven candidate types** from the converged list (decision, proposal, challenge, reminder, observation, question, tracking record), plus `mixed` and `abstain` as distinct outcomes. Rejected: a confidence score per type (false precision; EvidenceFit is the candidate for that, not built, DEC-158 item 3).
- **Status from explicit words only**, with an Evidence section of quotes so a grader can see what the status rests on. Rejected: inferring adoption from tone ("sounds great"), which is the commonest wrong commitment.
- **Generic destinations unless the context names places.** The tool must work outside any one project's ledger layout.
- **One next action.** "No action" is valid and tested.

## Distinctions that must survive revisions
- Classification vs authority (decision-shaped is not adopted).
- Mixed vs abstain.
- Destination vs next action (where it belongs vs what moves it).

## Evidence
- Design-time eval cases only (cases/kind-check.eval.yaml), written by the builder; no cold run yet.
- The blind replay in qat/studies/replay-dec158/ is the real test (DEC-158 item 2).

## Open questions
- Is "tracking record" one type or two (automated logs vs human status notes)? Keep one until the replay shows confusion.
- Should a project's own type vocabulary override the seven? Not until a second project asks.
