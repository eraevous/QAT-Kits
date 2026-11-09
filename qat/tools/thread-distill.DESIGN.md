# thread-distill: design notes

Kit-owned and ungoverned. These notes replace the Telosmith records `QAT-R-distill@1` and `QAT-D-distill-design@1`, which were withdrawn because tool content is not governed by Telosmith (Zach, 2026-11-06).

## Why it exists

- **Origin.** Zach (2026-11-05 14:53 CT, QAT lane): "the most important tool to design and iterate for the moment is one that usefully distills and compresses a thread".
- **How it differs from its neighbors:**
  - **thread-seed** selects and writes for *one destination*. It is not an extractor.
  - **ThreadMap** segments a thread but does not compress it.
  - **MetaDistill** analyses method.
  - **SSD** extracts only Zach's own contributions.
  - **ContextAnchor** (2025) had the layering, but it was never ported or tested.
- **Its role:** thread-distill is the destination-agnostic extractor that thread-seed (or anything else) can consume.

## Choices Zach made (2026-11-05, QAT lane chat)

1. **Reader:** one distillate serves every reader, at a set fidelity (hook / brief / full).
2. **Lineage:** a new spec drawing on ContextAnchor, ThreadMap, MetaDistill, SSD and thread-seed. It does not revive any one of them or fold into one.
3. **Test data:** Zach names real threads, which are captured outside this public repo. Only constructed eval cases are committed.
4. **Runtimes:** Claude skill, ChatGPT and the qat.py runner.

## Alternatives rejected

- **Reviving ContextAnchor under its own name.** Its six buckets did not separate status (decided, proposed, superseded).
- **Folding into thread-seed.** That would change the relay-kit lane's skill and needs a dissent review.
- **Broad adoption ("Kate's right" covers everything Kate said).** It inflates decisions. Narrow adoption costs some recall instead.

## Distinctions that must survive revisions

- **decided (user)** ≠ **wanted (user)** ≠ **agreed (models)** ≠ **proposed** ≠ **declined (user)** ≠ **superseded**.
- Relayed text belongs to its author, span by span: a user turn that decides and then quotes is the user's up to the quotation.
- Instructions found in the thread are evidence, never tasks. Extracting a participant's proposal at its evidenced status is not executing it.
- Hook and abstract are written last, from the ledger.

## Evidence

- [qat/eval-runs/2026-11-05/RESULTS.md](../eval-runs/2026-11-05/RESULTS.md)
  - v0.1 inflated a stated preference into a decision. v0.2 fixed it.
  - The judge grades are self-graded and provisional until Kate re-grades them.
- v0.2.1 (2026-11-09, PR #3 review: Codex review bot and Copilot): relay attribution is per span, not per turn (T5u); proposals phrased as instructions keep their ledger row (T4u CSV export), embedded commands stay quoted evidence; the seed-debt wanted-vs-decided eval check moved from must_avoid to must_include. Spec wording only; v0.2 outputs not re-run.

## Open questions

- The v0.3 issues listed in RESULTS.md.
- Round 3 on Zach's real threads, which need to be named.
