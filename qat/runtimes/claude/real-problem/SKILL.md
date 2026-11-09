---
name: real-problem
description: "Use when someone raises one challenge, objection, worry or 'what if' and has to decide what, if anything, to do about it (a review objection, an open challenge-log item, a concern in a thread). Turn one raised challenge, objection or worry into a disposition: is it a real problem here, and if so the smallest proportionate response, or explicitly no action."
---
<!-- Claude skill for real-problem v0.1.0, adapted from qat/tools/real-problem.qat.md. Update together with the spec. -->

# RealProblem

Answer one question about one challenge: what would separate a real problem from a concern we can safely monitor? You propose a disposition; the owner decides. Never write that a risk is accepted or a challenge closed.

1. **Failure mode**: the concrete outcome the challenge fears, as a hypothesis ("if X, then Y").
2. **Observable**: what differs between that failure and an acceptable state. Ask: would I also see this if everything were fine? If yes, find another or write "none nameable".
3. **Cheapest check**: least-effort look at the observable, or "none needed".
4. **Disposition**, exactly one of:
   - `investigate now`: discriminating observable, cheap check, costly or near failure
   - `monitor`: discriminating observable, no sign yet; set a tripwire
   - `propose accepting the risk`: plausible but bounded and cheaper to absorb; addressed to the owner
   - `no action`: the challenge does not apply here; give the reason and stop, inventing no follow-ups
   - `insufficient information`: name the one missing fact; do not guess it
5. **Tripwire**: observable plus threshold that would change the disposition; "none" for no action and insufficient information.
6. **Owner**: from the authority given, else "the owner".
7. **Source**: copy any pointer given, else "none given". Never invent ids, links, dates or quotes.

## Output
Use these headings, in order, with this format under each (one bullet per section; at most 120 words in total):
- `## Failure mode`: one bullet
- `## Observable`: one bullet
- `## Cheapest check`: one bullet
- `## Disposition`: one bullet
- `## Tripwire`: one bullet
- `## Owner`: one bullet
- `## Source`: one bullet
