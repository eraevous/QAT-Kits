<!-- ChatGPT paste block for effort-cost v0.6.0, hand-adapted from qat/tools/effort-cost.qat.md (creation study arm A).
     Cheapest first: for an ordinary thread, read the pocket card (effort-cost.card.md) instead; it costs nothing.
     If you run this check, switch ChatGPT's Power slider to Instant first (the check costs about one answer at
     whatever setting it runs on), then switch back.
     v0.6: every number below is precomputed by effort-cost.card.py. Live runs showed Instant cannot do the
     arithmetic reliably, so the model only looks values up.
     Fill in whatever you know on the first two lines (all optional), then paste everything below the line. -->
---
My setting (from the composer, before switching down for this check): ___   ·   Considering: ___
Where: ___   ·   Local time: ___

EFFORT CHECK (heuristic). Look numbers up in the tables below; do not recompute them. If my underlying question is a one-line fact not yet answered, you may answer it in one line before the first heading; otherwise don't answer it.

Use these nine headings, in order, with bullets under each except Cost by setting (a table) and Lean (one line): Your request · Cost by setting · This check · In perspective · What more effort buys here · Where and when · Ways to spend less · Lean · Basis and limits. Under 350 words, not counting the table.

1. Your request: pick the length column for the answer to my underlying request (Short ~100 tokens, Paragraph ~300, Page ~700, Essay ~1,500); the settings, place and time I gave. If I left place or time blank and you have an approximate location or time from your own context, you may use it, labelled "estimated". You cannot see your own setting; never state it. ChatGPT's Power slider: Instant → Instant row, Medium → Thinking standard, High → Thinking high.
2. Cost by setting: estimate thread size as words × 1.3 tokens, including this check and every lookup table. Below 5k tokens, use Tables A and B. At 5k tokens or more, choose the matching context tier in Tables A-context and B-context. Copy the five rows for my length column with columns Setting | Energy (Wh) | CO2e (g) | Water (mL) | Next 5 answers (Wh). Mark my named rows "now" / "considering". For CO2e and water, copy the full central (low–high) cells from Table D at the same context tier, setting and answer length; never multiply a rounded energy cell or drop its range. Use the Default CO2e column (0.35), or US midday (0.30) at local US time 10 am–4 pm, or US evening (0.45) at 4–10 pm. Copy the Water column unchanged: its range includes 1–5 mL/Wh uncertainty. For Next 5, use Table B below 5k tokens and the matching tier in Table B-context otherwise. If my region is Illinois or California, add a labelled "CO2e near you (g)" scenario column by copying that region’s Table D cell, including its range; it never replaces the main CO2e column.

TABLE A. Energy per answer (Wh): central (low–high)
| Setting | Short (~100 tokens) | Paragraph (~300) | Page (~700) | Essay (~1,500) |
| Instant | 0.040 (0.020–0.12) | 0.12 (0.060–0.36) | 0.28 (0.14–0.84) | 0.60 (0.30–1.8) |
| Thinking light | 1.2 (0.35–3.0) | 1.2 (0.35–3.0) | 1.8 (0.49–4.2) | 3.8 (1.0–9.0) |
| Thinking standard (Medium) | 3.0 (1.0–7.5) | 3.0 (1.0–7.5) | 4.2 (1.4–10) | 9.0 (3.0–22) |
| Thinking high (High) | 7.5 (2.5–20) | 7.5 (2.5–20) | 10 (3.5–28) | 22 (7.5–60) |
| Pro | 22 (7.5–75) | 22 (7.5–75) | 31 (10–100) | 68 (22–220) |

TABLE B. Next 5 answers (Wh, central): this answer + 4 one-paragraph follow-ups
| Setting | Short | Paragraph | Page | Essay |
| Instant | 0.52 | 0.60 | 0.76 | 1.1 |
| Thinking light | 6.2 | 6.2 | 6.8 | 8.8 |
| Thinking standard (Medium) | 15 | 15 | 16 | 21 |
| Thinking high (High) | 38 | 38 | 40 | 52 |
| Pro | 110 | 110 | 120 | 160 |

