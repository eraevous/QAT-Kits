#!/usr/bin/env python3
"""
auto_eda.py — rule-driven EDA companion file.

Profiles each column of a dataset, matches it against a registry of rules,
and writes one self-contained HTML report (charts embedded) plus a JSON
summary.

Usage:
    python auto_eda.py DATA_FILE [--out DIR] [--max-cats 8] [--title "..."]

DATA_FILE: .csv, .tsv, .xlsx/.xls, .json, .jsonl, or .parquet

Extending: add a function decorated with @rule(...) below, or drop a module
into scripts/plugins/ that does the same. Each rule receives (series, profile)
and returns a matplotlib Figure (or None to skip).
"""
from __future__ import annotations

import argparse
import base64
import html
import importlib.util
import io
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
CFG = {
    "max_cats": 8,          # <= this many distinct values -> "low-card categorical"
    "top_n": 15,            # high-card categoricals show the top N
    "id_ratio": 0.95,       # distinct/non-null above this -> treat as an ID column, skip charts
    "numeric_as_cat": True, # integer columns with <= max_cats values are charted as categories
}

PALETTE = ["#3b6ea8", "#e07b39", "#4e9a6b", "#b04a5a", "#7a5ea8",
           "#c9a227", "#3a9aa6", "#8a8a8a"]

# --------------------------------------------------------------------------
# Profiling
# --------------------------------------------------------------------------
@dataclass
class Profile:
    name: str
    dtype: str
    kind: str               # low_cat | high_cat | numeric | datetime | boolean | id | text | constant | empty
    n: int
    n_null: int
    n_unique: int
    notes: list[str] = field(default_factory=list)

    @property
    def null_pct(self) -> float:
        return 100 * self.n_null / self.n if self.n else 0.0


def _try_datetime(s: pd.Series) -> pd.Series | None:
    if not (s.dtype == object or pd.api.types.is_string_dtype(s)):
        return None
    sample = s.dropna().astype(str).head(200)
    if sample.empty or sample.str.len().median() < 6:
        return None
    parsed = pd.to_datetime(sample, errors="coerce", format="mixed")
    if parsed.notna().mean() > 0.9:
        return pd.to_datetime(s, errors="coerce", format="mixed")
    return None


def profile_column(s: pd.Series) -> tuple[Profile, pd.Series]:
    n, n_null = len(s), int(s.isna().sum())
    nn = s.dropna()
    n_unique = int(nn.nunique())
    p = Profile(s.name, str(s.dtype), "", n, n_null, n_unique)

    if nn.empty:
        p.kind = "empty"
        return p, s
    if n_unique == 1:
        p.kind = "constant"
        p.notes.append(f"single value: {str(nn.iloc[0])[:60]!r}")
        return p, s
    dt = _try_datetime(s)
    if dt is not None:
        p.kind, p.dtype = "datetime", "datetime (parsed)"
        return p, dt
    if pd.api.types.is_datetime64_any_dtype(s):
        p.kind = "datetime"
    elif pd.api.types.is_bool_dtype(s) or n_unique == 2 and set(map(str, nn.unique())) <= {"0", "1", "True", "False", "true", "false", "Y", "N", "yes", "no"}:
        p.kind = "boolean"
    elif pd.api.types.is_numeric_dtype(s):
        if CFG["numeric_as_cat"] and pd.api.types.is_integer_dtype(s) and n_unique <= CFG["max_cats"]:
            p.kind = "low_cat"
            p.notes.append("integer with few values; charted as categories")
        else:
            p.kind = "numeric"
    elif n_unique <= CFG["max_cats"]:
        p.kind = "low_cat"
    elif n_unique / len(nn) > CFG["id_ratio"]:
        avg_len = nn.astype(str).str.len().mean()
        p.kind = "text" if avg_len > 40 else "id"
    else:
        p.kind = "high_cat"
    return p, s

# --------------------------------------------------------------------------
# Rule registry
# --------------------------------------------------------------------------
RuleFn = Callable[[pd.Series, Profile], "plt.Figure | None"]
RULES: list[tuple[str, Callable[[Profile], bool], RuleFn]] = []


