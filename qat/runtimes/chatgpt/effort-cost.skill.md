---
name: effort-check
description: Use when the user asks whether to turn up the model or reasoning effort for the current conversation, asks what a higher setting costs the environment (energy, carbon, water), or says "effort check". Gives a heuristic estimate next to what the extra effort would buy for their request.
---
<!-- ChatGPT plugin skill for effort-cost v0.3.0, hand-adapted from qat/tools/effort-cost.qat.md (creation study arm A).
     Install: as of late 2026 custom GPTs are being replaced by plugins whose instructions are skills. Put this text
     in a plugin's skill, then invoke it in any thread with @ (or from + > More), or let ChatGPT pick it up when the
     description matches. Whether the plugin sees the whole thread when @-mentioned is unverified; if it does not,
     use the paste block (effort-cost.paste.md) instead. -->

# Effort check

The user is deciding whether to answer this conversation at a higher model or reasoning-effort setting. Give a heuristic estimate of the environmental cost of doing so, next to what the extra effort would buy for their request. Do not answer their underlying question.

Keep it under about 350 words, not counting the table. Use bullets under every heading except Estimate (a table) and Lean (one line).

## Before you start

- You cannot see your own effort setting (confirmed in a live test: a thread running at High assumed Medium).
- Ask the user which setting they are on now and which they are considering, unless they already said.
- This check costs about one answer at whatever setting it runs on. Suggest they switch to the lightest setting for the check, then switch back.

## Output, in this order, with these headings

1. **Settings assumed.**
   - Use the settings the user gave. If none, assume reasoning medium and label it "assumed".
   - The proposed setting defaults to one step up.
   - Map names to rows:
     - instant or non-thinking → fast
     - lightest thinking → minimal–low
     - standard thinking → medium
     - extended or high → high
     - heavy, Pro, parallel or deep research → Pro
   - Thread size ≈ words × 1.3 tokens.
   - Expected length: the answer to the underlying request, not to this check.
   - Turns ahead: 5. Follow-ups are a paragraph each (≈300 tokens) unless the request implies more.
2. **Estimate.**
   - A table with columns Energy (Wh) | CO2e (g) | Water (mL). Each cell reads "central (low–high)", at most two significant figures.
   - Rows:
     - next answer now
     - next answer at proposed
     - difference (central minus central, labelled approximate)
     - next N answers at proposed
     - "at proposed if served near you", only when the user's region is in the table below
3. **In everyday terms.** Translate the difference with 2–3 anchors.
4. **What the bump buys here.**
   - Higher effort helps: multi-step reasoning, argument, close reading of long passages, comparing sources, checking claims, math, code.
   - It helps little with: rephrasing, short recall, tone, idea lists, summaries of text already present.
   - Say which this request is.
5. **Where and when.**
   - Where consumer ChatGPT computes an answer is undisclosed, so the user's location is a scenario, not a fact.
   - Say which carbon factor you used.
   - Include the regional water note if their region is in the table.
   - Add one bullet on social costs not counted: water stress near datacenters, local grid strain, aggregate demand.
6. **Ways to spend less** in this thread. Include running checks like this one on the lightest setting.
7. **Lean.** Start with exactly one of: bump | bump for this message only | stay | your call. Then give one reason. No moralizing; the user decides.
8. **Basis and limits.**
   - Sources and dates as below.
   - Excludes training, hardware, networking and the user's device.
   - Heuristic: the sources disagree more than tenfold.

## Figures (use only these)

**Energy per ~1,000-token answer, short context, Wh (low / central / high):**
- Fast, no reasoning: 0.2 / 0.4 / 1.2
- Reasoning, minimal–low effort: 0.7 / 2.5 / 6
- Reasoning, medium effort: 2 / 6 / 15 (assumption, interpolated)
- Reasoning, high effort: 5 / 15 / 40
- Pro, parallel or deep research: 15 / 45 / 150 (assumed ≈3× high)

**Scaling and context:**
- Scale by answer length.
- For reasoning settings, never go below half the table value, because the hidden reasoning tokens are spent anyway.
- Once the thread passes 5k tokens, add per answer:
  - 3 (1–5) Wh at 5–20k tokens
  - 12 (5–20) Wh at 20–60k tokens
  - 30 (20–40) Wh over 60k tokens

**Carbon, g per Wh:**
- Default: 0.35
- US local time 10 am–4 pm: 0.30
- US local time 4–10 pm: 0.45

**If served near you (scenario only):**
- Illinois: 0.23 g/Wh (EIA 2024, 510 lb/MWh). Water note: the Great Lakes are water-abundant but finite, and Illinois is still among the five states with the most new datacenters in high water-stress locations.
- California: 0.18 g/Wh (EIA 2024, 407 lb/MWh, in-state generation, excludes imports). Water note: much of the state is water-stressed, and it is among those five states too.
- Any other region: no row. Say the region is not in the table.

**Water, mL per Wh:** central 3; low 1 (on-site cooling only); high 5 (including power generation).

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
- EIA state electricity profiles, 2024 (Illinois, California)
- Chicago Tribune via UWM (Sep 2025) and Bloomberg via DCD, on datacenter water stress
