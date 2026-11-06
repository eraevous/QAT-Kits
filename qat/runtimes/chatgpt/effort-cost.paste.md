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
2. Cost by setting: copy the five rows for my length column from Table A, with columns Setting | Energy (Wh) | CO2e (g) | Water (mL) | Next 5 answers (Wh). Mark my named rows "now" / "considering". CO2e (g) = the central Wh × carbon factor (0.35; US local time 10 am–4 pm 0.30; 4–10 pm 0.45). Water (mL) = the central Wh × 3. Next 5 from Table B. If my region is Illinois or California, add a column "CO2e near you (g)" = central Wh × 0.23 (Illinois) or 0.18 (California). If the thread is past roughly 4,000 words, say every answer costs about 3 Wh more (past 15,000 words, about 12 Wh more).

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

3. This check cost about 0.24 Wh if it ran on Instant, 3.6 Wh on Medium, 9.0 Wh on High, 27 Wh on Pro. If you don't know which, give the Instant and High figures. It was worth running if the next-answer gap between the settings I'm weighing is at least 2.4 Wh (on Instant), 36 Wh (on Medium) or 90 Wh (on High). If not, say so and point me to the pocket card or to running it on Instant.
4. In perspective: the main gap is the difference in Table A between my two named settings (or, if I named one or none, between Instant and the heaviest setting that would help). Translate it with: 10 W LED bulb = 1 Wh per 6 minutes; phone charge ≈ 15 Wh; laptop for an hour ≈ 50 Wh; kettle 1 L ≈ 100 Wh; car ≈ 400 g CO2 per mile (1 g ≈ 13 ft); sip ≈ 30 mL. Then copy the matching line from Table C, word for word (pick the nearest pair and length; do not compute a new one).

TABLE C. A million answers like this
- Instant → High, paragraph: gap 7.4 Wh; a million answers ≈ 0.70 household-years of electricity, 0.56 car-years of CO2, 20 household-days of water
- Instant → High, essay: gap 22 Wh; ≈ 2.1 household-years, 1.7 car-years, 60 household-days of water
- Medium → High, paragraph: gap 4.5 Wh; ≈ 0.43 household-years, 0.34 car-years, 12 household-days of water
- Medium → High, essay: gap 14 Wh; ≈ 1.3 household-years, 1.0 car-years, 37 household-days of water
- Instant → Medium, paragraph: gap 2.9 Wh; ≈ 0.27 household-years, 0.22 car-years, 7.9 household-days of water
- Instant → Medium, essay: gap 8.4 Wh; ≈ 0.80 household-years, 0.64 car-years, 23 household-days of water
- High → Pro, paragraph: gap 15 Wh; ≈ 1.4 household-years, 1.1 car-years, 41 household-days of water
- High → Pro, essay: gap 45 Wh; ≈ 4.3 household-years, 3.4 car-years, 120 household-days of water
- Instant → Pro, paragraph: gap 22 Wh; ≈ 2.1 household-years, 1.7 car-years, 61 household-days of water
- Instant → Pro, essay: gap 67 Wh; ≈ 6.4 household-years, 5.1 car-years, 180 household-days of water
(US household ≈ 10,500 kWh a year and ≈ 1,100 L of water a day; a typical car ≈ 4.6 t CO2 a year.)

5. What more effort buys here: helps multi-step reasoning, argument, close reading of long passages, comparing sources, checking claims, math, code; little for rephrasing, short recall, tone, idea lists, summaries of text already here. Say which my request is.
6. Where and when: consumer ChatGPT doesn't disclose where answers are computed, so my place is a scenario, not a fact; name the carbon factor used. Illinois: Great Lakes water is abundant but finite, and Illinois is still among the five states with the most new datacenters in high water-stress spots. California: much of it is water-stressed; also among those five. One bullet on social costs not counted (water stress near datacenters, local grid strain, aggregate demand).
7. Ways to spend less in this thread.
8. Lean: a setting from the table, optionally "for this message only, then <setting>", or "your call"; then one reason. No moralizing; I decide.
9. Basis and limits: OpenAI 0.34 Wh/query (Jun 2025); Google Gemini 0.24 Wh median (Aug 2025); Epoch AI (Feb 2025); Jegham et al. "How Hungry is AI?" (Nov 2025); Univ. of Rhode Island GPT-5 estimate (Aug 2025); EIA (2024); EPA; EPA WaterSense. Excludes training, hardware, networking, my device. Heuristic; sources disagree more than tenfold.
