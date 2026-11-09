---
name: effort-cost
version: 0.6.0
description: From inside a conversation, give a heuristic menu of what the next answer would cost the environment (energy, CO2e, water) at each available model or reasoning-effort setting, put the numbers in everyday and at-scale perspective, say what extra effort would buy for this request, and say whether the check itself was worth its own cost.
inputs:
  thread: {type: text, required: true, doc: "the conversation so far (in ChatGPT, the thread the tool is invoked in)"}
  current: {type: text, required: false, doc: "the setting the user is on, if they read it from the composer; marks a row, never required"}
  considering: {type: text, required: false, doc: "a setting the user is weighing; marks a row"}
  where_when: {type: text, required: false, doc: "optional location and local time; time adjusts carbon, a known region adds a 'near you' column"}
outputs:
  request: {type: claims, heading: Your request, doc: "bullets: expected answer length (estimate); thread size in tokens (estimate); settings the user named, if any; place and time used"}
  menu: {type: scorecard, heading: Cost by setting, doc: "table: Setting | Energy (Wh) | CO2e (g) | Water (mL) | Next 5 answers (Wh); one row per setting in Table 1, absolute cost of the next answer, cells 'central (low-high)'; rows marked 'now' or 'considering' when named; plus a 'CO2e near you (g)' column when the region is in Table 2b"}
  check: {type: claims, heading: This check, doc: "bullets: what running this check cost at the setting it ran on; the gap it informs; whether it was worth running; the cheaper route next time"}
  perspective: {type: claims, heading: In perspective, doc: "2-4 bullets putting the main gap in familiar terms, scaled to its size, plus one 'a million answers like this' line in household, car and water terms"}
  value: {type: claims, heading: What more effort buys here, doc: "bullets: what higher effort tends to improve for this request, and what it does not"}
  where: {type: claims, heading: Where and when, doc: "bullets: compute location undisclosed; carbon factor used; the near-you scenario and its water note, if a known region was given; social costs not counted"}
  levers: {type: claims, heading: Ways to spend less, doc: "2-5 bullets, concrete for this thread"}
  lean: {type: verdict, heading: Lean, doc: "a setting name from the menu, optionally 'for this message only, then <setting>', or 'your call'; then one reason"}
  basis: {type: claims, heading: Basis and limits, doc: "bullets: sources with dates; what is excluded (training, hardware, networking, devices); that all figures are heuristic"}
modules: [request, menu, check-cost]
reflexes:
  absolute-not-relative: The menu prices every setting for this request, so it is useful whether or not the user's current setting is known. A named setting only marks a row.
  ranges-not-points: Every figure is a central value with a low-high range. Never more than two significant figures.
  compute-is-not-local: The user's home grid is not known to be where the answer is computed (consumer routing is undisclosed). A known region adds a labelled scenario column, never replaces the default figures; time of day adjusts the default carbon factor.
  dont-claim-own-settings: The model cannot see its own effort setting (confirmed in a live ChatGPT test). Never state it as fact; use what the user said or leave the rows unmarked.
  check-costs-less-than-it-informs: The check must cost far less than the gap it informs. State its own cost; if it ran on a heavy setting or the gap is small, say it was not worth running and point to the pocket card or the lightest setting.
  perspective-scales-with-size: Pick anchors at the size of the number (minutes of a bulb for Wh; household days for kWh; household-years for MWh and GWh; car miles for grams and car-years for tonnes; sips, showers, household-days and pools for water).
  scale-honestly: Neither dismiss ("negligible") nor alarm. The per-answer share is small; the aggregate is where the impact is, and the million-answers line shows it.
  cost-next-to-value: The menu always sits next to what more effort would buy for this request.
  answer-the-cost-question: Do not answer the thread's underlying question; a one-line factual question not yet answered may get its one-line answer before the first heading.
  dated-figures: Every coefficient comes from the tables below, with its source and date. Do not invent figures; say when the tables are stale.
  user-decides: The lean is a lean. No moralizing, no guilt.
handoffs: []
---

# EffortCost

A person in a thread wants to know what an answer costs the environment at the settings they could choose (an instant mode, a thinking mode at some effort, a Pro mode), and whether more effort is worth it for what they are asking. This tool prices every setting for this request, puts the numbers in perspective, and says whether running the check was itself worth it. It is a heuristic built from published per-query figures that disagree with each other by more than tenfold, and it says so.

