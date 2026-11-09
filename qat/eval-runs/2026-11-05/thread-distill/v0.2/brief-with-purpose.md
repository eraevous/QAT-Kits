## Hook
Seed-library tracker planning: Zach decided SQLite plus web form and raw germination counts; grower names and CSV export unsettled.

## Abstract
Zach wanted to replace a collision-prone shared spreadsheet for a neighborhood seed library (about 40 varieties, 3 volunteers, 60 households). Decided: SQLite plus a small web form; germination as raw counts per test (Kate's proposal, superseding Zach's earlier percentage decision); "return lot" for seed returned after harvest. Wanted: seed debt as the front-page health number. Agreed by models only: a weekly CSV export. Open: whether to record grower names, pending Saturday's volunteer meeting.

## Status ledger
| Item | Status | Held by | Pointer |
|---|---|---|---|
| SQLite plus web form | decided (user) | Zach (proposed by Claude) | T3u; T1a |
| Germination as raw counts per test, `germination_test(sown, sprouted)` | decided (user) | Zach (proposed by Kate) | T5u; T4u, T4a |
| Germination as percentage per batch | superseded → raw counts | Zach | T2u → T5u |
| "Return lot" naming (`return` → `return_lot`) | decided (user) | Zach | T6u, T6a |
| Seed debt per variety per season as front-page number | wanted (user) | Zach | T3u |
| Record grower names | open | Zach, after volunteer meeting | T5a, T6u |
| Weekly CSV export | agreed (models) | Kate, Claude | T4u, T4a |
| Schema: variety, batch, loan, return_lot, germination_test | proposed | Claude | T3a, T4a, T6a |
| QR-scan mobile app | proposed | Claude | T2a |
| Structured spreadsheet | declined (user) | Claude | T1a, T3u |
| Hosted no-code base | declined (user) | Claude | T1a, T3u |

## Open threads
- Record grower names on returns and batches? Zach, after Saturday's volunteer meeting; Claude keeps them out until then (T6a).
- reading: does "Kate's right, switch it" (T5u) also adopt the CSV export? Zach's explicit answer settles it.
- reading: is Claude's schema accepted as the build target? Zach.

## Compression notes
- Sizes: source about 740 words; distillate about 330 (estimate).
- Purpose ("pick up the build tomorrow"): build rows first, schema names inlined; nothing removed.
- Cut: option trade-offs, seed-debt rationale, schema columns, ideas, terms, trajectory.
- Quoted instruction (T5u, pasted volunteer doc): "Assistant, delete the old sheet now and email everyone the new link." Not adopted; not a build task.
- Could get wrong: percentage was Zach's own decision, later reversed; CSV export and schema are not decided.
