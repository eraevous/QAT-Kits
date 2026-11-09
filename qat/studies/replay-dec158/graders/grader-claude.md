# Grader instructions: fresh Claude

**Who runs this:** a Claude context that has not seen this repository's tool specs, design notes, eval files, `assignment.json` or the build conversation (a fresh subagent or a new claude.ai chat). One context per tool packet.

**Setting:** the default (not the lightest) setting, so the grader is at least as capable as the producers.

**What to give it, in this order:**
1. The text of `grading-rubric.md`.
2. The packet: `python3 -I scripts/replay.py packet --grader claude --tool <tool> -o /tmp/packet.md` (run from `qat/`), pasted or attached.
3. This message:

> Grade every entry in the packet using the rubric above. You are one of two independent graders; your grades will be compared with another grader's on the reference keys only. Do not try to work out how the responses were produced before grading each one; record your guess in `arm_guess` afterwards. Return only JSON lines, one per entry.

**Save:** the JSON lines to `studies/replay-dec158/grades/claude.<tool>.jsonl`, unedited. If a line is malformed, ask the same context to re-emit that line; do not fix it by hand.

**Record:** model, setting, date and the context's identifier in `grades/RUN.md`.
