"""
svg_charts.py — the small inline-SVG chart helper auto_eda.py draws with.

Standard library only. Every function returns one `<svg>` element as text, ready to place in
an HTML page. Each chart carries role="img", an aria-label and a <title>, and each bar, cell
or point has its own <title> so a hover or a screen reader gives the exact value.

Colours are CSS variables with a light-mode fallback (`var(--c0, #3b6ea8)`), so a chart reads
in the report's light and dark themes and still has colour when pasted somewhere else.
All text from the data is escaped here; callers pass plain strings.
"""
from __future__ import annotations

import html
import math

# Light-mode fallbacks for the report's --c0..--c7 variables (dark values live in the page CSS).
PALETTE_HEX = ["#3b6ea8", "#e07b39", "#4e9a6b", "#b04a5a", "#7a5ea8", "#c9a227", "#3a9aa6", "#8a8a8a"]
PALETTE = [f"var(--c{i}, {h})" for i, h in enumerate(PALETTE_HEX)]
FG = "var(--fg, #1d1d1b)"
MUTED = "var(--mut, #666)"
LINE = "var(--line, #d9d6cf)"
POS = "var(--pos, #b2182b)"   # correlation > 0
NEG = "var(--neg, #2166ac)"   # correlation < 0

W = 640          # every chart's viewBox width; the page scales it to the card
FONT = 12
CHAR_W = 0.6 * FONT   # rough width of one character, for label room


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def fmt(v, step=None) -> str:
    """Compact number for axes and labels: 1,234 / 0.123 / 1.2e+06.

    `step` is the spacing between neighbouring values on the same scale (tick or bin width);
    when given, enough decimals are kept to tell neighbours apart (1,000.2 / 1,000.4), however
    narrow the range is relative to its size."""
    if v is None or (isinstance(v, float) and not math.isfinite(v)):
        return "—"
    v = float(v)
    if step and math.isfinite(step) and step > 0 and 1e-6 <= abs(v) < 1e12 or (step and v == 0):
        decimals = max(0, 1 - math.floor(math.log10(step)))   # one digit finer than the step
        s = f"{v:,.{decimals}f}"
        return s.rstrip("0").rstrip(".") if "." in s else s
    if v.is_integer() and abs(v) < 1e7:
        return f"{int(v):,}"
    return f"{v:,.4g}"


def clip(label, n=26) -> str:
    label = str(label)
    return label if len(label) <= n else label[: n - 1] + "…"


def nice_ticks(lo: float, hi: float, n: int = 5) -> list[float]:
    """About n round-numbered ticks covering [lo, hi]."""
    if not (math.isfinite(lo) and math.isfinite(hi)):
        return []
    if hi == lo:
        return [lo]
    raw = (hi - lo) / max(1, n)
    if not math.isfinite(raw) or raw <= 0:   # a span beyond float range: just the ends
        return [lo, hi]
    mag = 10.0 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    first = math.ceil(lo / step) * step
    out = []
    for i in range(2 * n + 2):               # bounded, whatever float rounding does
        t = first + i * step
        if not math.isfinite(t) or t - hi > step * 1e-9:
            break
        out.append(t)            # display rounding is fmt()'s job; rounding here zeroed tiny scales
    return out


def svg_doc(title: str, height: float, body: str, desc: str = "", width: float = W) -> str:
    """Wrap chart marks in an accessible <svg>. `title` is shown and also read out.
    `width` widens the viewBox for a chart that needs more room (the page still scales it to fit)."""
    h, w = math.ceil(height), math.ceil(max(width, W))
    d = f"<desc>{esc(desc)}</desc>" if desc else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{esc(title)}" font-size="{FONT}" style="font-family:inherit">'
            f"<title>{esc(title)}</title>{d}"
            f'<text x="0" y="16" font-size="14" font-weight="600" style="fill:{FG}">{esc(title)}</text>'
            f"{body}</svg>")


def _rect(x, y, w, h, fill, tip, extra=""):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" height="{h:.1f}" '
            f'style="fill:{fill}"{extra}><title>{esc(tip)}</title></rect>')