**Runtimes look numbers up; they do not compute them.** The check is meant to run on the lightest setting, and live ChatGPT runs showed the lightest setting cannot do this arithmetic reliably (it misapplied the reasoning floors and mis-scaled the million-answers line by 1,000-1,000,000×). So `qat/runtimes/chatgpt/effort-cost.card.py` applies the rules below once and the runtime texts carry its lookup tables. Its coefficients are hard-coded, not read from this spec: when a coefficient changes, manually synchronize the script constants, run it, and manually propagate the output to the runtime texts (then regenerate the skill from the paste block).

**The cheapest route is not to run it.** For ordinary threads, the pocket card (`qat/runtimes/chatgpt/effort-cost.card.md`) gives the same menu precomputed, at no cost. Run this tool when the thread is long, the answer unusual, or the user wants the reasoning applied to their request.

## Procedure
1. **Request** (module). Expected answer length, thread size, named settings, place and time.
2. **Menu** (module). Price the next answer at every setting in Table 1; add the next-5-answers column; mark named rows; add the near-you column if the region is in Table 2b.
3. **Check cost** (module).
4. **Perspective.** Take the main gap (between the two named settings, or else between the lightest and the heaviest setting that would plausibly help) and translate it with Table 4 at the right scale. Add the million-answers line.
5. **Value.** Higher effort tends to help with multi-step reasoning: argument, close reading of a long passage, comparison across sources, checking claims, math, code. It helps little with rephrasing, short recall, tone, lists of ideas, or summaries of text already in the thread. Say which this request is.
6. **Where and when**, **levers**, **lean**, **basis**.

Write every section as bullets except Cost by setting (the table) and Lean (one line). Keep the output under about 350 words, not counting the table.

### module: request
- Expected answer length: of the answer to the user's underlying request, not of this check. A paragraph ≈ 300 tokens; a page ≈ 700; an essay ≈ 1,500 (1,000-2,000).
- Thread size: words × 1.3 tokens, counting the pasted check. Say it is an estimate.
- Next 5 answers: the next answer plus four follow-ups of a paragraph each, unless the request implies more. Add the context add-on (midpoint) to each answer once the thread passes 5k tokens.
- Place and time: what the user gave; if blank and the runtime supplies an approximate location or time, use it, labelled "estimated" (seen in a live ChatGPT run, even in a Temporary chat).
- Named settings: map product names to Table 1 rows. ChatGPT's Power slider (GPT-6, Nov 2026) has three positions: Instant → Instant, Medium → Thinking standard, High → Thinking high; other plans and models may add the light and Pro rows. An instant or non-thinking mode → Instant; the lightest thinking effort → Thinking light; standard or default thinking → Thinking standard; extended or high → Thinking high; heavy, Pro, parallel or deep research → Pro.

### module: menu
**Table 1. Energy per answer**, Wh, for an answer of about 1,000 tokens with a short context. Scale by answer length (low, central and high columns all scale by the central length). For thinking and Pro rows, hidden reasoning tokens are spent even for short answers, so never go below half the table value.

| Setting | Low | Central | High | Basis |
|---|---|---|---|---|
| Instant (no reasoning) | 0.2 | 0.4 | 1.2 | OpenAI average query 0.34 Wh (Jun 2025); Google Gemini median text prompt 0.24 Wh (Aug 2025); Epoch AI GPT-4o 0.3 Wh (Feb 2025); Jegham et al. GPT-4o medium prompt 1.2 Wh (Nov 2025) |
| Thinking light | 0.7 | 2.5 | 6 | Jegham et al.: GPT-5 minimal effort 2.3 Wh, o3-mini 2.4 Wh, o3 5.2 Wh, medium prompts (Nov 2025) |
| Thinking standard | 2 | 6 | 15 | Assumption: between the rows above and below |
| Thinking high | 5 | 15 | 40 | Jegham et al.: GPT-5 high effort 17 Wh medium, 34 Wh long (Nov 2025); Univ. of Rhode Island GPT-5 average ≈ 18 Wh, up to 40 Wh (Aug 2025) |
| Pro (parallel or deep research) | 15 | 45 | 150 | Assumption: about 3× Thinking high; no published figure. Epoch AI calls Deep Research "far more compute-intensive" |

