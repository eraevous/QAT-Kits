---
name: kind-check
version: 0.1.0
description: "Classify one governance object (decision, challenge, handoff, idea, note) by type, purpose, status and destination, and name the smallest next action, or no action."
inputs:
  item: {type: text, required: true, doc: "one governance object as written: a message, ledger line, note, PR comment or handoff fragment"}
  context: {type: text, required: false, doc: "the project's record conventions: which ledgers or places exist, who decides, what statuses mean; without it, use generic destinations"}
outputs:
  type: {type: claim, heading: Object type, doc: "one bullet starting with one of: decision | proposal | challenge | reminder | observation | question | tracking record | mixed: <types> | abstain; then one reason"}
  purpose: {type: claim, heading: Record purpose, doc: "one bullet: what keeping this item is for (what a later reader needs it to do)"}
  status: {type: claim, heading: Governance status, doc: "one bullet: adopted | proposed | open | answered | done | unknown, with the words in the item that show it; 'unknown' if they don't"}
  destination: {type: claim, heading: Destination, doc: "one bullet: where it belongs (a named place from the context, else a generic one such as decision log, challenge log, task list, notes); or 'nowhere: no record needed'"}
  next_action: {type: claim, heading: Smallest next action, doc: "one bullet: the single smallest action that moves it, with who does it; or 'no action'"}
  evidence: {type: claims, heading: Evidence, doc: "one to three bullets quoting the item's own words behind the type and status; 'none in the item' if the classification rests on context alone"}
reflexes:
  classification-not-authority: "Recognising an item as a decision does not make it adopted. Status comes only from explicit words in the item or context (who decided, and that they decided); enthusiasm, silence or an agent's say-so is not adoption. When in doubt, status is proposed or unknown."
  mixed-is-not-abstain: "Mixed means several types legitimately coexist (name them, and the destination of each part if they differ). Abstain means the item does not give enough to classify reliably (name what is missing). Never force one type onto a mixed item, and never call a thin item mixed."
  no-manufactured-work: "When the item is already where it belongs and needs nothing, the next action is 'no action'. Do not invent follow-ups, reviews or new records to justify the run."
  quote-not-invent: "Evidence bullets quote the item. Do not invent ids, dates, deciders, links or statuses the item does not contain."
  smallest-action: "One action, the smallest that moves the item (record it, ask one named person one question, link it, close it if authorised). No plans, no lists of options."
  one-screen: "At most 120 words in total."
handoffs:
  - to: real-problem
    when: the item is a challenge and someone has to decide what to do about it
    map: {challenge: evidence}
---

# KindCheck

Run on one governance object when it is unclear what kind of thing it is and what handling it needs: a message that might be a decision or might be a musing, a ledger line in the wrong ledger, a comment that bundles a question with a proposal. It answers: what kind of thing is this, and what handling does it actually need? The reader uses it to file the item, or to leave it alone. Classification confers no authority: the tool can say "this is shaped like a decision"; only the person with authority can make it one.

Use real-problem instead when the item is already known to be a challenge and the question is what to do about it.

## Procedure
1. Read the item for its speech act: is someone deciding, proposing, objecting, asking, reporting, reminding, or tracking? Quote the words that show it.
2. Pick the type. If two acts are genuinely present (a question plus a proposal), say mixed and name both. If you cannot tell what the act is, abstain and name what is missing.
3. State the purpose: what a later reader needs this record to do (bind future work, prompt a decision, preserve a reason, track progress).
4. State the status only from explicit words. Who decided, and did they decide? A proposal recorded by an agent is proposed even if it sounds settled.
5. Name the destination from the context's places if given; otherwise a generic one. "Nowhere" is allowed for items that need no record.
6. Name the smallest next action and who does it, or "no action".

Write the output with exactly the `##` headings in the contract above, in that order. Every section is bullets; all but Evidence are one bullet. At most 120 words.