TABLE A-context. Energy per answer (Wh): central (low–high), by context tier
| Setting | Answer length | 5k–20k tokens | 20k–60k tokens | >60k tokens |
|---|---|---:|---:|---:|
| Instant | Short (~100 tokens) | 3.0 (1.0–5.1) | 12 (5.0–20) | 30 (20–40) |
| Instant | Paragraph (~300) | 3.1 (1.1–5.4) | 12 (5.1–20) | 30 (20–40) |
| Instant | Page (~700) | 3.3 (1.1–5.8) | 12 (5.1–21) | 30 (20–41) |
| Instant | Essay (~1,500) | 3.6 (1.3–6.8) | 13 (5.3–22) | 31 (20–42) |
| Thinking light | Short (~100 tokens) | 4.2 (1.4–8.0) | 13 (5.3–23) | 31 (20–43) |
| Thinking light | Paragraph (~300) | 4.2 (1.4–8.0) | 13 (5.3–23) | 31 (20–43) |
| Thinking light | Page (~700) | 4.8 (1.5–9.2) | 14 (5.5–24) | 32 (20–44) |
| Thinking light | Essay (~1,500) | 6.8 (2.0–14) | 16 (6.0–29) | 34 (21–49) |
| Thinking standard (Medium) | Short (~100 tokens) | 6.0 (2.0–12) | 15 (6.0–28) | 33 (21–48) |
| Thinking standard (Medium) | Paragraph (~300) | 6.0 (2.0–12) | 15 (6.0–28) | 33 (21–48) |
| Thinking standard (Medium) | Page (~700) | 7.2 (2.4–16) | 16 (6.4–30) | 34 (21–50) |
| Thinking standard (Medium) | Essay (~1,500) | 12 (4.0–28) | 21 (8.0–42) | 39 (23–62) |
| Thinking high (High) | Short (~100 tokens) | 10 (3.5–25) | 20 (7.5–40) | 38 (22–60) |
| Thinking high (High) | Paragraph (~300) | 10 (3.5–25) | 20 (7.5–40) | 38 (22–60) |
| Thinking high (High) | Page (~700) | 14 (4.5–33) | 22 (8.5–48) | 40 (24–68) |
| Thinking high (High) | Essay (~1,500) | 26 (8.5–65) | 34 (12–80) | 52 (28–100) |
| Pro | Short (~100 tokens) | 26 (8.5–80) | 34 (12–95) | 52 (28–120) |
| Pro | Paragraph (~300) | 26 (8.5–80) | 34 (12–95) | 52 (28–120) |
| Pro | Page (~700) | 34 (12–110) | 44 (16–120) | 62 (30–140) |
| Pro | Essay (~1,500) | 70 (24–230) | 80 (28–240) | 98 (42–260) |

TABLE B-context. Next 5 answers (Wh, central), by context tier
| Setting | Answer length | 5k–20k tokens | 20k–60k tokens | >60k tokens |
|---|---|---:|---:|---:|
| Instant | Short (~100 tokens) | 16 | 61 | 150 |
| Instant | Paragraph (~300) | 16 | 61 | 150 |
| Instant | Page (~700) | 16 | 61 | 150 |
| Instant | Essay (~1,500) | 16 | 61 | 150 |
| Thinking light | Short (~100 tokens) | 21 | 66 | 160 |
| Thinking light | Paragraph (~300) | 21 | 66 | 160 |
| Thinking light | Page (~700) | 22 | 67 | 160 |
| Thinking light | Essay (~1,500) | 24 | 69 | 160 |
| Thinking standard (Medium) | Short (~100 tokens) | 30 | 75 | 160 |
| Thinking standard (Medium) | Paragraph (~300) | 30 | 75 | 160 |
| Thinking standard (Medium) | Page (~700) | 31 | 76 | 170 |
| Thinking standard (Medium) | Essay (~1,500) | 36 | 81 | 170 |
| Thinking high (High) | Short (~100 tokens) | 52 | 98 | 190 |
| Thinking high (High) | Paragraph (~300) | 52 | 98 | 190 |
| Thinking high (High) | Page (~700) | 56 | 100 | 190 |
| Thinking high (High) | Essay (~1,500) | 68 | 110 | 200 |
| Pro | Short (~100 tokens) | 130 | 170 | 260 |
| Pro | Paragraph (~300) | 130 | 170 | 260 |
| Pro | Page (~700) | 140 | 180 | 270 |
| Pro | Essay (~1,500) | 170 | 220 | 310 |

<!-- BEGIN GENERATED CARBON/WATER LOOKUPS -->
TABLE D. CO2e (g) and water (mL): central (low–high), including context.
Copy the full cell, including its range. Illinois and California are near-you scenarios only.

