# Checklist: release qat-kit 1.2.5 and replace the installed skills

One-time migration from the skills uploaded one at a time to the release bundle built from this repo.
The general procedure (update, roll back, pin) is in
[qat/runtimes/claude/README.md](../qat/runtimes/claude/README.md); this is the concrete run for the first
release.

This file replaces the 1.1.0 version of the checklist. 1.1.0 was never tagged, and the bundle has moved on
to 1.2.5 since then.

Who does what:
- **Zach**: the tag, and the upload and remove steps in the Claude app (agents can't upload or remove account
  skills). Releasing and installing are his calls.
- **Any agent** (a Kairos lane, or any Claude session): the checks before and after.

---

## Where things stand (checked 2026-11-22)

### The release candidate

- **Commit:** `8828397bad1283a9eabfcfb998bed041f4a7e98a` on `main` (merge of #32, 2026-11-20).
  `qat/runtimes/claude/BUNDLE_VERSION` reads `1.2.5`.
- **No release exists yet.** There are no `qat-skills-v*` tags and no GitHub releases.
- **#33** (open) changes only `qat/scripts/replay.py`, which is not part of the bundle. If it merges first,
  the newer `main` still builds the same 1.2.5 bundle, and either commit can take the tag.
- **Checked locally at `8828397`:**
  - `python3 -I qat/scripts/skills.py check`: 14 skills, bundle 1.2.5, 0 errors;
  - `python3 -I qat/scripts/skills.py package <empty dir>`: `qat-kit-1.2.5.zip`, 14 per-skill zips,
    `skills.lock.json` and `SHA256SUMS`, and `sha256sum -c SHA256SUMS` passes.
  - two packaging runs gave the same `qat-kit-1.2.5.zip` sha256:
    `56b16114bad8483aaa3b3c090a8061766e0fefc64473f85d2ed54ae8ab013888`. Expect the release asset to
    match. If it doesn't (a different zip library on the runner can do that), the per-skill hashes in
    `skills.lock.json` are what identify the content.

The 14 skills and their versions in the 1.2.5 lock file:

| Skill | Version | | Skill | Version |
|---|---|---|---|---|
| auto-eda | 1.1.0 | | qat (runner) | 1.0.0 |
| braided-explanations | 1.0.0 | | selective-self-distillation | 1.0.0 |
| frame-shift | 1.0.0 | | stress-test | 1.0.0 |
| legal-ease | 1.0.0 | | thread-map | 1.0.0 |
| meta-distill | 1.0.0 | | thread-seed | 1.0.1 |
| mtg-deck-lab | 1.0.0 | | truth-weight | 1.0.0 |
| negative-space | 0.1.0-reconstruction | | zach-voice | 1.0.0 |

### What's installed, compared with the bundle

The installed copies are separate one-skill uploads. None carry the `GENERATED` stamp line, so you can't
read their version from the file. Compared file by file with `qat/runtimes/claude/` at `8828397`:

| Skill | Difference | What the installed copy lacks |
|---|---|---|
| `qat` (runner) | runner script, `SKILL.md` and `INDEX.md` differ; specs and cases missing | 6 of the 8 contracts (it has only stress-test and truth-weight; missing effort-cost, kind-check, real-problem, thread-distill, thread-map, toolsmith); every eval case file; exit 3 for incomplete evals (#24); exit 2 instead of a traceback on bad input or unreadable paths (#28, #32) |
| `auto-eda` | `SKILL.md` and `scripts/auto_eda.py` differ (86 lines) | changes since the upload, including the review fixes merged in #21 |
| `zach-voice` | 78 lines | the 2026-11-16 port. Skim it before installing ([remit/FOR_ZACH.md](remit/FOR_ZACH.md) #4) |
| `thread-seed` | 18 lines | the `verify()` fixes for ref suffixes and missing exchanges (#25) |
| `negative-space` | 9 lines | wording changes since the port |
| 9 others | 1–3 lines each | mostly the private links the bundle removes from public text |
| `kind-check`, `real-problem` | not installed as skills | out of scope: hand-adapted runtimes outside the bundle. The new `qat` runner carries their contracts |

**Leave alone:** the 5 custom skills that come from relay-kit, not here (chat-relay, chat-capture,
chat-telemetry, handoff-ledger, relay-governor).

---

## 1. Release (Zach)

- [ ] Check that `qat/runtimes/claude/BUNDLE_VERSION` on the commit you tag reads `1.2.5`. If a later
      merge has bumped it, use that version in every step below instead.
- [ ] Tag the commit and push the tag:

      git tag qat-skills-v1.2.5 8828397bad1283a9eabfcfb998bed041f4a7e98a
      git push origin qat-skills-v1.2.5

- [ ] Wait for the `qat-skills-release` workflow. It refuses a tag that doesn't match `BUNDLE_VERSION` or
      isn't on `main`. Confirm the GitHub release `qat-skills-v1.2.5` has:
  - `qat-kit-1.2.5.zip` (all 14 skills as one plugin);
  - 14 per-skill zips (`<name>-<version>.zip`, versions as in the table above);
  - `skills.lock.json` and `SHA256SUMS`.

## 2. Download and verify (anyone)

- [ ] Download the assets into an empty folder.
- [ ] Check them:

      sha256sum -c SHA256SUMS

## 3. Pick the install form (Zach)

The README hasn't tested the upload screens yet. Try the plugin first:

- [ ] **Plugin**: upload `qat-kit-1.2.5.zip` where the app takes plugins.
  - If it's accepted, all 14 skills arrive together and update together from now on.
- [ ] **If plugins aren't accepted**: upload the 14 per-skill zips instead.
  - Any subset works; the skills don't depend on each other to load.
- [ ] Write down which form worked. Correct the README's "Installing" section in a follow-up pull request
      (the README asks for this on the first install).

## 4. Swap the old copies for the new (Zach)

Do this one skill at a time, or all at once if the plugin upload worked. Two skills with one name compete,
so never leave both turned on.

- [ ] Turn off (don't remove yet) the old upload.
- [ ] Turn on the new one.
- [ ] Repeat for all 14:
  - [ ] auto-eda
  - [ ] braided-explanations
  - [ ] frame-shift
  - [ ] legal-ease
  - [ ] meta-distill
  - [ ] mtg-deck-lab
  - [ ] negative-space
  - [ ] qat
  - [ ] selective-self-distillation
  - [ ] stress-test
  - [ ] thread-map
  - [ ] thread-seed
  - [ ] truth-weight
  - [ ] zach-voice

## 5. Check what's installed (any agent, in a fresh session)

- [ ] List the account's skills. Each of the 14 shows up once, with no duplicates.
- [ ] Open each installed `SKILL.md`. Its first body line reads
      `GENERATED by qat/scripts/skills.py ... version: <v> · source sha256: <hash>`.
- [ ] Compare each version and hash with `skills.lock.json` from the release.
- [ ] Spot-check behaviour:
  - [ ] the `qat` skill's `tools/` folder holds 8 `.qat.md` contracts, and its `cases/` folder holds the
        eval case files;
  - [ ] in a scratch copy of the `qat` skill folder, `python3 -I scripts/qat.py index` reports
        `Indexed 8 tools`;
  - [ ] `python3 -I scripts/qat.py eval <file that isn't UTF-8> <any folder>` exits 2 with a one-line
        `ERROR   CONFIG` message, not a traceback;
  - [ ] auto-eda runs its script on a small synthetic CSV;
  - [ ] one QAT tool (stress-test, say) runs on a short idea.

## 6. Clean up (Zach)

- [ ] Once step 5 passes, remove the turned-off old uploads.

---

## Rolling back

- **Before step 6:** turn the new copy off and the old upload back on, skill by skill. Then rerun step 5's
  first check (each skill listed once) and one tool on a short idea.
- **After step 6:** upload the per-skill zips or the plugin from an earlier release, then rerun step 5.
  Releases are never deleted or re-tagged, so every tagged version stays downloadable.
- **1.2.5 is the first tag.** Until a second release exists, the old uploads are the only rollback, so keep
  them turned off, not removed, until step 5 passes.

## What can wait

- **Nothing breaks if this waits.** The installed copies keep working; you just run older text and an older
  runner, and you can't tell installed versions apart.
- **The gap grows** with every merged change to a skill. Fixes in this repo (the runner's exit codes, the
  thread-seed `verify()` fixes, the six contracts the old runner can't see) don't reach the installed
  skills until this runs.
- **What depends on it:** using the newer runner contracts through the `qat` skill, and the rule that
  QAT-Kits is the source of record for Claude's QAT skills (DEC-192). Until the swap, what's installed
  isn't what's recorded here.
