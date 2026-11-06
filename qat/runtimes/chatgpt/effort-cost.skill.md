---
name: effort-check
description: Use when the user asks what an answer costs the environment (energy, carbon, water) at different model or reasoning-effort settings, whether to turn the effort up or down for this conversation, or says "effort check". Prices every setting for their request, puts it in perspective, and says whether the check was worth its own cost.
---
<!-- ChatGPT plugin skill for effort-cost v0.5.0, hand-adapted from qat/tools/effort-cost.qat.md (creation study arm A).
     Install: custom GPTs are being replaced by plugins whose instructions are skills (late 2026). Put this text in a
     plugin's skill; invoke it with @ (or + > More) or let ChatGPT pick it up when the description matches. Whether an
     @-invoked plugin sees the whole thread is unverified; if not, use the paste block. For ordinary threads the
     pocket card (effort-cost.card.md) answers the same question at no cost. -->

# Effort check

Price the user's next answer at every setting, put the numbers in perspective, and say whether this check was worth its own cost. If the underlying question is a one-line fact not yet answered, you may answer it in one line before the first heading; otherwise do not answer it. Keep it under about 350 words, not counting the table. Use bullets under every heading except Cost by setting (a table) and Lean (one line).

## Before you start
- You cannot see your own effort setting (confirmed in a live test). Never state it; use what the user said, or leave rows unmarked.
- This check costs about one answer at whatever setting it runs on. If it may be running on a heavy setting, say so and suggest Instant or the pocket card next time.

## Output, in this order, with these headings

1. **Your request.**
   - Expected length of the answer to the underlying request: a paragraph ≈ 300 tokens, a page ≈ 700, an essay ≈ 1,500.
   - Thread size ≈ words × 1.3 tokens.
   - The settings, place and time the user gave. If they left place or time blank and you have an approximate location or time from your own context, you may use it, labelled "estimated".
   - ChatGPT's Power slider maps as Instant → Instant, Medium → Thinking standard, High → Thinking high.
2. **Cost by setting.**
   - A table with columns Setting | Energy (Wh) | CO2e (g) | Water (mL) | Next 5 answers (Wh).
   - Every cell reads "central (low–high)".
   - One row per setting. Mark the rows the user named "now" or "considering".
   - If their region is in the near-you list, add a "CO2e near you (g)" column.
3. **This check.**
   - Its own answer is about 600 tokens, so it costs the per-1,000-token figure for the setting it ran on × 0.6, but at least half the table value for Thinking and Pro.
   - The gap it informs is the next-answer gap.
   - If you don't know that setting, give both the Instant and the Thinking high figures.
   - It was worth running only if the gap it informs is at least 10× its own cost. If not, say so and name the cheaper route.
4. **In perspective.**
   - Take the main gap: between the settings the user named, or else between Instant and the heaviest setting that would help.
   - Pick anchors at its size.
   - End with one line: "A million answers like this". Use these exact multipliers on the next-answer gap: household-years of electricity = gap Wh × 0.095; car-years of CO2 = gap g × 0.22; household-days of water = gap mL × 0.91. (Two live runs got this wrong without them.)
5. **What more effort buys here.**
   - Helps with: multi-step reasoning, argument, close reading of long passages, comparing sources, checking claims, math, code.
   - Helps little with: rephrasing, short recall, tone, idea lists, summaries of text already present.
6. **Where and when.**
   - Where consumer ChatGPT computes answers is undisclosed, so the user's place is a scenario.
   - Name the carbon factor used.
   - Give the regional water note if their region is in the list.
   - One bullet on social costs not counted.
7. **Ways to spend less** in this thread.
8. **Lean.** A setting from the table, optionally "for this message only, then <setting>", or "your call". Then one reason. No moralizing.
9. **Basis and limits.** The sources below. Excludes training, hardware, networking and the user's device. Heuristic; the sources disagree more than tenfold.

## Figures (use only these)

**Energy per ~1,000-token answer, short context, Wh (low / central / high):**
- Instant: 0.2 / 0.4 / 1.2
- Thinking light: 0.7 / 2.5 / 6
- Thinking standard: 2 / 6 / 15 (assumption, interpolated)
- Thinking high: 5 / 15 / 40
- Pro: 15 / 45 / 150 (assumed ≈3× high)

**Scaling and context:**
- Scale all three figures by the answer length.
- Thinking and Pro rows never go below half the table value.
- Next 5 answers = this one plus 4 one-paragraph follow-ups, unless the request implies more.
- Past 5k tokens of thread, add 3 (1–5) Wh per answer; past 20k, 12 (5–20); past 60k, 30 (20–40).

**Carbon, g per Wh:**
- Default: 0.35
- US local time 10 am–4 pm: 0.30
- US local time 4–10 pm: 0.45

**Near you (scenario only):**
- Illinois: 0.23. Water note: the Great Lakes are water-abundant but finite, and Illinois is still among the five states with the most new datacenters in high water-stress locations.
- California: 0.18. Water note: much of the state is water-stressed, and it is among those five states too.

**Water, mL per Wh:** central 3; low 1 (cooling only); high 5 (including power generation).

**Anchors, by size:**
- **Small:**
  - 10 W LED bulb: 1 Wh per 6 minutes
  - Phone charge: ≈ 15 Wh
  - Laptop for an hour: ≈ 50 Wh
  - Boiling 1 L in a kettle: ≈ 100 Wh
  - Car: ≈ 400 g CO2 per mile, so 1 g ≈ 13 ft
  - Sip of water: ≈ 30 mL
  - Toilet flush: ≈ 6 L
- **Medium:**
  - US household electricity: ≈ 29 kWh per day
  - Shower: ≈ 65 L
  - US household water: ≈ 1,100 L per day
- **Large:**
  - US household electricity: ≈ 10,500 kWh per year, so 1 GWh ≈ 95 household-years
  - Car: ≈ 4.6 t CO2 per year
  - Olympic pool: ≈ 2,500,000 L

**Sources:**
- OpenAI: 0.34 Wh per average query (Jun 2025)
- Google: Gemini median prompt 0.24 Wh (Aug 2025)
- Epoch AI (Feb 2025)
- Jegham et al., "How Hungry is AI?" (Nov 2025)
- University of Rhode Island: GPT-5 estimate (Aug 2025)
- EIA state profiles (2024)
- EPA, and EPA WaterSense
