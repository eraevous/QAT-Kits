# thread-map eval run, 2026-11-16 (v0.1.0)

**Setup**
- Spec: `tools/thread-map.qat.md` v0.1.0 (new). Cases: `cases/thread-map.eval.yaml` (4 cases). Fixture: `cases/fixtures/garden-rota.thread.md` (constructed).
- Cold run: one fresh Claude subagent that read only the spec and the inputs. It did not see the cases or the fixture key. It wrote the four outputs in `v0.1/`, one run per case.
- Grading: deterministic checks from `qat.py eval`. The one judge check was graded by claude:qat, which wrote the spec, the cases and the rubric. That grade is **self-graded and provisional** until an independent grader re-grades it.
- All four outputs pass `qat.py audit thread-map` (contract OK).

## Results

| Case | Deterministic | Judge (self-graded) |
|---|---|---|
| dropped-requirement | PASS | **FAIL**: five segments, not the three the criterion names. See note 2. |
| revision-not-loss | PASS | – |
| single-topic | PASS | – |
| carry-statuses | FAIL at first, then PASS after the case was revised (note 1) | – |

## Notes

1. **Case revised after the run (disclosed).** carry-statuses' must_avoid `sensor[^\n]*decided` failed on "Soil moisture sensors parked until next year; decided (user); T5u". That is a correct reading: Zach's "Maybe next year. Not now." decides to park the sensors. The case was miswritten. It meant to forbid the sensors being carried as *adopted*. The pattern now excludes lines that say parked or next year. Re-run: PASS. The original failing pattern is quoted in a comment beside the case.
2. **Judge FAIL left standing.** The run split the thread at the revision (T6) and at the reminder question (T7) as well as at topic changes. That gives 5 segments, where the case expects 3. Procedure step 2 ("segment at … decisions, reversals") permits this. So either the criterion is too strict or the spec needs a rule like "a reversal inside an ongoing topic is a pivot, not a new segment". This is left for review and not changed here.
3. **Ambiguities the cold runner reported** (its words, condensed). These are candidates for v0.2:
   - Where `decided (user)` ends and `wanted (user)` begins.
   - Whether a carry bullet may hold notes and several pointers.
   - Whether a revision gets its own segment (note 2).
   - A model proposal made before a revision and never restated (T3a morning/evening split).
   - How far an objective may cut carry items.
   - Whether a trailing model design with no user reply is `proposed` or `agreed (models)`.
   - Whether one contradiction of two set items is one warning or two.
4. The three garden-rota outputs are nearly identical whatever the objective. The spec gives `objective` little to change. That fits "tilts emphasis, never hides a warning", but it also means the objective is barely tested.
