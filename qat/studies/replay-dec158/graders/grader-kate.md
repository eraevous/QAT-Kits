# Grader instructions: Kate (ChatGPT)

**Who runs this:** the coordinator relays this to a ChatGPT thread that has not seen the tool specs, design notes, eval files or the debate that produced the tools: a new thread, not the QAT debate thread. Until RelayKit can reach ChatGPT, the coordinator pastes by hand (or via the chat-relay skill) and saves the reply. Not run by the QAT lane.

**Message to paste** (rubric, then packet, then the closing instruction):

> You're one of two independent graders in a small blind study. Below is a rubric, then a packet of about 20 entries from a fictional software project. Each entry has an item, a reference key, and one response card whose origin is hidden. Grade every entry with the rubric. Your grades will be compared with the other grader's only on whether the reference keys are defensible, so judge the keys honestly too. Don't try to work out how each response was produced before grading it; put your guess in `arm_guess` afterwards. Reply with JSON lines only, one per entry, no commentary.
>
> RUBRIC
> <paste grading-rubric.md>
>
> PACKET
> <paste the output of: python3 -I scripts/replay.py packet --grader kate --tool <tool>>

**Save:** the reply's JSON lines to `studies/replay-dec158/grades/kate.<tool>.jsonl`, unedited, with the thread link and date in `grades/RUN.md`. Tag the file's provenance as Kate's (kate:qat label, not an authorized actor).
