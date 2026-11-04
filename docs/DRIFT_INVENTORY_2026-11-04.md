# QAT-Kit drift inventory, 2026-11-04

Authority: DEC-048 (Zach, 2026-11-04 09:17 CT), with Kate's amendment: **no copy is declared canonical here.** This document records what each copy contains so that a canonical-source recommendation can be made later with evidence. It contains no such recommendation.

Prepared by claude:qat#01GZK2KncnZ4v7e6ZAQ4C1ZH. Companion files: `docs/IMPLEMENTATION_COMPARISON_2026-11-04.md`, `qat/` (eval port and run results).

## 1. What was compared, and how far to trust it

| Copy class | Where | What I could see |
|---|---|---|
| **repo** | `Toolkits/dialogic_toolkit/Tools/*.md` plus its `toolkit.json` and `qat_manifest.json` (this repo, one commit, c992004, 2025-07-14) | Everything, byte-exact. |
| **vault** | Obsidian vault via `vault-digest.md` (entries are path, mtime, size, lines, first 25 lines) | Header and first 25 lines only. Anything past line 25 is unseen and marked "tail unseen". |
| **skill** | `/root/.claude/skills/synced/7bbdaa89-.../<name>/SKILL.md` (Claude account skills) | Everything. |
| **spec** | `.../qat/tools/*.qat.md` (lean typed spec read by `qat.py`) | Everything. Exists for stress-test and truth-weight only. |

Date caveats, so no one reads a date as authorship:
- Every repo file has the same git date (2025-07-14) because there is one commit. The files' filesystem mtimes (2026-11-03) are checkout times.
- Skill file mtimes (2026-11-03) are sync times. The dates below for skills and the spec are the plugin `updatedAt` values in the skill `manifest.json`.
- Vault mtimes are the digest's. They can predate or postdate use: the ChatGPT export in the digest has TruthWeight first used by Zach on 2025-06-29, yet the vault's `TruthWeight.md` is dated 2025-06-04.
- Memory records the tools as written "early 2024"; the earliest tool-name use in the digest's ChatGPT export is 2025-06-11 (FrameShift) and 2024-11-21 for the phrase "negative space". Unreconciled (see section 6).
- None of the repo, vault or skill tool files carries a tool-level version string, except `negative-space` ("0.1.0-reconstruction") and the two `.qat.md` specs ("2.0.0"). `toolkit.json` has a kit-level `version: 0.1` (last_updated 2025-06-29).

## 2. Coverage matrix

Count of distinct copies found (a dash means none found).

| Tool | repo | vault | skill | spec | Total |
|---|---|---|---|---|---|
| StressTest | 1 | 2 | 1 | 1 | 5 |
| TruthWeight | 1 | 1 | 1 | 1 | 4 |
| FrameShift | 1 | 2 | 1 | - | 4 |
| MetaDistill | 1 | 2 | 1 | - | 4 |
| ThreadMap | 1 | 3 | 1 | - | 5 |
| LegalEase | 1 | 1 | 1 | - | 3 |
| BraidedExplanations | 1 | 2 | 1 | - | 4 |
| NegativeSpace | - | - | 1 | - | 1 |
| SelectiveSelfDistillation | - | - | 1 | - | 1 |
| **All** | 7 | 13 | 9 | 2 | **31** |

Notes on counting: where the vault holds a probable twin (same size, line count and visible head) of a repo file I count it as a copy and give it a short row. A row marked vault-2 for FrameShift and BraidedExplanations groups the 2-3 files of one earlier split layout, so it counts once. Vault files that are outputs of a tool, not the tool, are listed in section 5 and not counted.

## 3. Inventory table

"Unique" means present in this copy and, as far as I could verify, in none of the other copies of that tool. Items are tagged `[Unn]` so they can be counted. "Lost if dropped" assumes the other copies are kept.

### StressTest

