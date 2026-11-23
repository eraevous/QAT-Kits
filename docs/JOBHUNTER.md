# JobHunter: portable chat tools

Status: four **0.1.0 candidate** tools, bundle **1.4.0**. All are independently usable chat-executed prompts with native contracts and offline acceptance tests. They make no network or model API calls. Semantic quality has **not** been independently evaluated. The three companion ports are a separate draft stacked on parser PR #37; the parser source and that PR remain unchanged.

## Use it now

**ChatGPT or another chat model:** paste [the complete paste block](../qat/runtimes/chatgpt/job-intel-parser.paste.md), followed by your `listing:` text. `candidate_evidence:` and `priorities:` are optional. The block is self-contained and requires neither a repository checkout nor another tool. Example (fictional):

```text
Run JobIntelParser.
listing:
L1: Required: SQL or equivalent project experience. Python preferred.
Salary: USD 70,000 per year. Remote. Some evening support required.
candidate_evidence:
E1: Built a SQL inventory report for a fictional volunteer project.
priorities:
P1: I need daytime work and at least USD 65,000 per year.
```

**Claude:** use the generated [job-intel-parser skill](../qat/runtimes/claude/job-intel-parser/SKILL.md), packaged by the existing `skills.py` path. Install this skill independently or use the bundled `qat` runner contract. Packaging checks do not verify app upload UI behavior. Nothing has been installed or released by this change.

**Native QAT:** give the model [the contract](../qat/tools/job-intel-parser.qat.md) and the labeled input. Save the returned dossier outside the public checkout when using real material, then audit it locally. The CLI does **not** generate model output. From `qat/`:

```sh
python3 -I scripts/qat.py validate tools/job-intel-parser.qat.md
python3 -I scripts/qat.py audit job-intel-parser /path/to/dossier.md --json /path/to/dossier.json
```

The JSON is a mapping of the eight declared fields to bullet lists, suitable for explicit future adapters. The audit checks section presence and bullet shape, not whether quotations, facts or reasoning are correct. No automated handoffs are registered. The three companion contracts now exist, but transfers remain explicit and optional.

For a fully offline smoke test on the included fictional fixture:

```sh
python3 -I scripts/qat.py audit job-intel-parser eval-runs/2026-11-23/job-intel-parser/ordinary.md
python3 -I scripts/qat.py eval cases/job-intel-parser.eval.yaml eval-runs/2026-11-23/job-intel-parser
```

The second command must exit **3**, incomplete: all six authored examples pass mechanical checks, but 13 semantic judgments remain ungraded. These are design-time exemplars, not cold model outputs. See [RESULTS.md](../qat/eval-runs/2026-11-23/job-intel-parser/RESULTS.md). To complete semantic evaluation, produce fresh outputs from only the spec and each expanded input, then have an independent reviewer grade every YAML `judge` criterion using the runner's hash-bound `--judgments` format. Keep failures visible. The repository also requires independent review followed by fresh-context execution review before the owner merges.

## Scope and provenance

The historical four tools already exist under `Toolkits/Job Hunter Arsenel/`. They are left untouched, as required by AGENTS.md. The new native implementation narrows JobIntelParser to supplied-text analysis; it does not carry forward historical company lookup, guessed recruiter/ATS priorities, or automatic pipeline/cache behavior. Current main was checked at `47b16ab1ad399c2362705b10936373d94cddf5cd`; no native JobHunter contracts or skills existed. There is no `.agents/skills/` directory in this checkout. NegativeSpace overlaps omission analysis, but does not provide the listing/screener, modality-preserving, six-axis dossier contract.

Authoritative procedure: `qat/tools/job-intel-parser.qat.md`. The standalone `.skill.md` and ChatGPT paste adaptation currently carry the identical procedure, enforced by `test_job_intel.py`; Claude files are generated using the existing build system. Edit sources and adaptations together, never generated files. New versions follow CONTRIBUTING.md's eval gates. No runner implementation, existing spec, record, dependency, or legacy tool was changed.

## Companion tools: use them independently

Paste the linked block, then supply the inputs shown. These examples are fictional and need no prior JobHunter run. Each has a matching `qat/tools/<name>.qat.md`, `.skill.md`, generated `qat/runtimes/claude/<name>/SKILL.md`, and `qat/cases/<name>.eval.yaml`.

