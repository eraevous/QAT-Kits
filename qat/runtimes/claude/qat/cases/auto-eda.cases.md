---
tool: auto-eda
spec: qat/tools/auto-eda.skill.md
version: 1.1.0
---

# auto-eda: cases

Cases for the standalone skill (CONTRIBUTING.md, "Standalone skill"). Inputs are synthetic: generate
them with the snippet in each case, never with real or employer data. Run each case against the skill
(SKILL.md plus `scripts/`) in a fresh session, save the reply as
`qat/eval-runs/<date>/auto-eda/<case id>.md` (and the HTML report beside it if small), and grade
PASS/FAIL against "Must" and "Must not".

## AE-01: Mixed-kind CSV (rules fire deterministically)

**Input:** a CSV made by

```python
import numpy as np, pandas as pd
rng = np.random.default_rng(0)
n = 500
pd.DataFrame({
    "order_id": [f"ORD-{i:04d}" for i in range(n)],
    "region": rng.choice(["N", "S", "E", "W"], n),
    "is_return": rng.choice(["yes", "no"], n, p=[0.1, 0.9]),
    "amount": rng.lognormal(3, 1, n).round(2),
    "qty": rng.integers(1, 40, n),
    "ordered_at": pd.date_range("2026-01-01", periods=n, freq="h").astype(str),
    "constant_flag": "A",
}).assign(amount=lambda d: d.amount.mask(rng.random(n) < 0.2)).to_csv("orders.csv", index=False)
```

and the message "Run auto-eda on orders.csv."

**Must:**
- Run `scripts/auto_eda.py` (not hand-written charts) and deliver the HTML report.
- Classify `order_id` as an ID (profiled, not charted) and `constant_flag` as constant (flagged, not charted).
- Mention the ~20% missingness in `amount` and its right skew, read from the JSON summary.
- Keep the reply to the 2-4 most notable findings.

**Must not:**
- Describe every chart, or state findings the JSON summary doesn't support.

Known behaviour (1.0.0, found while writing this case): an integer ID column (`range(n)`) is classified
`numeric` and charted, not `id`. The case uses string IDs so it tests the stated rule; whether integer IDs
should count as IDs is an open question for a later version.

## AE-02: Stated threshold (stated rule)

**Input:** the AE-01 file plus "Use 12 categories as the cutoff."

**Must:**
- Pass `--max-cats 12` to the script.

## AE-03: Connector output, not a file (workflow step 1)

**Input:** a JSON payload pasted in the message, shaped `{"data": [{"a": 1, "b": {"c": "x"}}, ...]}`
with 30 synthetic records, and "What's in this data?"

**Must:**
- Write the payload to a file first, then run the script on it (nested fields flattened).
- Treat the request as an EDA request even though no chart was asked for.

## AE-04: Nested JSONL (load path; added in 1.1.0)

**Input:** a JSONL file made by

```python
import json, random
random.seed(1)
with open("events.jsonl", "w") as f:
    for i in range(40):
        f.write(json.dumps({"id": f"E{i:03d}", "kind": random.choice(["view", "click"]),
                            "user": {"plan": random.choice(["free", "pro", "team"])},
                            "tags": random.sample(["a", "b", "c"], 2)}) + "\n")
```

and "Run auto-eda on events.jsonl."

**Must:**
- Produce the report (no crash). `user.plan` appears as its own flattened column, as it would from `.json`.
- Name a dominant category, or say none dominates, using the counts in the JSON summary's `stats.top`.

**Must not:**
- Rewrite the file to CSV or hand-flatten it to get around the loader.

(Under 1.0.0 this input crashed with `TypeError: unhashable type: 'dict'` before any report was written:
Codex finding 4592443369 and Copilot finding 4592762498 on #20.)