Context: Below 5k tokens
| Setting | Length | Default CO2e (0.35) | US midday CO2e (0.30) | US evening CO2e (0.45) | Illinois CO2e (0.23) | California CO2e (0.18) | Water |
|---|---|---|---|---|---|---|---|
| Instant | Short reply | 0.014 (0.0070–0.042) | 0.012 (0.0060–0.036) | 0.018 (0.0090–0.054) | 0.0092 (0.0046–0.028) | 0.0072 (0.0036–0.022) | 0.12 (0.020–0.60) |
| Instant | Paragraph | 0.042 (0.021–0.13) | 0.036 (0.018–0.11) | 0.054 (0.027–0.16) | 0.028 (0.014–0.083) | 0.022 (0.011–0.065) | 0.36 (0.060–1.8) |
| Instant | Page | 0.098 (0.049–0.29) | 0.084 (0.042–0.25) | 0.13 (0.063–0.38) | 0.064 (0.032–0.19) | 0.050 (0.025–0.15) | 0.84 (0.14–4.2) |
| Instant | Essay | 0.21 (0.10–0.63) | 0.18 (0.090–0.54) | 0.27 (0.14–0.81) | 0.14 (0.069–0.41) | 0.11 (0.054–0.32) | 1.8 (0.30–9.0) |
| Thinking light | Short reply | 0.44 (0.12–1.0) | 0.38 (0.10–0.90) | 0.56 (0.16–1.4) | 0.29 (0.080–0.69) | 0.22 (0.063–0.54) | 3.8 (0.35–15) |
| Thinking light | Paragraph | 0.44 (0.12–1.0) | 0.38 (0.10–0.90) | 0.56 (0.16–1.4) | 0.29 (0.080–0.69) | 0.22 (0.063–0.54) | 3.8 (0.35–15) |
| Thinking light | Page | 0.61 (0.17–1.5) | 0.52 (0.15–1.3) | 0.79 (0.22–1.9) | 0.40 (0.11–0.97) | 0.32 (0.088–0.76) | 5.2 (0.49–21) |
| Thinking light | Essay | 1.3 (0.37–3.2) | 1.1 (0.32–2.7) | 1.7 (0.47–4.0) | 0.86 (0.24–2.1) | 0.68 (0.19–1.6) | 11 (1.0–45) |
| Thinking standard | Short reply | 1.0 (0.35–2.6) | 0.90 (0.30–2.2) | 1.4 (0.45–3.4) | 0.69 (0.23–1.7) | 0.54 (0.18–1.4) | 9.0 (1.0–38) |
| Thinking standard | Paragraph | 1.0 (0.35–2.6) | 0.90 (0.30–2.2) | 1.4 (0.45–3.4) | 0.69 (0.23–1.7) | 0.54 (0.18–1.4) | 9.0 (1.0–38) |
| Thinking standard | Page | 1.5 (0.49–3.7) | 1.3 (0.42–3.2) | 1.9 (0.63–4.7) | 0.97 (0.32–2.4) | 0.76 (0.25–1.9) | 13 (1.4–52) |
| Thinking standard | Essay | 3.2 (1.0–7.9) | 2.7 (0.90–6.8) | 4.0 (1.4–10) | 2.1 (0.69–5.2) | 1.6 (0.54–4.0) | 27 (3.0–110) |
| Thinking high | Short reply | 2.6 (0.88–7.0) | 2.2 (0.75–6.0) | 3.4 (1.1–9.0) | 1.7 (0.58–4.6) | 1.4 (0.45–3.6) | 22 (2.5–100) |
| Thinking high | Paragraph | 2.6 (0.88–7.0) | 2.2 (0.75–6.0) | 3.4 (1.1–9.0) | 1.7 (0.58–4.6) | 1.4 (0.45–3.6) | 22 (2.5–100) |
| Thinking high | Page | 3.7 (1.2–9.8) | 3.2 (1.0–8.4) | 4.7 (1.6–13) | 2.4 (0.80–6.4) | 1.9 (0.63–5.0) | 32 (3.5–140) |
| Thinking high | Essay | 7.9 (2.6–21) | 6.8 (2.2–18) | 10 (3.4–27) | 5.2 (1.7–14) | 4.0 (1.4–11) | 68 (7.5–300) |
| Pro | Short reply | 7.9 (2.6–26) | 6.8 (2.2–22) | 10 (3.4–34) | 5.2 (1.7–17) | 4.0 (1.4–14) | 68 (7.5–380) |
| Pro | Paragraph | 7.9 (2.6–26) | 6.8 (2.2–22) | 10 (3.4–34) | 5.2 (1.7–17) | 4.0 (1.4–14) | 68 (7.5–380) |
| Pro | Page | 11 (3.7–37) | 9.4 (3.2–32) | 14 (4.7–47) | 7.2 (2.4–24) | 5.7 (1.9–19) | 94 (10–520) |
| Pro | Essay | 24 (7.9–79) | 20 (6.8–68) | 30 (10–100) | 16 (5.2–52) | 12 (4.0–40) | 200 (22–1,100) |

