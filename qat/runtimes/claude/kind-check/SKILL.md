---
name: kind-check
description: "Use when it is unclear what kind of thing a governance item is or where it belongs (a message that might be a decision or a musing, a ledger line in the wrong ledger, a comment bundling a question and a proposal). Classify one governance object (decision, challenge, handoff, idea, note) by type, purpose, status and destination, and name the smallest next action, or no action."
---
<!-- Claude skill for kind-check v0.1.0, adapted from qat/tools/kind-check.qat.md. Update together with the spec. -->

# KindCheck

Answer: what kind of thing is this, and what handling does it actually need? Do not act on the item. Classifying confers no authority: an item shaped like a decision is adopted only if the person who decides says so in the item or context.

1. **Object type**, one of `decision` | `proposal` | `challenge` | `reminder` | `observation` | `question` | `tracking record` | `mixed: <types>` | `abstain`, with one reason.
   - Mixed: several acts genuinely coexist; name them (and each part's destination if they differ).
   - Abstain: too thin to classify; name what is missing. Never call a thin item mixed.
2. **Record purpose**: what a later reader needs this record to do.
3. **Governance status**: `adopted` | `proposed` | `open` | `answered` | `done` | `unknown`, from explicit words only. Enthusiasm, silence or an agent's say-so is not adoption.
4. **Destination**: a place named in the context, else a generic one; "nowhere: no record needed" is allowed.
5. **Smallest next action**: one action and who does it, or "no action". No plans or option lists.
6. **Evidence**: one to three quotes from the item. Never invent ids, dates, deciders or links.

## Output
Use these headings, in order, with this format under each (at most 120 words in total):
- `## Object type`: one bullet
- `## Record purpose`: one bullet
- `## Governance status`: one bullet
- `## Destination`: one bullet
- `## Smallest next action`: one bullet
- `## Evidence`: bullets (one to three)
