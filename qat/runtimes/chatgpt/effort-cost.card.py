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
    3. A million answers like this, for every setting pair and answer length,
       already converted to household-years, car-years and household-days of water.
    4. Table D: carbon and water, central (low-high), for every context tier,
       setting and answer length. Copy this block into both runtime texts.

RULES MIRRORED FROM THE SPEC (qat/tools/effort-cost.qat.md, module: menu)
    - Scale by answer length (per 1,000 tokens).
    - Thinking and Pro rows never go below half the table value (hidden reasoning).
    - Carbon 0.35 g/Wh by default; water 3 mL/Wh central.
    - US household 10,500 kWh/yr; car 4.6 t CO2/yr; household water 1,100 L/day.
    - Two significant figures.

Run: python3 -I runtimes/chatgpt/effort-cost.card.py     (from qat/)
Only Table D: add --conversions. Tests check both runtime copies against it.

The coefficients are hard-coded below, not read from the spec. When one changes,
manually synchronize the matching constants, rerun this script, and propagate
the output to the paste block and pocket card; then regenerate the skill text.
"""
import argparse
from decimal import Decimal
from itertools import combinations
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
# Keep synchronized with the spec's context add-on and Tables 2, 2b and 3.
CONTEXTS = [
    ("Below 5k tokens", (0, 0, 0)),
    ("5k–20k tokens", (1, 3, 5)),
    ("20k–60k tokens", (5, 12, 20)),
    (">60k tokens", (20, 30, 40)),
]
CARBON_FACTORS = [("Default", 0.35), ("US midday", 0.30), ("US evening", 0.45),
                  ("Illinois", 0.23), ("California", 0.18)]
WATER_RANGE = (1, WATER, 5)
CONVERSIONS_START = "<!-- BEGIN GENERATED CARBON/WATER LOOKUPS -->"
CONVERSIONS_END = "<!-- END GENERATED CARBON/WATER LOOKUPS -->"


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


def conversion_cells(vals, factor, reasoning, context):
    """Convert unrounded, context-adjusted low/central/high energy, then round.

    Decimal keeps exact source coefficients at rounding boundaries. Carbon's
    range comes from energy; water also carries its own 1/3/5 mL/Wh factors.
    """
    scale = max(Decimal(str(factor)), Decimal("0.5")) if reasoning else Decimal(str(factor))
    energy = tuple(Decimal(str(v)) * scale + Decimal(str(add))
                   for v, add in zip(vals, context))

    def cell(values):
        low, central, high = values
        return f"{sig(central)} ({sig(low)}–{sig(high)})"

    carbon = [cell(tuple(v * Decimal(str(f)) for v in energy)) for _, f in CARBON_FACTORS]
    water = cell(tuple(v * Decimal(str(f)) for v, f in zip(energy, WATER_RANGE)))
    return carbon + [water]


def conversion_tables():
    """Standalone lookup block shared byte-for-byte by paste and skill runtimes."""
    lines = [CONVERSIONS_START,
             "TABLE D. CO2e (g) and water (mL): central (low–high), including context.",
             "Copy the full cell, including its range. Illinois and California are near-you scenarios only."]
    for tier, context in CONTEXTS:
        lines.extend(["", f"Context: {tier}",
                      "| Setting | Length | " + " | ".join(f"{name} CO2e ({factor:.2f})" for name, factor in CARBON_FACTORS) + " | Water |",
                      "|---|---|" + "---|" * (len(CARBON_FACTORS) + 1)])
        for name, vals, reasoning in T1:
            for length, factor in LENGTHS:
                cells = conversion_cells(vals, factor, reasoning, context)
                lines.append(f"| {name.split(' (')[0]} | {length.split(' (')[0]} | " + " | ".join(cells) + " |")
    lines.append(CONVERSIONS_END)
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--conversions", action="store_true", help="print only the generated Table D block")
    args = parser.parse_args(argv)
    if args.conversions:
        print(conversion_tables())
        return
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

    print("\nA MILLION ANSWERS LIKE THIS (all setting pairs and answer lengths, already converted)")
    central = {n: {l: per_answer(v, f, r)[1] for l, f in LENGTHS} for n, v, r in T1}
    names = [n for n, _, _ in T1]
    for a, b in combinations(names, 2):
        for l, _ in LENGTHS:
            gap = central[b][l] - central[a][l]
            print(f"- {a.split(' (')[0]} → {b.split(' (')[0]}, {l.split(' (')[0].lower()}: gap {sig(gap)} Wh; a million answers ≈ {million(gap)}")
    print("\n" + conversion_tables())


if __name__ == "__main__":
    main()
