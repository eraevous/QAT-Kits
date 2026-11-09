#!/usr/bin/env python3
"""replay: counterbalanced blind replay for QAT study tools (DEC-158 item 2).

WHAT THIS IS
    The bookkeeping for one study design, so that blinding and counterbalancing
    are reproducible rather than done by hand. Three commands:

        assign   split each tool's items into two stratum-balanced halves and give
                 each grader one half per arm, under opaque ids, in shuffled order
        packet   assemble one grader's packet: item, reference key, and one
                 normalized response card per opaque id (the arm is never shown)
        tally    join grades back to arms; per-arm counts, paired by item; the
                 owner's adjudication queue; a blinding check

    Arms: A = plain prompt (no tool), B = the tool's runtime text. Every item is
    produced in both arms. Each grader sees every item exactly once, in one arm,
    and never the same item both ways; the other grader sees the other arm.

WHAT IT WILL NOT DO
    - Run any model. Producing, normalizing and grading are done by people or
      fresh model contexts following studies/replay-dec158/README.md.
    - Decide anything. The adjudication queue is a list for the owner.
    - Read a key into anything a producer sees. Keys only enter grader packets.

LAYOUT (relative to the study directory, default qat/studies/replay-dec158)
    items/<tool>.items.json        items (no keys)
    keys/<tool>.key.json           reference keys
    assignment.json                written by `assign`
    runs/<tool>/raw/{A,B}/<ITEM>.md     producer outputs (for word counts)
    runs/<tool>/cards/{A,B}/<ITEM>.md   normalized cards (what graders see)
    grades/<grader>.<tool>.jsonl   one JSON object per graded opaque id

USAGE (run from qat/)
    python3 -I scripts/replay.py assign --seed 158
    python3 -I scripts/replay.py packet --grader claude --tool real-problem
    python3 -I scripts/replay.py tally --tool real-problem

Stdlib only. Exit codes: 0 ok; 1 missing or malformed inputs; 2 bad arguments.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_STUDY = Path(__file__).resolve().parent.parent / "studies" / "replay-dec158"
TOOLS = ("real-problem", "kind-check")
GRADERS = ("claude", "kate")
ARMS = ("A", "B")
FLAGS = ("incorrect_commitment", "unnecessary_action", "missed_abstention", "invented_detail")


def _load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"replay: cannot read {path}: {e}")


def split_halves(items: list[dict], rng: random.Random) -> tuple[list[str], list[str]]:
    """Two halves with each stratum split as evenly as possible (odd remainders alternate)."""
    by_stratum = defaultdict(list)
    for it in items:
        by_stratum[it["stratum"]].append(it["id"])
    h1, h2, flip = [], [], False
    for stratum in sorted(by_stratum):
        ids = sorted(by_stratum[stratum])
        rng.shuffle(ids)
        half = len(ids) // 2
        extra = len(ids) % 2
        a, b = ids[: half + (extra if not flip else 0)], ids[half + (extra if not flip else 0):]
        if extra:
            flip = not flip
        h1 += a
        h2 += b
    return sorted(h1), sorted(h2)


def assign(study: Path, seed: int) -> dict:
    """Grader 'claude' gets H1 in arm A and H2 in arm B for the first tool, the reverse for
    the second; 'kate' gets the complement. Opaque ids carry no arm or item information."""
    rng = random.Random(seed)
    out = {"seed": seed, "design": "within-item, cross-grader Latin square; see README", "tools": {}}
    for t_index, tool in enumerate(TOOLS):
        items = _load(study / "items" / f"{tool}.items.json")["items"]
        h1, h2 = split_halves(items, rng)
        first, second = ("A", "B") if t_index % 2 == 0 else ("B", "A")
        plan = {
            "claude": [(i, first) for i in h1] + [(i, second) for i in h2],
            "kate": [(i, second) for i in h1] + [(i, first) for i in h2],
        }
        tool_out = {"halves": {"H1": h1, "H2": h2}, "graders": {}}
        prefix = "RP" if tool == "real-problem" else "KC"
        for grader in GRADERS:
            rows = plan[grader][:]
            rng.shuffle(rows)
            codes = rng.sample(range(100, 1000), len(rows))
            tool_out["graders"][grader] = [
                {"oid": f"{prefix[0]}{grader[0].upper()}{code}", "item": item, "arm": arm}
                for (item, arm), code in zip(rows, codes)
            ]
        out["tools"][tool] = tool_out
    (study / "assignment.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


def packet(study: Path, grader: str, tool: str) -> str:
    asg = _load(study / "assignment.json")["tools"][tool]["graders"][grader]
    items = {it["id"]: it for it in _load(study / "items" / f"{tool}.items.json")["items"]}
    shared = _load(study / "items" / f"{tool}.items.json").get("shared_context", "")
    keys = _load(study / "keys" / f"{tool}.key.json")["keys"]
    lines = [f"# Grading packet: {tool}, grader {grader}", "",
             "Grade every response with the instructions you were given. The response's origin is hidden.", "",
             f"**Shared context for every item:** {shared}", ""]
    missing = []
    for row in asg:
        card = study / "runs" / tool / "cards" / row["arm"] / f"{row['item']}.md"
        if not card.exists():
            missing.append(str(card))
            continue
        it = items[row["item"]]
        key = {k: v for k, v in keys[row["item"]].items() if k != "seen_in_design"}
        body = {k: v for k, v in it.items() if k not in ("id", "stratum")}
        lines += [f"## {row['oid']}", "", "**Item:**", "```json", json.dumps(body, indent=1, ensure_ascii=False), "```",
                  "", "**Reference key (a claim; you may dispute it):**", "```json",
                  json.dumps(key, indent=1, ensure_ascii=False), "```", "", "**Response card:**", "",
                  card.read_text(encoding="utf-8").strip(), "", "---", ""]
    if missing:
        sys.exit("replay: missing normalized cards:\n  " + "\n  ".join(missing))
    return "\n".join(lines)


def _words(path: Path) -> int | None:
    return len(path.read_text(encoding="utf-8").split()) if path.exists() else None


def tally(study: Path, tool: str, exclude_seen: bool = False) -> dict:
    asg = _load(study / "assignment.json")["tools"][tool]["graders"]
    keys = _load(study / "keys" / f"{tool}.key.json")["keys"]
    by_oid = {row["oid"]: (g, row["item"], row["arm"]) for g, rows in asg.items() for row in rows}
    grades, problems = {}, []
    for grader in GRADERS:
        f = study / "grades" / f"{grader}.{tool}.jsonl"
        if not f.exists():
            problems.append(f"no grades file {f.name}")
            continue
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                g = json.loads(line)
            except json.JSONDecodeError:
                problems.append(f"{f.name}:{n} not JSON")
                continue
            if g.get("oid") not in by_oid or by_oid[g["oid"]][0] != grader:
                problems.append(f"{f.name}:{n} unknown oid {g.get('oid')} for {grader}")
                continue
            grades[g["oid"]] = g
    for oid in sorted(set(by_oid) - set(grades)):
        grader, item, arm = by_oid[oid]
        if not (exclude_seen and keys[item].get("seen_in_design")):
            problems.append(f"missing grade {oid} for {grader} ({item}, arm {arm})")
    arms = {a: Counter() for a in ARMS}
    per_item = defaultdict(dict)
    guesses = Counter()
    for oid, g in grades.items():
        grader, item, arm = by_oid[oid]
        if exclude_seen and keys[item].get("seen_in_design"):
            continue
        c = arms[arm]
        c["graded"] += 1
        c[f"defensible_{g.get('defensible', 'missing')}"] += 1
        c["corrections"] += int(g.get("corrections", 0))
        for flag in FLAGS:
            c[flag] += bool(g.get(flag))
        w = _words(study / "runs" / tool / "raw" / arm / f"{item}.md")
        if w is not None:
            c["words"] += w
        per_item[item][grader] = g
        guess = g.get("arm_guess", "unsure")
        truth = "tool" if arm == "B" else "plain"
        guesses["unsure" if guess == "unsure" else ("right" if guess == truth else "wrong")] += 1
    queue = []
    for item, gs in sorted(per_item.items()):
        verdicts = {gr: g.get("key", "agree") for gr, g in gs.items()}
        if len(gs) == 2 and len(set(verdicts.values())) == 2:
            queue.append({"item": item, "why": "graders split on the key",
                          "notes": {gr: g.get("key_note", "") for gr, g in gs.items()}})
        elif len(gs) == 2 and set(verdicts.values()) == {"dispute"}:
            queue.append({"item": item, "why": "both graders dispute the key",
                          "notes": {gr: g.get("key_note", "") for gr, g in gs.items()}})
    return {"tool": tool, "exclude_seen_in_design": exclude_seen, "arms": {a: dict(c) for a, c in arms.items()},
            "adjudication_queue": queue, "blinding": dict(guesses), "problems": problems}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--study", type=Path, default=DEFAULT_STUDY)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("assign"); a.add_argument("--seed", type=int, required=True)
    p = sub.add_parser("packet"); p.add_argument("--grader", choices=GRADERS, required=True)
    p.add_argument("--tool", choices=TOOLS, required=True); p.add_argument("-o", "--out", type=Path)
    t = sub.add_parser("tally"); t.add_argument("--tool", choices=TOOLS, required=True)
    t.add_argument("--exclude-seen", action="store_true", help="drop items that appear in the design-time evals")
    args = ap.parse_args(argv)
    if args.cmd == "assign":
        out = assign(args.study, args.seed)
        for tool, d in out["tools"].items():
            print(f"{tool}: H1={','.join(d['halves']['H1'])} H2={','.join(d['halves']['H2'])}")
        print(f"wrote {args.study / 'assignment.json'}")
    elif args.cmd == "packet":
        text = packet(args.study, args.grader, args.tool)
        if args.out:
            args.out.write_text(text, encoding="utf-8"); print(f"wrote {args.out}")
        else:
            print(text)
    else:
        print(json.dumps(tally(args.study, args.tool, args.exclude_seen), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
