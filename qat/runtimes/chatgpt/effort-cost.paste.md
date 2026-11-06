<!-- ChatGPT paste block for effort-cost v0.1.0, hand-adapted from qat/tools/effort-cost.qat.md (creation study arm A).
     Paste everything below the line into any ChatGPT thread. Optionally add your settings at the end, e.g.
     "I'm on Thinking, standard effort; considering High. Chicago, 9:40 pm." -->
---
EFFORT CHECK (heuristic; do not answer my underlying question). Answer quickly at your current setting.

Estimate the environmental cost of answering this thread at a higher model or effort setting than now, next to what the extra effort would buy for my request. Use only the figures below; give ranges, two significant figures at most. Use these eight headings, in order: Settings assumed, Estimate, In everyday terms, What the bump buys here, Where and when, Ways to spend less, Lean, Basis and limits.

1. Settings assumed: current and proposed setting (use what I said; you may not know your own setting, so if I didn't say, ask me to read it from the composer, or assume the default and label it "assumed"; proposed defaults to one step up). Thread size ≈ words × 1.3 tokens. Expected answer length. Turns ahead (default 5).
2. Estimate: a table with columns Energy (Wh) | CO2e (g) | Water (mL), cells "central (low–high)", rows: next answer now · next answer at proposed · difference · next N answers at proposed.
   Energy per ~1,000-token answer, short context (low / central / high Wh): fast, no reasoning 0.2 / 0.4 / 1.2 · reasoning minimal-low 0.7 / 2.5 / 6 · reasoning medium 2 / 6 / 15 · reasoning high 5 / 15 / 40 · Pro, parallel or deep research 15 / 45 / 150 (assumed ≈3× high). Scale by answer length; for reasoning settings treat the value as a floor. Long thread reread without cache: add 1–5 Wh (5–20k tokens), 5–20 (20–60k), 20–40 (over 60k).
   Carbon g per Wh: 0.35; if my local time is a US evening peak (about 5–9 pm) 0.45; overnight or sunny midday 0.25.
   Water mL per Wh: 3 (1 on-site cooling only, 5 including power generation).
3. In everyday terms, for the difference: 10 W LED bulb = 1 Wh per 6 minutes; phone charge ≈ 15 Wh; boiling 1 L in a kettle ≈ 100 Wh; average US car ≈ 400 g CO2 per mile; a sip ≈ 30 mL. Pick 2–3 that fit.
4. What the bump buys here: higher effort helps multi-step reasoning, argument, close reading of long passages, comparing sources, checking claims, math, code. It helps little with rephrasing, short recall, tone, idea lists, summaries of text already here. Say which my request is.
5. Where and when: my location is not where the answer is computed, so it barely matters; time of day shifts carbon somewhat. One line on social costs not counted (water stress near datacenters, local grid strain, aggregate demand).
6. Ways to spend less in this thread (e.g. bump for one message then switch back, ask for shorter answers, avoid regenerating, start fresh with a summary if the thread is long).
7. Lean: bump | bump for this message only | stay | your call, with one reason. No moralizing; I decide.
8. Basis and limits: OpenAI 0.34 Wh/query (Jun 2025); Google Gemini 0.24 Wh median (Aug 2025); Epoch AI (Feb 2025); Jegham et al. "How Hungry is AI?" (Nov 2025); Univ. of Rhode Island GPT-5 estimate (Aug 2025). Excludes training, hardware, networking, my device. Heuristic; sources disagree more than tenfold.

Under 350 words.
