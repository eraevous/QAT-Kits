# real-problem: design notes

Kit-owned and ungoverned (Telosmith governs the creation machinery, not tools).

## Why it exists
- Origin: the owner's question on an open challenge, 2026-11-05: "How would we handle this if it was a real problem?" (relay-kit-private CH-022). Many open challenges sat with no disposition because nobody separated "real" from "safely monitored".
- Proposed by the Claude QAT lane with Kate (ChatGPT), two rounds, converged, 2026-11-06 (DEC-145); adopted by the owner as DEC-158 on 2026-11-07. Kate ranked it first by attention saved.
- Separate from **stress-test** (probes a whole idea; many findings) and **truth-weight** (two positions, a verdict). real-problem takes one challenge to one disposition.

## Choices and the alternatives rejected
- **Seven one-bullet sections, 120 words**, from the converged field list (failure mode, observable, cheapest check, disposition, tripwire, owner) plus an optional source pointer. Rejected: a free-text "assessment" section, which is where Instant-tier runs hide a non-decision.
- **Five dispositions, not four.** The converged list had investigate now / monitor / propose accepting the risk / insufficient information. DEC-158 requires a no-action output, so `no action` is its own value rather than folded into monitor (a monitor with nothing to watch is a decorative tripwire).
- **"Propose accepting the risk", never "accept".** Risk acceptance is the owner's act; the wording keeps it a proposal at the token level, and an eval case checks for closure language.
- **Handoff to stress-test** on investigate-now, mapping the failure mode as the idea. Optional; neither tool is a required step.

## Distinctions that must survive revisions
- Observable vs symptom-that-appears-either-way (the discriminating test in Procedure step 2).
- Proposed disposition vs authorized closure.
- No action vs insufficient information: the first is a judgment that the concern does not apply; the second says what fact is missing.

## Evidence
- Design-time eval cases only (cases/real-problem.eval.yaml), written by the builder. No cold run yet: the builder has seen the eval, so a cold run must be done by an actor that has not.
- The blind replay in qat/studies/replay-dec158/ is the real test (DEC-158 item 2).

## Open questions
- Is 120 words enough for `investigate now` with a non-obvious check? Watch the replay's correction counts.
- Should the disposition values be configurable per project (some projects have "wontfix")? Not until a second project asks.
