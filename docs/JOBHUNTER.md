# JobHunter: first runnable slice

Status: JobIntelParser **0.1.0 candidate**, bundle **1.4.0**. This is a chat-executed prompt tool, with offline contract acceptance tests. It makes no network or model API calls. Semantic quality has **not** been independently evaluated.

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

The JSON is a mapping of the eight declared fields to bullet lists, suitable for explicit future adapters. The audit checks section presence and bullet shape, not whether quotations, facts or reasoning are correct. No automated downstream handoffs are registered because the other three native contracts do not yet exist.

For a fully offline smoke test on the included fictional fixture:

```sh
python3 -I scripts/qat.py audit job-intel-parser eval-runs/2026-11-23/job-intel-parser/ordinary.md
python3 -I scripts/qat.py eval cases/job-intel-parser.eval.yaml eval-runs/2026-11-23/job-intel-parser
```

The second command must exit **3**, incomplete: all six authored examples pass mechanical checks, but 13 semantic judgments remain ungraded. These are design-time exemplars, not cold model outputs. See [RESULTS.md](../qat/eval-runs/2026-11-23/job-intel-parser/RESULTS.md). To complete semantic evaluation, produce fresh outputs from only the spec and each expanded input, then have an independent reviewer grade every YAML `judge` criterion using the runner's hash-bound `--judgments` format. Keep failures visible. The repository also requires independent review followed by fresh-context execution review before the owner merges.

## Scope and provenance

The historical four tools already exist under `Toolkits/Job Hunter Arsenel/`. They are left untouched, as required by AGENTS.md. The new native implementation narrows JobIntelParser to supplied-text analysis; it does not carry forward historical company lookup, guessed recruiter/ATS priorities, or automatic pipeline/cache behavior. Current main was checked at `47b16ab1ad399c2362705b10936373d94cddf5cd`; no native JobHunter contracts or skills existed. There is no `.agents/skills/` directory in this checkout. NegativeSpace overlaps omission analysis, but does not provide the listing/screener, modality-preserving, six-axis dossier contract.

Authoritative procedure: `qat/tools/job-intel-parser.qat.md`. The standalone `.skill.md` and ChatGPT paste adaptation currently carry the identical procedure, enforced by `test_job_intel.py`; Claude files are generated using the existing build system. Edit sources and adaptations together, never generated files. New versions follow CONTRIBUTING.md's eval gates. No runner implementation, existing spec, record, dependency, or legacy tool was changed.

## Integration map (not built)

The workflow is non-linear. Each future tool must work on direct user input without the other tools, while allowing explicit, optional evidence transfers. Reflection can revise search criteria or trigger a fresh listing analysis; tailoring can expose gaps worth rehearsing; interview questions can send the user back to clarify a listing. No tool automatically advances or writes a second ledger.

| Tool | Proposed standalone input → output | Required acceptance evidence before shipping |
|---|---|---|
| ResumeTailor | Supplied evidence + target text, optionally a dossier → evidence-linked reframes, unsupported requirements/gaps, optional cover-letter draft | No invented credentials/metrics; preserve level of contribution; distinguish no evidence from no capability; never claim a draft was submitted |
| InterviewCommander | Supplied stories/experience + target questions or listing → grounded story outlines, rehearsal prompts/feedback, employer questions | Mark missing story details for the candidate; no fabricated outcomes; separate candidate demonstration from authority/resources/sustainability questions |
| ReflectiveJobNote | Supplied interview recollections and reactions → observation/interpretation split, lessons, proposed search-criteria/story changes | No invented interviewer motives; reactions stay distinct from facts; changes are suggestions, not automatic ledger edits or outreach |

These three have **no new native implementations in this PR**. Their contracts need separate evidence-sensitive cases and cold semantic evaluation; expanding all four while that remains pending would give a misleading impression of a validated suite. Legacy descriptions remain historical, not newly tested deliverables.

Later integration candidates, deliberately outside this slice:

- Employer-first search and two-pass Upwork discovery: user-controlled discovery inputs/adapters, with explicit scope and evidence provenance; no scraping, connectors or automation here.
- Optional intake/fit profile: user-supplied priorities along the six independent axes. Never a mandatory questionnaire or prestige-based composite score.
- Modular résumé evidence bank: explicit evidence IDs and candidate-confirmed facts for tailoring and stories. No personal evidence bank committed or created here.
- Application-form inventory: user-supplied questions/requirements with original wording; no form filling or submission.
- Career Compass opportunity ledger: future explicit export to the user's existing ledger, not another ledger. This implementation stores nothing and performs no synchronization.

Keep intellectual fit, demonstrated qualifications, organizational authority, resources, structure/sustainability and compensation independent throughout every future adapter.
