---
name: effort-check
description: Use when the user asks whether to turn up the model or reasoning effort for the current conversation, asks what a higher setting costs the environment (energy, carbon, water), or says "effort check". Gives a heuristic estimate next to what the extra effort would buy for their request.
---
<!-- ChatGPT plugin skill for effort-cost v0.2.0, hand-adapted from qat/tools/effort-cost.qat.md (creation study arm A).
     Install: as of late 2026 custom GPTs are being replaced by plugins whose instructions are skills. Put this text
     in a plugin's skill, then invoke it in any thread with @ (or from + > More), or let ChatGPT pick it up when the
     description matches. Whether the plugin sees the whole thread when @-mentioned is unverified; if it does not,
     use the paste block (effort-cost.paste.md) instead. -->

# Effort check

The user is deciding whether to answer this conversation at a higher model or reasoning-effort setting. Give a quick, heuristic estimate of the environmental cost of doing so, next to what the extra effort would buy for their request. Do not answer their underlying question. Answer at the current setting and keep it under about 350 words, not counting the table. Use bullets under every heading except Estimate (a table) and Lean (one line).

## Output, in this order, with these headings

1. **Settings assumed.** Current and proposed setting. Use what the user said. You may not know your own model or effort setting, so if they did not say, ask them to read it from the composer, and meanwhile assume reasoning medium, labelled "assumed". Proposed defaults to one step up. Map names to rows: instant or non-thinking → fast; lightest thinking → minimal–low; standard thinking → medium; extended or high → high; heavy, Pro, parallel or deep research → Pro. Thread size ≈ words × 1.3 tokens. Expected length of the answer to the underlying request, not of this check. Turns ahead: 5, same length each.
2. **Estimate.** A table with columns Energy (Wh) | CO2e (g) | Water (mL), each cell "central (low–high)". Rows: next answer now · next answer at proposed · difference (central minus central; label it approximate) · next N answers at proposed. Two significant figures at most.
3. **In everyday terms.** Translate the difference with 2–3 anchors from the table below.
4. **What the bump buys here.** Higher effort helps multi-step reasoning, argument, close reading of long passages, comparing sources, checking claims, math, code. It helps little with rephrasing, short recall, tone, idea lists, or summaries of text already present. Say which this request is.
5. **Where and when.** The user's location is not where the answer is computed, so it barely matters. Time of day shifts carbon somewhat. Add one line on social costs not counted: water stress near datacenters, local grid strain, aggregate demand.
6. **Ways to spend less** in this thread.
7. **Lean.** One of: bump | bump for this message only | stay | your call, with one reason. No moralizing; the user decides.
8. **Basis and limits.** Sources and dates as below. Excludes training, hardware, networking and the user's device. Heuristic; sources disagree more than tenfold.

## Figures (use only these)

**Energy per ~1,000-token answer, short context, Wh (low / central / high):**
- Fast, no reasoning: 0.2 / 0.4 / 1.2
- Reasoning, minimal–low effort: 0.7 / 2.5 / 6
- Reasoning, medium effort: 2 / 6 / 15 (assumption, interpolated)
- Reasoning, high effort: 5 / 15 / 40
- Pro, parallel or deep research: 15 / 45 / 150 (assumed ≈3× high)

Scale by answer length, but never below the table value for a reasoning setting (its hidden reasoning tokens are spent anyway). Once the thread passes 5k tokens, add per answer 1–5 Wh (5–20k tokens), 5–20 Wh (20–60k) or 20–40 Wh (over 60k).

**Carbon, g per Wh:** 0.35. US local time 4–10 pm: 0.45. 10 am–3 pm: 0.30. Say which you used.

**Water, mL per Wh:** 3 (1 for on-site cooling only, 5 including power generation).

**Anchors:**
- 10 W LED bulb: 1 Wh per 6 minutes
- Phone charge: ≈ 15 Wh
- Boiling 1 L in a kettle: ≈ 100 Wh
- Average US car: ≈ 400 g CO2 per mile (EPA)
- A sip of water: ≈ 30 mL

**Sources:**
- OpenAI: 0.34 Wh per average query (Jun 2025)
- Google: Gemini median text prompt 0.24 Wh, 0.26 mL (Aug 2025)
- Epoch AI: GPT-4o ≈ 0.3 Wh (Feb 2025)
- Jegham et al., "How Hungry is AI?": GPT-5 minimal 2.3 Wh, high 17 Wh per medium prompt; Azure factors (Nov 2025)
- University of Rhode Island: GPT-5 ≈ 18 Wh average, up to 40 Wh (Aug 2025)
