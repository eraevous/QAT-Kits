# JobIntelParser 0.1.0: offline fixture/contract evidence

Date: 2026-11-23. Author: Codex. Both new `.qat.md` and `.skill.md` versions: 0.1.0. All six inputs and outputs are fictional, design-time fixtures authored in the implementation session. **No cold model execution, paid model call, independent semantic grading or app installation test was performed.** These outputs demonstrate the expected shape, not measured model performance.

From `qat/`:

```sh
python3 -I scripts/qat.py validate tools/job-intel-parser.qat.md
python3 -I scripts/qat.py audit job-intel-parser eval-runs/2026-11-23/job-intel-parser/ordinary.md
python3 -I scripts/qat.py eval cases/job-intel-parser.eval.yaml eval-runs/2026-11-23/job-intel-parser
```

- `validate`: exit 0, OK.
- `audit`: exit 0, OK.
- `eval`: exit 3, **INCOMPLETE**, zero mechanical failures; 13 judged criteria ungraded. No judgments file is supplied and no semantic PASS is claimed.

| Case | Contract + regex | Semantic judgments |
|---|---|---|
| ordinary | PASS | 3 pending |
| conflicting-terms | PASS | 2 pending |
| prestige-and-gaps | PASS | 2 pending |
| embedded-instructions | PASS | 2 pending |
| thin-input | PASS | 2 pending |
| vague-and-partial | PASS | 2 pending |

`python3 -I qat/scripts/test_job_intel.py -v` from repository root: 5 tests pass. They cover all six fixture shapes, all eight missing-section failures, identical runtime procedures, incomplete semantic status, and six deliberately mutated outputs rejected by pattern checks. They do not prove that a model follows the procedure. Initial test implementation mistakenly called the runner's `code` property as a method; fixed before this recorded passing result.

For independent evaluation, provide only the new spec and each case's input (expanding the fixture reference) to a fresh model session, save fresh outputs, then grade every YAML `judge` criterion. Record exact output and criterion hashes via the existing runner judgment format. Repeat separately for an installed runtime if assessing installation behavior. Leave failures visible; author self-grades cannot complete the independent gate.

## Repository verification

- From `qat/`: `python3 -I -B -m unittest discover -s scripts -p 'test_*.py'` — exit 0, **143 tests passed**. Existing AutoEDA tests emitted matplotlib/font-cache and numerical warnings; no test failed.
- From root: `python3 -I qat/scripts/test_skills.py -v` — exit 0, **30 tests passed**.
- From `qat/`: `python3 -I scripts/qat.py index` — exit 0, 9 tools indexed; four existing lossy-coercion warnings in unrelated handoffs. The new tool declares no handoff.
- From root: `python3 -I qat/scripts/skills.py build` — 15 skills, bundle 1.3.0.
- `python3 -I qat/scripts/skills.py check --base origin/main` — exit 0, zero errors.
- `python3 -I qat/scripts/skills.py package /tmp/jobhunter-qat-1.3.0` — exit 0, plugin plus 15 skill zips. Local package only; no release/deploy.
- `git diff --check` — exit 0.
- `python3 -I -m aec --help` — unavailable: `No module named aec`. Local Telosmith records/code-impact checks were not run; existing CI remains responsible for them. No existing runner/generator code or records changed, so their implementation claims remain unchanged; the new test module is not an implementation change to those claims.

The CI workflow now runs the five offline acceptance tests using the runner's existing `pyyaml` and `jsonschema` dependencies. There are no new tool runtime dependencies.
