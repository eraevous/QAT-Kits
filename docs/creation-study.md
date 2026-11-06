# Tool-creation feasibility study (and Telosmith pilot observation log)

**What this study is.** A small feasibility study of how lightweight QAT tool creation can be. It is not a benchmark.

**Where it comes from.** It was agreed by Claude and Kate on 2026-11-05 and accepted by Zach on 2026-11-06 11:02 CT. The record of that is in relay-kit-private: `handoffs/outputs/qat-2026-11-05-telosmith-scope-debate.md`, items 2 and 4.

## The two arms

- **Arm A:** slim ToolSmith (`qat/tools/toolsmith.qat.md`), plus `qat.py validate`, plus runtime texts adapted by hand.
- **Arm B:** arm A, plus `qat.py new` (a scaffold command). `qat.py new` is not built yet.

## What each tool records

- **Human interventions:** each time Zach supplied or corrected something.
- **Correction cycles:** spec versions before the cold run passes.
- **First cold-run pass rate:**
  - deterministic checks;
  - judge checks, marked self-graded until someone independent grades them.
- **Effort:** wall-clock time, and the token cost of subagent runs.
- **Infrastructure-fix time:** time spent fixing the creation machinery or process rather than the tool. Kate asked for this one.
- **Learning effects:** what carried over from the previous tool.

## Tool 0: thread-distill (2026-11-05)

Built by hand, before ToolSmith existed, so it is a baseline and not part of either arm. See `qat/eval-runs/2026-11-05/RESULTS.md`.

- **Correction cycles:** 1 (v0.1 → v0.2).
- **First cold run:**
  - deterministic: 0 of 3 cases passed. One contract check failed in all three: a section was written as prose instead of bullets;
  - judge: 5 of 6, self-graded.

## Tool 1: effort-cost (2026-11-06), arm A

- **Idea.** Zach, 11:02 CT. Invocable from any ChatGPT thread. It gives a heuristic environmental cost of answering at a higher model or effort setting. The prompt for it was a conversation with his partner about literary analysis.

**Human interventions**
- 1: the idea message.
- No corrections from Zach yet.

**ToolSmith run**
- Followed in order: brief → build-or-reuse (build; no neighbor) → failure modes (9) → contract → reflexes (9, one per failure mode) → method with a sourced table → eval stub (3 cases) → runtime notes → design notes.

**Research**
- 5 web searches and 6 fetches, for the per-query energy, carbon and water figures.
- One finding changed the runtime plan: custom GPTs are being replaced by plugins and skills.

**Correction cycles**
- 1 so far (v0.1 → v0.2).

**First cold run (v0.1)**
- Deterministic: 0 of 3 cases passed. Same pattern as thread-distill: in every case, three sections were written as prose where the contract says bullets.
- Judge: 9 of 9, self-graded.
- The blind runner also reported 9 ambiguities. The material ones:
  - product names had no mapping to the effort tiers;
  - the "default" setting was undefined;
  - "floor" had two readings, with a 5× swing in the result;
  - the time-of-day bands had gaps (9:40 pm fit none);
  - range arithmetic for the difference row was unspecified;
  - the word limit was unclear about counting the table.

**v0.2**
- Fixed all of the above in the spec and in both runtime texts.
- Bullets are now required under every heading except Estimate and Lean.
- Second cold run: see `qat/eval-runs/2026-11-06/RESULTS.md`.

**Infrastructure and process cost**
- **Paste block missing heading names.** Caught before the first run (about 2 minutes).
- **A `git stash` displaced the tool's files while the blind run was reading them.** This was the lane's own error, fixed within about a minute. The runner reported that Bash could not see the fixtures, so it counted words by hand. The lesson: use a worktree, never a stash, while a run is live.
- **Same-model limit.** The cold runs are Claude playing ChatGPT, not ChatGPT. Running in real ChatGPT needs Zach's go-ahead, because it posts from his account.

**Carried over from tool 0 (learning effects)**
- The fixture-with-planted-key pattern.
- The blind-subagent cold run.
- The ambiguity report.

**Lesson for ToolSmith**
- Runtime texts must name the exact headings and say "bullets". Both tools failed the same contract check on their first run.
- Candidate change for ToolSmith's runtime-adaptation module: "state the headings and the format of each section verbatim".

## Telosmith pilot observation log

**What gets logged.** A record that changed a consequential decision, set against what the files and the ledger already said. Also any record that confused, duplicated or misled.

**Ends.** When the study ends. If there are zero positive entries, the hook and the CI job are removed (item 2 of the ruling).

| Date | Actor | Record | Effect | Positive? |
|---|---|---|---|---|
| 2026-11-06 | claude:qat | none consulted for effort-cost | Kits are out of Telosmith scope, so nothing in `.aec/` bore on this tool | no (neutral) |
| 2026-11-06 | claude:qat | QAT-R-distill@1, QAT-D-distill-design@1 | Withdrawn and moved to DESIGN.md under the new scope; a maintenance cost, no decision changed | no (cost) |
