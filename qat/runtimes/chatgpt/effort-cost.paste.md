<!-- ChatGPT paste block for effort-cost v0.3.0, hand-adapted from qat/tools/effort-cost.qat.md (creation study arm A).
     Before pasting: switch the composer to its lightest setting. The check costs about one answer at whatever
     setting it runs on (a live test at High took 51 s), so running it at High costs about what it measures.
     Fill in the first two lines, then paste everything below the line into any ChatGPT thread. -->
---
My setting now (read from the composer before I switched down for this check): ___
Considering: ___   ·   Where (optional): ___   ·   Local time (optional): ___

EFFORT CHECK (heuristic; do not answer my underlying question).

Estimate the environmental cost of answering this thread at a higher model or effort setting than the one I named, next to what the extra effort would buy for my request. Use only the figures below. Give ranges, two significant figures at most. Use these eight headings, in order, with bullets under each except Estimate (a table) and Lean (one line): Settings assumed, Estimate, In everyday terms, What the bump buys here, Where and when, Ways to spend less, Lean, Basis and limits. Under 350 words, not counting the table.

1. Settings assumed. Use the settings I filled in; you cannot see your own effort setting. If I left them blank, assume reasoning medium, label it "assumed", and ask me to read the composer. "Considering" defaults to one step up. Map names to rows: instant/non-thinking → fast; lightest thinking → minimal-low; standard thinking → medium; extended/high → high; heavy/Pro/parallel/deep research → Pro. Thread size ≈ words × 1.3 tokens. Expected length of the answer to my underlying request (paragraph ≈ 150–300 tokens; essay ≈ 1,000–2,000). Turns ahead: 5; follow-ups a paragraph each (≈300 tokens) unless my request implies more.
2. Estimate. Columns Energy (Wh) | CO2e (g) | Water (mL); cells "central (low–high)"; rows: next answer now · next answer at proposed · difference (central minus central; label approximate) · next N answers at proposed · and, only if my region is Illinois or California, "at proposed if served near you".
   Energy per ~1,000-token answer, short context (low / central / high Wh): fast 0.2 / 0.4 / 1.2 · reasoning minimal-low 0.7 / 2.5 / 6 · reasoning medium 2 / 6 / 15 · reasoning high 5 / 15 / 40 · Pro 15 / 45 / 150 (assumed ≈3× high). Scale by answer length; for reasoning settings never below half the table value (hidden reasoning tokens). Once the thread passes 5k tokens, add per answer 3 (1–5) Wh at 5–20k tokens, 12 (5–20) at 20–60k, 30 (20–40) over 60k.
   Carbon g per Wh: 0.35; if my local US time is 10 am–4 pm 0.30, 4–10 pm 0.45. If served near me (scenario): Illinois 0.23, California 0.18 (EIA 2024 state averages, in-state generation).
   Water mL per Wh: central 3, low 1 (on-site cooling only), high 5 (including power generation).
3. In everyday terms, for the difference: 10 W LED bulb = 1 Wh per 6 minutes; phone charge ≈ 15 Wh; boiling 1 L in a kettle ≈ 100 Wh; average US car ≈ 400 g CO2 per mile; a sip ≈ 30 mL. Pick 2–3 that fit.
4. What the bump buys here: higher effort helps multi-step reasoning, argument, close reading of long passages, comparing sources, checking claims, math, code; little for rephrasing, short recall, tone, idea lists, summaries of text already here. Say which my request is.
5. Where and when: where the answer is computed is not disclosed for consumer ChatGPT, so my location is a scenario, not a fact; say which carbon factor you used. If I'm in Illinois: the Great Lakes are water-abundant but finite, and Illinois is still among the five states with the most new datacenters in high water-stress spots. If California: much of it is water-stressed, and it is among those five too. One bullet on social costs not counted: water stress near datacenters, local grid strain, aggregate demand.
6. Ways to spend less in this thread (e.g. bump for one message then switch back, shorter answers, no regenerating, start fresh with a summary if the thread is long, run checks like this one on the lightest setting).
7. Lean: start with exactly one of: bump | bump for this message only | stay | your call; then one reason. No moralizing; I decide.
8. Basis and limits: OpenAI 0.34 Wh/query (Jun 2025); Google Gemini 0.24 Wh median (Aug 2025); Epoch AI (Feb 2025); Jegham et al. "How Hungry is AI?" (Nov 2025); Univ. of Rhode Island GPT-5 estimate (Aug 2025); EIA state profiles (2024). Excludes training, hardware, networking, my device. Heuristic; sources disagree more than tenfold.