Context: 5k–20k tokens
| Setting | Length | Default CO2e (0.35) | US midday CO2e (0.30) | US evening CO2e (0.45) | Illinois CO2e (0.23) | California CO2e (0.18) | Water |
|---|---|---|---|---|---|---|---|
| Instant | Short reply | 1.1 (0.36–1.8) | 0.91 (0.31–1.5) | 1.4 (0.46–2.3) | 0.70 (0.23–1.2) | 0.55 (0.18–0.92) | 9.1 (1.0–26) |
| Instant | Paragraph | 1.1 (0.37–1.9) | 0.94 (0.32–1.6) | 1.4 (0.48–2.4) | 0.72 (0.24–1.2) | 0.56 (0.19–0.96) | 9.4 (1.1–27) |
| Instant | Page | 1.1 (0.40–2.0) | 0.98 (0.34–1.8) | 1.5 (0.51–2.6) | 0.75 (0.26–1.3) | 0.59 (0.21–1.1) | 9.8 (1.1–29) |
| Instant | Essay | 1.3 (0.46–2.4) | 1.1 (0.39–2.0) | 1.6 (0.58–3.1) | 0.83 (0.30–1.6) | 0.65 (0.23–1.2) | 11 (1.3–34) |
| Thinking light | Short reply | 1.5 (0.47–2.8) | 1.3 (0.40–2.4) | 1.9 (0.61–3.6) | 0.98 (0.31–1.8) | 0.76 (0.24–1.4) | 13 (1.4–40) |
| Thinking light | Paragraph | 1.5 (0.47–2.8) | 1.3 (0.40–2.4) | 1.9 (0.61–3.6) | 0.98 (0.31–1.8) | 0.76 (0.24–1.4) | 13 (1.4–40) |
| Thinking light | Page | 1.7 (0.52–3.2) | 1.4 (0.45–2.8) | 2.1 (0.67–4.1) | 1.1 (0.34–2.1) | 0.86 (0.27–1.7) | 14 (1.5–46) |
| Thinking light | Essay | 2.4 (0.72–4.9) | 2.0 (0.62–4.2) | 3.0 (0.92–6.3) | 1.6 (0.47–3.2) | 1.2 (0.37–2.5) | 20 (2.0–70) |
| Thinking standard | Short reply | 2.1 (0.70–4.4) | 1.8 (0.60–3.8) | 2.7 (0.90–5.6) | 1.4 (0.46–2.9) | 1.1 (0.36–2.2) | 18 (2.0–62) |
| Thinking standard | Paragraph | 2.1 (0.70–4.4) | 1.8 (0.60–3.8) | 2.7 (0.90–5.6) | 1.4 (0.46–2.9) | 1.1 (0.36–2.2) | 18 (2.0–62) |
| Thinking standard | Page | 2.5 (0.84–5.4) | 2.2 (0.72–4.6) | 3.2 (1.1–7.0) | 1.7 (0.55–3.6) | 1.3 (0.43–2.8) | 22 (2.4–78) |
| Thinking standard | Essay | 4.2 (1.4–9.6) | 3.6 (1.2–8.2) | 5.4 (1.8–12) | 2.8 (0.92–6.3) | 2.2 (0.72–5.0) | 36 (4.0–140) |
| Thinking high | Short reply | 3.7 (1.2–8.8) | 3.2 (1.0–7.5) | 4.7 (1.6–11) | 2.4 (0.80–5.8) | 1.9 (0.63–4.5) | 32 (3.5–120) |
| Thinking high | Paragraph | 3.7 (1.2–8.8) | 3.2 (1.0–7.5) | 4.7 (1.6–11) | 2.4 (0.80–5.8) | 1.9 (0.63–4.5) | 32 (3.5–120) |
| Thinking high | Page | 4.7 (1.6–12) | 4.0 (1.4–9.9) | 6.1 (2.0–15) | 3.1 (1.0–7.6) | 2.4 (0.81–5.9) | 40 (4.5–160) |
| Thinking high | Essay | 8.9 (3.0–23) | 7.6 (2.6–20) | 11 (3.8–29) | 5.9 (2.0–15) | 4.6 (1.5–12) | 76 (8.5–320) |
| Pro | Short reply | 8.9 (3.0–28) | 7.6 (2.6–24) | 11 (3.8–36) | 5.9 (2.0–18) | 4.6 (1.5–14) | 76 (8.5–400) |
| Pro | Paragraph | 8.9 (3.0–28) | 7.6 (2.6–24) | 11 (3.8–36) | 5.9 (2.0–18) | 4.6 (1.5–14) | 76 (8.5–400) |
| Pro | Page | 12 (4.0–38) | 10 (3.4–33) | 16 (5.2–50) | 7.9 (2.6–25) | 6.2 (2.1–20) | 100 (12–550) |
| Pro | Essay | 25 (8.2–80) | 21 (7.0–69) | 32 (11–100) | 16 (5.4–53) | 13 (4.2–41) | 210 (24–1,200) |

