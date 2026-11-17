# Proposal: one provider-neutral tool contract

Author: claude:qat#01GZK2Knb8aP6VTtZ7bf5tRv · Reviewer: Abigail (review of #22 at `4c1b794`, relayed), API Kate (ask b46ce5353e2f; handoff only, not these files) · model=claude-opus-5-5 · Handoff: HO-QAT-20261116-Y0HJ
Status: **proposed**. Nothing here is adopted. It changes no spec, runner or generator yet. The remit it serves is authorized (Zach, 2026-11-16); this contract is one proposed way to implement it.
Revised 2026-11-17 after Abigail's review of #22 at `4c1b794` (relayed) and API Kate's reply (ask b46ce5353e2f): contract authority (§1), judged checks (§2), the ChatGPT skill target and four evidence tiers (§3).

## Problem

Today a tool has up to four texts: a Claude skill source (`*.skill.md`), a runner contract (`*.qat.md`), a hand-adapted ChatGPT paste block or skill (`runtimes/chatgpt/`), and, for stress-test and truth-weight, a second standalone text that has drifted from the contract (AGENTS.md "Open"). Only the Claude side is generated and checked. ChatGPT copies are hand-made, so fixes land in one place and not the other: the ThreadSeed fixes exist only in the ChatGPT copy today (INVENTORY §2).

## Proposal in one line

One source per tool, written provider-neutral, plus a short per-runtime adapter block; a generator emits every runtime from it; and an installation counts as working only after an observed smoke test, recorded.

## 1. Spec format

One file per tool, `qat/tools/<name>.tool.md` (new suffix, so nothing existing changes meaning). YAML frontmatter, then the text.

```yaml
name: thread-seed                # kebab-case, unique
version: 1.3.0                   # semver; bump rule as qat/runtimes/claude/README.md
kind: prompt | prompt+script     # prompt tools carry no files; prompt+script tools bundle files/
description: >                   # one paragraph, trigger-oriented, provider-neutral
inputs:                          # same field vocabulary as *.qat.md today
  source: {type: text, required: true}
outputs:                         # named sections the output must have
  seed: {type: text}
files: files/                    # optional; scripts and tables, standard-library Python preferred
requires:                        # what the host must offer; adapters map these
  - python3                      # optional capabilities: python3, file_out, browser, web
runtimes:                        # which adapters to build; absent = all
  - claude-skill
  - chatgpt-gpt
```

Body rules:
- **Neutral core.** No provider tool names (`SendUserFile`, `Code Interpreter`, `pip --break-system-packages`). Say what must happen ("deliver the HTML to the user") and let the adapter say how.
- **Adapter blocks.** Optional `## Runtime: claude-skill`, `## Runtime: chatgpt-gpt`, … sections carry the provider-specific steps. The generator keeps the matching block and drops the others.
- **Limits stay in the core** (for example SSD's "relay classification isn't proof of authorship", MTG Deck Lab's "no executable simulator").

**Which file is authoritative for what (one owner per field, no duplicates).**
- `*.qat.md` is the **only** authority for a tool's machine-checkable contract: typed inputs, outputs, handoffs, and the eval cases that point at it. It stays as it is.
- `*.tool.md` is the authority for the instruction text, the runtime adapter blocks, `kind`, `requires` and `runtimes`. When a tool has a contract, its `.tool.md` names it (`contract: <name>.qat.md`) and **omits** `inputs:`/`outputs:`; the generator reads them from the contract. A `.tool.md` declares `inputs:`/`outputs:` only when no contract exists. `skills.py check` would refuse a `.tool.md` that both names a contract and declares fields.
- Stress-test and truth-weight keep their open two-text question (AGENTS.md "Open"); this rule doesn't settle it, it only stops a third copy forming.

## 2. Inputs, outputs and evals

- **Inputs and outputs:** the same typed fields the runner already validates (`text`, `claims`, `verdict`, `scorecard` …). A tool without a contract still names its output sections so a case can check them.
- **Cases:** `qat/cases/<name>.cases.md` (or `.eval.yaml` for contract tools), unchanged, but each case says which runtimes it applies to (default: all).
- **Eval gate (DEC-193, unchanged):** a spec change bumps the version and records a run. New: the run names the runtime it ran on (`eval-runs/<date>/<name>/<runtime>/`). A change to the neutral core needs a run on at least one runtime; a change to one adapter needs a run on that runtime.
- **Runner exit codes (proposed with this contract):** `0` every deterministic check ran and passed, `1` errors, `2` usage, `3` incomplete (any case SKIP). Today a run with every output missing exits 0 (INVENTORY §2).
- **Judged checks aren't graded by the runner.** Today `qat.py eval` prints the `judge:` criteria under "Needs model judgment" and records no judgment (`run_eval`, the `judge` list). So exit `0` means "deterministic checks passed", never "fully graded eval". Proposed: a run with judged checks reports `deterministic: pass, judged: N ungraded` and stays `3` (incomplete) unless a judgments file is supplied (`--judgments <file>`: case id, check, PASS/FAIL, one-line reason, grader, and whether the grader is the output's author). A recorded run under `eval-runs/` says which of the two it is.

## 3. Packaging and installation targets

