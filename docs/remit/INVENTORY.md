# Inventory: tools joining QAT-Kits under the 2026-11-16 remit

Author: claude:qat#01GZK2Knb8aP6VTtZ7bf5tRv · Reviewer: none yet · model=claude-opus-5-5 · Handoff: HO-QAT-20261116-Y0HJ
Base: QAT-Kits `3efb46f3d3e2` (main, 2026-11-17). Proposal only: nothing here moves, deletes or rewrites any source.

"Installed" below means the account skill set synced into this session on 2026-11-17. Installed copies are the pre-release uploads (no `GENERATED` stamp) and none is byte-identical to the generated copy in `qat/runtimes/claude/`. That is expected until Zach installs a `qat-skills-v*` release; it isn't evidence that either side is wrong.

## 1. Tools named by Zach

### AutoEDA (`auto-eda`)

| | |
|---|---|
| Lives now | Source of record already here: `qat/tools/auto-eda.skill.md` v1.1.0 + `qat/tools/auto-eda.files/scripts/` (`auto_eda.py`, `plugins/example_donut.py`), ported in #20, review fixes in #21. Generated: `qat/runtimes/claude/auto-eda/`. Installed: account skill `auto-eda` (pre-release upload). Cases: `qat/cases/auto-eda.cases.md`; tests: `qat/scripts/test_auto_eda.py`. |
| Depends on | Python 3 with pandas, numpy, matplotlib; openpyxl for XLSX; pyarrow or fastparquet for Parquet (optional). Claude-side delivery step (`SendUserFile`). |
| What would move | Nothing from Claude: it is already here. The ChatGPT port is the missing runtime (see port findings). |
| Integration boundary | Input: one data file (CSV, JSON/JSONL, XLSX, Parquet). Output: `<stem>_eda.html` + `<stem>_eda.json`, one JSON status line on stdout. The provider-specific parts are only step 3 (delivery) and how the script gets into the sandbox. |
| ChatGPT port findings (Abigail's port against QAT-Kits `8f3b443e87e7`; relayed, not re-run here) | The port drops Claude-only delivery assumptions, avoids `pip --break-system-packages`, and restricts plugin imports to reviewed code. **Passed:** CSV, nested JSON and XLSX checks; PNG decoding; bundled plugin execution. **Untested:** Parquet (no optional engine present) and browser layout. |
| Upstream gaps these findings expose | (a) The skill text names `SendUserFile` and the Claude sandbox; the provider-specific delivery should move to a per-runtime section (contract §3). (b) `plugins/` loads any `.py` dropped beside the script; "reviewed code only" should become the upstream rule too. Both are spec changes, so eval-gated; not done in this slice. |

### MTG Deck Lab (`mtg-deck-lab`)

| | |
|---|---|
| Lives now | Source of record already here: `qat/tools/mtg-deck-lab.skill.md` v1.0.0 (text only, no bundled files). Generated: `qat/runtimes/claude/mtg-deck-lab/`. Installed: account skill `mtg-deck-lab` (SKILL.md only). Cases: `qat/cases/mtg-deck-lab.cases.md`. |
| Depends on | Zach's MTG doctrine documents (DIO v3, DBEP v1.x, Kairos–GATE), supplied in-thread; optionally his inventory workbook. The executable side (KB, DIO lookup, evaluator, simulator) is the **eraevous/mtg** repository (`python3 -m mtgtools …`), which this skill does not require. |
| What would move | Nothing more. The mtg repository is a Python project with its own charter and purpose contracts; it should **not** move here (it is the "Python package" side of the open boundary question). |
| Integration boundary | The skill is a prompt tool. It may *point at* `mtgtools` when a thread has it, never require it (DEC-193 optionality). |
| ChatGPT port finding | "The bundled Monte Carlo code is an incomplete sketch, not a working simulator." **Note:** the upstream source here bundles no Monte Carlo code; §"Simulation" (L172-173) only lists what a simulation must model. So the sketch exists only in the ChatGPT copy. Proposal: keep upstream code-free and add an explicit line that the skill carries no executable simulator, and that simulations come from a tested implementation (eraevous/mtg) or are labelled as the model's own estimate. Spec change, eval-gated; not done in this slice. |

## 2. Tools already here whose port findings were relayed

| Tool | Finding (relayed) | Upstream status at `3efb46f` | Proposed next step |
|---|---|---|---|
| ThreadSeed (`thread-seed.skill.md`, embedded `seed_index.py`) | Two helper defects, fixed only in the ChatGPT copy | **Both present.** `verify()` (source L238-260): a bare `T2` passes when `1 ≤ n ≤ max` even if no T2 exists (L249 checks existence only for refs with a suffix); a quote cited to `T1a2` is searched in every assistant message of T1 (L257, `k.startswith('a')`), so T1a's text matches. | Fix upstream with regression tests: nonexistent T2 in a T1/T3 capture; wrong quote; T1a text cited as T1a2. Spec change (version bump + eval run), next slice. |
| QAT runner (`qat/scripts/qat.py`) | `eval` exits 0 with every case SKIP when outputs are missing | **Present.** `run_eval` records a missing output as a warning + SKIP (L391-394); exit code comes from errors only (L213, L487). | Distinct non-success exit (proposed `3`, "incomplete") when any case is SKIP, with a regression test; keep the index's four lossy-coercion warnings visible. Code change to the runner (carried by the `qat` skill), next slice. |
| SSD (`selective-self-distillation`) | Extraction, dedup and provenance pass; relay classification still needs manual screening | Unchanged. | Keep the limit stated: relay classification isn't automated proof of authorship. |
| Zach Voice (`zach-voice`) | ChatGPT copy's biography corrected (data science, complex systems); skill now requires writing samples that are actually accessible | Not checked line by line in this slice. | Zach reviews the source profile for stale claims (FOR_ZACH item 4). |
| Validation receipt | 15 synthetic CLI checks had the expected outcomes | n/a | Not a model-quality evaluation, and it doesn't show every installation works. Installation verification is Abigail's, running separately. |

## 3. Other candidates that fit "invoked as or by chat threads"

Found in the account skill set and in relay-kit; none moved. Ownership is a decision for Zach (FOR_ZACH item 3).

| Tool | Lives now | Depends on | Fit and boundary |
|---|---|---|---|
| chat-capture | relay-kit `skills/chat-capture/` (installed) | A browser tool in the session | Invoked by a thread; provider-specific by nature (drives the chat sites). Fits the remit, but its source of record is relay-kit. |
| chat-relay, relay-governor | relay-kit `skills/` (installed) | Browser tool; relay-kit governance | Browser relay to ChatGPT was retired for Kate (lane-rules §9, ChatGPT terms). Moving these would carry that limit with them. |
| chat-telemetry | relay-kit `skills/chat-telemetry/` (installed) | chat-capture output | Thread-invoked analysis; text + small script. Good candidate. |
| handoff-ledger | relay-kit `skills/handoff-ledger/` (+ `scripts/handoff.py`) | relay-kit records layout | Kairos coordination infrastructure, not a lightweight user tool. Suggest it stays in relay-kit. |
| morning | account skill only | Connectors | Personal workflow; not suggested. |
| kind-check, real-problem, thread-distill, toolsmith, effort-cost | already here (`*.qat.md`) | runner | Already in; kind-check and real-problem have hand-adapted Claude and ChatGPT runtimes outside the generator. |

QAT: negative-space (installed skill, 2026-10-15 upload: not run as a separate pass in this wake; the "what we'd expect and don't see" check was done by hand: no README, no ChatGPT generator, no install verification record).