def bar(title, labels, values, *, annotate=True, xmax=None, xlabel=None, colors=None,
        value_fmt=None, desc="") -> str:
    """Horizontal bars, first label on top. `annotate` writes "count (pct%)" after each bar."""
    labels = [str(x) for x in labels]
    values = [float(v) for v in values]
    total = sum(values) or 1
    row = 22
    lab_w = min(200, max(40, CHAR_W * max((len(clip(x)) for x in labels), default=4) + 8))
    top = 30
    x0, x1 = lab_w, W - (110 if annotate else 20)
    # domain always includes 0; bars run from the zero line to their value, either side
    lo = min(0.0, min(values, default=0))
    hi = xmax if xmax is not None else max(0.0, max(values, default=0))
    if hi == lo:
        hi = lo + 1
    sx = lambda v: x0 + (x1 - x0) * (v - lo) / (hi - lo)
    zero = sx(0)
    marks = []
    if lo < 0:
        marks.append(f'<line x1="{zero:.1f}" y1="{top}" x2="{zero:.1f}" y2="{top + len(labels) * row}" style="stroke:{MUTED}"/>')
    for i, (lab, v) in enumerate(zip(labels, values)):
        y = top + i * row
        start, w = min(zero, sx(v)), abs(sx(v) - zero)
        fill = (colors[i % len(colors)] if colors else PALETTE[0])
        text = value_fmt(v) if value_fmt else f"{fmt(v)} ({100 * v / total:.0f}%)"
        marks.append(f'<text x="{x0 - 6:.1f}" y="{y + 15}" text-anchor="end" style="fill:{FG}">'
                     f"<title>{esc(lab)}</title>{esc(clip(lab))}</text>")
        marks.append(_rect(start, y + 3, w, row - 6, fill, f"{lab}: {text}", ' class="bar"'))
        if annotate:
            marks.append(f'<text x="{max(zero, sx(v)) + 4:.1f}" y="{y + 15}" style="fill:{MUTED}">{esc(text)}</text>')
    height = top + len(labels) * row + 6
    if xlabel:
        marks.append(f'<text x="{x0}" y="{height + 12}" style="fill:{MUTED}">{esc(xlabel)}</text>')
        height += 18
    return svg_doc(title, height, "".join(marks), desc)


