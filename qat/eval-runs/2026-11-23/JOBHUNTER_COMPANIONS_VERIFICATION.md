# JobHunter companions: verification record

2026-11-23, Codex. ResumeTailor, InterviewCommander and ReflectiveJobNote 0.1.0; bundle 1.4.0. Stack base: parser head `220cdbdcbdcd42ecea78fb7cfab9e3d0e1a66a8e` on `feat/jobhunter-dossier`. No changes to parser sources, cases, outputs or tests; PR #37 remains separate and untouched.

## Executed checks

From `qat/`:

```sh
MPLCONFIGDIR=/tmp/qat-jh-mpl XDG_CACHE_HOME=/tmp/qat-jh-cache python3 -I -B -m unittest discover -s scripts -p 'test_*.py'
```

Exit 0: **148 tests passed** (includes 30 generator tests, five parser tests and five companion tests). Existing AutoEDA extreme-number cases emitted numerical warnings; no failures. Temporary cache paths avoid unwritable home directories.

For each of `resume-tailor`, `interview-commander`, `reflective-job-note`, these exact command forms were executed from `qat/`:

```sh
python3 -I scripts/qat.py validate tools/<name>.qat.md
python3 -I scripts/qat.py audit <name> eval-runs/2026-11-23/<name>/cold.md
python3 -I scripts/qat.py eval cases/<name>.eval.yaml eval-runs/2026-11-23/<name>
```

All validates/audits exit 0. Each eval exits **3: INCOMPLETE**, with five mechanical fixture passes and 10 ungraded judge criteria. Totals: **15 mechanical passes, 30 semantic criteria pending**. These are authored fictional examples, not outputs from cold model execution. No semantic results, independent verification or cross-provider execution are claimed.

From repository root:

- `python3 -I qat/scripts/test_jobhunter_companions.py -v` — five tests pass: all three contracts/15 fixture shapes, provider procedure parity, all 19 missing-section failures, incomplete status, 11 deliberate mutations.
- `python3 -I qat/scripts/qat.py index` — exit 0, 12 tools indexed; same four unrelated existing lossy-coercion warnings.
- `python3 -I qat/scripts/skills.py build` — 18 skills, bundle 1.4.0.
- `python3 -I qat/scripts/skills.py check --base feat/jobhunter-dossier` — exit 0, zero errors.
- `python3 -I qat/scripts/skills.py package /tmp/jobhunter-qat-1.4.0` — exit 0; plugin and 18 per-skill archives. All SHA256SUMS verified; each new single-skill archive contains its own SKILL.md and passes ZIP integrity checks. Local artifacts only, no release or installation.
- `git diff --check` — exit 0.
- `git diff --exit-code feat/jobhunter-dossier --` with parser source, cases, eval-output, test and runtime paths — exit 0; parser unchanged.
- `python3 -I -m aec --help` — unavailable locally (`No module named aec`). Existing Telosmith and Kairos CI remain the checks for records/code impact. No existing implementation code or records were edited; their implementation claims remain unchanged.

One initial mutation test exposed a regex that could match “Assisted” in an evidence annotation after a bad “Led” rewrite. Tightening it to the text immediately after `After:` fixed that blind spot; a transient YAML quoting error during the fix was corrected. The final full suite above passed.

## Outstanding verification

Independent semantic execution/grading, installed-app behavior, independent review and fresh-context execution review remain pending. The run directories retain that incomplete status rather than supplying author judgments as independent evidence. No paid model calls, private source material or actual candidate/application history were used. The integration map and historical comparison are in `docs/JOBHUNTER.md` and `docs/JOBHUNTER_PORTS.md`.