def rule(name: str, when: Callable[[Profile], bool]):
    """Register a chart rule. `when` decides from the profile alone."""
    def deco(fn: RuleFn) -> RuleFn:
        RULES.append((name, when, fn))
        return fn
    return deco


def _fig(w=6.4, h=3.6):
    fig, ax = plt.subplots(figsize=(w, h), dpi=110)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(colors="#444")
    return fig, ax


@rule("bar: category counts", lambda p: p.kind in ("low_cat", "boolean"))
def bar_low_card(s, p):
    counts = s.astype("string").fillna("(missing)").value_counts()
    fig, ax = _fig(6.4, 0.45 * len(counts) + 1.2)
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(counts))]
    bars = ax.barh(counts.index[::-1], counts.values[::-1], color=colors[::-1])
    total = counts.sum()
    for b, v in zip(bars, counts.values[::-1]):
        ax.text(b.get_width(), b.get_y() + b.get_height() / 2,
                f" {v:,} ({100*v/total:.0f}%)", va="center", fontsize=9, color="#333")
    ax.set_xlim(0, counts.max() * 1.25)
    ax.set_title(f"{p.name} — {p.n_unique} categories", loc="left", fontsize=11)
    return fig


@rule("bar: top-N categories", lambda p: p.kind == "high_cat")
def bar_top_n(s, p):
    k = CFG["top_n"]
    counts = s.astype("string").value_counts()
    top = counts.head(k)
    other = counts.iloc[k:].sum()
    fig, ax = _fig(6.4, 0.32 * len(top) + 1.4)
    ax.barh(top.index[::-1], top.values[::-1], color=PALETTE[0])
    ax.set_title(f"{p.name} — top {len(top)} of {p.n_unique}"
                 + (f" (other: {other:,} rows)" if other else ""), loc="left", fontsize=11)
    return fig


@rule("histogram + box", lambda p: p.kind == "numeric")
def hist_numeric(s, p):
    x = pd.to_numeric(s, errors="coerce").dropna()
    fig, (ax_b, ax_h) = plt.subplots(2, 1, figsize=(6.4, 3.8), dpi=110,
                                     sharex=True, gridspec_kw={"height_ratios": [1, 4]})
    ax_b.boxplot(x, orientation="horizontal", widths=0.6, patch_artist=True,
                 boxprops=dict(facecolor="#dbe6f2", color=PALETTE[0]),
                 medianprops=dict(color=PALETTE[1]), flierprops=dict(markersize=3))
    ax_b.axis("off")
    ax_h.hist(x, bins=min(50, max(10, int(len(x) ** 0.5))), color=PALETTE[0], alpha=0.85)
    for side in ("top", "right"):
        ax_h.spines[side].set_visible(False)
    ax_b.set_title(f"{p.name} — median {x.median():,.3g}, IQR {x.quantile(.25):,.3g}–{x.quantile(.75):,.3g}",
                   loc="left", fontsize=11)
    return fig


@rule("time: rows per period", lambda p: p.kind == "datetime")
def time_counts(s, p):
    t = pd.to_datetime(s, errors="coerce").dropna()
    span = (t.max() - t.min()).days
    freq = "D" if span <= 90 else "W" if span <= 730 else "MS"
    series = t.dt.to_period({"D": "D", "W": "W", "MS": "M"}[freq]).value_counts().sort_index()
    fig, ax = _fig()
    ax.plot(series.index.to_timestamp(), series.values, color=PALETTE[0], lw=1.6)
    ax.set_title(f"{p.name} — rows per {'day' if freq=='D' else 'week' if freq=='W' else 'month'}"
                 f" ({t.min():%Y-%m-%d} → {t.max():%Y-%m-%d})", loc="left", fontsize=11)
    fig.autofmt_xdate()
    return fig


# Dataset-level rules (run once on the whole frame)
FRAME_RULES: list[tuple[str, Callable[[pd.DataFrame, list[Profile]], "plt.Figure | None"]]] = []


def frame_rule(name: str):
    def deco(fn):
        FRAME_RULES.append((name, fn))
        return fn
    return deco


