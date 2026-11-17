# Proposal: one provider-neutral tool contract

Author: claude:qat#01GZK2Knb8aP6VTtZ7bf5tRv · Reviewer: none yet · model=claude-opus-5-5 · Handoff: HO-QAT-20261116-Y0HJ
Status: **proposed**. Nothing here is adopted. It changes no spec, runner or generator yet.

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

`*.qat.md` runner contracts stay as they are: they are the machine-checkable output shape. A `.tool.md` may point at its contract (`contract: <name>.qat.md`) so the runner can audit any runtime's output the same way.

## 2. Inputs, outputs and evals

- **Inputs and outputs:** the same typed fields the runner already validates (`text`, `claims`, `verdict`, `scorecard` …). A tool without a contract still names its output sections so a case can check them.
- **Cases:** `qat/cases/<name>.cases.md` (or `.eval.yaml` for contract tools), unchanged, but each case says which runtimes it applies to (default: all).
- **Eval gate (DEC-193, unchanged):** a spec change bumps the version and records a run. New: the run names the runtime it ran on (`eval-runs/<date>/<name>/<runtime>/`). A change to the neutral core needs a run on at least one runtime; a change to one adapter needs a run on that runtime.
- **Runner exit codes (proposed with this contract):** `0` all cases graded, `1` errors, `2` usage, `3` incomplete (any case SKIP). Today a run with every output missing exits 0 (INVENTORY §2).

## 3. Packaging and installation targets

| Runtime | Artifact the generator emits | How it is installed | Acceptance check (observed, recorded) |
|---|---|---|---|
| `claude-skill` | `<name>/SKILL.md` (+ files), per-skill zip and the `qat-kit-<v>.zip` plugin; already built by `skills.py` | Upload in the Claude app (Skills / plugins); Claude Code: copy into `.claude/skills/` | In a fresh Claude session: the skill is listed; its first body line shows the version and source hash matching `skills.lock.json`; one smoke case runs and passes its stated behaviour |
| `chatgpt-gpt` | `<name>.chatgpt/instructions.md` (≤ the GPT instructions limit), `knowledge/` files, and for `prompt+script` tools the script files to attach for Code Interpreter | Create or update a custom GPT (or a Project's instructions + files) by hand | In a fresh ChatGPT thread with that GPT: it states the tool name and version when asked; one smoke case passes; for script tools, the script runs in Code Interpreter and produces the declared files |
| `paste` (any chat) | `<name>.paste.md`: one block for pasting into any chat, prompt tools only | Paste at the top of a thread | One smoke case in a fresh thread of the target app |
| later: `codex`, `gemini-gem`, `mcp-prompt` | added when one is needed | — | same pattern: listed, version visible, one smoke case |

**"Working" means observed.** An installation is recorded as working only with a line in `qat/installs/<runtime>.jsonl`: tool, version, source hash, runtime, date, who observed it, the smoke case id and its result, and a pointer to the evidence (transcript or screenshot, kept private if it isn't public-safe). No line, no claim. Generation, packaging or a passing CLI test doesn't count (the 15 synthetic CLI checks in the ChatGPT port were exactly that: useful, not an installation proof).

## 4. Migration (proposed order, each its own PR)

1. Add the runner's `incomplete` exit code with a regression test (small, independent).
2. Fix ThreadSeed's `verify()` defects upstream with the three regression cases (spec change, eval-gated).
3. Add `.tool.md` support to `skills.py` beside `.skill.md`, emitting the existing Claude output byte-for-byte for a tool with no adapter blocks (so the bundle doesn't change).
4. Add the `chatgpt-gpt` and `paste` emitters; regenerate `kind-check` and `real-problem` ChatGPT texts from source and retire the hand-adapted copies.
5. Convert tools one at a time (auto-eda first: it has the clearest provider-specific step), each with its eval run and an observed install line per runtime.

What does **not** change: DEC-193 optionality, the eval gate, the review order (Kate first, then a fresh-context execution review, then Zach merges), and the stress-test/truth-weight text question (still Zach's call).

## Risks (stress-tested by hand)

- *A neutral core reads worse on both providers than a tuned text.* Mitigation: adapter blocks may hold more than delivery steps; the eval runs per runtime show the cost.
- *Observed installs are manual and will lag.* That's the point: the record says what has been seen, not what should work. A stale record is visible, a false claim isn't.
- *Another generator target is more machinery than tools.* AGENTS.md Drift trigger. Step 3 is gated on byte-identical Claude output so the machinery adds no behaviour change; if steps 3-4 grow past one PR each, stop and ask.

QAT: stress-test (installed skill, 2026-10-15 upload): not run as a separate session in this wake; the three risks above are a by-hand pass in its frame (assumptions, backfire, the tweak). Same-family only; Kate review requested.
