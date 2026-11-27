"""
Median of a numeric column per category, largest first.

Ported from plot_amount_by_region(df): the data work is unchanged
(groupby category -> median -> sort descending); the matplotlib barh is replaced
by a "bar" chart spec, which auto-eda 2.0 draws as inline SVG.

The original hard-coded region x amount. Here it runs for every pair of a
low-cardinality categorical column and a numeric column, capped at MAX_PAIRS
charts so wide tables don't explode. Each slot is its own dataset-level rule,
because a frame rule returns one chart.
"""
from auto_eda import frame_rule

MAX_PAIRS = 6


def _pairs(profiles):
    cats = [p.name for p in profiles if p.kind == "low_cat"]
    nums = [p.name for p in profiles if p.kind == "numeric"]
    return [(c, n) for c in cats for n in nums][:MAX_PAIRS]


def _median_by(df, cat, num):
    g = df.groupby(cat)[num]
    m = g.median().dropna().sort_values(ascending=False)   # medians skip missing values
    if m.empty:
        return None
    n = g.count()
    return {
        "kind": "bar",
        "title": f"Median {num} by {cat}",
        "labels": [f"{k} (n={n[k]:,})" for k in m.index],   # n = non-missing rows behind each median
        "values": m.values.tolist(),
        # the default "count (pct%)" label would be a share of summed medians; show the median alone
        "value_fmt": lambda v: f"{v:,.3g}",
    }


def _slot(k):
    def fn(df, profiles):
        pairs = _pairs(profiles)
        return _median_by(df, *pairs[k]) if k < len(pairs) else None
    fn.__name__ = f"median_by_category_{k + 1}"
    return fn


for _k in range(MAX_PAIRS):
    frame_rule(f"median numeric by category #{_k + 1}")(_slot(_k))
