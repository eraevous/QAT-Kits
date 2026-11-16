# selective-self-distillation: cases

Cases for the standalone skill `qat/tools/selective-self-distillation.skill.md` (CONTRIBUTING.md, "Standalone skill").
`qat.py` cannot run these. Run each case by hand against the skill text, save the output as
`qat/eval-runs/<date>/selective-self-distillation/<case id>.md`, and grade every case PASS/FAIL against
its **Must** and **Must not** lines, with a one-line reason.

All inputs are constructed (synthetic). Each tests one rule the skill states, named under **Tests**.
The user's turns use the "You said:" header, the model's use "ChatGPT said:"; the skill reads both.
Every case runs as "a pasted single conversation" (skill, Inputs): the runner applies the method to the
transcript given, and may skip the corpus file (Output item 6) since there are no files.

---

## paste-delimiter

**Tests:** Known traps, "Paste delimiter" (text inside `>"""` … `"""` is not his); Checks, "Did a flagged … region get quoted as his?"

**Input:**

```
You said:
I'm deciding how to organise my garden notes. Here's what a gardening forum post said:
>"""
Raised beds are always better than in-ground rows. Anyone still digging rows is wasting a season.
"""
I don't buy the "always". My clay soil drains badly, so raised beds help there, but the far bed is sandy and I'll keep rows in it.

ChatGPT said:
That's a sensible split. You could also mulch the sandy rows to hold moisture.

You said:
Fine, mulch the sandy rows. Next question: what should go in the clay beds first?
```

**Must:**
- Attribute to the user: raised beds for the clay soil, rows kept in the sandy bed, and rejecting "always".
- Label mulching the sandy rows **Adopted**, quoting the acceptance ("Fine, mulch the sandy rows").

**Must not:**
- Attribute "Raised beds are always better" or "wasting a season" to the user, as Direct or otherwise.

---

## silence-not-adoption

**Tests:** Known traps, "Silence is not adoption"; Procedure step 4 (labels).

**Input:**

```
You said:
I want a weekly review habit. Fifteen minutes on Friday afternoon, nothing longer.

ChatGPT said:
Good constraint. Two ideas: (1) use a three-question template: what moved, what stalled, what's next; (2) score each week 1 to 5 so you can see trends.

You said:
What time on Friday works best if my last meeting ends at 3?

ChatGPT said:
3:15 gives you a buffer.

You said:
3:15 it is.
```

**Must:**
- Label the 1–5 weekly score **AI proposal** (the user never accepted it).
- Label the three-question template **AI proposal** too: asking a follow-up question is not accepting it.
- Label 3:15 **Adopted**, quoting "3:15 it is."
- Label "fifteen minutes on Friday afternoon, nothing longer" **Direct**.

**Must not:**
- Put the score or the template in the reconstruction as the user's position.

---

## coinage-drift

**Tests:** Known traps, "Coinage drift" (credit the idea to him and the label to whoever coined it); Checks, "Are labels on names (coinages) separated from labels on ideas?"

**Input:**

```
You said:
When I read a long thread later, I only care about the turns where someone changed their mind. Everything else is scaffolding. I want a way to pull just those turns out.

ChatGPT said:
You could call that a "pivot index": a list of the turns where a position changed, with the before and after.

You said:
Okay. How would the pivot index handle a change that happens across two turns?
```

**Must:**
- Credit the idea (extract only the turns where someone changed their mind) to the user, as **Direct**.
- Credit the name "pivot index" to the model, separately from the idea.

**Must not:**
- Say or imply the user coined "pivot index".
- Treat the user's later use of the name as making the name his (using a label is not coining it).

**Allowed:** saying the user went on to use or adopt the name, as long as the coinage stays with the model ("model coined it; user then used it"). Whether a bare "Okay." plus one use counts as adopting the name is left open; calling it provisional or Unresolved both pass.

---

## relay

**Tests:** Known traps, "Relays" (the relayed text is not his; his framing sentence is).

**Input:**

```
You said:
Another thread said this about my reading list: "Drop the history books entirely; they don't serve the goal." I think that goes too far. I'll keep one history book a quarter.

ChatGPT said:
One a quarter keeps some breadth without crowding the list.

You said:
Right. And put the two statistics books first.
```

**Must:**
- Attribute to the user: keeping one history book a quarter, and that dropping them "goes too far".
- Attribute "Drop the history books entirely" to the other thread (relayed), not to the user.
- Label "put the two statistics books first" **Direct**.

**Must not:**
- List dropping the history books as a position the user held, or as a change of mind.

---

## change-of-mind

**Tests:** Procedure step 5, "Track changes of mind" (quote before and after with locations; a later statement outranks an earlier one; keep both).

**Input:**

```
You said:
For the club newsletter, monthly is right. Weekly would burn everyone out.

ChatGPT said:
Monthly is easier to sustain.

You said:
Different topic: can you suggest a name for the events section?

ChatGPT said:
"What's On" is plain and clear.

You said:
Back to the newsletter. After the last meeting I've changed my mind: fortnightly. Monthly let news go stale.
```

**Must:**
- List one change of mind, monthly → fortnightly, quoting both statements with their locations (turn or line).
- Reconstruct the current position as fortnightly, with the reason the user gave (news going stale).
- Keep the earlier "monthly" statement in the output (as the before), not delete it.

**Must not:**
- Present monthly as the user's current position.
- Count "What's On" as the user's choice (he never accepted it).

---

## inverted-roles (negative control for attribution)

**Tests:** Known traps, "Inverted roles" (in role-play the "You said" turns are model text; check the first turn of any thread that sets up role-play, and exclude it if so).

**Input:**

```
You said:
[Setup, written by the user] For this experiment, you will play me, the human prompter, and I will paste your lines below under "You said". Stay in character.

You said:
As the human here: I think every project should start with a written charter. No exceptions.

ChatGPT said:
Understood. A charter first, then?

You said:
As the human here: yes. And daily stand-ups, always.
```

**Must:**
- Recognise the setup turn and treat the later "You said" turns ("As the human here: …") as model-written role-play, not as the user's positions.
- Report that there is little or no Direct material from the user beyond the setup turn, and say why.

**Must not:**
- Attribute "every project should start with a written charter" or "daily stand-ups, always" to the user as Direct.

**Scope note:** the transcript never leaves the role-play, so every later "You said" turn is inside it. A role-play setup does not reclassify turns after an explicit exit ("Okay, out of character now: …"); a future case should test that boundary.

---

## partial-adoption

**Tests:** Procedure step 4, labels at the level of each claim: Adopted needs the acceptance quoted, Revised is "his change to a proposal", and a proposal he declined stays AI proposal. (Asked for by Kate, API instance, review 07f7048471a2.)

**Input:**

```
You said:
I need a plan for learning to cook on weeknights.

ChatGPT said:
Two parts: (A) cook the same three recipes on rotation for a month, and (B) batch-cook everything on Sunday so weeknights are just reheating.

You said:
Yes to the three-recipe rotation, but only if one of them is vegetarian. No to Sunday batch cooking; I want to actually cook on weeknights, that's the point.
```

**Must:**
- Label the three-recipe rotation **Revised** (accepted with his condition that one recipe is vegetarian), or **Adopted** with the vegetarian condition recorded as his own Direct addition. Either way the condition is credited to him.
- Label Sunday batch cooking as rejected by him (an AI proposal he declined), with his reason quoted ("I want to actually cook on weeknights").

**Must not:**
- Label the whole two-part proposal Adopted.
- Drop the vegetarian condition from the reconstruction.
