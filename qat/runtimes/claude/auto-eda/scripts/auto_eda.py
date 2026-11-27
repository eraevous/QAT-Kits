#!/usr/bin/env python3
"""
auto_eda.py — rule-driven EDA companion file.

Profiles each column of a dataset, matches it against a registry of rules,
and writes one self-contained HTML report (charts drawn as inline SVG) plus a
JSON summary. Needs pandas; the charts need nothing beyond the standard library
(svg_charts.py, beside this file).

Usage:
    python auto_eda.py DATA_FILE [--out DIR] [--max-cats 8] [--title "..."]

DATA_FILE: .csv, .tsv, .xlsx/.xls, .json, .jsonl, or .parquet

Extending: add a function decorated with @rule(...) below, or drop a module
into scripts/plugins/ that does the same. Each rule receives (series, profile)
and returns a chart: SVG text (one <svg> element), a chart spec dict such as
{"kind": "bar", "title": ..., "labels": [...], "values": [...]} that
svg_charts.draw() renders, or None to skip.
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Union

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))  # svg_charts sits beside this file, also under python -I
import svg_charts as sc  # noqa: E402
from svg_charts import PALETTE, draw  # noqa: E402,F401  (re-exported for plugins)

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
CFG = {
    "max_cats": 8,          # <= this many distinct values -> "low-card categorical"
    "top_n": 15,            # high-card categoricals show the top N
    "id_ratio": 0.95,       # distinct/non-null above this -> treat as an ID column, skip charts
    "numeric_as_cat": True, # integer columns with <= max_cats values are charted as categories
}


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
Chart = Union[str, dict, None]   # SVG text, a chart spec for svg_charts.draw(), or None
RuleFn = Callable[[pd.Series, Profile], Chart]
RULES: list[tuple[str, Callable[[Profile], bool], RuleFn]] = []


def rule(name: str, when: Callable[[Profile], bool]):
    """Register a chart rule. `when` decides from the profile alone."""
    def deco(fn: RuleFn) -> RuleFn:
        RULES.append((name, when, fn))
        return fn
    return deco


def to_svg(chart: Chart) -> str | None:
    """The plugin contract: accept SVG text or a chart spec; refuse anything else by name."""
    if chart is None:
        return None
    if isinstance(chart, str):
        if chart.lstrip().startswith("<svg"):
            return chart
        raise TypeError("a rule returned text that is not an <svg> element")
    if isinstance(chart, dict):
        return draw(chart)
    if hasattr(chart, "savefig"):
        raise TypeError("a rule returned a matplotlib Figure; since auto-eda 2.0 rules return SVG "
                        "text or a chart spec (see SKILL.md, Adding rules)")
    raise TypeError(f"a rule returned {type(chart).__name__}; expected SVG text, a chart spec or None")


@rule("bar: category counts", lambda p: p.kind in ("low_cat", "boolean"))
def bar_low_card(s, p):
    counts = s.astype("string").fillna("(missing)").value_counts()
    return sc.bar(f"{p.name} — {p.n_unique} categories", counts.index, counts.values,
                  colors=PALETTE)


@rule("bar: top-N categories", lambda p: p.kind == "high_cat")
def bar_top_n(s, p):
    k = CFG["top_n"]
    counts = s.astype("string").value_counts()
    top = counts.head(k)
    other = counts.iloc[k:].sum()
    return sc.bar(f"{p.name} — top {len(top)} of {p.n_unique}"
                  + (f" (other: {other:,} rows)" if other else ""), top.index, top.values,
                  annotate=True, value_fmt=lambda v: f"{v:,.0f}")


@rule("histogram + box", lambda p: p.kind == "numeric")
def hist_numeric(s, p):
    x = pd.to_numeric(s, errors="coerce").dropna()
    x = x[np.isfinite(x)]
    if x.empty:
        return None
    counts, edges = np.histogram(x, bins=min(50, max(10, int(len(x) ** 0.5))))
    q1, med, q3 = x.quantile(.25), x.median(), x.quantile(.75)
    iqr = q3 - q1
    box = {"q1": q1, "median": med, "q3": q3,  # whiskers: furthest points within 1.5 IQR
           "min": x[x >= q1 - 1.5 * iqr].min(), "max": x[x <= q3 + 1.5 * iqr].max(),
           "outliers": x[(x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)].tolist()}
    return sc.histogram(f"{p.name} — median {med:,.3g}, IQR {q1:,.3g}–{q3:,.3g}",
                        counts.tolist(), edges.tolist(), box=box)


@rule("time: rows per period", lambda p: p.kind == "datetime")
def time_counts(s, p):
    t = pd.to_datetime(s, errors="coerce").dropna()
    span = (t.max() - t.min()).days
    freq = "D" if span <= 90 else "W" if span <= 730 else "M"
    counts = t.dt.to_period(freq).value_counts()
    # every period in the span, empty ones as 0, so x position is elapsed time (Codex 4670109273)
    series = counts.reindex(pd.period_range(counts.index.min(), counts.index.max(), freq=freq), fill_value=0)
    unit = {"D": "day", "W": "week", "M": "month"}[freq]
    labels = [str(per.start_time.date()) if freq != "M" else per.strftime("%Y-%m") for per in series.index]
    return sc.line(f"{p.name} — rows per {unit} ({t.min():%Y-%m-%d} → {t.max():%Y-%m-%d})",
                   labels, series.values.tolist())


# Dataset-level rules (run once on the whole frame)
FRAME_RULES: list[tuple[str, Callable[[pd.DataFrame, list[Profile]], Chart]]] = []


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
    miss.sort(key=lambda t: -t[1])
    return sc.bar("Missing values by column", [m[0] for m in miss], [m[1] for m in miss],
                  xmax=100, xlabel="% of rows missing", colors=[PALETTE[3]],
                  value_fmt=lambda v: f"{v:.1f}%")


@frame_rule("correlation heatmap")
def correlations(df, profiles):
    cols = [p.name for p in profiles if p.kind == "numeric"]
    if len(cols) < 2:
        return None
    c = df[cols].apply(pd.to_numeric, errors="coerce").corr()
    return sc.heatmap("Pearson correlation (numeric columns)", cols,
                      [[None if pd.isna(v) else float(v) for v in row] for row in c.values])

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
        name = f"auto_eda_plugin_{f.stem}"
        if name not in sys.modules:  # a second run() in one process must not register its rules twice
            spec = importlib.util.spec_from_file_location(name, f)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            sys.modules[name] = mod
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
        # Same flattening as .json: nested objects become dotted columns ("b.c"), not dict cells.
        records = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        return pd.json_normalize(records)
    if ext == ".json":
        raw = json.loads(path.read_text())
        if isinstance(raw, dict):  # {"data": [...]} or {"rows": [...]} style payloads
            for v in raw.values():
                if isinstance(v, list) and v and isinstance(v[0], dict):
                    raw = v
                    break
        return pd.json_normalize(raw)
    raise SystemExit(f"Unsupported file type: {ext}")


def make_hashable(df: pd.DataFrame) -> pd.DataFrame:
    """Turn list or dict cells (left by json_normalize, e.g. arrays) into JSON text.

    Profiling counts distinct values, which fails on unhashable cells; as text they are
    profiled like any other string column.
    """
    for col in df.columns:
        if df[col].dtype == object and df[col].map(lambda v: isinstance(v, (list, dict))).any():
            df[col] = df[col].map(lambda v: json.dumps(v, sort_keys=True, default=str)
                                  if isinstance(v, (list, dict)) else v)
    return df


def _num(v):
    """Round a statistic for the JSON summary (4 significant figures).

    NaN and infinities become None: strict JSON has no token for them, and rounding can itself
    overflow (1.7976931348623157e308 rounds to inf).
    """
    if v is None or pd.isna(v):
        return None
    rounded = float(f"{float(v):.4g}")
    return rounded if -float("inf") < rounded < float("inf") else None


def column_stats(s: pd.Series, p: Profile) -> dict:
    """The measurements behind each chart, so findings can be read from the JSON summary."""
    if p.kind == "numeric":
        x = pd.to_numeric(s, errors="coerce").dropna()
        return {"count": int(len(x)), "mean": _num(x.mean()), "std": _num(x.std()),
                "min": _num(x.min()), "p25": _num(x.quantile(.25)), "median": _num(x.median()),
                "p75": _num(x.quantile(.75)), "max": _num(x.max()), "skew": _num(x.skew())}
    if p.kind in ("low_cat", "boolean", "high_cat"):
        # Same basis as the charts: pct is of all rows, missing included. Low-cardinality and
        # boolean charts show a "(missing)" bar, so it is listed here as a value too.
        total = len(s)
        if p.kind == "high_cat":
            counts = s.astype("string").value_counts()
            k = CFG["top_n"]
        else:
            counts = s.astype("string").fillna("(missing)").value_counts()
            k = len(counts)
        top = [{"value": str(v), "count": int(c), "pct": round(100 * c / total, 1)}
               for v, c in counts.head(k).items()]
        out = {"pct_of": "all rows", "top": top}
        if len(counts) > k:
            out["other_count"] = int(counts.iloc[k:].sum())
        if p.kind == "high_cat" and p.n_null:
            out["missing_count"] = p.n_null
        return out
    if p.kind == "datetime":
        t = pd.to_datetime(s, errors="coerce").dropna()
        return {"min": str(t.min()), "max": str(t.max())} if len(t) else {}
    return {}


def correlation_pairs(df: pd.DataFrame, profiles: list[Profile], limit: int = 50) -> list[dict]:
    """Pearson r for each pair of numeric columns, strongest first (the heatmap's numbers)."""
    cols = [p.name for p in profiles if p.kind == "numeric"]
    if len(cols) < 2:
        return []
    c = df[cols].apply(pd.to_numeric, errors="coerce").corr()
    pairs = [{"a": a, "b": b, "r": _num(c.loc[a, b])}
             for i, a in enumerate(cols) for b in cols[i + 1:] if pd.notna(c.loc[a, b])]
    pairs.sort(key=lambda d: -abs(d["r"]))
    return pairs[:limit]


def run(path: Path, out: Path, title: str | None):
    plugins = load_plugins()
    df = make_hashable(load(path))
    profiles, charts, stats = [], [], {}

    for col in df.columns:
        p, s = profile_column(df[col])
        profiles.append(p)
        stats[p.name] = column_stats(s, p)
        for name, when, fn in RULES:
            if when(p):
                try:
                    svg = to_svg(fn(s, p))
                except Exception as e:  # one bad column shouldn't kill the report
                    p.notes.append(f"{name} failed: {e}")
                    continue
                if svg is not None:
                    charts.append({"column": p.name, "rule": name, "svg": svg})

    frame_charts = []
    for name, fn in FRAME_RULES:
        try:
            svg = to_svg(fn(df, profiles))
        except Exception as e:
            print(f"warning: {name} failed: {e}", file=sys.stderr)
            continue
        if svg is not None:
            frame_charts.append({"rule": name, "svg": svg})

    out.mkdir(parents=True, exist_ok=True)
    stem = path.stem
    summary = {
        "source": str(path), "rows": len(df), "columns": len(df.columns),
        "max_cats": CFG["max_cats"], "plugins": plugins,
        "kinds": {k: [p.name for p in profiles if p.kind == k]
                  for k in sorted({p.kind for p in profiles})},
        "profiles": [{**{k: v for k, v in p.__dict__.items()}, "null_pct": round(p.null_pct, 1),
                      "stats": stats[p.name]}
                     for p in profiles],
        "correlations": correlation_pairs(df, profiles),
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
    img = lambda c, cap: f"<figure>{c['svg']}<figcaption>{e(cap)}</figcaption></figure>"
    low = [c for c in charts if c["rule"].startswith("bar: category")]
    rest = [c for c in charts if c not in low]
    sec = lambda h, items: (f"<h2>{h}</h2><div class=grid>{''.join(items)}</div>" if items else "")
    return f"""<!doctype html><html><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>{e(title)}</title>
<style>
:root{{--bg:#fafaf8;--fg:#1d1d1b;--mut:#666;--line:#e3e1dc;--card:#fff;
--c0:#3b6ea8;--c1:#e07b39;--c2:#4e9a6b;--c3:#b04a5a;--c4:#7a5ea8;--c5:#c9a227;--c6:#3a9aa6;--c7:#8a8a8a;
--pos:#b2182b;--neg:#2166ac}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1b1b1a;--fg:#ecebe8;--mut:#a5a39e;--line:#3a3934;--card:#242422;
--c0:#7fa7d9;--c1:#f0a06a;--c2:#7cc49a;--c3:#e08a98;--c4:#ad97dc;--c5:#e3c35c;--c6:#6cc3cc;--c7:#b0b0b0;
--pos:#ef6f6c;--neg:#5fa2e0}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;margin:0;padding:24px 16px;max-width:1200px;margin-inline:auto}}
h1{{font-size:1.5rem;margin:0 0 4px}} h2{{font-size:1.1rem;margin:32px 0 12px;border-bottom:1px solid var(--line);padding-bottom:6px}}
.meta{{color:var(--mut)}} table{{border-collapse:collapse;width:100%;font-size:13px;display:block;overflow-x:auto}}
th,td{{text-align:left;padding:6px 10px;border-bottom:1px solid var(--line)}} td.n{{text-align:right;font-variant-numeric:tabular-nums}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,460px),1fr));gap:16px;align-items:start}}
figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px}}
figure svg{{width:100%;height:auto;display:block}} figcaption{{font-size:12px;color:var(--mut);padding-top:4px}}
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