| Copy | Path | Date | Size | Version | Sections present | Unique capabilities | Lost if dropped |
|---|---|---|---|---|---|---|---|
| repo | `Toolkits/dialogic_toolkit/Tools/StressTest.md` | 2025-07-14 | 1,745 B, 34 lines | none | Opening request in the user's voice; 9 questions; 5 lens blocks (Reversal, Sharpen & Refine, Ethical Echo, Application Stress, Bias Climber) | [U01] First-person paste-able prompt ("Could you pick apart..."), no wrapper needed for a ChatGPT thread. [U02] Via `qat_manifest.json`/`toolkit.json`: invocation grammar ("Run StressTest modules: {[modules]}", "Run a StressTest comparison"), 5 report formats (basic, full, modular, comparison, table), actions diagnose/reframe/tweak/full/compare, 5 usage caveats, thread types thinker/worker/commander. | The comparison mode and the module-selection grammar exist nowhere else. The ChatGPT-ready phrasing. |
| vault-1 | `kAIros/AI Workflow/AI-Augmented Development/QAT-Kit/Design and Thinking/New Version/StressTest.qspec.md` | 2025-07-27 | 4,324 B, 194 lines | none visible | Tool Summary (name, description, author, audience, thread types, tags, caveats), Inputs; **tail unseen (169 lines)**. Says it was "converted from StressTest.md into the QAT Markdown-native format ... rendering into YAML, JSON, LangChain, and instruction modules". Companion `StressTest_diagnostics.md` (2025-07-27, 3,594 B, 104 lines): "reflective critique of StressTest using MetaDistill and StressTest itself". | [U03] A third format (qspec) with a stated render-to-YAML/JSON/LangChain path. Cannot say more without the tail. | Unknown beyond line 25. The self-critique file is the only record of StressTest being run on itself. |
| vault-2 | `.../QAT-Kit/Thread Tools v0/Templates 1/QAT_Tool_Signatures_and_Agent_Archetypes.md` | 2025-07-03 | 2,730 B, 106 lines (StressTest block visible) | none | JSON signature: `stress_test(input: idea, intensity: 1-5) -> issues: list, robustness: score`; modules ReversalLens, BiasClimber, EthicalEcho | [U04] An `intensity` input (1-5) and a `robustness` score output. The spec's `stakes` ("raises depth") is the nearest relative; nothing else scores robustness. | The robustness score concept. |
| skill | `stress-test/SKILL.md` | 2026-10-15 | 4,391 B | none (frontmatter has name, description) | Purpose, Invocation, Inputs, core mini stress-test (9 Qs), Lenses (5), Workflow, Output (7 headings), Checks, Provenance | [U05] Empty-invocation behaviour (summarise, list lenses, ask for idea/domain/stakes/depth). [U06] Sibling pointers to negative-space and frame-shift (the spec points only to truth-weight). [U07] "Depth" input and "compact report, expand with stakes". [U08] "Can be applied to your own prior outputs when the user asks." | Invocation UX and routing to two sibling tools. |
| spec | `qat/tools/stress-test.qat.md` | 2026-10-26 | 3,599 B | 2.0.0 | Frontmatter contract (3 inputs, 7 outputs), 5 reflexes, 1 handoff, procedure, 5 `### module:` sections | [U09] Typed, auditable output contract (`premise_set`, `claims`, `claim`) and the enforced handoff to truth-weight (`core_idea` -> `position_a`, `strongest_counterargument` -> `position_b`). [U10] Named reflexes (`no-forced-criticism`, `questions-not-diagnoses`). [U11] 3 eval cases (`cases/stress-test.eval.yaml`). Also wording drift: Application Stress drops "dangerous" ("something strange"); Bias Climber drops "trauma". | Machine checking, the handoff, the evals. |

### TruthWeight

