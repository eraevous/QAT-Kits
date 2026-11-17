# QAT-Kits

Lightweight tools that can be invoked as, or by, chat threads, kept provider-neutral: one source per tool, with installations for Claude and ChatGPT at a minimum, and more platforms as they turn up.

> **Status: proposed remit, provisional.** This README states the remit Zach set on 2026-11-16 (quoted below, relayed by Abigail). The purpose record that carries it (`P0@3` in `.aec/records.jsonl`) stays provisional until Zach commits it. Where this file and an accepted record disagree, the record wins.

Zach's words (Slack #kairos, 2026-11-16 16:17 CT, relayed verbatim by Abigail):

> "For QAT Kit, I am amending the directions. New instructions are that repository and those tools are for any lightweight tools that can be invoked as or by chat threads. It should also be as provider-agnostic as possible. That includes installations into Claude and into ChatGPT at a minimum, preferably also additional common platforms as we find them. This is replacing the directive that the QAT Kit is only for thread and chat tools. That means, that means things like AutoEDA, MTG Deck Lab, and others are joining into QAT Kit."

## What belongs here

- **In:** a tool that a chat thread can run itself (a prompt tool such as StressTest or ThreadMap), or that a thread can call (a small script a thread runs, such as AutoEDA's report generator or ThreadSeed's index helper).
- **Out:** general development tooling and Python packages that stand on their own. Those follow Zach's standing rule (Telosmith-instantiated). Where the line falls between the two is open: see [docs/remit/FOR_ZACH.md](docs/remit/FOR_ZACH.md).
- **Unchanged:** each tool stays optional (DEC-193). Nothing here requires another Kairos repository, and nothing outside requires these tools.

## Where things are

| What | Where |
|---|---|
| Tool sources (edit these) | `qat/tools/<name>.skill.md` (standalone skill), `qat/tools/<name>.qat.md` (runner contract), `qat/tools/<name>.files/` (bundled scripts) |
| Eval cases and recorded runs | `qat/cases/`, `qat/eval-runs/` |
| Runner (contracts, chaining, evals) | `qat/scripts/qat.py`; index in `qat/INDEX.md` |
| Claude installation (generated) | `qat/runtimes/claude/` and its [README](qat/runtimes/claude/README.md) |
| ChatGPT installation (hand-adapted today) | `qat/runtimes/chatgpt/` |
| Inventory of tools joining under the new remit | [docs/remit/INVENTORY.md](docs/remit/INVENTORY.md) |
| Proposed provider-neutral tool contract | [docs/remit/TOOL_CONTRACT.proposal.md](docs/remit/TOOL_CONTRACT.proposal.md) |
| Roadmap | [docs/remit/ROADMAP.md](docs/remit/ROADMAP.md) |
| History (do not edit to reconcile) | `Toolkits/`, `QAT-Kit_Architecture/`, `docs/DRIFT_INVENTORY_2026-11-04.md` |

## Working rules

[AGENTS.md](AGENTS.md) for agents, [CONTRIBUTING.md](CONTRIBUTING.md) for spec changes (eval-gated, DEC-193). Kate reviews first, then a fresh-context execution review; Zach merges.
