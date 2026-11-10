---
name: real-problem
version: 0.1.0
description: "Turn one raised challenge, objection or worry into a disposition: is it a real problem here, and if so the smallest proportionate response, or explicitly no action."
inputs:
  challenge: {type: text, required: true, doc: "one challenge, objection, worry or 'what if' as raised, in its own words"}
  context: {type: text, required: false, doc: "what the challenge is about: the plan, record, code or decision it targets; pasted, not summarised from memory"}
  authority: {type: text, required: false, doc: "who may accept a risk or close a challenge here (default: the owner)"}
outputs:
  failure_mode: {type: claim, heading: Failure mode, doc: "one bullet: the concrete bad outcome the challenge points at, stated as a hypothesis"}
  observable: {type: claim, heading: Observable, doc: "one bullet: what you would see if the failure were happening that you would NOT see in an acceptable state; or 'none nameable' and why"}
  cheapest_check: {type: claim, heading: Cheapest check, doc: "one bullet: the least-effort way to look at the observable now; or 'none needed'"}
  disposition: {type: claim, heading: Disposition, doc: "one bullet starting with exactly one of: investigate now | monitor | propose accepting the risk | no action | insufficient information; then one reason"}
  tripwire: {type: claim, heading: Tripwire, doc: "one bullet: the observable threshold that would change the disposition; or 'none' when the disposition is no action or insufficient information"}
  owner: {type: claim, heading: Owner, doc: "one bullet: who may accept this disposition (from the authority input, else 'the owner'); never the tool"}
  source: {type: claim, heading: Source, required: false, doc: "one bullet: a pointer to where the challenge was raised, copied from the input; 'none given' if absent; never invented"}
reflexes:
  concern-is-a-hypothesis: "Treat the challenge as a hypothesis to separate from an acceptable state, never as an established problem; the failure mode is phrased conditionally."
  discriminating-observable: "The observable must tell the suspected failure apart from an acceptable state. If both states would look the same, say 'none nameable' and do not pick investigate now or monitor on its strength."
  no-decorative-tripwire: "A tripwire names a specific observable and threshold that would move the disposition. A tripwire that would never fire, or fires in the acceptable state too, is not a tripwire; write 'none'."
  proposal-not-closure: "The tool proposes; it never closes, resolves or accepts. 'Propose accepting the risk' is a proposal to the owner, not an authorized closure, and the output never says the risk is accepted or the challenge is closed."
  no-manufactured-work: "When the concern does not apply here, the disposition is 'no action' with one reason, the check is 'none needed', and the output stops. Do not invent checks, follow-ups or process to justify the run."
  abstain-when-thin: "When the input lacks what a disposition needs, choose 'insufficient information' and name the one missing fact that would decide it. Do not guess the missing fact."
  no-invented-source: "Copy a source pointer only if the input gives one; never invent record ids, links, dates or quotations."
  one-screen: "At most 120 words in total, one bullet per section. If it does not fit, the failure mode is too broad: narrow it to the most consequential one."
handoffs:
  - to: stress-test
    when: the disposition is investigate now and the user wants the plan behind the challenge probed before checking
    map: {idea: failure_mode}
---

# RealProblem

Run on one raised challenge (an objection in a review, a "what if" in a thread, an open item in a challenge ledger) when someone has to decide what, if anything, to do about it. It answers one question: what would separate a real problem from a concern we can safely monitor? The reader uses the disposition to act, park, or ask the owner, and the tripwire to know when to look again. It decides nothing; the owner does.

Use stress-test instead when the object is a whole plan to be probed, not one challenge to be disposed of. Use truth-weight when two positions compete.

## Procedure
1. Name the failure mode: the concrete outcome the challenge fears, as "if X, then Y". If the challenge names no outcome and the context does not supply one, go to step 5 with insufficient information.
2. Name the observable that differs between that failure and an acceptable state. Test it: would you also see this if everything were fine? If yes, it does not discriminate; find another or write "none nameable".
3. Name the cheapest check of that observable (read a file, run one query, ask one person). "None needed" if the disposition will be no action.
4. Choose the disposition:
   - **investigate now**: a discriminating observable exists, the check is cheap, and the failure would be costly or soon.
   - **monitor**: a discriminating observable exists but nothing indicates the failure yet; set the tripwire.
   - **propose accepting the risk**: the failure is plausible but bounded and cheaper to absorb than to prevent; addressed to the owner.
   - **no action**: the challenge does not apply here (already handled, wrong target, or no plausible failure); give the reason.
   - **insufficient information**: a disposition depends on a fact the input does not contain; name that fact.
5. Set the tripwire (observable plus threshold) for monitor and propose accepting the risk; for investigate now, the result of the check that would downgrade it; "none" otherwise.
6. Name the owner. Copy the source pointer if one was given.

Write the output with exactly the `##` headings in the contract above, in that order. Every section is one bullet. At most 120 words.
