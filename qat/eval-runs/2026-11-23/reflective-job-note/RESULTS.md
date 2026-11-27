# reflective-job-note 0.1.0: offline acceptance evidence

Date: 2026-11-23. Author: Codex. Contract and standalone skill versions: 0.1.0. Five fictional inputs and outputs authored during implementation. **No cold model run, independent semantic grading, paid model call or app installation test performed.**

From `qat/`:

```sh
python3 -I scripts/qat.py validate tools/reflective-job-note.qat.md
python3 -I scripts/qat.py audit reflective-job-note eval-runs/2026-11-23/reflective-job-note/cold.md
python3 -I scripts/qat.py eval cases/reflective-job-note.eval.yaml eval-runs/2026-11-23/reflective-job-note
```

Validation and audit: exit 0. Eval: exit **3, INCOMPLETE**, with five mechanical fixture passes and **10 semantic criteria ungraded**. These results are verified by `test_jobhunter_companions.py`; see [the combined verification record](../JOBHUNTER_COMPANIONS_VERIFICATION.md) for executed commands/results. No semantic PASS is claimed and no judgments file is supplied.

For semantic evaluation, run each input in a fresh context containing only the spec, then independently grade every YAML judge criterion using the existing runner's output/criterion hash-bound `--judgments` format. Author grades remain provisional. Installed runtime behavior and cross-provider consistency also need evaluation.
