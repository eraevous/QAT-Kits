# QAT-Kits

Lightweight tools that can be invoked as, or by, chat threads, kept provider-neutral: one source per tool, with installations for Claude and ChatGPT at a minimum, and more platforms as they turn up.

QAT-Kits is one repository of Kairos, Zach Rhodes's umbrella project for Cognitive Augmentation: the tools, the coordination environment and the research. Decisions cited as `DEC-n` are Kairos's decision records (in the style of Architecture Decision Records), kept in a separate records repository; the README quotes what each one says where it matters.

> **Status: remit authorized; wording and implementation provisional.** Zach set this remit on 2026-11-16 (quoted below, relayed verbatim by Abigail), and it replaces the earlier "only for thread and chat tools" rule. That retired rule takes precedence nowhere, including in older handoffs, prompts and roadmaps that still quote it. What stays provisional is the purpose record's wording (`P0@3` in `.aec/records.jsonl`, until Zach commits it) and everything under [docs/remit/](docs/remit/), which is proposals.

Zach's words (Slack #kairos, 2026-11-16 16:17 CT, relayed verbatim by Abigail):

> "For QAT Kit, I am amending the directions. New instructions are that repository and those tools are for any lightweight tools that can be invoked as or by chat threads. It should also be as provider-agnostic as possible. That includes installations into Claude and into ChatGPT at a minimum, preferably also additional common platforms as we find them. This is replacing the directive that the QAT Kit is only for thread and chat tools. That means, that means things like AutoEDA, MTG Deck Lab, and others are joining into QAT Kit."

## What belongs here

- **In:** a tool that a chat thread can run itself (a prompt tool such as StressTest or ThreadMap), or that a thread can call (a small script a thread runs, such as AutoEDA's report generator or ThreadSeed's index helper).
- **Also in (proposed reading, not yet decided):** a bounded function a thread calls through an explicit, versioned adapter, even when it ships a CLI wrapper, a small local state file or declared, versioned dependencies. Packaging alone doesn't disqualify a tool.
- **Separate projects that QAT integrates rather than holds:** independently useful applications, maintained libraries and persistent services (eraevous/mtg's `mtgtools`, for example). Those follow Zach's standing rule (Telosmith-instantiated: set up with Telosmith, Kairos's requirements-traceability tool); a QAT adapter may point at them. Where exactly the line falls is Zach's call: see [docs/remit/FOR_ZACH.md](docs/remit/FOR_ZACH.md) item 2.
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

## JobHunter

[JobHunter](docs/JOBHUNTER.md) provides four independently usable chat tools: JobIntelParser, ResumeTailor, InterviewCommander and ReflectiveJobNote. Each has a portable prompt, native QAT contract, generated Claude skill and fictional offline acceptance cases. Transfers are optional; semantic evaluation is pending. The companion ports are stacked separately from parser PR #37.

## Working rules

[AGENTS.md](AGENTS.md) for agents, [CONTRIBUTING.md](CONTRIBUTING.md) for spec changes (eval-gated, DEC-193). Review order: first an independent review by a different model family (ChatGPT (Kate), Zach's ChatGPT partner thread, or API Kate, the ChatGPT API reviewer), then a fresh-context execution review; Zach merges.
