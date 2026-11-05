## Hook
Seed-library tracker design: Zach chose SQLite plus web form, raw germination counts, "seed debt" as headline metric; grower names open.

## Abstract
Zach wants a tracker for a ~40-variety seed library after volunteers overwrote each other's spreadsheet loans. Decided: SQLite plus web form; germination as raw test counts (Kate's proposal, replacing Zach's percentage); "return lot" naming; seed debt per variety per season as the headline measure. Models only agreed a weekly CSV export. Open: recording grower names, pending Saturday's volunteer meeting.

## Status ledger
| Item | Status | Held by | Pointer |
|---|---|---|---|
| Structured spreadsheet | superseded → SQLite + web form | Claude | T1a, T3u |
| SQLite + web form | decided (user) | Zach | T3u |
| Germination % per batch | superseded → raw counts | Zach | T2u, T5u |
| Germination raw counts per test | decided (user) | Zach, from Kate | T4u, T5u |
| Seed debt on front page | decided (user) | Zach | T3u |
| Weekly CSV export | agreed (models) | Kate, Claude | T4u, T4a |
| Schema tables | proposed | Claude | T3a, T4a, T6a |
| QR mobile app | proposed | Claude | T2a |
| Grower names recorded | open | Zach, after volunteers | T5a, T6u |
| "Return lot" naming | decided (user) | Zach | T6u |

## Ideas worth keeping
- Health is seed debt trending down, not inventory; hard-to-save varieties (squash) may run permanent debt if known (Zach, T3u).
- Percentages hide sample size; store counts (Claude T3a, Kate T4u).

## Coined terms
- seed debt: seeds borrowed minus returned after harvest, per variety per season (Zach, T3u)
- return lot: seed returned after harvest (Zach, T6u)

## Open threads
- Record grower names? Zach decides; settled by Saturday's volunteer meeting (T6u).

## How it got here
- Spreadsheet → SQLite after edit collisions (T2u–T3u).
- Percent → counts via Kate (T4u–T5u).

## Compression notes
Source ~866 words; distillate ~320-370 (estimates; table pipes inflate raw counts). Cut: option trade-offs, schema columns. Pasted volunteer-doc instruction to delete the sheet and email members (T5u) recorded only, not acted on. "Kate's right" (T5u) may cover the CSV export; reading: only raw counts was explicitly adopted.