| Tool / paste block | Minimal inputs | Output |
|---|---|---|
| [ResumeTailor](../qat/runtimes/chatgpt/resume-tailor.paste.md) | `evidence: E1: Assisted with testing a SQL inventory report.` and `target: L1: SQL required; Python preferred.` | Evidence/gaps, before/after edits with source IDs, facts to confirm; cover letter only when `request` explicitly asks |
| [InterviewCommander](../qat/runtimes/chatgpt/interview-commander.paste.md) | `target: L1: Explain a debugging example.` and optionally `evidence: E1: I wrote a diagnostic query; the team fixed the import.` | Grounded story frames, hypothetical rehearsal or feedback on a supplied answer, questions to assess the employer on six axes |
| [ReflectiveJobNote](../qat/runtimes/chatgpt/reflective-job-note.paste.md) | `notes: N1: They mentioned weekend support; frequency unclear.` and optionally `context: P1: I need predictable weekends.` | Reported observations, reactions/hypotheses, practice lessons, proposed criteria changes and optional artifact feedback |

The native audit/eval path is identical for each tool. For example, from `qat/`:

```sh
python3 -I scripts/qat.py validate tools/resume-tailor.qat.md
python3 -I scripts/qat.py audit resume-tailor eval-runs/2026-11-23/resume-tailor/cold.md
python3 -I scripts/qat.py eval cases/resume-tailor.eval.yaml eval-runs/2026-11-23/resume-tailor
```

Substitute `interview-commander` or `reflective-job-note` for the other tools. These evaluate authored fictional examples, not model executions. Each companion eval returns **3: incomplete** with 10 semantic criteria pending. The [port comparison](JOBHUNTER_PORTS.md) records historical behavior retained versus deliberately excluded; the [verification record](../qat/eval-runs/2026-11-23/JOBHUNTER_COMPANIONS_VERIFICATION.md) records actual checks.

## Explicit, optional interoperability

The workflow is non-linear. No output is automatically fed to another tool, no tool requires another, and nothing writes a second ledger. To transfer material, copy the relevant sections and original evidence/source IDs into the named input; label prior model output as derived. Original facts should travel with a derived claim where available; otherwise retain “source unavailable.”

| From | User-controlled transfer | What stays separate |
|---|---|---|
| JobIntelParser | Copy selected dossier sections into a companion's optional `context`; paste original requirements as ResumeTailor `target` or InterviewCommander `target` | Parser analysis never establishes candidate credentials or employer facts beyond its sources |
| ResumeTailor | Copy a proposed edit plus its original evidence into InterviewCommander `evidence`, labeling the edit as derived | A rewritten bullet is not new corroboration or proof of a result |
| InterviewCommander | Supply actual recollections/answers to ReflectiveJobNote `notes`; preparation sheet may go in `context` | Hypothetical practice questions are not events that occurred |
| ReflectiveJobNote | Manually carry a confirmed proposed criterion to JobIntelParser `priorities`, or confirmed story facts to tailoring/preparation | Proposals remain unaccepted until the user decides; no ledger, criteria or source artifact is automatically updated |

A dossier can be revisited after reflection, and rehearsal can expose a fact that needs clarification before tailoring. The user chooses the order or uses only one tool.

Later integration candidates, deliberately outside this slice:

- Employer-first search and two-pass Upwork discovery: user-controlled discovery inputs/adapters, with explicit scope and evidence provenance; no scraping, connectors or automation here.
- Optional intake/fit profile: user-supplied priorities along the six independent axes. Never a mandatory questionnaire or prestige-based composite score.
- Modular résumé evidence bank: explicit evidence IDs and candidate-confirmed facts for tailoring and stories. No personal evidence bank committed or created here.
- Application-form inventory: user-supplied questions/requirements with original wording; no form filling or submission.
- Career Compass opportunity ledger: future explicit export to the user's existing ledger, not another ledger. This implementation stores nothing and performs no synchronization.

Keep intellectual fit, demonstrated qualifications, organizational authority, resources, structure/sustainability and compensation independent throughout every future adapter.
