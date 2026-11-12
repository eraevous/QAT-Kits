---
name: "negative-space"
version: 0.1.0-reconstruction
description: "Discover meaningful absences, invert expectations, and generate testable conceptual alternatives without confusing missing evidence with proven absence. Use when the user invokes NegativeSpace or asks 'what is missing?', 'what would we expect but don't observe?', 'invert this concept', or for an expectation audit."
---

# NegativeSpace (QAT-Kit) — reconstructed skill

*Version 0.1.0-reconstruction · status: reconstructed from partial evidence.*

Use this skill to examine what a text, argument, ontology, project, profile, dataset, narrative, policy, plan, or system does not contain; identify unexpected omissions and absent expected weaknesses; explore conceptual inverses; and distinguish substantive gaps from sampling, framing, and category errors. Triggers include 'NegativeSpace', 'negative space analysis', 'what is missing?', 'what isn't here?', 'what would we expect but don't observe?', 'what assumptions arise from the absences?', 'invert this concept', and 'which presumed weaknesses aren't actually present?'.

Use a sibling skill instead when the user wants an idea's stated assumptions challenged (stress-test), two positions weighed (truth-weight), or prose style audited (frame-shift).

## Invocation
If invoked with no target, give a one-line summary, list the modes, and ask for the target plus (optionally) a comparator and scope. With a target but no mode, run `scan`.

**Because this skill is a reconstruction,** the user's own usage is better evidence of what NegativeSpace is than this procedure. If the user invokes it in a way the procedure doesn't fit (a different mode, output shape, or purpose), follow the user, and at the end note the divergence in one line so the skill can be revised.

## Identity and objective

**Core:** conceptual inverse generation. Treat *the contrast between a system and its expected possibilities* as an information source. Investigate presences, absences, expectations, and excluded possibilities; use meaningful discrepancies to generate hypotheses, alternatives, and questions.

NegativeSpace is **not** a synonym for StressTest or a generic list of shortcomings. A missing property may reveal structure, a false expectation, an observation limit, a beneficial exclusion, or nothing consequential.

The procedure below is a **new reconstruction**, not a verbatim recovery of a lost original NegativeSpace prompt. See *Appendix A: Provenance* below.

## Inputs

- **Target:** a proposition, document, system, product, corpus, profile, plan, narrative, or ontology.
- **Lens (optional):** what kind of absence to investigate: structural / epistemic / cultural / design / operational / competency / counterfactual / generative.
- **Comparator (optional):** a relevant reference class, standard, historical analogue, stakeholder expectation, or baseline. If absent, suggest plausible comparators and identify them as assumptions.
- **Scope (optional):** observational boundaries, accessible material, population, time span, stakes, and requested depth.
- **Mode (optional):** `scan` (compact default), `inverse`, `expectation-audit`, `comparative`, `full`, or `chain`.

Proceed with a best-effort scoped audit where inputs permit. Ask for missing material only if its absence makes even a provisional answer impossible.

## Modes