Context: 20k–60k tokens
| Setting | Length | Default CO2e (0.35) | US midday CO2e (0.30) | US evening CO2e (0.45) | Illinois CO2e (0.23) | California CO2e (0.18) | Water |
|---|---|---|---|---|---|---|---|
| Instant | Short reply | 4.2 (1.8–7.0) | 3.6 (1.5–6.0) | 5.4 (2.3–9.1) | 2.8 (1.2–4.6) | 2.2 (0.90–3.6) | 36 (5.0–100) |
| Instant | Paragraph | 4.2 (1.8–7.1) | 3.6 (1.5–6.1) | 5.5 (2.3–9.2) | 2.8 (1.2–4.7) | 2.2 (0.91–3.7) | 36 (5.1–100) |
| Instant | Page | 4.3 (1.8–7.3) | 3.7 (1.5–6.3) | 5.5 (2.3–9.4) | 2.8 (1.2–4.8) | 2.2 (0.93–3.8) | 37 (5.1–100) |
| Instant | Essay | 4.4 (1.9–7.6) | 3.8 (1.6–6.5) | 5.7 (2.4–9.8) | 2.9 (1.2–5.0) | 2.3 (0.95–3.9) | 38 (5.3–110) |
| Thinking light | Short reply | 4.6 (1.9–8.0) | 4.0 (1.6–6.9) | 6.0 (2.4–10) | 3.0 (1.2–5.3) | 2.4 (0.96–4.1) | 40 (5.4–120) |
| Thinking light | Paragraph | 4.6 (1.9–8.0) | 4.0 (1.6–6.9) | 6.0 (2.4–10) | 3.0 (1.2–5.3) | 2.4 (0.96–4.1) | 40 (5.4–120) |
| Thinking light | Page | 4.8 (1.9–8.5) | 4.1 (1.6–7.3) | 6.2 (2.5–11) | 3.2 (1.3–5.6) | 2.5 (0.99–4.4) | 41 (5.5–120) |
| Thinking light | Essay | 5.5 (2.1–10) | 4.7 (1.8–8.7) | 7.1 (2.7–13) | 3.6 (1.4–6.7) | 2.8 (1.1–5.2) | 47 (6.0–140) |
| Thinking standard | Short reply | 5.2 (2.1–9.6) | 4.5 (1.8–8.2) | 6.8 (2.7–12) | 3.4 (1.4–6.3) | 2.7 (1.1–5.0) | 45 (6.0–140) |
| Thinking standard | Paragraph | 5.2 (2.1–9.6) | 4.5 (1.8–8.2) | 6.8 (2.7–12) | 3.4 (1.4–6.3) | 2.7 (1.1–5.0) | 45 (6.0–140) |
| Thinking standard | Page | 5.7 (2.2–11) | 4.9 (1.9–9.2) | 7.3 (2.9–14) | 3.7 (1.5–7.0) | 2.9 (1.2–5.5) | 49 (6.4–150) |
| Thinking standard | Essay | 7.4 (2.8–15) | 6.3 (2.4–13) | 9.4 (3.6–19) | 4.8 (1.8–9.8) | 3.8 (1.4–7.6) | 63 (8.0–210) |
| Thinking high | Short reply | 6.8 (2.6–14) | 5.8 (2.2–12) | 8.8 (3.4–18) | 4.5 (1.7–9.2) | 3.5 (1.4–7.2) | 58 (7.5–200) |
| Thinking high | Paragraph | 6.8 (2.6–14) | 5.8 (2.2–12) | 8.8 (3.4–18) | 4.5 (1.7–9.2) | 3.5 (1.4–7.2) | 58 (7.5–200) |
| Thinking high | Page | 7.9 (3.0–17) | 6.8 (2.6–14) | 10 (3.8–22) | 5.2 (2.0–11) | 4.0 (1.5–8.6) | 68 (8.5–240) |
| Thinking high | Essay | 12 (4.4–28) | 10 (3.8–24) | 16 (5.6–36) | 7.9 (2.9–18) | 6.2 (2.2–14) | 100 (12–400) |
| Pro | Short reply | 12 (4.4–33) | 10 (3.8–28) | 16 (5.6–43) | 7.9 (2.9–22) | 6.2 (2.2–17) | 100 (12–480) |
| Pro | Paragraph | 12 (4.4–33) | 10 (3.8–28) | 16 (5.6–43) | 7.9 (2.9–22) | 6.2 (2.2–17) | 100 (12–480) |
| Pro | Page | 15 (5.4–44) | 13 (4.6–38) | 20 (7.0–56) | 10 (3.6–29) | 7.8 (2.8–22) | 130 (16–620) |
| Pro | Essay | 28 (9.6–86) | 24 (8.2–74) | 36 (12–110) | 18 (6.3–56) | 14 (5.0–44) | 240 (28–1,200) |

