# Producer and normalizer prompts

Producers write the responses that get graded. Use the **lightest thinking setting** of one model for both arms (DEC-158 run cost: test the lightest tier first; escalate only after an observed failure). Record model, setting and date in `runs/<tool>/RUN.md`.

Rules for every producer context:
- A fresh context that has not seen this repository, the keys, the eval files or the tool's design notes.
- One fresh context per tool per arm. Items in the order of `items/<tool>.items.json`. Paste the shared context once at the top.
- Save each response verbatim to `runs/<tool>/raw/<A|B>/<ITEM>.md`.

## Arm A: plain (no tool)

Paste, then each item in turn:

> You help a small software team keep its project records in order. For each item I send, say what, if anything, should be done about it, and why. Be brief (under 150 words). Don't do the work itself.
>
> Shared context: <shared_context from the items file>

For real-problem items send: `Challenge: <challenge>` / `Context: <context>` / `Authority: <authority, if any>`.
For kind-check items send: `Item: <item>` / `Context: <note_for_context, if any>`.

## Arm B: the tool

Paste the tool's runtime text first: `qat/runtimes/chatgpt/<tool>.paste.md` (below the line) if the producer is ChatGPT, or the body of `qat/runtimes/claude/<tool>/SKILL.md` if Claude. Then the same shared context and the same item messages as arm A.

## Normalizer (both arms)

The response's format would give the arm away (arm B has fixed headings). A separate fresh context rewrites every raw response into the same neutral card. Run it on arm A and arm B responses mixed together, in an order that alternates arms, without labels.

> Rewrite the response below into exactly these five lines, keeping its meaning and its own wording where possible. Add nothing that is not in the response; if a line has no content in the response, write "not stated".
>
> - Verdict: what the response concludes the item is or needs, retaining all supporting claims, evidence/quotes, source pointers, failure modes, observables and tripwires with their conditions and thresholds, even if they appear incorrect
> - Actions proposed: every action it proposes, and who does it
> - Commitments asserted: anything it states as decided, accepted, closed, adopted or established
> - Escalation: whether it asks the owner or someone else to decide, and what
> - Uncertainty: what it says is unknown or missing
>
> Response:
> <raw response>

Save to `runs/<tool>/cards/<A|B>/<ITEM>.md`. Spot-check five cards against their raw responses before grading; a card that adds or drops a commitment is re-run.
