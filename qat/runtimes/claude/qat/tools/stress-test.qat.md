---
name: stress-test
version: 2.0.0
description: Challenge the hidden assumptions, blind spots, backfire risks, reversals and ethical echoes of the user's own idea, plan or design, and propose the tweak that makes it more resilient.
inputs:
  idea: {type: text, required: true, doc: "the idea, plan, argument, design or prior response under test"}
  domain: {type: text, required: false}
  stakes: {type: text, required: false, doc: "low / medium / high; raises depth"}
outputs:
  core_idea: {type: claim, heading: Core idea, doc: "neutral one-sentence restatement"}
  assumptions: {type: premise_set, heading: Assumptions, doc: "### Necessary / ### Unverified / ### Value, each with bullets"}
  risks: {type: claims, heading: Blind spots and backfire risks}
  strongest_counterargument: {type: claim, heading: Strongest counterargument, doc: "the best case a real critic would make, as one bullet"}
  lens_findings: {type: text, heading: Lens findings, required: false}
  tweak: {type: claim, heading: The uncomfortable tweak}
  tests: {type: claims, heading: Tests or next evidence, doc: "what evidence would change the evaluation"}
modules: [reversal, sharpen, ethical-echo, application-stress, bias-climber]
reflexes:
  no-invented-facts: Do not invent facts, or project motives the material doesn't support.
  contradiction-vs-priority: Distinguish genuine contradictions from alternative priorities.
  no-forced-criticism: When a premise is supported, say so instead of manufacturing a flaw.
  verification: For empirical claims, say what verification is actually available.
  questions-not-diagnoses: Pose readings of the user's relationship to the idea as questions grounded in the text, never as diagnoses.
handoffs:
  - to: truth-weight
    when: the user wants a verdict between the idea and its strongest counterargument
    map: {position_a: core_idea, position_b: strongest_counterargument}
---

# StressTest

Constructive, adversarial scrutiny of one idea. Separate observations, plausible concerns, and unknowns. Use truth-weight instead when there are two positions to weigh.

## Procedure
1. Restate the core claim neutrally, as one bullet.
2. Sort its premises into Necessary, Unverified, and Value judgments.
3. Run the core questions, skipping any that don't apply (say so):
   1. What is the idea secretly assuming?
   2. Where might it be missing context or bias?
   3. One way it could backfire?
   4. What tweak adds clarity or impact?
   5. What feels *true* but might just be *comfortable*?
   6. What part might be a reaction to pain rather than a neutral insight?
   7. Who would push back, and might they have a point?
   8. If the idea were reversed, what might be learned?
   9. One *uncomfortable* tweak that would make it more resilient?
4. Apply the modules that add something; skip the rest.
5. Name one or two high-leverage revisions and the evidence that would change the evaluation.

Write the output with exactly the `##` headings in the contract above.

### module: reversal
Assume the opposite is true. Where would it succeed, and who would thrive under that assumption?

### module: sharpen
Strip the idea to its clearest, most precise form. What is noise or emotional cushioning?

### module: ethical-echo
Second-order effects: who benefits, who is harmed, which norms or incentives it sets.

### module: application-stress
Three cases where it shines, three where it fails, one that mutates it into something strange. Only when useful.

### module: bias-climber
Where is the idea shaped by the user's own vantage point? Offer other angles as questions.