Context: >60k tokens
| Setting | Length | Default CO2e (0.35) | US midday CO2e (0.30) | US evening CO2e (0.45) | Illinois CO2e (0.23) | California CO2e (0.18) | Water |
|---|---|---|---|---|---|---|---|
| Instant | Short reply | 11 (7.0–14) | 9.0 (6.0–12) | 14 (9.0–18) | 6.9 (4.6–9.2) | 5.4 (3.6–7.2) | 90 (20–200) |
| Instant | Paragraph | 11 (7.0–14) | 9.0 (6.0–12) | 14 (9.0–18) | 6.9 (4.6–9.3) | 5.4 (3.6–7.3) | 90 (20–200) |
| Instant | Page | 11 (7.0–14) | 9.1 (6.0–12) | 14 (9.1–18) | 7.0 (4.6–9.4) | 5.5 (3.6–7.4) | 91 (20–200) |
| Instant | Essay | 11 (7.1–15) | 9.2 (6.1–13) | 14 (9.1–19) | 7.0 (4.7–9.6) | 5.5 (3.7–7.5) | 92 (20–210) |
| Thinking light | Short reply | 11 (7.1–15) | 9.4 (6.1–13) | 14 (9.2–19) | 7.2 (4.7–9.9) | 5.6 (3.7–7.7) | 94 (20–220) |
| Thinking light | Paragraph | 11 (7.1–15) | 9.4 (6.1–13) | 14 (9.2–19) | 7.2 (4.7–9.9) | 5.6 (3.7–7.7) | 94 (20–220) |
| Thinking light | Page | 11 (7.2–15) | 9.5 (6.1–13) | 14 (9.2–20) | 7.3 (4.7–10) | 5.7 (3.7–8.0) | 95 (20–220) |
| Thinking light | Essay | 12 (7.4–17) | 10 (6.3–15) | 15 (9.5–22) | 7.8 (4.8–11) | 6.1 (3.8–8.8) | 100 (21–240) |
| Thinking standard | Short reply | 12 (7.4–17) | 9.9 (6.3–14) | 15 (9.4–21) | 7.6 (4.8–11) | 5.9 (3.8–8.6) | 99 (21–240) |
| Thinking standard | Paragraph | 12 (7.4–17) | 9.9 (6.3–14) | 15 (9.4–21) | 7.6 (4.8–11) | 5.9 (3.8–8.6) | 99 (21–240) |
| Thinking standard | Page | 12 (7.5–18) | 10 (6.4–15) | 15 (9.6–23) | 7.9 (4.9–12) | 6.2 (3.9–9.1) | 100 (21–250) |
| Thinking standard | Essay | 14 (8.0–22) | 12 (6.9–19) | 18 (10–28) | 9.0 (5.3–14) | 7.0 (4.1–11) | 120 (23–310) |
| Thinking high | Short reply | 13 (7.9–21) | 11 (6.8–18) | 17 (10–27) | 8.6 (5.2–14) | 6.8 (4.0–11) | 110 (22–300) |
| Thinking high | Paragraph | 13 (7.9–21) | 11 (6.8–18) | 17 (10–27) | 8.6 (5.2–14) | 6.8 (4.0–11) | 110 (22–300) |
| Thinking high | Page | 14 (8.2–24) | 12 (7.0–20) | 18 (11–31) | 9.3 (5.4–16) | 7.3 (4.2–12) | 120 (24–340) |
| Thinking high | Essay | 18 (9.6–35) | 16 (8.2–30) | 24 (12–45) | 12 (6.3–23) | 9.4 (5.0–18) | 160 (28–500) |
| Pro | Short reply | 18 (9.6–40) | 16 (8.2–34) | 24 (12–52) | 12 (6.3–26) | 9.4 (5.0–21) | 160 (28–580) |
| Pro | Paragraph | 18 (9.6–40) | 16 (8.2–34) | 24 (12–52) | 12 (6.3–26) | 9.4 (5.0–21) | 160 (28–580) |
| Pro | Page | 22 (11–51) | 18 (9.2–44) | 28 (14–65) | 14 (7.0–33) | 11 (5.5–26) | 180 (30–720) |
| Pro | Essay | 34 (15–93) | 29 (13–80) | 44 (19–120) | 22 (9.8–61) | 18 (7.6–48) | 290 (42–1,300) |
<!-- END GENERATED CARBON/WATER LOOKUPS -->

3. This check's base cost is about 0.24 Wh on Instant, 1.5 Wh on Thinking light, 3.6 Wh on Medium, 9.0 Wh on High, or 27 Wh on Pro. Add the thread-context cost (none through 5k tokens, 3 Wh at 5–20k, 12 Wh at 20–60k, 30 Wh over 60k) to both the check's cost and its ten-times-cost cutoff. Use this lookup (check cost / minimum next-answer gap, Wh; rounded to two significant figures):