| Copy | Path | Date | Size | Version | Sections present | Unique capabilities | Lost if dropped |
|---|---|---|---|---|---|---|---|
| repo | `Tools/TruthWeight.md` | 2025-07-14 | 2,828 B, 70 lines | none | Prompt framework; Objective; Instructions 1-5; 5-row category table; Example Structure; Philosophical Notes; optional Solaic certification | [U12] **Scores 0-100 per category** (sum out of 500); "categories can be ties". [U13] Via the JSON files: `invokeable_tools: [StressTest]`, `self_applicable: false` (the only tool flagged not self-applicable), and caveats saying it "does not evaluate positions in-practice, only in-theory" and "does not consider bad-faith variants". | The 0-100 scale (it is the scale the vault copy and any ChatGPT Project run use). The in-theory-only caveat, which contradicts the skill's use of empirical search and is a design question to settle. |
| vault | `kAIros/AI Workflow/Tooling/Prompts/TruthWeight.md` | 2025-06-04 | 2,828 B, 70 lines | none | First 25 lines equal the repo's; same size and line count; tail unseen | None found. Probable byte-identical twin of the repo file (unverified past line 25). | Nothing visible, if the twin holds. |
| skill | `truth-weight/SKILL.md` | 2026-10-15 | 5,901 B | none | Purpose, Invocation, Inputs, Instructions (6 steps), 5-row category table, Optional extensions, Template, Philosophical notes, Checks, Provenance | [U14] **0-10 scale with anchors** (0-2 contradicted ... 9-10 convergent); total /50. [U15] "Keeping Burden of Proof distinct" (fit between claim and evidence, no double-counting evidence quality). [U16] Weight-sensitivity test and "name the value judgment if the verdict flips". [U17] Framing flaws flagged before scoring; search-when-empirical; "separate observation from inference, speculation and normative judgment". [U18] Unscored version on request. [U19] Provenance note records the 0-100 to 0-10 change and why. | The whole scoring discipline; the repo prompt has none of it. |
| spec | `qat/tools/truth-weight.qat.md` | 2026-10-26 | 2,377 B | 2.0.0 | Contract (3 inputs, 5 outputs), `burden-of-proof` module, 4 reflexes, 1 handoff, procedure | [U20] Typed contract with `## Positions / Framing notes / Scorecard / Verdict / Would reverse if` and `## Scorecard` as a `Category|A|B|Why` table; handoff `verdict` -> stress-test `idea`. [U21] Reflex `noise-floor` as a named rule. Gap against the skill: no optional extensions, no Solaic line, no unscored mode, no empty-invocation behaviour, no philosophical notes. | The checkable contract; (new this PR) the truth-weight evals run against it. |

### FrameShift

| Copy | Path | Date | Size | Version | Sections present | Unique capabilities | Lost if dropped |
|---|---|---|---|---|---|---|---|
| repo | `Tools/FrameShift_Full.md` | 2025-07-14 | 12,834 B, 296 lines | none | Persona preamble; heuristic table (10 rows, repeated verbatim ~line 130); 6 modes; Substance Rating (4 criteria); Signal-to-Fluff bands; **AI Authorship Probability** bands; 9 meta-modes; Addenda (Overpolish Backfire, RS-AIMR, Style Leakage Alert, Wall of Text Paradox, Cultural Implication); Overclipped Cadence heuristic; Cadence Compression Flag; Optional Repair ("Narrative Breath Pass") | [U22] "AI Authorship Probability" as a probability label, and Cadence Compression "increases AI-authorship probability score" (the skill relabels both). [U23] "Cultural Implication": clarity becomes a risk "unless you fracture it on purpose" (skill keeps the paradox, drops this recommendation). [U24] "You are FrameShift" persona line. [U25] Via JSON: actions detect_ai/rate_substance/simulate_reverse_prompt/analyze_style, `invokeable_tools: [TruthWeight, StressTest]`, 7 caveats. | The original probability framing and the fracture-on-purpose advice. |
| vault-1 | `kAIros/AI Workflow/Tooling/FrameShift/FrameShift_Full.md` | 2025-07-07 | 12,834 B, 296 lines | none | First 25 lines equal the repo's; same size and line count; tail unseen | None found. Probable twin of the repo file. | Nothing visible. |
| vault-2 | `.../Tooling/FrameShift/FrameShift Instructions.md` (2025-06-16, 1,530 B, 15 lines) + `FrameShift Attachments.md` (2025-06-18, 11,301 B, 279 lines) + `Design/Conv - One design thread.md` (2025-06-18, 36,772 B, 567 lines) | 2025-06-16/18 | 12,831 B instructions+attachments | none | Earlier split layout: short instructions plus modular attachment (custom-GPT knowledge-file style); design conversation. Tails unseen. | [U26] The earlier split form (instructions vs attachments) and the design rationale thread. Not diffed against the merged `_Full` file (tail unseen). | Design rationale; the split layout used when FrameShift was a custom GPT. |
| skill | `frame-shift/SKILL.md` | 2026-10-15 | 12,620 B | none | Purpose, Invocation, **Two jobs (detection vs repair)**, Inputs, Core modes, Scoring, Meta-modes, Heuristics with shelf-life note (12 rows, "last reviewed October 2026"), Workflow, Output, Checks, Provenance | [U27] Detection/repair separation, including "never run detection on text you just repaired". [U28] Shelf-life note on the AI-tell table. [U29] "AI-likeness band", explicitly not a probability of authorship. [U30] Refusal framing: repair is for the author's own voice, not for passing AI text as human. [U31] Workflow and output headings (core message, substance, rhetorical findings, edits, ratings). | The ethics boundary and the aging note. |

