<!-- ChatGPT paste block for real-problem v0.1.0, hand-adapted from qat/tools/real-problem.qat.md.
     Paste everything below the line into any ChatGPT thread. Keep it short enough to paste repeatedly.
     When the spec's outputs change, update the heading list below in the same commit. -->
---
REALPROBLEM: for the one challenge, objection or worry I give you, decide whether it is a real problem here and the smallest proportionate response. Do not solve the underlying problem, and do not close or accept anything: you propose, the owner decides.

1. Failure mode: the concrete bad outcome, phrased as a hypothesis ("if X, then Y"), not as a fact.
2. Observable: what you would see if the failure were happening that you would NOT see if things were fine. If both would look the same, write "none nameable".
3. Cheapest check: the least-effort way to look at it now, or "none needed".
4. Disposition: start with exactly one of `investigate now` | `monitor` | `propose accepting the risk` | `no action` | `insufficient information`, then one reason. If it doesn't apply here, say no action and stop; invent no follow-ups. If a fact is missing, say insufficient information and name that one fact; don't guess it.
5. Tripwire: observable plus threshold that would change the disposition, or "none".
6. Owner: who may accept this (default "the owner").
7. Source: copy the pointer I gave, or "none given". Never invent ids, links or dates.

Use these headings, in order, with this format under each (one bullet per section, 120 words total at most):
- `## Failure mode`: one bullet
- `## Observable`: one bullet
- `## Cheapest check`: one bullet
- `## Disposition`: one bullet
- `## Tripwire`: one bullet
- `## Owner`: one bullet
- `## Source`: one bullet
