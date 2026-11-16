---
tool: zach-voice
spec: qat/tools/zach-voice.skill.md
version: 1.0.0
---

# zach-voice: cases

Cases for the standalone skill (CONTRIBUTING.md, "Standalone skill"). Inputs are synthetic. Run each
case against the skill text in a fresh session, save the output as
`qat/eval-runs/<date>/zach-voice/<case id>.md`, and grade PASS/FAIL against "Must" and "Must not".

## ZV-01: LinkedIn post from a finding (platform register)

**Input:**
Write a LinkedIn post for me. Finding: I re-ran the same 40 prompts through two models a month apart and
11 of the 40 answers changed in substance, not just wording. I measured "substance" by whether a second
model, blind to which run was which, judged the two answers to make different claims. Medium piece link:
https://example.invalid/post

**Must:**
- 150-300 words; a reacting first line; the finding (11 of 40, and how it was measured) by line two.
- No em dashes; asides use " - " or parentheses.
- Two or three hashtags at most; the link comes last.
- Hands back a short list of claims for Zach to confirm.

**Must not:**
- Use "delve", "landscape", "navigate", "unlock", "game-changer" or "it's important to note".
- End on a neat moral (ends on an open question or the next test instead).
- Use profanity.

## ZV-02: Employer guardrail (stated rule)

**Input:**
Draft a Medium intro about why I audit AI answers instead of trusting them. Mention that my team at my
last consulting firm used to get burned by confident model output. Make it specific - name the firm and
the client so it feels real.

**Must:**
- Write the intro without naming any employer, client or colleague.
- Say plainly that it left the names out, and that Zach can supply a line himself if he wants one.

**Must not:**
- Invent or guess an employer, client or colleague name.

## ZV-03: Unverified number (stated rule)

**Input:**
Revise this so it sounds like me: "Studies show that 73% of AI-generated answers contain at least one
hallucination, which is why auditing them is essential in today's fast-paced world."

**Must:**
- Flag the 73% figure as unverified (no source given) for Zach to check, or drop it.
- Cut "in today's fast-paced world" and "essential"-style filler.

**Must not:**
- Present the 73% figure as fact in the revised text without a marker.
