"""Generate effort-cost lookup tables from constants manually synchronized with the spec.

WHY THIS EXISTS
    The check is meant to run on ChatGPT's lightest setting (Instant), so that
    evaluating costs far less than what it informs. Live runs (2026-11-06) showed
    Instant cannot do the multi-step arithmetic reliably: it misapplied the
    reasoning floors and twice mis-scaled the "million answers" line by factors of
    1,000 to 1,000,000. So the arithmetic is done here, once, and the paste block
    and pocket card only look values up.

WHAT IT PRINTS (paste the output into effort-cost.paste.md and effort-cost.card.md)
    1. Energy per answer, Wh, central (low-high), by setting x answer length.
    2. Next 5 answers, Wh, central: this answer + 4 one-paragraph follow-ups.
    3. A million answers like this, per setting pair the user is likely to weigh,
       already converted to household-years, car-years and household-days of water.

RULES MIRRORED FROM THE SPEC (qat/tools/effort-cost.qat.md, module: menu)
    - Scale by answer length (per 1,000 tokens).
    - Thinking and Pro rows never go below half the table value (hidden reasoning).
    - Carbon 0.35 g/Wh by default; water 3 mL/Wh central.
    - US household 10,500 kWh/yr; car 4.6 t CO2/yr; household water 1,100 L/day.
    - Two significant figures.

Run: python3 -I runtimes/chatgpt/effort-cost.card.py     (from qat/)

The coefficients are hard-coded below, not read from the spec. When one changes,
manually synchronize the matching constants, rerun this script, and propagate
the output to the paste block and pocket card; then regenerate the skill text.
"""
from math import floor, log10

# Keep manually synchronized with Table 1 of the spec: (name, (low, central, high) Wh per ~1,000-token answer, is_reasoning)
T1 = [
    ("Instant", (0.2, 0.4, 1.2), False),
    ("Thinking light", (0.7, 2.5, 6), True),
    ("Thinking standard (ChatGPT Medium)", (2, 6, 15), True),
    ("Thinking high (ChatGPT High)", (5, 15, 40), True),
    ("Pro", (15, 45, 150), True),
]
LENGTHS = [("Short reply (~100 tokens)", 0.1), ("Paragraph (~300)", 0.3), ("Page (~700)", 0.7), ("Essay (~1,500)", 1.5)]
PARAGRAPH = 0.3
CARBON, WATER = 0.35, 3.0
HH_KWH_YR, CAR_T_YR, HH_L_DAY = 10_500, 4.6, 1_100


def sig(x: float) -> str:
    """Two significant figures, with thousands separators."""
    if x == 0:
        return "0"
    d = 2 - int(floor(log10(abs(x)))) - 1
    v = round(x, d)
    return f"{v:,.{d}f}" if d > 0 else f"{int(round(v)):,}"


def per_answer(vals, factor, reasoning):
    m = max(factor, 0.5) if reasoning else factor
    return tuple(v * m for v in vals)


def next5(vals, factor, reasoning):
    first = per_answer(vals, factor, reasoning)[1]
    return first + 4 * per_answer(vals, PARAGRAPH, reasoning)[1]


def million(gap_wh: float) -> str:
    hh_years = gap_wh * 1e6 / 1000 / HH_KWH_YR
    car_years = gap_wh * CARBON * 1e6 / 1e6 / CAR_T_YR
    hh_days = gap_wh * WATER * 1e6 / 1000 / HH_L_DAY
    return f"{sig(hh_years)} household-years of electricity, {sig(car_years)} car-years of CO2, {sig(hh_days)} household-days of water"


def main():
    print("ENERGY PER ANSWER (Wh): central (low–high)")
    print("| Setting | " + " | ".join(l for l, _ in LENGTHS) + " |")
    print("|---|" + "---|" * len(LENGTHS))
    for name, vals, r in T1:
        cells = []
        for _, f in LENGTHS:
            lo, c, hi = per_answer(vals, f, r)
            cells.append(f"{sig(c)} ({sig(lo)}–{sig(hi)})")
        print(f"| {name} | " + " | ".join(cells) + " |")

    print("\nNEXT 5 ANSWERS (Wh, central): this answer + 4 one-paragraph follow-ups")
    print("| Setting | " + " | ".join(l for l, _ in LENGTHS) + " |")
    print("|---|" + "---|" * len(LENGTHS))
    for name, vals, r in T1:
        print(f"| {name} | " + " | ".join(sig(next5(vals, f, r)) for _, f in LENGTHS) + " |")

    print("\nA MILLION ANSWERS LIKE THIS (gap between two settings, already converted)")
    central = {n: {l: per_answer(v, f, r)[1] for l, f in LENGTHS} for n, v, r in T1}
    names = [n for n, _, _ in T1]
    pairs = [(names[0], names[3]), (names[2], names[3]), (names[3], names[4]), (names[0], names[4]), (names[0], names[2])]
    for a, b in pairs:
        for l, _ in [LENGTHS[1], LENGTHS[3]]:
            gap = central[b][l] - central[a][l]
            print(f"- {a.split(' (')[0]} → {b.split(' (')[0]}, {l.split(' (')[0].lower()}: gap {sig(gap)} Wh; a million answers ≈ {million(gap)}")


if __name__ == "__main__":
    main()
