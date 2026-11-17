---
tool: thread-seed
spec: qat/tools/thread-seed.skill.md
version: 1.0.1
---

# thread-seed: cases

Cases for the standalone skill (CONTRIBUTING.md, "Standalone skill"). Inputs are synthetic. TS-01 to TS-03
exercise the bundled helper `seed_index.py --verify` (the skill's step 9, "Verify") and are deterministic:
run the helper from the skill text against the capture and seed below and save its output. TS-04 tests the
model's reflex at the same step and is run in a fresh session that sees only the built skill and the case.
Save each result as `qat/eval-runs/<date>/thread-seed/<version>/<case id>.md` and grade PASS/FAIL against
"Must" and "Must not".

`qat/scripts/test_thread_seed.py` pins TS-01 to TS-03 as unit tests.

## Shared capture (`capture.json`)

A T1/T3 capture: exchange 2 is missing, and T1 has two replies.

```json
{"turns": [
  {"n": 1, "role": "user", "label": "User", "messages": [{"text": "Please keep the seed short and cite every claim you carry over."}]},
  {"n": 1, "role": "assistant", "label": "Claude", "messages": [
    {"text": "First reply: we agreed the budget stays at three pages for the successor."},
    {"text": "Second reply: the reviewer is chosen by Zach, not by the lane."}]},
  {"n": 3, "role": "user", "label": "User", "messages": [{"text": "Thanks, now draft the open decisions section for the successor thread."}]},
  {"n": 3, "role": "assistant", "label": "Claude", "messages": [{"text": "Open decisions wait on Zach; the lane only proposes them."}]}
]}
```

## TS-01: A ref to a missing exchange below the maximum (port finding 1)

**Seed:** `Budget was settled earlier [T2].`

**Must:** report `FAIL ref T2` and exit 1.
**Must not:** pass because 2 is below the capture's highest exchange (3).

## TS-02: A wrong quote

**Seed:** `"the budget stays at five pages for the successor" [T1a]`

**Must:** report `FAIL quote` and exit 1.

## TS-03: First-reply text cited as the second reply (port finding 2)

**Seed:** `"the budget stays at three pages for the successor" [T1a2]`

**Must:** report `FAIL quote` and exit 1. The same quote cited as `[T1a]` or `[T1a1]` passes.
**Must not:** match the quote against T1's other reply.

## TS-04: The model fixes or drops failing pointers before delivering

**Input:** the shared capture, and this message: "Here's my draft seed for the successor. Run your check on it
before I paste it." with the draft:

```
# Continuing: seed-budget lane
## 4. Where things stand
- Seed budget is three pages (decided) [T2].
- "the reviewer is chosen by Zach, not by the lane" [T1a]
- Open decisions wait on Zach [T3a].
```

**Must:**
- Run `seed_index.py --verify` (not an eyeball check) and report the count of failures it found (2).
- Fix or drop both failures: the budget claim's pointer becomes `[T1a]` (or the claim is dropped), and the
  reviewer quote's pointer becomes `[T1a2]` (or the quote is dropped).
- Leave the valid `[T3a]` line as it is.

**Must not:** deliver the seed with a failing pointer, or claim the check passed when it did not.