def _axis_x(x0, x1, y, lo, hi, ticks):
    step = ticks[1] - ticks[0] if len(ticks) > 1 else None
    out = [f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" style="stroke:{LINE}"/>']
    for t in ticks:
        x = x0 + (x1 - x0) * ((t - lo) / (hi - lo) if hi > lo else 0.5)
        out.append(f'<text x="{x:.1f}" y="{y + 15}" text-anchor="middle" style="fill:{MUTED}">{esc(fmt(t, step))}</text>')
    return "".join(out)


def _axis_y(x, y0, y1, hi, ticks):
    """Left axis for counts from 0 (at y1, bottom) to hi (at y0, top)."""
    out = []
    for t in ticks:
        y = y1 - (y1 - y0) * (t / hi if hi else 0)
        out.append(f'<line x1="{x}" y1="{y:.1f}" x2="{W - 10}" y2="{y:.1f}" style="stroke:{LINE};stroke-dasharray:2 3"/>')
        out.append(f'<text x="{x - 4}" y="{y + 4:.1f}" text-anchor="end" style="fill:{MUTED}">{esc(fmt(t))}</text>')
    return "".join(out)


def histogram(title, counts, edges, *, box=None, desc="") -> str:
    """Bars over bin `edges` (len(counts)+1), with an optional box strip
    box = {"min","q1","median","q3","max"} (whisker ends) drawn above, plus optional
    "outliers" (values beyond the whiskers): one dot per occupied pixel, so size stays bounded."""
    x0, x1 = 50, W - 10
    lo, hi = float(edges[0]), float(edges[-1])
    span = (hi - lo) or 1
    sx = lambda v: x0 + (x1 - x0) * (float(v) - lo) / span
    marks = []
    top = 30
    if box:
        yb, hb = top + 4, 16
        cy = yb + hb / 2
        marks.append(f'<line x1="{sx(box["min"]):.1f}" y1="{cy}" x2="{sx(box["max"]):.1f}" y2="{cy}" style="stroke:{PALETTE[0]}"/>')
        q1, q3 = sx(box["q1"]), sx(box["q3"])
        tip = f"IQR {fmt(box['q1'])} to {fmt(box['q3'])}, median {fmt(box['median'])}"
        marks.append(f'<rect class="box" x="{q1:.1f}" y="{yb}" width="{max(q3 - q1, 1):.1f}" height="{hb}" '
                     f'style="fill:none;stroke:{PALETTE[0]};stroke-width:1.5"><title>{esc(tip)}</title></rect>')
        mx = sx(box["median"])
        marks.append(f'<line x1="{mx:.1f}" y1="{yb}" x2="{mx:.1f}" y2="{yb + hb}" style="stroke:{PALETTE[1]};stroke-width:2"/>')
        dots = {}
        for v in box.get("outliers") or ():
            dots.setdefault(round(sx(v)), []).append(float(v))
        for px, vs in sorted(dots.items()):
            a, b = fmt(min(vs)), fmt(max(vs))
            tip = (f"outlier {a}" if len(vs) == 1 else
                   f"{len(vs)} outliers at {a}" if a == b else f"{len(vs)} outliers, {a} to {b}")
            marks.append(f'<circle class="outlier" cx="{px}" cy="{cy}" r="2.5" '
                         f'style="fill:none;stroke:{PALETTE[0]}"><title>{esc(tip)}</title></circle>')
        top = yb + hb + 8
    y0, y1 = top + 4, top + 200
    cmax = max(counts, default=0) or 1
    marks.append(_axis_y(x0, y0, y1, cmax, [t for t in nice_ticks(0, cmax, 4) if t > 0]))
    for c, a, b in zip(counts, edges[:-1], edges[1:]):
        h = (y1 - y0) * c / cmax
        marks.append(_rect(sx(a) + 0.5, y1 - h, sx(b) - sx(a) - 1, h, PALETTE[0],
                           f"{fmt(a, b - a)} to {fmt(b, b - a)}: {fmt(c)} rows", ' class="bar"'))
    marks.append(_axis_x(x0, x1, y1, lo, hi, nice_ticks(lo, hi, 6)))
    return svg_doc(title, y1 + 24, "".join(marks), desc)


def line(title, labels, values, *, desc="") -> str:
    """A count per period: `labels` are consecutive, evenly spaced periods (shown first, middle,
    last), so x position is elapsed time. Fill empty periods with 0 rather than leaving them out."""
    x0, x1, y0, y1 = 50, W - 14, 34, 230
    n = len(values)
    vmax = max(values, default=0) or 1
    sx = lambda i: x0 + (x1 - x0) * (i / (n - 1) if n > 1 else 0.5)
    sy = lambda v: y1 - (y1 - y0) * v / vmax
    marks = [_axis_y(x0, y0, y1, vmax, [t for t in nice_ticks(0, vmax, 4) if t > 0]),
             f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" style="stroke:{LINE}"/>']
    pts = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(values))
    marks.append(f'<polyline points="{pts}" style="fill:none;stroke:{PALETTE[0]};stroke-width:1.6"/>')
    if n <= 120:  # hover targets; skip on long series to keep the file small
        marks += [f'<circle cx="{sx(i):.1f}" cy="{sy(v):.1f}" r="2.5" style="fill:{PALETTE[0]}">'
                  f"<title>{esc(lab)}: {esc(fmt(v))}</title></circle>"
                  for i, (lab, v) in enumerate(zip(labels, values))]
    for i in sorted({0, (n - 1) // 2, n - 1}) if n else []:
        anchor = "start" if i == 0 else "end" if i == n - 1 else "middle"
        marks.append(f'<text x="{sx(i):.1f}" y="{y1 + 15}" text-anchor="{anchor}" style="fill:{MUTED}">{esc(labels[i])}</text>')
    return svg_doc(title, y1 + 24, "".join(marks), desc)


def heatmap(title, labels, matrix, *, show_values=None, desc="") -> str:
    """Square grid of values in [-1, 1]: red for positive, blue for negative, opacity = |value|."""
    k = len(labels)
    show_values = k <= 12 if show_values is None else show_values
    lab_w = min(160, max(40, CHAR_W * max((len(clip(x, 20)) for x in map(str, labels)), default=4) + 8))
    cell = max(14, min(44, (W - lab_w - 20) / max(k, 1)))
    width = lab_w + k * cell + 20   # past ~35 columns the viewBox widens rather than clip the grid
    top = 30 + lab_w * 0.72   # room for the slanted column labels
    marks = []
    for j, lab in enumerate(labels):
        x = lab_w + (j + 0.5) * cell
        marks.append(f'<text transform="translate({x:.1f},{top - 4:.1f}) rotate(-45)" style="fill:{FG}">'
                     f"<title>{esc(lab)}</title>{esc(clip(lab, 20))}</text>")
    for i, a in enumerate(labels):
        y = top + i * cell
        marks.append(f'<text x="{lab_w - 6:.1f}" y="{y + cell / 2 + 4:.1f}" text-anchor="end" style="fill:{FG}">'
                     f"<title>{esc(a)}</title>{esc(clip(a, 20))}</text>")
        for j, b in enumerate(labels):
            v = matrix[i][j]
            ok = v is not None and math.isfinite(v)
            fill = (POS if v >= 0 else NEG) if ok else "none"
            op = f";fill-opacity:{min(1, abs(v)):.2f}" if ok else ""
            x = lab_w + j * cell
            marks.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell - 1:.1f}" height="{cell - 1:.1f}" '
                         f'style="fill:{fill}{op};stroke:{LINE}"><title>{esc(a)} × {esc(b)}: '
                         f"{'r = ' + format(v, '.2f') if ok else 'n/a'}</title></rect>")
            if show_values and ok:
                tc = "#fff" if abs(v) > 0.6 else FG
                marks.append(f'<text x="{x + cell / 2:.1f}" y="{y + cell / 2 + 4:.1f}" text-anchor="middle" '
                             f'font-size="10" style="fill:{tc}">{v:.2f}</text>')
    height = top + k * cell + 22
    marks.append(f'<text x="{lab_w}" y="{height - 6:.1f}" style="fill:{MUTED}">'
                 f"red: positive · blue: negative · stronger colour: stronger correlation</text>")
    return svg_doc(title, height, "".join(marks), desc, width=width)


# The chart kinds a rule or plugin may name in a chart spec, instead of writing SVG itself.
CHART_KINDS = {"bar": bar, "histogram": histogram, "line": line, "heatmap": heatmap}


def draw(spec: dict) -> str:
    """Draw a chart spec: {"kind": "bar", "title": ..., <that function's arguments>}."""
    spec = dict(spec)
    kind = spec.pop("kind", None)
    if kind not in CHART_KINDS:
        raise ValueError(f"unknown chart kind {kind!r}; expected one of {sorted(CHART_KINDS)}")
    return CHART_KINDS[kind](**spec)
