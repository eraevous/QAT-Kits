"""Regenerate the effort-cost pocket card numbers from the spec's Table 1.

Run: python3 -I runtimes/chatgpt/effort-cost.card.py
Prints the energy table and the key gaps (with million-answer perspective) used in
effort-cost.card.md. Keep T1 in step with Table 1 of qat/tools/effort-cost.qat.md.
Rules mirrored from the spec: scale by answer length; thinking and Pro rows never go below
half the table value; carbon 0.35 g/Wh; water 3 mL/Wh; household 10,500 kWh/yr; car 4.6 t/yr;
household water 1,100 L/day; Olympic pool 2,500,000 L. Two significant figures.
"""
from math import log10, floor
T1 = [("Instant", (0.2, 0.4, 1.2), False), ("Thinking light", (0.7, 2.5, 6), True),
      ("Thinking standard", (2, 6, 15), True), ("Thinking high", (5, 15, 40), True),
      ("Pro", (15, 45, 150), True)]
LENGTHS = [("Paragraph (~300 tokens)", 0.3), ("Page (~700)", 0.7), ("Essay (~1,500)", 1.5)]
def sig(x):
    if x == 0: return "0"
    d = 2 - int(floor(log10(abs(x)))) - 1
    v = round(x, d)
    return f"{v:,.{max(d,0)}f}" if d > 0 else f"{int(round(v)):,}"
def cost(vals, f, reasoning):
    m = max(f, 0.5) if reasoning else f
    return tuple(v * m for v in vals)
rows = []
for name, vals, r in T1:
    cells = []
    for _, f in LENGTHS:
        lo, c, hi = cost(vals, f, r)
        cells.append(f"{sig(c)} ({sig(lo)}–{sig(hi)})")
    rows.append(f"| {name} | " + " | ".join(cells) + " |")
print("| Setting | " + " | ".join(l for l, _ in LENGTHS) + " |")
print("|---|" + "---|" * len(LENGTHS))
print("\n".join(rows))
# key gaps, essay length
e = {n: cost(v, 1.5, r)[1] for n, v, r in T1}
p = {n: cost(v, 0.3, r)[1] for n, v, r in T1}
for a, b, d in [("Thinking standard", "Thinking high", e), ("Instant", "Thinking high", e), ("Thinking high", "Pro", e), ("Instant", "Pro", p)]:
    g = d[b] - d[a]
    print(f"GAP {a}->{b}: {sig(g)} Wh, {sig(g*0.35)} g, {sig(g*3)} mL | x1M: {sig(g)} MWh = {sig(g*1e6/10500e3)} household-years; {sig(g*0.35)} t = {sig(g*0.35/4.6)} car-years; {sig(g*3)} kL = {sig(g*3e3/1100)} household-days, pools {sig(g*3e3/2.5e6)}")