@frame_rule("missingness by column")
def missingness(df, profiles):
    miss = [(p.name, p.null_pct) for p in profiles if p.n_null]
    if not miss:
        return None
    miss.sort(key=lambda t: t[1])
    fig, ax = _fig(6.4, 0.32 * len(miss) + 1.2)
    ax.barh([m[0] for m in miss], [m[1] for m in miss], color=PALETTE[3])
    ax.set_xlim(0, 100)
    ax.set_xlabel("% missing")
    ax.set_title("Missing values by column", loc="left", fontsize=11)
    return fig


@frame_rule("correlation heatmap")
def correlations(df, profiles):
    cols = [p.name for p in profiles if p.kind == "numeric"]
    if len(cols) < 2:
        return None
    c = df[cols].apply(pd.to_numeric, errors="coerce").corr()
    k = len(cols)
    fig, ax = plt.subplots(figsize=(min(1 + 0.55 * k, 9), min(0.8 + 0.5 * k, 8)), dpi=110)
    im = ax.imshow(c.values, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(k), cols, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(k), cols, fontsize=8)
    if k <= 12:
        for i in range(k):
            for j in range(k):
                ax.text(j, i, f"{c.values[i, j]:.2f}", ha="center", va="center", fontsize=7,
                        color="white" if abs(c.values[i, j]) > 0.6 else "#222")
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title("Pearson correlation (numeric columns)", loc="left", fontsize=11)
    return fig

