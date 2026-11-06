---
name: effort-cost
version: 0.2.0
description: From inside a conversation, give a heuristic estimate of the environmental cost (energy, CO2e, water) of answering it at a higher model or reasoning-effort setting versus the current one, in everyday terms, next to what the extra effort would plausibly buy for this particular request.
inputs:
  thread: {type: text, required: true, doc: "the conversation so far (in ChatGPT, the thread the tool is invoked in)"}
  proposed: {type: text, required: false, doc: "the setting being considered, e.g. 'Thinking, high effort' or 'Pro'; default: one step above current"}
  current: {type: text, required: false, doc: "the current model and effort, if the user knows them"}
  where_when: {type: text, required: false, doc: "location and local time, if known; used only for the grid-carbon adjustment"}
outputs:
  settings: {type: claims, heading: Settings assumed, doc: "bullets: current and proposed setting (stated or assumed, say which); thread size in tokens (estimate); answer length expected; turns ahead assumed"}
  estimate: {type: scorecard, heading: Estimate, doc: "table: Scenario | Energy (Wh) | CO2e (g) | Water (mL); each cell 'central (low-high)'; rows: next answer now, next answer at proposed, difference, next N answers at proposed"}
  anchors: {type: claims, heading: In everyday terms, doc: "2-4 bullets translating the difference into familiar quantities"}
  value: {type: claims, heading: What the bump buys here, doc: "bullets: what higher effort tends to improve for this request, and what it does not"}
  where: {type: claims, heading: Where and when, doc: "bullets: why the user's location matters little; how time of day shifts the carbon figure; social costs not counted"}
  levers: {type: claims, heading: Ways to spend less, doc: "2-5 bullets, concrete for this thread"}
  lean: {type: verdict, heading: Lean, doc: "one of: bump | bump for this message only | stay | your call; one reason; the decision stays with the user"}
  basis: {type: claims, heading: Basis and limits, doc: "bullets: sources with dates; what is excluded (training, hardware, networking, devices); that all figures are heuristic"}
modules: [settings, estimate]
reflexes:
  ranges-not-points: Every figure is a central value with a low-high range. Never more than two significant figures.
  compute-is-not-local: The user's home grid is not where the answer is computed. Location informs the carbon figure only weakly (which country's datacenters are likely); time of day informs it somewhat (US datacenters share the evening peak).
  dont-claim-own-settings: The model may not know its own model name or effort setting. Use what the user said; otherwise ask one question or state an assumption and label it.
  scale-honestly: Neither dismiss ("negligible") nor alarm. Give the anchors and let them carry the scale; say that the per-answer share is small and the aggregate is where the impact is.
  cost-next-to-value: The estimate always sits next to what the bump would buy for this request. A cost with no benefit side is half an answer.
  answer-the-cost-question: Do not answer the thread's underlying question (the essay, the analysis) while doing this check.
  dated-figures: Every coefficient comes from the table below, with its source and date. Do not invent new figures; say when the table is stale.
  user-decides: The lean is a lean. No moralizing, no guilt, no instruction to the user.
  cheap-check: This check should itself be quick. Do not reason at length; the tables do the work.
handoffs: []
---

# EffortCost

A person in a thread is deciding whether to turn the effort up (a reasoning mode, higher effort, a bigger model). They want to know roughly what that costs the environment, and whether it is worth it for what they are asking. This tool gives a heuristic answer in under a minute of reading. It is an estimate built from published per-query figures that disagree with each other by more than tenfold, and it says so.

## Procedure
1. **Settings** (module). Establish current and proposed settings, the thread's size, the expected answer length, and how many more turns are likely (default 5).
2. **Estimate** (module). Energy per answer from Table 1, adjusted for length and context; carbon from Table 2; water from Table 3. Fill the four rows. Round to two significant figures.
3. **Anchors.** Translate the *difference* row with Table 4: pick the two or three that land closest to the number.
4. **Value.** Read the request. Higher effort tends to help with multi-step reasoning: argument, close reading of a long passage, comparison across sources, checking claims, math, code. It helps little with rephrasing, short recall, tone, lists of ideas, or summaries of text already in the thread. Say which this request is, specifically.
5. **Where and when.** Apply the compute-is-not-local reflex. Name the time adjustment you used. One bullet on social costs not counted (water stress near datacenters, local grid strain and prices, aggregate demand).
6. **Levers**, specific to this thread.
7. **Lean**, then **Basis and limits**.

