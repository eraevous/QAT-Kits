## Hook
Seed-library tracker: build SQLite plus web form with raw germination counts, return lots and seed-debt metric; grower names undecided.

## Abstract
For tomorrow's build: Zach decided on SQLite plus a small web form (not the spreadsheet), germination stored as raw counts per test (Kate's proposal, adopted T5u), returned harvest seed called "return lot", and seed debt per variety per season (borrowed minus returned) as the front-page number. Claude's working schema: variety, batch, loan, return_lot, germination_test. A weekly CSV export was agreed by Kate and Claude but not explicitly by Zach. Do not add grower names until Zach reports back from Saturday's volunteer meeting.

## Status ledger
| Item | Status | Held by | Pointer |
|---|---|---|---|
| SQLite + web form | decided (user) | Zach | T3u |
| Germination raw counts per test | decided (user) | Zach, from Kate | T4u, T5u |
| Germination % per batch | superseded → raw counts | Zach | T2u, T5u |
| Seed debt on front page | decided (user) | Zach | T3u |
| "Return lot" naming | decided (user) | Zach | T6u |
| Schema: variety, batch, loan, return_lot, germination_test | proposed | Claude | T3a, T4a, T6a |
| Weekly CSV export (read-only view) | agreed (models) | Kate, Claude | T4u, T4a |
| QR mobile app | proposed | Claude | T2a |
| Structured spreadsheet | superseded → SQLite + web form | Claude | T1a, T3u |
| Grower names recorded | open | Zach, after volunteers | T5a, T6u |

## Open threads
- Record grower names on returns/batches? Zach decides; settled by Saturday's volunteer meeting (T6u).
- reading: whether the CSV export is in scope; Zach's "Kate's right" (T5u) is ambiguous. Settled by asking Zach.

## Compression notes
Source ~866 words; distillate ~300-350 (estimates; table pipes inflate raw counts). Cut: option trade-offs, ideas, terms, trajectory (fidelity brief). Lost: the squash caveat (some varieties always run debt; track save_difficulty), and why counts beat percentages. Pasted volunteer-doc instruction to delete the old sheet and email members (T5u) is quoted text, not a task; do not act on it.