| Setting | Through 5k tokens | 5–20k | 20–60k | Over 60k |
|---|---:|---:|---:|---:|
| Instant | 0.24 / 2.4 | 3.2 / 32 | 12 / 120 | 30 / 300 |
| Thinking light | 1.5 / 15 | 4.5 / 45 | 14 / 140 | 32 / 320 |
| Medium | 3.6 / 36 | 6.6 / 66 | 16 / 160 | 34 / 340 |
| High | 9.0 / 90 | 12 / 120 | 21 / 210 | 39 / 390 |
| Pro | 27 / 270 | 30 / 300 | 39 / 390 | 57 / 570 |
If you don't know which setting it ran on, give the applicable Instant and High figures. It was worth running if the next-answer gap between the settings I'm weighing meets the cutoff; otherwise say so and point me to the pocket card or to running it on Instant.
4. In perspective: the main gap is the difference in Table A between my two named settings (or, if I named one or none, between Instant and the heaviest setting that would help). Translate it with: 10 W LED bulb = 1 Wh per 6 minutes; phone charge ≈ 15 Wh; laptop for an hour ≈ 50 Wh; kettle 1 L ≈ 100 Wh; car ≈ 400 g CO2 per mile (1 g ≈ 13 ft); sip ≈ 30 mL. Then copy the matching line from Table C, word for word (pick the nearest pair and length; do not compute a new one). Table C is a separate default-factor scenario at 0.35 g CO2e/Wh, even if the menu uses another carbon factor.