### MetaDistill

| Copy | Path | Date | Size | Version | Sections present | Unique capabilities | Lost if dropped |
|---|---|---|---|---|---|---|---|
| repo | `Tools/MetaDistill.md` | 2025-07-14 | 775 B, 11 lines | none | 5 bullets (effective, tactics, reusable method, optional uses, drift check) + "Cognitive Ownership Checkpoint" (3 questions) | [U32] The checkpoint as three first-person probes the user can put to the model ("Which parts did I generate, and which came from you?"). [U33] Via JSON: actions summarize/recommend/identify_risks/comparison and a `recommendations` output. | The question-form checkpoint. |
| vault-1 | `.../Tooling/Prompts/MetaDistill/MetaDistill.md` | 2025-07-07 | 775 B, 11 lines | none | **All 11 lines visible; text equals the repo's** | None. Confirmed identical text. | Nothing. |
| vault-2 | `.../Tooling/Prompts/MetaDistill/MetaDistill Refinement 1.md` | 2025-06-18 | 638 B, 12 lines | none | Fragment: rationale ("an evolved prompt lifecycle ... a new stance") + the same 3 questions, called a "Midpoint Validation Ritual" | [U34] Origin/rationale of the checkpoint and its framing as a mid-conversation ritual, not an end-of-run section. | The design rationale. |
| skill | `meta-distill/SKILL.md` | 2026-10-15 | 2,760 B | none | Purpose, Invocation, Inputs, Workflow (6 steps), Output (6 named parts), Checks, Provenance ("adapted, not verbatim") | [U35] Default to the current conversation; "too short, say so and ask". [U36] Ownership split into user-originated / model-originated / joint refinement, "quote the turn where an idea first appears". [U37] Checks: don't credit yourself for the user's ideas; don't claim authorship without evidence. [U38] Six named output parts. | Attribution discipline and the invocation rules. |

### ThreadMap