**Context add-on**, per answer once the thread passes 5k tokens: 3 (1-5) Wh at 5-20k tokens; 12 (5-20) at 20-60k; 30 (20-40) over 60k. Based on Epoch AI's 10k-token ≈ 2.4 Wh and 100k-token ≈ 40 Wh estimates for GPT-4o (Feb 2025); follow-ups in an active thread are often cached and cost less, so treat these as upper-end.

**Table 2. Carbon**, g CO2e per Wh. Default 0.35, the Azure factor used by Jegham et al. (Nov 2025). If the user's local US time is 10 am-4 pm, 0.30 (midday solar); 4-10 pm, 0.45 (evening peak). The time bands are assumptions. Clean-energy-matched accounting can be far lower (Google reports 0.03 g for a 0.24 Wh prompt, Aug 2025).

**Table 2b. Near you** (a scenario column, not a fact: consumer routing is undisclosed; OpenAI offers inference residency by region only to Enterprise and Edu customers). EIA 2024 state averages, in-state generation, no time adjustment.

| Region | g CO2e per Wh | Water note |
|---|---|---|
| Illinois / Chicago area | 0.23 (510 lb/MWh) | Great Lakes water is abundant but finite (Chicago Tribune, Sep 2025); Illinois is still among the five states with the most new datacenters in high water-stress locations (Bloomberg via DCD) |
| California | 0.18 (407 lb/MWh; excludes imports) | much of the state is water-stressed; it is among those five states too |
| elsewhere | no column | say the region is not in the table |

**Table 3. Water**, mL per Wh: central 3; low 1 (on-site cooling only: OpenAI 0.32 mL per 0.34 Wh, Jun 2025; Google 0.26 mL per 0.24 Wh, Aug 2025); high 5 (including water used to generate the electricity, Jegham et al., Azure factors, Nov 2025).

**Ranges.** Low = energy low × the low factor; high = energy high × the high factor. Carbon uses one factor, so its range comes from energy only.

### module: check-cost
- This check's own answer is about 600 tokens. At the setting it ran on, it costs that setting's per-1,000-token energy × 0.6, but at least half the table value for thinking and Pro rows. The gap it informs is the next-answer gap between the settings being weighed. If the setting is unknown, give the Instant figure and the Thinking high figure.
- The pasted check also stays in the thread (about 1,200 tokens), slightly raising the cost of later answers once the thread is long.
- **Worth running** if the gap it informs is at least ten times its own cost. Otherwise say plainly that it was not worth running, and name the cheaper route: the pocket card, or running the check on Instant.

**Table 4. Perspective**, approximate; pick by size.

| Size | Energy | CO2e | Water |
|---|---|---|---|
| small | 10 W LED bulb: 1 Wh per 6 minutes · phone charge ≈ 15 Wh · laptop for an hour ≈ 50 Wh · boiling 1 L in a kettle ≈ 100 Wh | gasoline car ≈ 400 g per mile (EPA), so 1 g ≈ 13 feet | sip ≈ 30 mL · toilet flush ≈ 6 L |
| medium | US household ≈ 29 kWh per day | 1 kg ≈ 2.5 car miles | shower ≈ 65 L (EPA WaterSense) · US household ≈ 1,100 L per day (EPA WaterSense, about 300 gal) |
| large | US household ≈ 10,500 kWh per year (Epoch AI, citing the US average) · 1 GWh ≈ 95 household-years | typical car ≈ 4.6 t per year (EPA) | Olympic pool ≈ 2,500,000 L |

**A million answers like this**: use these exact multipliers on the next-answer gap, because two live runs mis-converted units without them: household-years of electricity = gap Wh × 0.095 (1 MWh ÷ 10,500 kWh); car-years of CO2 = gap g × 0.22 (1 t ÷ 4.6 t); household-days of water = gap mL × 0.91 (1,000 L ÷ 1,100 L). ChatGPT handles on the order of a billion messages a day, so a million is a small slice.

The tables are dated November 2026 from sources published 2025 (EIA 2024 data). Efficiency changes fast (Google reported a 33× energy drop per prompt in 12 months), so figures more than a year old are likely high.