Write every section as bullets except Estimate (the table) and Lean (one line). Keep the output under about 350 words, not counting the table.

### module: settings
- Use the user's statement of current and proposed settings. In ChatGPT the effort level is shown in the composer; ask the user to read it if they have not said. If they cannot, assume reasoning medium (a thinking mode at its standard effort) and label it "assumed".
- Map product names to Table 1 rows: an instant or non-thinking mode → fast; the lightest thinking effort → minimal or low; standard or default thinking → medium; extended or high → high; heavy, Pro, parallel or deep research → Pro. Say which row you used.
- Thread size: estimate tokens as words × 1.3. Say it is an estimate.
- Expected answer length: of the answer to the user's underlying request, not of this check (a paragraph ≈ 150 tokens; an essay-length answer ≈ 1,000-2,000 tokens).
- Next N answers: assume the same length each; add the context add-on once the thread will pass 5k tokens.

### module: estimate
**Table 1. Energy per answer**, for an answer of about 1,000 tokens with a short context. Scale in proportion to expected answer length, except that a reasoning setting never goes below its table value: its hidden reasoning tokens are spent even when the visible answer is short.

| Setting | Low | Central | High | Basis |
|---|---|---|---|---|
| Fast, no reasoning | 0.2 | 0.4 | 1.2 | OpenAI average query 0.34 Wh (Jun 2025); Google Gemini median text prompt 0.24 Wh (Aug 2025); Epoch AI GPT-4o 0.3 Wh (Feb 2025); Jegham et al. GPT-4o medium prompt 1.2 Wh (Nov 2025) |
| Reasoning, minimal or low effort | 0.7 | 2.5 | 6 | Jegham et al.: GPT-5 minimal effort 2.3 Wh, o3-mini 2.4 Wh, o3 5.2 Wh, medium prompts (Nov 2025) |
| Reasoning, medium effort | 2 | 6 | 15 | Assumption: between the rows above and below |
| Reasoning, high effort | 5 | 15 | 40 | Jegham et al.: GPT-5 high effort 17 Wh medium, 34 Wh long (Nov 2025); Univ. of Rhode Island GPT-5 average ≈ 18 Wh, up to 40 Wh (Aug 2025) |
| Pro, parallel or deep-research modes | 15 | 45 | 150 | Assumption: about 3× high effort; no published figure. Epoch AI calls Deep Research "far more compute-intensive" |

**Context add-on**, when the model rereads a long thread without a cache (follow-ups in an active thread are often cached and cost less): under 5k tokens +0; 5-20k +1-5 Wh; 20-60k +5-20 Wh; over 60k +20-40 Wh. Based on Epoch AI's 10k-token ≈ 2.4 Wh and 100k-token ≈ 40 Wh estimates for GPT-4o (Feb 2025). Treat as an upper-end adjustment.

**Table 2. Carbon**, kg CO2e per kWh (= g per Wh). Central 0.35, the Azure factor used by Jegham et al. (Nov 2025). Adjust for the user's local time if in the US: 4-10 pm (evening peak) 0.45; 10 am-3 pm (midday solar) 0.30; otherwise 0.35. Clean-energy-matched accounting can be far lower (Google reports 0.03 g for a 0.24 Wh prompt, Aug 2025). The time adjustments are assumptions.

**Table 3. Water**, mL per Wh. On-site cooling only ≈ 1 (OpenAI 0.32 mL per 0.34 Wh, Jun 2025; Google 0.26 mL per 0.24 Wh, Aug 2025). Including water used to generate the electricity ≈ 5 (Jegham et al., Azure factors, Nov 2025). Report central 3 (1-5).

**Ranges.** Low = energy low × the low factor; high = energy high × the high factor (carbon uses one factor, so its range comes from energy only). For the difference row, central = proposed central − current central; low and high likewise, rounded, and labelled approximate.

**Table 4. Anchors** (approximate): a 10 W LED bulb uses 1 Wh in 6 minutes · a phone charge ≈ 15 Wh · boiling 1 L in an electric kettle ≈ 100 Wh · an average US gasoline car ≈ 400 g CO2 per mile (EPA) · a sip of water ≈ 30 mL · a toilet flush ≈ 6 L.

The tables are dated November 2026 from sources published 2025. Hardware and software efficiency change fast (Google reported a 33× energy drop per prompt in 12 months), so figures more than a year old are likely high.