| Copy | Path | Date | Size | Version | Sections present | Unique capabilities | Lost if dropped |
|---|---|---|---|---|---|---|---|
| repo | `Tools/ThreadMap.md` | 2025-07-14 | 1,892 B, 33 lines | none ("Tool Name: TokenMap Analyzer") | Purpose, Input, Behavior (3 steps), Output (example table + narratives), Bonus Option (thread stitching) | [U39] Token-fade framing: ~1.5k-token threshold, "visualize where fade-out likely begins", `Tokens` and `Fade Warning` columns with warning emoji. [U40] Two worked example rows and two example narratives. [U41] Via JSON: actions summarize/identify_topics/suggest_forks/comparison; caveat that audio/multimodal threads are unsupported. | Fade-zone estimation and worked examples. |
| vault-1 | `.../Prompts/Compression Pipeline/ThreadMap1.md` | 2025-07-04 | 1,892 B, 33 lines | none | First 25 lines equal the repo's; same size and line count; tail unseen | None found. Probable twin of the repo file. | Nothing visible. |
| vault-2 | `.../Tooling/Prompts/ThreadMap.md` | **2026-04-22** | 1,991 B, 35 lines | none | Repo text plus two edits: Purpose adds "including current thread"; Input becomes "One of: attached log, or the current conversation where this has been used as a prompt". The +99 B and +2 lines are fully accounted for by these two edits (checked), so the unseen tail is probably the repo's | [U42] Current-conversation input mode in the prompt itself. | The newest edit by date of any non-skill ThreadMap. |
| vault-3 | `kAIros/.md` (untitled) | 2025-09-16 | 2,939 B, 87 lines | none | "TokenMap Analyzer AND Context Compressor": Step 1 segmentation table + narrative outline tagged conversational / slide-style list / conclusion; "block >1.5k tokens is a candidate for compression"; Step 2 emits composite `memory_nodes`; tail unseen | [U43] Combined segment-then-compress prompt producing YAML-compatible memory nodes. [U44] Narrative tagging by rhythm (slide-style list vs conversational vs conclusion). | The only ThreadMap variant that goes on to produce compressed artifacts. Related: `Compression Pipeline/Context Compressor.md` (2025-09-16, 2,100 B, 82 lines) and `Modular Compressor Kit .md`. |
| skill | `thread-map/SKILL.md` | 2026-10-15 | 2,843 B | none | Purpose, Invocation, Inputs, Workflow (6 steps), Output (table + narrative reconstruction + context to carry forward), Checks, Provenance ("adapted, not verbatim") | [U45] Evidence-based `Continuity warning` column (dropped requirement, contradicted decision, unanswered question) in place of fade zones; the provenance note says the 1.5k threshold was dropped "because current models don't degrade at that length". [U46] `Context to carry forward` output and per-segment links to adjacent sections and key decisions. [U47] Length labelled approximate, words x ~1.3. [U48] Sibling routing (negative-space takes a ThreadMap as input). | The handoff output and the evidence rule. |

### LegalEase

| Copy | Path | Date | Size | Version | Sections present | Unique capabilities | Lost if dropped |
|---|---|---|---|---|---|---|---|
| repo | `Tools/LegalEase.md` | 2025-07-14 | 1,805 B, 34 lines | none | User-voice request; consumer-advocate role with 5 jobs; red/yellow/green flag legend; second review prompt (3-part issue template); closing instructions | [U49] First-person ready-to-paste request. [U50] Via JSON: thread types worker/consumer/watchdog; caveats "not legal advice", "framing is human-centered; may miss strategic benefits to business operators". | The business-operator caveat and the paste-ready request. |
| vault | `.../Tooling/Prompts/LegalEase.md` | 2025-05-29 | 1,805 B, 34 lines | none | First 24 lines equal the repo's; same size and line count; tail unseen | None found. Probable twin. Older than the repo date. | Nothing visible. |
| skill | `legal-ease/SKILL.md` | 2026-10-15 | 3,025 B | none | Purpose, Invocation, Inputs, Workflow (6), Output (5 named parts), Checks, Provenance ("adapted, not verbatim") | [U51] "Never review terms from memory of what a company's terms usually say." [U52] Clause quote or locator per finding. [U53] Jurisdiction-dependence flagged; industry or competitor comparisons need a cited basis; no "unlawful" without support; suggest a lawyer for consequential agreements. | The anti-invention rules. |

### BraidedExplanations

