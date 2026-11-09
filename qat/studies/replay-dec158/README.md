# Blind replay: real-problem and kind-check (DEC-158 item 2)

**Status:** packet prepared, nothing run. Producers, normalizer and graders have not been run; Kate's grading is relayed by the coordinator, not run from here.

## Question
Does each tool reduce the work needed to reach a defensible disposition, without increasing:
- incorrect commitments,
- unnecessary actions, or
- the number of disputes the owner has to settle?

## What is in this folder
| path | what |
|---|---|
| `items/<tool>.items.json` | 20 constructed items per tool (6 easy, 8 medium, 6 hard). No keys. |
| `keys/<tool>.key.json` | reference answers written before any run, with acceptable alternatives and traps |
| `assignment.json` | who grades what, in which arm, under which opaque id (`replay.py assign --seed 158`) |
| `prompts/producers.md` | arm A (plain) and arm B (tool) producer prompts; the normalizer prompt |
| `graders/` | shared rubric; instructions for a fresh Claude grader and for Kate |
| `runs/`, `grades/` | empty until run |

## Sanitization
All 40 items are constructed for a fictional project ("Lantern", one owner, agent-A, agent-B). None is copied from a real conversation, ledger or employer system. They keep the diagnostic structure of failure patterns seen in practice:
- a proposal or relayed remark recorded as adopted;
- a concern treated as an established problem;
- an observable or tripwire that looks the same whether or not the failure is happening;
- a classification forced where the item is mixed or too thin;
- work manufactured for items that need none.

## Design
1. **Two arms, every item produced in both.** A = plain prompt, B = the tool's runtime text. Same model, same lightest setting, fresh contexts.
2. **Normalized cards.** A separate context rewrites every response into five neutral lines (verdict, actions, commitments, escalation, uncertainty), so the tool's headings don't reveal the arm.
3. **Counterbalanced, within-item, cross-grader.** Items are split into two halves balanced by stratum. The Claude grader sees half 1 in arm A and half 2 in arm B (reversed for the second tool); Kate sees the complement. So each grader:
   - sees every item exactly once,
   - never sees the same item both ways,
   - grades 10 cards per arm;
   - and every item is graded in both arms, by different graders.
4. **Keys are visible to graders and disputable.** Every grader judges every item's key, so the graders' agreement on keys is measured on all 20 items without either grader seeing both arms.
5. **The owner adjudicates only disagreements:** items where the graders split on the key, or both dispute it. The queue's length is part of the result.
6. **Blinding check:** graders guess the arm after grading; `tally` reports how often they were right.

## Measures (per arm, from `replay.py tally`)
| measure | from |
|---|---|
| defensible yes / partly / no | grades |
| corrections needed (0 / 1 / 2+) | grades; the main "work to a defensible disposition" proxy |
| incorrect commitments | grades |
| unnecessary actions or escalations | grades |
| missed abstentions | grades |
| invented details | grades |
| words in the raw response | word count of `runs/<tool>/raw/` |
| owner adjudications | the queue |

**Limit:** model effort is not human attention. This estimates deliberation and correction saved, not the owner's minutes.

## Decision rule (fixed before any run)
Arm B is better for a tool if **all** of these hold:
- arm B needs fewer total corrections than arm A, or has more `defensible: yes`;
- arm B has no more incorrect commitments, unnecessary actions or missed abstentions than arm A;
- the adjudication queue is no longer than 4 items (20%) for that tool.

With 20 items per tool these are counts, not significance tests. Report results twice: all items, and excluding the 6 items per tool that also appear in the design-time evals (`seen_in_design` in the keys; `tally --exclude-seen`).

## How to run
From `qat/`:
1. Producers: follow `prompts/producers.md` for both tools and both arms; save to `runs/<tool>/raw/{A,B}/`.
2. Normalizer: same file; save to `runs/<tool>/cards/{A,B}/`; spot-check five.
3. Packets: `python3 -I scripts/replay.py packet --grader claude --tool real-problem -o <file>` (and for kate, and for kind-check).
4. Graders: `graders/grader-claude.md` (fresh Claude); `graders/grader-kate.md` (relayed by the coordinator).
5. `python3 -I scripts/replay.py tally --tool real-problem` (and `--exclude-seen`); the same for kind-check.
6. The owner adjudicates the queue; record adjudications next to the grades.

Graders get only the packet and the rubric, never this folder: `assignment.json` would unblind them.
