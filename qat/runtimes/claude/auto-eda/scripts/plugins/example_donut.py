"""
Example plugin: shows how to port a function from your own viz repo.

Pattern: import the registry from auto_eda, wrap your existing plotting
function so it takes (series, profile) and returns a matplotlib Figure,
and register it with a condition on the column profile.

Profile fields available: name, dtype, kind, n, n_null, n_unique, null_pct, notes
kind is one of: low_cat, high_cat, numeric, datetime, boolean, id, text, constant, empty
"""
import matplotlib.pyplot as plt
from auto_eda import rule, PALETTE


@rule("donut: share of total", lambda p: p.kind == "low_cat" and p.n_unique <= 5)
def donut(s, p):
    counts = s.astype("string").fillna("(missing)").value_counts()
    fig, ax = plt.subplots(figsize=(4.2, 4.2), dpi=110)
    ax.pie(counts.values, labels=counts.index, colors=PALETTE[:len(counts)],
           autopct="%1.0f%%", pctdistance=0.78, startangle=90, counterclock=False,
           wedgeprops=dict(width=0.38, edgecolor="white"), textprops=dict(fontsize=9))
    ax.set_title(f"{p.name} — share", loc="left", fontsize=11)
    return fig