| Copy | Path | Date | Size | Version | Sections present | Unique capabilities | Lost if dropped |
|---|---|---|---|---|---|---|---|
| repo | `Tools/BraidedExplanations_Full.md` | 2025-07-14 | 6,495 B, 108 lines | none | Persona + 6 strands; clarifying questions with skip conditions; embedded WWH Braiding (overview, add-ons, "Why it works" table, **Use Cases**, sample template) | [U54] "Use Cases" list (zettels from conversations, drafting while fatigued, teaching an AI to walk you through a subject). [U55] Via JSON: `invokeable_tools: [TruthWeight, StressTest, MetaDistill, ThreadMap]` (it may call four other tools; the manifest gives SparkResearch, out of scope here, five) and 7 actions (dive_deeper, generate_metaphors, check_knowledge, suggest_connections...). | The use-case list and the cross-tool invocation rights. |
| vault-1 | `.../Tooling/BraidedExplanations/BraidedExplanations_Full.md` | 2025-07-07 | 6,495 B, 108 lines | none | First 24 lines equal the repo's; same size and line count; tail unseen | None found. Probable twin. | Nothing visible. |
| vault-2 | `.../BraidedExplanations/BraidedExplanations Instructions.md` (2025-06-16, 2,823 B, 32 lines), `WWH Braiding.md` (2025-06-16, 3,663 B, 74 lines), `Prompts/WWH Braiding.md` (2025-06-05, 3,771 B, 76 lines) | 2025-06-05/16 | see left | none | Earlier split form; **two different WWH Braiding files (3,663 B vs 3,771 B)**. Tails unseen. | [U56] The earlier split layout and the older, longer WWH file (108 B larger). Not diffed. | Possible text in the 3,771 B WWH file that the merged `_Full` lacks. |
| skill | `braided-explanations/SKILL.md` | 2026-10-15 | 6,595 B | none | Purpose, Invocation, Default strands, **Choosing a path (quick / full)**, Full workflow (4 steps incl. Integrate), WWH strings with worked examples, Output, Checks, Provenance ("Restored from the original") | [U57] Quick path (no clarifying questions, 2-3 strands, adjustment offer) vs full path. [U58] Integrate step: one working model, limits and misconceptions, practice example. [U59] Checks: every strand must advance understanding; the poetic strand must still carry an idea; label analogies and where they break. | The quick path and the checks. |

### NegativeSpace

| Copy | Path | Date | Size | Version | Sections present | Unique capabilities | Lost if dropped |
|---|---|---|---|---|---|---|---|
| skill | `negative-space/SKILL.md` | 2026-10-15 | 16,899 B | "0.1.0-reconstruction" | Identity, Inputs, 6 modes (scan, inverse, expectation-audit, comparative, full, chain), 7-step procedure, Default output (scan), Fit Signature specialisation, QAT-Kit interoperability, Integrity rules, Appendix A (provenance ledger dated 2026-10-15), Appendix B (5 acceptance cases A-E) | [U60] The entire tool: no repo, vault or spec copy exists; repo grep for "negative space" finds nothing. Its own ledger says it is a new reconstruction, not a recovery. [U61] Appendix B: five acceptance cases with expected behaviour and failure condition (an eval seed). [U62] Expectation-audit Parts A/B (missing strengths vs unwarranted presumed weaknesses). | Everything. |

Vault evidence that the idea predates the skill (not copies of the tool): "negative space" first used by Zach in the ChatGPT export on 2024-11-21 (167 mentions, 61 conversations); `Basic Tool Inclusion.md` (2025-07-01) lists "NegativeSpace (and others)"; `Articles/Experiments/US Budget Negative Space.md` (2025-06-04, 3,035 B); a "Negative Space Analysis: What Doesn't Exist in PIE Myth?" section inside `Articles/Experiments/Conv - AI tool use learning.md` (2025-05-22); a "Negative space exploration" core module in the Job Arsenal Fit Signature (2025-07-18).

### SelectiveSelfDistillation

| Copy | Path | Date | Size | Version | Sections present | Unique capabilities | Lost if dropped |
|---|---|---|---|---|---|---|---|
| skill | `selective-self-distillation/SKILL.md` | 2026-10-16 | 9,133 B, 155 lines | none | Inputs, Known traps (6), Procedure (7), Output (6), Checks, embedded `extract_turns.py` | [U63] The whole tool: no repo, vault or spec copy of a procedure. [U64] Embedded `extract_turns.py`, evidence labels (Direct / Adopted / Revised / AI proposal / Unresolved), quote verification step. | Everything. |

