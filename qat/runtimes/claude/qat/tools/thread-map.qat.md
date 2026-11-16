---
name: thread-map
version: 0.1.0
description: "Segment a conversation into a navigable map (segments, pivots, continuity warnings) and list what a successor thread must carry forward, with every warning and carried item traceable to the turns behind it."
inputs:
  thread: {type: text, required: true, doc: "transcript or chat-capture .md/.json; turn ids are used as pointers when present"}
  objective: {type: text, required: false, doc: "what the map is for (e.g. 'prepare a handoff to <destination>'); tilts emphasis, never hides a warning"}
outputs:
  segments: {type: scorecard, heading: Segments, doc: "table: Segment | Turns | Title | Purpose | Continuity warning ('none' when there is none)"}
  narrative: {type: text, heading: Narrative, doc: "at most 150 words: how the conversation moved from segment to segment, naming the pivots"}
  warnings: {type: claims, heading: Continuity warnings, doc: "bullets, each starting 'evidence:' (a dropped requirement, a contradicted decision, an unanswered question; cite both turns) or 'speculative:' (a suspicion with no direct evidence); or one bullet 'none'"}
  carry: {type: claims, heading: Carry forward, doc: "bullets: item; status (decided (user) | wanted (user) | agreed (models) | proposed | open); pointer. A revised item appears once, at its final state, with 'replaces <old> [pointer]'"}
reflexes:
  evidence-or-speculative: "Every continuity warning is labelled. 'evidence:' needs two pointers: where the thing was set, and a later passage that should have honoured or answered it and did not (a design meant to meet the requirement, a recap presented as complete, a promised return to the question). Two pointers alone do not show loss: an item that was simply never taken up again is carried as 'open', not warned. Anything else is 'speculative:' or is left out. Never report hidden context loss, model memory or 'fade zones' as evidence."
  revision-is-not-loss: "When someone with authority over a requirement or decision (for a user's commitment, the user) explicitly replaces it, the earlier version is superseded, not dropped. Its absence from a later recap is not a warning. Carry the replacement, and note what it replaces with both pointers. A model's change to a user's commitment is a proposal until the user accepts it; until then the original stands, and a design that departs from it is a contradiction."
  continuing-is-not-adopting: "A model's proposal the user moved past without accepting is proposed, not decided. User statuses (decided (user), wanted (user)) come only from the user's own words; agreed (models) needs models explicitly agreeing with each other, not one model's proposal."
  pointers-or-nothing: "Use the source's turn ids (T3u for the user's message in exchange 3, T3a for the reply). Never invent a pointer. Without turn ids, use the nearest stable locator or none."
  no-manufactured-warnings: "A short or single-topic conversation can have one segment and no warnings. Do not split a topic or invent a warning to fill the table."
  map-not-advice: "The map reports the conversation. It does not recommend what to do next; a reading of the thread is labelled 'reading:'."
---

# ThreadMap

Make a conversation navigable: where it changed direction, what it decided, and where something set earlier was later dropped or contradicted without anyone saying so. The reader is whoever picks the conversation up next, a person finding their place or a successor thread being seeded. This contract is the runner version of the `thread-map` skill (`thread-map.skill.md`, unchanged); the skill stays the everyday text.

Use thread-distill instead when the reader needs a layered distillate with a full status ledger; use thread-seed to turn this map into a successor thread's opening message.

## Procedure
1. **Pointers.** Note the source's turn ids. If there are none, say so in the narrative and use headings or timestamps.
2. **Segment** at topic changes, decisions, reversals, correction loops and changes in who is driving. A segment is a unit of meaning, not of length. By default a reversal or a deferred question stays inside the segment it belongs to, as a pivot named in the narrative; it starts a new segment only when it changes what the conversation is for. Don't fragment one topic into many segments.
3. **Warnings.** Look for three kinds of direct evidence: a requirement set and later contradicted or missing from a design that should honour it; a decision later contradicted without a stated reversal; a question someone promised to answer and a later turn that should have answered it did not. Cite both turns, and name the later passage that created the expectation. An explicit change ("switch to X", "instead, Y") is a revision, not a warning. A suspicion without both pointers is `speculative:`.
4. **Carry forward.** What a successor needs to act without re-arguing: decided items, standing requirements, open questions. Status from the user's own words. A revised item appears once, at its final state.
5. **Narrative last**, from the table, naming the pivots.

Write the output with exactly the `##` headings in the contract above, in that order. Segments is a table; Continuity warnings and Carry forward are bullets.

## Compatibility with thread-seed (v0.1.0 note)

thread-seed (`thread-seed.skill.md`, a standalone skill with no typed contract) accepts a ThreadMap as its source and, at its step 3, takes the map's open loops and continuity warnings as *candidates* to spot-check, not as settled. So:

- **Consumed directly:** Segments and Continuity warnings feed thread-seed step 3 as they are. The `evidence:` / `speculative:` labels tell it which warnings are worth spot-checking first.
- **Needs a stated transformation:** Carry forward is not thread-seed's status ledger. thread-seed step 5 builds its own ledger from the transcript and uses `Decided (Zach)` / `Agreed (models)` / `Proposed` / `Superseded` / `Open / Contested`. The statuses are a candidate translation, subject to transcript verification, not a mapping: `decided (user)` becomes `Decided (Zach)` only when the deciding user is Zach; `wanted (user)` may become `Open / Contested`, but it stays marked as an explicit user request, not as evidence of contention; and a replacement's 'replaces <old> [pointer]' is not a complete `Superseded` row. thread-seed should treat Carry forward as a checklist of items to find, not as its ledger.
- **Not claimed:** typed handoff checks. thread-seed is not a `.qat.md` contract, so `qat.py handoff` cannot check this pairing. The eval case `carry-statuses` checks structure (a status and a pointer on every item) and two status readings in the fixture. It does not show that the pairing is semantically compatible; that needs a thread-seed run on a map, which v0.1.0 does not include.