TABLE C. A million answers like this (separate default-factor scenario: 0.35 g CO2e/Wh)
- Instant → Thinking light, short reply: gap 1.2 Wh; a million answers ≈ 0.12 household-years of electricity, 0.092 car-years of CO2, 3.3 household-days of water
- Instant → Thinking light, paragraph: gap 1.1 Wh; a million answers ≈ 0.11 household-years of electricity, 0.086 car-years of CO2, 3.1 household-days of water
- Instant → Thinking light, page: gap 1.5 Wh; a million answers ≈ 0.14 household-years of electricity, 0.11 car-years of CO2, 4.0 household-days of water
- Instant → Thinking light, essay: gap 3.1 Wh; a million answers ≈ 0.30 household-years of electricity, 0.24 car-years of CO2, 8.6 household-days of water
- Instant → Thinking standard, short reply: gap 3.0 Wh; a million answers ≈ 0.28 household-years of electricity, 0.23 car-years of CO2, 8.1 household-days of water
- Instant → Thinking standard, paragraph: gap 2.9 Wh; a million answers ≈ 0.27 household-years of electricity, 0.22 car-years of CO2, 7.9 household-days of water
- Instant → Thinking standard, page: gap 3.9 Wh; a million answers ≈ 0.37 household-years of electricity, 0.30 car-years of CO2, 11 household-days of water
- Instant → Thinking standard, essay: gap 8.4 Wh; a million answers ≈ 0.80 household-years of electricity, 0.64 car-years of CO2, 23 household-days of water
- Instant → Thinking high, short reply: gap 7.5 Wh; a million answers ≈ 0.71 household-years of electricity, 0.57 car-years of CO2, 20 household-days of water
- Instant → Thinking high, paragraph: gap 7.4 Wh; a million answers ≈ 0.70 household-years of electricity, 0.56 car-years of CO2, 20 household-days of water
- Instant → Thinking high, page: gap 10 Wh; a million answers ≈ 0.97 household-years of electricity, 0.78 car-years of CO2, 28 household-days of water
- Instant → Thinking high, essay: gap 22 Wh; a million answers ≈ 2.1 household-years of electricity, 1.7 car-years of CO2, 60 household-days of water
- Instant → Pro, short reply: gap 22 Wh; a million answers ≈ 2.1 household-years of electricity, 1.7 car-years of CO2, 61 household-days of water
- Instant → Pro, paragraph: gap 22 Wh; a million answers ≈ 2.1 household-years of electricity, 1.7 car-years of CO2, 61 household-days of water
- Instant → Pro, page: gap 31 Wh; a million answers ≈ 3.0 household-years of electricity, 2.4 car-years of CO2, 85 household-days of water
- Instant → Pro, essay: gap 67 Wh; a million answers ≈ 6.4 household-years of electricity, 5.1 car-years of CO2, 180 household-days of water
- Thinking light → Thinking standard, short reply: gap 1.8 Wh; a million answers ≈ 0.17 household-years of electricity, 0.13 car-years of CO2, 4.8 household-days of water
- Thinking light → Thinking standard, paragraph: gap 1.8 Wh; a million answers ≈ 0.17 household-years of electricity, 0.13 car-years of CO2, 4.8 household-days of water
- Thinking light → Thinking standard, page: gap 2.4 Wh; a million answers ≈ 0.23 household-years of electricity, 0.19 car-years of CO2, 6.7 household-days of water
- Thinking light → Thinking standard, essay: gap 5.2 Wh; a million answers ≈ 0.50 household-years of electricity, 0.40 car-years of CO2, 14 household-days of water
- Thinking light → Thinking high, short reply: gap 6.2 Wh; a million answers ≈ 0.60 household-years of electricity, 0.48 car-years of CO2, 17 household-days of water
- Thinking light → Thinking high, paragraph: gap 6.2 Wh; a million answers ≈ 0.60 household-years of electricity, 0.48 car-years of CO2, 17 household-days of water
- Thinking light → Thinking high, page: gap 8.8 Wh; a million answers ≈ 0.83 household-years of electricity, 0.67 car-years of CO2, 24 household-days of water
- Thinking light → Thinking high, essay: gap 19 Wh; a million answers ≈ 1.8 household-years of electricity, 1.4 car-years of CO2, 51 household-days of water
- Thinking light → Pro, short reply: gap 21 Wh; a million answers ≈ 2.0 household-years of electricity, 1.6 car-years of CO2, 58 household-days of water
- Thinking light → Pro, paragraph: gap 21 Wh; a million answers ≈ 2.0 household-years of electricity, 1.6 car-years of CO2, 58 household-days of water
- Thinking light → Pro, page: gap 30 Wh; a million answers ≈ 2.8 household-years of electricity, 2.3 car-years of CO2, 81 household-days of water
- Thinking light → Pro, essay: gap 64 Wh; a million answers ≈ 6.1 household-years of electricity, 4.9 car-years of CO2, 170 household-days of water
- Thinking standard → Thinking high, short reply: gap 4.5 Wh; a million answers ≈ 0.43 household-years of electricity, 0.34 car-years of CO2, 12 household-days of water
- Thinking standard → Thinking high, paragraph: gap 4.5 Wh; a million answers ≈ 0.43 household-years of electricity, 0.34 car-years of CO2, 12 household-days of water
- Thinking standard → Thinking high, page: gap 6.3 Wh; a million answers ≈ 0.60 household-years of electricity, 0.48 car-years of CO2, 17 household-days of water
- Thinking standard → Thinking high, essay: gap 14 Wh; a million answers ≈ 1.3 household-years of electricity, 1.0 car-years of CO2, 37 household-days of water
- Thinking standard → Pro, short reply: gap 20 Wh; a million answers ≈ 1.9 household-years of electricity, 1.5 car-years of CO2, 53 household-days of water
- Thinking standard → Pro, paragraph: gap 20 Wh; a million answers ≈ 1.9 household-years of electricity, 1.5 car-years of CO2, 53 household-days of water
- Thinking standard → Pro, page: gap 27 Wh; a million answers ≈ 2.6 household-years of electricity, 2.1 car-years of CO2, 74 household-days of water
- Thinking standard → Pro, essay: gap 58 Wh; a million answers ≈ 5.6 household-years of electricity, 4.5 car-years of CO2, 160 household-days of water
- Thinking high → Pro, short reply: gap 15 Wh; a million answers ≈ 1.4 household-years of electricity, 1.1 car-years of CO2, 41 household-days of water
- Thinking high → Pro, paragraph: gap 15 Wh; a million answers ≈ 1.4 household-years of electricity, 1.1 car-years of CO2, 41 household-days of water
- Thinking high → Pro, page: gap 21 Wh; a million answers ≈ 2.0 household-years of electricity, 1.6 car-years of CO2, 57 household-days of water
- Thinking high → Pro, essay: gap 45 Wh; a million answers ≈ 4.3 household-years of electricity, 3.4 car-years of CO2, 120 household-days of water
(US household ≈ 10,500 kWh a year and ≈ 1,100 L of water a day; a typical car ≈ 4.6 t CO2 a year.)

5. What more effort buys here: helps multi-step reasoning, argument, close reading of long passages, comparing sources, checking claims, math, code; little for rephrasing, short recall, tone, idea lists, summaries of text already here. Say which my request is.
6. Where and when: consumer ChatGPT doesn't disclose where answers are computed, so my place is a scenario, not a fact; name the carbon factor used. Illinois: Great Lakes water is abundant but finite, and Illinois is still among the five states with the most new datacenters in high water-stress spots. California: much of it is water-stressed; also among those five. One bullet on social costs not counted (water stress near datacenters, local grid strain, aggregate demand).
7. Ways to spend less in this thread.
8. Lean: a setting from the table, optionally "for this message only, then <setting>", or "your call"; then one reason. No moralizing; I decide.
9. Basis and limits: OpenAI 0.34 Wh/query (Jun 2025); Google Gemini 0.24 Wh median (Aug 2025); Epoch AI (Feb 2025); Jegham et al. "How Hungry is AI?" (Nov 2025); Univ. of Rhode Island GPT-5 estimate (Aug 2025); EIA (2024); EPA; EPA WaterSense. Excludes training, hardware, networking, my device. Heuristic; sources disagree more than tenfold.