# --------------------------------------------------------------------------
# Plugins: scripts/plugins/*.py can import this module and call @rule/@frame_rule
# --------------------------------------------------------------------------
def load_plugins():
    pdir = Path(__file__).parent / "plugins"
    if not pdir.is_dir():
        return []
    loaded = []
    sys.modules.setdefault("auto_eda", sys.modules[__name__])
    for f in sorted(pdir.glob("*.py")):
        if f.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(f"auto_eda_plugin_{f.stem}", f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        loaded.append(f.stem)
    return loaded

# --------------------------------------------------------------------------
# I/O and report
# --------------------------------------------------------------------------
def load(path: Path) -> pd.DataFrame:
    ext = path.suffix.lower()
    if ext == ".csv":
        return pd.read_csv(path)
    if ext in (".tsv", ".tab"):
        return pd.read_csv(path, sep="\t")
    if ext in (".xlsx", ".xls", ".xlsm"):
        return pd.read_excel(path)
    if ext == ".parquet":
        return pd.read_parquet(path)
    if ext == ".jsonl":
        return pd.read_json(path, lines=True)
    if ext == ".json":
        raw = json.loads(path.read_text())
        if isinstance(raw, dict):  # {"data": [...]} or {"rows": [...]} style payloads
            for v in raw.values():
                if isinstance(v, list) and v and isinstance(v[0], dict):
                    raw = v
                    break
        return pd.json_normalize(raw)
    raise SystemExit(f"Unsupported file type: {ext}")


def fig_to_b64(fig) -> str:
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def run(path: Path, out: Path, title: str | None):
    plugins = load_plugins()
    df = load(path)
    profiles, charts = [], []

    for col in df.columns:
        p, s = profile_column(df[col])
        profiles.append(p)
        for name, when, fn in RULES:
            if when(p):
                try:
                    fig = fn(s, p)
                except Exception as e:  # one bad column shouldn't kill the report
                    p.notes.append(f"{name} failed: {e}")
                    continue
                if fig is not None:
                    charts.append({"column": p.name, "rule": name, "png": fig_to_b64(fig)})

    frame_charts = []
    for name, fn in FRAME_RULES:
        try:
            fig = fn(df, profiles)
        except Exception as e:
            print(f"warning: {name} failed: {e}", file=sys.stderr)
            continue
        if fig is not None:
            frame_charts.append({"rule": name, "png": fig_to_b64(fig)})

    out.mkdir(parents=True, exist_ok=True)
    stem = path.stem
    summary = {
        "source": str(path), "rows": len(df), "columns": len(df.columns),
        "max_cats": CFG["max_cats"], "plugins": plugins,
        "kinds": {k: [p.name for p in profiles if p.kind == k]
                  for k in sorted({p.kind for p in profiles})},
        "profiles": [{**{k: v for k, v in p.__dict__.items()}, "null_pct": round(p.null_pct, 1)}
                     for p in profiles],
        "charts": [{"column": c["column"], "rule": c["rule"]} for c in charts]
                  + [{"column": None, "rule": c["rule"]} for c in frame_charts],
    }
    (out / f"{stem}_eda.json").write_text(json.dumps(summary, indent=2, default=str))
    (out / f"{stem}_eda.html").write_text(render_html(title or f"EDA — {path.name}", df, profiles,
                                                      charts, frame_charts, plugins))
    print(json.dumps({"html": str(out / f"{stem}_eda.html"),
                      "json": str(out / f"{stem}_eda.json"),
                      "rows": len(df), "columns": len(df.columns),
                      "charts": len(charts) + len(frame_charts),
                      "kinds": {k: len(v) for k, v in summary["kinds"].items()}}, indent=2))


def render_html(title, df, profiles, charts, frame_charts, plugins) -> str:
    e = html.escape
    rows = "".join(
        f"<tr><td>{e(str(p.name))}</td><td>{e(p.kind)}</td><td>{e(p.dtype)}</td>"
        f"<td class=n>{p.n_unique:,}</td><td class=n>{p.null_pct:.1f}%</td>"
        f"<td>{e('; '.join(p.notes))}</td></tr>" for p in profiles)
    img = lambda c, cap: (f"<figure><img alt='{e(cap)}' src='data:image/png;base64,{c['png']}'>"
                          f"<figcaption>{e(cap)}</figcaption></figure>")
    low = [c for c in charts if c["rule"].startswith("bar: category")]
    rest = [c for c in charts if c not in low]
    sec = lambda h, items: (f"<h2>{h}</h2><div class=grid>{''.join(items)}</div>" if items else "")
    return f"""<!doctype html><html><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>{e(title)}</title>
<style>
:root{{--bg:#fafaf8;--fg:#1d1d1b;--mut:#666;--line:#e3e1dc;--card:#fff}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1b1b1a;--fg:#ecebe8;--mut:#a5a39e;--line:#34332f;--card:#f6f5f2}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;margin:0;padding:24px 16px;max-width:1200px;margin-inline:auto}}
h1{{font-size:1.5rem;margin:0 0 4px}} h2{{font-size:1.1rem;margin:32px 0 12px;border-bottom:1px solid var(--line);padding-bottom:6px}}
.meta{{color:var(--mut)}} table{{border-collapse:collapse;width:100%;font-size:13px;display:block;overflow-x:auto}}
th,td{{text-align:left;padding:6px 10px;border-bottom:1px solid var(--line)}} td.n{{text-align:right;font-variant-numeric:tabular-nums}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,460px),1fr));gap:16px}}
figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px}}
figure img{{width:100%;height:auto;display:block}} figcaption{{font-size:12px;color:#777;padding-top:4px}}
</style></head><body>
<h1>{e(title)}</h1>
<p class=meta>{len(df):,} rows × {len(df.columns)} columns · low-cardinality threshold ≤ {CFG['max_cats']}
{(' · plugins: ' + e(', '.join(plugins))) if plugins else ''}</p>
<h2>Column profile</h2>
<table><thead><tr><th>Column</th><th>Kind</th><th>dtype</th><th>Distinct</th><th>Missing</th><th>Notes</th></tr></thead>
<tbody>{rows}</tbody></table>
{sec(f"Categorical (≤ {CFG['max_cats']} levels)", [img(c, f"{c['column']} · {c['rule']}") for c in low])}
{sec("Other columns", [img(c, f"{c['column']} · {c['rule']}") for c in rest])}
{sec("Dataset-level", [img(c, c['rule']) for c in frame_charts])}
</body></html>"""


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data")
    ap.add_argument("--out", default="eda_out")
    ap.add_argument("--max-cats", type=int, default=CFG["max_cats"])
    ap.add_argument("--top-n", type=int, default=CFG["top_n"])
    ap.add_argument("--title")
    a = ap.parse_args()
    CFG["max_cats"], CFG["top_n"] = a.max_cats, a.top_n
    run(Path(a.data), Path(a.out), a.title)