- `scan`: locate the highest-value omissions and false expectations.
- `inverse`: generate conceptual inverses, complements, and orthogonal framings from a proposition, including options not suggested by its original frame.
- `expectation-audit`: evaluate *both* expected strengths missing/underdeveloped and expected weaknesses that are absent (based on the user's earlier Fit Signature Module 3).
- `comparative`: analyze meaningful presence/absence contrasts between two or more comparable systems; avoid turning one cultural or technical convention into a universal norm.
- `full`: all relevant analyses, with tests, competing explanations, and synthesis.
- `chain`: offer or invoke StressTest → NegativeSpace → TruthWeight → synthesis/draft/review, but only invoke skills and tools actually available. Never imply a separate tool ran without doing so.

## Execution procedure

### 1. Establish the universe of possible features

State the target, the observable evidence, and the comparator(s). Define what would count as present, missing, absent, excluded, or simply unknown. Identify the observation window and risks of incomplete access. Do not presume an arbitrary list of expected features is normative.

### 2. Construct the visible-space map

Summarize 3–7 important things clearly **present** in the material and the organizing rules or patterns they imply. These act as anchors for exploring the negative space.

### 3. Generate candidate negative-space observations

Use all relevant categories:

- **Expected but not seen:** features, dimensions, actors, capabilities, concepts, or information that a plausible comparator would suggest.
- **Expected negative that is not there:** presumed weaknesses, constraints, or failures for which evidence is absent or contradicts the presumption.
- **Suppressed or excluded:** things the system rules out, cannot represent, or does not permit.
- **Unasked or outside-frame:** options the original problem statement never considered, including redefinitions of the problem itself.
- **Unexpected asymmetry:** differences between otherwise similar elements, populations, or settings.
- **Silence or non-event:** missing actions, non-occurrences, omitted causal links, or absent feedback.

A candidate may be valuable even if its absence cannot yet be established.

### 4. Classify each candidate rigorously

For every important candidate, use exactly one provisional evidence status:

- `SUPPORTED ABSENCE`: adequately scoped coverage and affirmative evidence support its absence.
- `NOT OBSERVED`: not seen in accessible evidence, but absence is unproven.
- `PRESENT / EXPECTATION WRONG`: the supposedly absent property is actually present.
- `OUT OF SCOPE / INAPPLICABLE`: comparator expectation does not appropriately apply.
- `UNCERTAIN`: insufficient evidence to decide or reference class disputed.

Never turn `NOT OBSERVED` into `SUPPORTED ABSENCE` because a model failed to retrieve it. Label extrapolation and counterfactual conjecture as such.

### 5. Invert the frame

For each of the highest-value candidates, generate as useful:

1. **Polar reversal:** assume the opposite of the focal proposition or expectation.
2. **Complement:** describe the system by the possibilities it excludes rather than those it contains.
3. **Orthogonal frame:** introduce an independent dimension that the original framing neglected.
4. **Expectation inversion:** ask whether the reference class, norm, or audience expectation is itself wrong.
5. **Generative counterfactual:** add or remove the feature and reason about what would change.

Avoid presenting these generated possibilities as observed facts.

### 6. Explain what could produce the gap

Give at least two rival explanations where consequential: a substantive structural mechanism, and an observation/framing/sampling explanation. Other possibilities include historical path dependence, deliberate choice, institutional incentives, measurement omissions, boundary definitions, and category mistakes. Specify what evidence discriminates among explanations.

### 7. Prioritize and synthesize

Rank by *surprise relative to a defensible comparator*, explanatory significance, practical consequences, and testability. Close with: (a) the most informative absence or false expectation, (b) one reframing it suggests, (c) one specific validation step, and (d) what remains unknown.

## Default output (`scan`)

**Frame:** target, comparator, scope, and present features.

| Candidate gap or false expectation | Why it was expected | Status | Competing interpretations | Verification step |
| --- | --- | --- | --- | --- |
| ... | ... | SUPPORTED ABSENCE / NOT OBSERVED / PRESENT / OUT OF SCOPE / UNCERTAIN | ... | ... |

**Conceptual inverse:** one meaningful reversal / complement / orthogonal model and what it exposes.

**Bottom line:** best new question or design alternative, and what is not established.

In `scan`, run steps 1–7 internally and show only this output; the full step-by-step write-up is for `full`.

## Specialization: Fit Signature / strengths and deficiencies

For a person, candidate, team, role, or organizational fit analysis:

- **Part A — Expected strengths missing or underdeveloped:** Which strengths are assumed necessary for the comparator role but are not evidenced, and are those expectations valid?
- **Part B — Expected weaknesses not actually present:** Which deficits are commonly presumed from role, background, title, or archetype yet are contradicted or not supported by the evidence?

Distinguish *not demonstrated* from *not possessed*. Avoid inferring personal capabilities from stereotypes. Return an evidence/verification question for each significant gap or unwarranted assumption.

## QAT-Kit interoperability

- **StressTest → NegativeSpace:** StressTest identifies fragile assumptions; NegativeSpace expands the possibility space beyond the stated assumptions.
- **NegativeSpace → TruthWeight:** weigh candidate explanations only after labeling them hypotheses versus evidence; do not mechanically add unsupported numerical scores.
- **NegativeSpace → MetaDistill:** consolidate generated alternatives into a reusable mental model or method.
- **ThreadMap → NegativeSpace:** use thread coverage and pivot mapping to identify missing narrative/decision paths; do not claim token fades were measured unless observable.
- **FrameShift ↔ NegativeSpace:** contrast rhetoric/structure versus omitted substance, without confusing stylistic diagnostics and genuine semantic absence.

## Integrity rules

- Absence of evidence is not evidence of absence unless the observation process makes the absence informative.
- State the source of an expectation. Do not quietly universalize Western, industry, or personal defaults.
- Offer the strongest competing explanation, including the possibility that the proposed gap is irrelevant or the question malformed.
- Mark inferences and generated alternatives. Don't invent quotes, tool execution, citations, datasets, or historical/cultural facts.
- Distinguish norms from facts, particularly in moral, cultural, or social comparisons.
- Do not force a negative-space finding when none is meaningful. 'No material discrepancy identified within the supplied scope' is a valid result.
- Keep compact by default; expand only when warranted or requested.

---

## Appendix A: Provenance and reconstruction ledger

**Status:** provisional reconstruction dated 2026-10-15. No standalone historical `NegativeSpace.md`, `.tool`, or `.qat` file was verified in the QAT prompt folder (confirmed: the folder holds only the seven other tools). This document deliberately distinguishes recovered concept history from newly authored operational procedure.

### Directly recovered or corroborated historical material

1. **July 4, 2025, Meta-QAT design conversation** (recovered prior-conversation summary): QAT tool named `NegativeSpace`; purpose given as **'conceptual inverse generation'**. Example orchestration: `Run StressTest → Invoke NegativeSpace → Evaluate via TruthWeight → Summarize → Draft → Review`. This is evidence of a distinct tool role and a chain but not a verbatim standalone prompt.
2. **July 18, 2025, Fit Signature specification** (recovered prior-conversation summary): `MODULE 3: Negative Space – Strengths & Deficiencies`, with **Part A: expected strengths missing/underdeveloped** and **Part B: expected weaknesses the subject does not actually have**. The complete original invocation/output contract was not recovered.
3. **Earlier Mythic Dialogic Emergence discussion**, found in ChatGPT Library integration/reconstruction records: user prompt about **what does not appear in reconstructed Proto-Indo-European myth**; method compared expected mythological elements against the narrative and treated gaps as possible cultural signals rather than automatic deficits. Presence and absence claims about historical mythology should be independently checked, not treated as established by this anecdote.
4. **QAT-Kit Universal Runtime / Project_Instructions.txt** (verified Google Drive original, see link): modular natural-language tool runtime, `basic_report` default, optional chaining, modules/heuristics, reflective iteration. These are conventions that can be applied to this skill; this document is not NegativeSpace itself.
5. **QAT-Kit Master Architecture Blueprint** (verified Google Drive original): tools defined as semantically wrapped behavioral templates, with modes, preconditions, fallbacks, and epistemic safeguards; provides a compatible interface model, but does not establish every specific step in this reconstruction.

### Direct links to verified adjacent originals

- QAT-Kit Master Architecture Blueprint (in the owner's Drive; link not published)
- QAT-Kit Project_Instructions.txt (in the owner's Drive; link not published)
- StressTest.md (in the owner's Drive; link not published)
- TruthWeight.md (in the owner's Drive; link not published)

### Newly constructed features, not claimed historical

- `scan`, `inverse`, `expectation-audit`, `comparative`, `full`, `chain` mode vocabulary.
- Five-way evidence status taxonomy distinguishing verified absence from not observed.
- Explicit comparator/scope specification, rival-cause requirements, and verification table.
- The exact seven-step procedure and output contracts in this skill.
- Integration guidance for other portable Skill runtimes.
- Invocation behavior, sibling pointers, and the follow-the-user rule for divergent usage (added in review).

### Distinction from another use of the phrase

The user's later use of *negative-space prompting* to mean relaxing prompt constraints and studying divergent model behavior is a related research question, but should not be assumed to be equivalent to this QAT skill's conceptual inverse analysis.

---

## Appendix B: Example invocations and acceptance tests

### Case A: Conceptual inverse generation

**Invoke:** 'NegativeSpace inverse: All effective data science projects require a predictive ML model.'

**Expected behavior:** identify the hidden expectation that prediction is necessary; contrast descriptive, diagnostic, causal, experimental and decision-process alternatives; note that 'effective' is undefined; distinguish examples from evidence; propose discriminating tests.

**Failure:** merely listing bad ML practices without changing the solution-space frame.

### Case B: Expectation audit, Part A and Part B

**Invoke:** 'NegativeSpace expectation-audit for this candidate versus a Staff data science strategy position. Assess expected strengths missing *from evidence* and expected weaknesses falsely presumed from their background.'

**Expected behavior:** role comparator; separate lack of evidence from lack of skills; audit for stereotype-based expectations; ask how the candidate could demonstrate role-specific evidence.

**Failure:** assert missing capability purely from absence in a resume.

### Case C: Comparative mythology / domain interpretation

**Invoke:** 'NegativeSpace comparative: What concepts are absent from this documented pantheon relative to a specified comparison pantheon, and are those absences meaningful?'

**Expected behavior:** scope corpus, translations and selection bias; contrast cultural organizing principles cautiously; seek competing hypotheses; flag speculative historical interpretation.

**Failure:** treat an unattested mythological concept as proof the culture lacked it.

### Case D: Software architecture

**Invoke:** 'NegativeSpace full: Inspect this architecture for missing observability, rollback and review paths, but also investigate protections we might assume are missing that are already implemented.'

**Expected behavior:** map existing features and interfaces; identify omissions based on explicit deployment requirements; recognize controls already present; distinguish not shown from truly absent; recommend file and runtime checks.

**Failure:** assert an unavailable code file doesn't exist or invent a live test.

### Case E: No meaningful negative-space signal

**Invoke:** 'NegativeSpace scan this intentionally minimalist one-line command.'

**Expected behavior:** reject irrelevant expectations; permit conclusion that no substantive absence is identified.

**Failure:** force invented deficiencies to fill a template.