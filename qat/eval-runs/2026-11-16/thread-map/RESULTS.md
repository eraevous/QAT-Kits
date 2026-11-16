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

## Round 2: after Kate's review (`v0.1-r2/`), reported separately

Kate (API instance, reply 9580bf77e377) found two blocking problems and asked for a looser segmentation check. The spec version stays 0.1.0, because the spec is new and unmerged. Changes:
- **Authority for revisions.** `revision-is-not-loss` now requires authority over the original commitment. A model's change to a user's commitment is a proposal, not a revision, until the user accepts it.
- **Status rules.** `continuing-is-not-adopting` reserves user statuses for the user's own words. `agreed (models)` now needs models explicitly agreeing with each other.
- **Evidence of omission.** An `evidence:` warning now needs a later passage that created the expectation: a design meant to meet the requirement, a recap presented as complete, or a promised return. Otherwise the item is carried as `open`. Procedure step 3 was changed to match.
- **Segmentation.** By default a reversal or deferred question stays inside its segment. The judge criterion no longer grades the exact count. It checks ordered coverage, real boundaries, named pivots and no fragmentation. (It previously expected three segments.)
- **Compatibility note.** It now says "candidate translation, subject to transcript verification" instead of "map directly". It also states that `carry-statuses` checks structure, not semantic compatibility.

A new cold run on the final text by a fresh subagent, which saw only the spec and the inputs:

| Case | Deterministic | Judge (self-graded) |
|---|---|---|
| dropped-requirement | PASS | PASS: 3 segments (rota / sensors aside / rota revised and design). The switch to fortnightly and the deferred reminder question are named as pivots in the narrative. |
| revision-not-loss | PASS | – |
| single-topic | PASS | – |
| carry-statuses | PASS | – |

All four outputs pass `qat.py audit`. No case was edited after this run. Ambiguities the runner reported that are still open (v0.2 candidates):
- the line between `decided (user)` and `wanted (user)`;
- no status for "parked";
- implicit acceptance ("Fine with that" vs "OK, sketch it");
- whether every model proposal is carried;
- whether an item can be both warned and carried as open;
- a contiguous Turns column after a return from an aside;
- the pointer range format;
- how much an objective may change.

## Case fixes after Codex review (no spec change, no new run)

Codex's review of a3e3d76 raised two P2 findings against the cases. Both were verified and fixed:
- **4592342386.** The "weekly carried as decided" exclusion looked for replacement wording only *after* "weekly". So it would have failed a valid line such as "Fortnightly rota replaces weekly fixed days [T3u]; decided (user); T6u". The same flaw was in the matching warnings exclusion. Both now look across the whole line.
- **4592342398.** carry-statuses checked a pointer on every item but not a status, although the compatibility note claims both. A per-item status check was added.

Both recorded runs (`v0.1/`, `v0.1-r2/`) were re-graded on the fixed cases: 4/4 PASS each. Neither recorded output had a line the old patterns misjudged. So these fixes tighten the cases without changing any result.

## Case fixes after Copilot review (no spec change, no new run)

Copilot's review raised two medium findings against the cases. Both were verified and fixed:
- **4592570535.** The per-item status check matched a status word anywhere in the line. So "- No login: open a link and tap a name; T2u" passed because it contains "open". The check now requires the status as a semicolon-delimited field.
- **4592570615.** The sensors exclusion looked for parking wording only after "sensor". So it would have failed "- Park soil moisture sensors; decided (user); T5u". The check now looks across the whole line.

Both recorded runs (`v0.1/`, `v0.1-r2/`) were re-graded: 4/4 PASS each, so no result changed.