Vault origin: `kAIros/Conv - Selective Self Distillation.md` (2026-03-31, 35,926 B, 1,763 lines): the design conversation ("extract your cognition, not the AI's"), extending Cognitive Scaffolding. In the ChatGPT export the model, not Zach, first used the term (2025-06-16). It is a conversation, not a tool copy, and is not counted.

## 4. Counts

- Tools: **9** (StressTest, TruthWeight, FrameShift, MetaDistill, ThreadMap, LegalEase, BraidedExplanations, NegativeSpace, SelectiveSelfDistillation). `qat` (the runner) is infrastructure and `thread-seed` has no ancestor, so neither is a row.
- Copies: **31** (repo 7, vault 13, skill 9, spec 2). Two tools (NegativeSpace, SSD) exist as a single copy.
- Tagged unique capabilities: **64** `[Unn]` items. 59 are differences between copies of the seven tools that have more than one copy; 5 (U60-U64) belong to the two tools that have a single copy and so are "unique" only trivially.
- Per tool: StressTest 11, TruthWeight 10, FrameShift 10, MetaDistill 7, ThreadMap 10, LegalEase 5, BraidedExplanations 6, NegativeSpace 3, SelectiveSelfDistillation 2.
- Tags are my judgment of distinct capabilities, not a mechanical count; a different reader could split or merge some.
- Probable byte-identical repo/vault twins (same size, line count and visible head): FrameShift_Full, TruthWeight, LegalEase, BraidedExplanations_Full, ThreadMap (vs ThreadMap1), MetaDistill (full text compared, identical). Five of the six are unverified past line 25.
- Drift worth reading about first: ThreadMap (3 different behaviours: fade zones, current-conversation mode, segment-then-compress, evidence-based continuity) and MetaDistill (checkpoint as user questions vs model-run attribution split). TruthWeight is the sharpest numeric split (0-100 vs 0-10).

## 5. Vault files that look like copies but are outputs

These are easy to mistake for tool versions. They record what the tool was used to produce.

| File | Date | Size | What it is |
|---|---|---|---|
| `.../Tooling/Prompts/Prompt Behavior Diagnostic - MetaDistill.md` | 2025-06-16 | 5,562 B, 72 lines | A diagnostic of how prompts in `MetaDistill Results.md` shape AI responses (rubric: Structure, Ambiguity, Role Priming, Recursion, Artifacts, Failure Mode; PromptCraft archetype assignments). Not a MetaDistill spec. The earlier lane brief counted it as the vault's 5.6 KB MetaDistill version; its first lines say otherwise. |
| `kAIros/PromptCraft/Artifacts/MetaDistill Results.md` | 2025-06-16 | 76,075 B, 1,959 lines | Results corpus. |
| `kAIros/Articles/Codex++/MetaDistill Report.md`, `StressTest Report.md`, `TruthWeight Report.md` | 2025-07-09 | 9,736 / 3,990 / 3,422 B | Tool outputs on the Codex++ intro. The MetaDistill report uses its own headings ("Core Thesis", "Narrative Structure Breakdown"), unlike the skill's six parts. |
| `.../Tooling/Job Arsenel/StressTest Assessment.md` | 2025-07-18 | 4,601 B, 90 lines | StressTest run on the Fit Signature framework. |
| `.../Tooling/Prompts/Examples/legalease results v1, v2, v3` | 2025-05-28, 05-28, 06-04 | 4,201 / 4,957 / 4,776 B | LegalEase outputs (three revisions). |
| `.../QAT-Kit/James/Final FrameShift pass.md` | 2025-06-28 | 2,943 B | FrameShift output ("reader-side AI misattribution risk" cited by name). |

## 6. Findings that affect the decision but are not recommendations

