---
name: truth-weight
version: 2.0.0
description: Steelman two competing claims and score which holds up better under historical, empirical, predictive, ethical and burden-of-proof scrutiny, without forcing artificial balance.
inputs:
  position_a: {type: claim, required: true}
  position_b: {type: claim, required: true}
  evidence: {type: text, required: false}
outputs:
  positions: {type: text, heading: Positions, doc: "steelman of A and B, and whether they truly conflict"}
  framing: {type: claims, heading: Framing notes, doc: "loaded terms, false dichotomies, slanted questions"}
  scorecard: {type: scorecard, heading: Scorecard, doc: "table: Category | A | B | Why"}
  verdict: {type: verdict, heading: Verdict, doc: "totals /50, weight sensitivity, conclusion for now"}
  reversal: {type: claims, heading: Would reverse if}
modules: [burden-of-proof]
reflexes:
  no-fabricated-support: Do not fabricate historical support or create forced equivalence.
  search-when-empirical: For empirical or current questions, search rather than rely on memory, and cite.
  noise-floor: A one-point score difference is judgment noise; don't build a verdict on it.
  heuristic-scores: Scores are transparent heuristic judgments, not calibrated probabilities.
handoffs:
  - to: stress-test
    when: the user wants to probe the winning position further
    map: {idea: verdict}
---

# TruthWeight

Fair, but not symmetric by default.

## Procedure
1. Steelman both positions; check whether they actually conflict and note shared premises.
2. Flag framing flaws before scoring.
3. Gather evidence (search for empirical claims when tools allow).
4. Score each side 0–10 on Historical Attestation, Empirical Outcomes, Predictive Counterfactuals, Moral & Ethical Coherence, Burden of Proof. Anchors: 0–2 contradicted · 3–4 weak · 5–6 mixed · 7–8 solid with gaps · 9–10 strong, convergent.
5. Total out of 50 (equal weights; say so), test whether a plausible reweighting flips it, and state the verdict *for now* plus what would reverse it.

Write the output with exactly the `##` headings in the contract above.

### module: burden-of-proof
Score the fit between claim and evidence, not evidence quality again. Claims that overturn a supported status quo, assert large effects, or demand costly action carry heavier burdens; modest or reversible claims lighter ones.
