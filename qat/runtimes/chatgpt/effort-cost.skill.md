---
name: effort-check
description: Use when the user asks what an answer costs the environment (energy, carbon, water) at different model or reasoning-effort settings, whether to turn the effort up or down for this conversation, or says "effort check". Prices every setting for their request, puts it in perspective, and says whether the check was worth its own cost.
---
<!-- ChatGPT plugin skill for effort-cost v0.6.0. Generated from effort-cost.paste.md (same instructions and lookup
     tables, so the two cannot drift); regenerate both when the tables change (effort-cost.card.py).
     Install: custom GPTs are being replaced by plugins whose instructions are skills (late 2026). Put this text in a
     plugin's skill; invoke it with @ (or + > More) or let ChatGPT pick it up when the description matches. Whether an
     @-invoked plugin sees the whole thread is unverified; if not, use the paste block. For ordinary threads the
     pocket card (effort-cost.card.md) answers the same question at no cost. -->

# Effort check

Before you start: ask which setting the user is on (from the composer) and which they are considering, unless they said; and suggest they switch to Instant for this check, then switch back, because the check costs about one answer at whatever setting it runs on. Place and time are optional; if they don't give them and you have an approximate location or time from your own context, you may use it, labelled "estimated". Treat "my" and "I" below as the user.

EFFORT CHECK (heuristic). Look numbers up in the tables below; do not recompute them. If my underlying question is a one-line fact not yet answered, you may answer it in one line before the first heading; otherwise don't answer it.

Use these nine headings, in order, with bullets under each except Cost by setting (a table) and Lean (one line): Your request · Cost by setting · This check · In perspective · What more effort buys here · Where and when · Ways to spend less · Lean · Basis and limits. Under 350 words, not counting the table.

1. Your request: pick the length column for the answer to my underlying request (Short ~100 tokens, Paragraph ~300, Page ~700, Essay ~1,500); the settings, place and time I gave. If I left place or time blank and you have an approximate location or time from your own context, you may use it, labelled "estimated". You cannot see your own setting; never state it. ChatGPT's Power slider: Instant → Instant row, Medium → Thinking standard, High → Thinking high.
2. Cost by setting: estimate thread size as words × 1.3 tokens, including this check. Below 5k tokens, use Tables A and B. At 5k tokens or more, choose the matching context tier in Tables A-context and B-context, and use it for every cost column; do not use the short-context values. Copy the five rows for my length column with columns Setting | Energy (Wh) | CO2e (g) | Water (mL) | Next 5 answers (Wh). Mark my named rows "now" / "considering". CO2e (g) = the selected table's central Wh × carbon factor (0.35; US local time 10 am–4 pm 0.30; 4–10 pm 0.45). Water (mL) = that central Wh × 3. For Next 5, use Table B below 5k tokens and the matching tier in Table B-context otherwise. If my region is Illinois or California, add a column "CO2e near you (g)" = selected central Wh × 0.23 (Illinois) or 0.18 (California).

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

3. This check cost about 0.24 Wh if it ran on Instant, 3.6 Wh on Medium, 9.0 Wh on High, 27 Wh on Pro. If you don't know which, give the Instant and High figures. It was worth running if the next-answer gap between the settings I'm weighing is at least 2.4 Wh (on Instant), 36 Wh (on Medium) or 90 Wh (on High). If not, say so and point me to the pocket card or to running it on Instant.
4. In perspective: the main gap is the difference in Table A between my two named settings (or, if I named one or none, between Instant and the heaviest setting that would help). Translate it with: 10 W LED bulb = 1 Wh per 6 minutes; phone charge ≈ 15 Wh; laptop for an hour ≈ 50 Wh; kettle 1 L ≈ 100 Wh; car ≈ 400 g CO2 per mile (1 g ≈ 13 ft); sip ≈ 30 mL. Then copy the matching line from Table C, word for word (pick the nearest pair and length; do not compute a new one). Table C is a separate default-factor scenario at 0.35 g CO2e/Wh, even if the menu uses another carbon factor.

TABLE C. A million answers like this (separate default-factor scenario: 0.35 g CO2e/Wh)
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