1. **Two scoring systems for one tool.** Repo and vault TruthWeight score 0-100; skill and spec score 0-10. The `toolkit.json` TruthWeight caveats (theory only, best-faith only) are in tension with the skill's empirical-search step. A prompt that "just runs" in a ChatGPT Project is the 0-100 form.
2. **Repo packaging carries behaviour the Markdown files lack.** `toolkit.json` and `qat_manifest.json` define invocation phrases, actions, report formats, flags and which tools may call which. The skills route between tools only by prose sibling pointers, and the specs by two declared handoffs (stress-test and truth-weight); neither reproduces the manifest's `invokeable_tools` lists. One manifest quirk: TruthWeight's caveats include a sentence about "miss-identifying human and AI-generated content" that reads as FrameShift boilerplate.
3. **The skills describe themselves two ways.** Provenance lines say "Restored from the user's original" for StressTest, TruthWeight, FrameShift and BraidedExplanations, and "adapted, not verbatim" for MetaDistill, ThreadMap and LegalEase. The cited originals are Google Drive files; I did not open them.
4. **The repo is stale relative to its own architecture.** One commit; `qat_tool.instructions.template.md` says v2.1 while the commit message says "V-2.3"; modules template v2.2; `qat_schema.md` is v2.0. The vault holds a Tool Schema Specification v3.0 (2025-07-28) and a `StressTest.qspec.md` (2025-07-27) that the repo lacks. The `.qat.md` format (version 2.0.0) is a fourth format. "Version" therefore means different things across copies.
5. **Two copies carry an explicit refusal or guardrail the others lack:** frame-shift (not helping AI text pass as human), legal-ease (no memory-based terms review), stress-test spec (`questions-not-diagnoses`). Dropping the repo copies would not lose these; dropping the skills would.
6. **Dates conflict.** Memory says early 2024; the ChatGPT export's first use of tool names is mid-2025; vault mtimes for TruthWeight and LegalEase (2025-06-04, 2025-05-29) precede or sit near those first uses; the repo shows only 2025-07-14.

## 7. Evidence a decision would need

Not yet in hand, in rough order of value:

1. **The Drive originals** that the skills cite (file IDs are in each SKILL.md Provenance). A diff of original vs skill for each of the 7 tools with an original would show what was changed and whether "restored" and "adapted" are accurate. The repo and vault copies may or may not equal those originals.
2. **Full vault text** (not the 25-line digest) for the 5 unverified twins and for the split files (FrameShift Instructions/Attachments, the two WWH files, the 169-line qspec tail). A `sha256` of each vault file against its repo twin would settle identity in one step.
3. **Independent eval runs.** The truth-weight eval run in `qat/eval-runs/2026-11-04/` was written by the same agent that wrote the cases. Needed: a fresh subagent per case, and the same inputs run through each copy (repo 0-100 prompt, skill, spec) so outputs can be compared. Evals exist for 1 spec tool of 9 (3 cases) plus the 5 new truth-weight cases.
4. **Runtime targets.** Which environments must each tool run in: ChatGPT Project (no skills; repo files), Claude skills, or the `qat.py` runner. The vault note "Conv - Invocation Problems" (2025-07-18) records tools failing in ChatGPT. Different targets may need different artifacts regardless of the source decision.
5. **Zach's ranking of the "lost if dropped" items.** Several are policy choices, not data: 0-100 vs 0-10; fade-zone estimation vs evidence-based continuity warnings; ownership questions as user probes vs a model-run attribution section; fracture-on-purpose advice in FrameShift.
6. **Real-use evidence.** Which outputs Zach kept and reused (section 5 files) and which headings he relied on, to see which copy's behaviour he actually valued.
7. **Ownership of thread-map, meta-distill and SSD** (they now feed thread-seed and the relay-kit lane). The decision on a canonical source for those may follow the ownership decision.
8. **Missing artifacts:** QAT-Kit Master Architecture Blueprint (Drive), the v2.1 Reconciliation Plan and Tool Schema Specification v3.0 (vault, 2025-07-14 and 2025-07-28, only headers seen), and any original NegativeSpace prompt in ChatGPT history.