### Evidence tiers (kept separate; a higher tier never stands in for a lower one, or the reverse)

| Tier | Means | Doesn't mean |
|---|---|---|
| **installed / discoverable** | the runtime lists the artifact, and its identity is checked against `skills.lock.json` by **hash** (file bytes, or the source hash in the generated header read from the installed file) | that it runs. A version or name the model reports about itself is **not** hash verification |
| **invoked** | in a fresh thread, the runtime actually loaded and used the installed artifact (its trigger fired, or it was called by name) | that the output was right |
| **smoke-tested** | one named case ran on the installed artifact and its stated behaviour was observed | model quality or full correctness |
| **evaluated** | the tool's eval cases ran on that runtime and the run is recorded under `eval-runs/` (deterministic and judged parts reported separately, §2) | that other runtimes or versions behave the same |

### Targets

| Runtime | Artifact the generator emits | How it is installed | Checks per tier |
|---|---|---|---|
| `claude-skill` | `<name>/SKILL.md` (+ files), per-skill zip and the `qat-kit-<v>.zip` plugin; already built by `skills.py` | Upload in the Claude app (Skills / plugins); Claude Code: copy into `.claude/skills/` | installed: listed, and the installed file's hash or header source hash matches the lock · invoked: fires in a fresh session · smoke: one case · evaluated: eval run on Claude |
| `chatgpt-skill` | `<name>.chatgpt/` skill folder (SKILL-style instructions + files) | ChatGPT personal skills. **An installation already exists**: Abigail installed the ported tools as personal skills (relayed with the port findings; this lane hasn't observed it). Record it as `installed` with her evidence; invocation and behaviour are separate rows still to be observed | as for Claude, on ChatGPT |
| `chatgpt-gpt` | `<name>.chatgpt/instructions.md` (≤ the GPT instructions limit), `knowledge/` files, and for `prompt+script` tools the scripts to attach for code execution | Create or update a custom GPT (or a Project's instructions + files) by hand | installed: the GPT's files hash-match the lock (not "it states its version") · invoked · smoke: for script tools, the script runs and produces the declared files · evaluated |
| `paste` (any chat) | `<name>.paste.md`: one block for pasting into any chat, prompt tools only | Paste at the top of a thread | smoke and evaluated only (nothing is installed) |
| later: `codex`, `gemini-gem`, `mcp-prompt` | added when one is needed | — | same four tiers |

**Two different gaps, named separately.** For ChatGPT today: (a) there is **no upstream generator**: the ChatGPT texts are hand-adapted copies, so fixes drift (contract steps 3-4 fix this); (b) a **runtime capability** may be missing on the ChatGPT side for a given tool (for example a Parquet engine for AutoEDA, or file delivery). (a) is ours to build; (b) is recorded per tool as an untested or unsupported capability, not as a generator gap.

### Test receipts

A tier is claimed only with a line in `qat/installs/<runtime>.jsonl`. These are **test receipts**, not Zach's verification or acceptance. Fields (API Kate's list, adopted into the proposal):
- tool, version, source commit, installed artifact identity (hash), runtime and model, installation method;
- tier, test case, expected result, observed result, status (`pass` / `fail` / `blocked`);
- timestamp, observing actor, evidence pointer (kept private if not public-safe), untested capabilities.

Failed and blocked attempts are recorded too. No credentials or personal data in a receipt. No receipt, no claim: generation, packaging or a passing CLI test doesn't count (the 15 synthetic CLI checks in the ChatGPT port were exactly that: useful, not an installation proof).

## 4. Migration (proposed order, each its own PR)

1. Add the runner's `incomplete` exit code with a regression test (small, independent); report ungraded judged checks as incomplete (§2).
2. Fix ThreadSeed's `verify()` defects upstream with the three regression cases (spec change, eval-gated).
3. Add `.tool.md` support to `skills.py` beside `.skill.md`, emitting the existing Claude output byte-for-byte for a tool with no adapter blocks (so the bundle doesn't change).
4. Add the `chatgpt-skill`, `chatgpt-gpt` and `paste` emitters; regenerate `kind-check` and `real-problem` ChatGPT texts from source and retire the hand-adapted copies.
5. Convert tools one at a time (auto-eda first: it has the clearest provider-specific step), each with its eval run and test receipts per runtime and tier.

What does **not** change: DEC-193 optionality, the eval gate, the review order (Kate first, then a fresh-context execution review, then Zach merges), and the stress-test/truth-weight text question (still Zach's call).

## Risks (stress-tested by hand)

- *A neutral core reads worse on both providers than a tuned text.* Mitigation: adapter blocks may hold more than delivery steps; the eval runs per runtime show the cost.
- *Observed installs are manual and will lag.* That's the point: the record says what has been seen, not what should work. A stale record is visible, a false claim isn't.
- *Another generator target is more machinery than tools.* AGENTS.md Drift trigger. Step 3 is gated on byte-identical Claude output so the machinery adds no behaviour change; if steps 3-4 grow past one PR each, stop and ask.

QAT: stress-test (installed skill, 2026-10-15 upload): not run as a separate session in this wake; the three risks above are a by-hand pass in its frame (assumptions, backfire, the tweak). Same-family only; Kate review requested.
