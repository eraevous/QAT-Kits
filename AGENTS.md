# AGENTS.md: working rules for coding agents in this repo

These rules apply to Claude Code, Codex or any other coding agent.

- **No copy of a QAT tool is canonical yet** (DEC-048 / DEC-051 in the relay-kit-private ledger;
  [docs/DRIFT_INVENTORY_2026-11-04.md](docs/DRIFT_INVENTORY_2026-11-04.md)). Do not declare or treat one as
  canonical, and do not edit a tool copy to "reconcile" it, until Zach decides.
- `qat/` holds a byte-for-byte copy of the runner and two specs ([qat/PROVENANCE.md](qat/PROVENANCE.md)).
  Run from `qat/` (needs `pyyaml` and `jsonschema`): `python3 -I scripts/qat.py index` and
  `python3 -I scripts/qat.py eval cases/<tool>.eval.yaml <output dir>`.

## Records and ledgers

Two places hold reasons, and they do different jobs:

- **Records** (`.aec/records.jsonl`, [Telosmith](https://github.com/eraevous/Telosmith)) are the design truth
  inside this repo: its purpose (`P0`), the requirements behind the spec/contract machinery and the code that
  implements them (`implemented_by code:qat.scripts.qat...`). A record is provisional until Zach commits it
  (`"epistemic": "committed"`); agents may append provisional records and proposed decisions, never accepted ones.
- **Ledgers** (the relay-kit-private repository, `governance/decisions.jsonl` and `challenges.jsonl`) hold
  cross-repo coordination and the owner's decisions. Records cite their ids as text (for example
  `QAT-D-canon` cites DEC-048 and DEC-051).
- **Append only.** Never edit or delete an earlier line in `.aec/records.jsonl`. To change a record, append
  the same `id` with the next `version` and a `supersedes` relation.

After editing code, the Claude Code hook in `.claude/settings.json` runs `aec check` and `aec code-impact`
(it needs Telosmith installed at the commit pinned in `.github/workflows/telosmith.yml`; without it the hook
reports that and does not block). `[stale]` / `[needs_review]` means your change touched code a record relies
on; say in your summary whether the record still holds. The `telosmith` CI job runs the same check on every
pull request.
