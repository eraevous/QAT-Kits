#!/usr/bin/env python3
"""qat new: scaffold a new QAT tool so that it validates from the first minute.

WHAT THIS IS
    The "qat.py new" step of the tool-creation pipeline (arm B of the creation
    feasibility study, docs/creation-study.md). Given a tool name, it writes:

        tools/<name>.qat.md                  a minimal spec that `qat.py validate` accepts
        cases/<name>.eval.yaml               an eval stub: one ordinary case, one failure-mode case
        cases/fixtures/<name>.example.md     a constructed fixture with a slot for the planted key
        tools/<name>.DESIGN.md               (--design) Kit-owned design notes, five questions
        runtimes/chatgpt/<name>.paste.md     (--runtime chatgpt) paste-block stub
        runtimes/claude/<name>/SKILL.md      (--runtime skill) Claude skill stub

    It then runs the unchanged runner (scripts/qat.py validate) on the new spec
    and prints what to do next.

WHY A SEPARATE MODULE, NOT A SUBCOMMAND IN qat.py
    qat/scripts/qat.py is a byte-for-byte copy of the runner in Zach's skill
    bucket (qat/PROVENANCE.md). Editing it would make a third, drifting copy of
    the runner, which is the problem DEC-048/051 is about. This module only
    calls qat.py; it never imports or patches it. It can be dropped in or taken
    out without touching anything else.

WHAT IT WILL NOT DO
    - Overwrite an existing file. If any target exists it stops, writes nothing,
      and says which file it found (use a new name, or delete the stub by hand).
    - Touch legacy tools in Toolkits/ (DEC-048/051).
    - Decide anything. The stubs are full of TODO markers on purpose: the
      scaffold saves typing, not thinking. ToolSmith (tools/toolsmith.qat.md)
      is the design procedure that fills them in.

FOR AGENTS (the agent-aided creation seam)
    --json prints one machine-readable result instead of prose:
        {"ok": bool, "tool": name, "created": [paths], "validate": {"ok": bool,
         "exit_code": int, "output": str}, "next": [steps], "error": str|null}
    An agent can drive: scaffold -> fill (ToolSmith) -> validate -> cold run ->
    eval -> revise. It cannot accept the result; only Zach does.

LESSONS BAKED IN (from the first two tools)
    Both thread-distill and effort-cost failed their first cold run the same
    way: runtime text that did not name the exact headings and say "bullets",
    so sections came back as prose and the contract check failed. Every
    runtime stub generated here lists the spec's headings verbatim and states
    each section's format.

USAGE (run from qat/)
    python3 -I scripts/new.py my-tool --description "One sentence of at least twenty characters."
    python3 -I scripts/new.py my-tool --runtime chatgpt --runtime skill --design
    python3 -I scripts/new.py my-tool --json
    python3 -I scripts/new.py my-tool --root /tmp/scratch     # write somewhere else (tests)

Exit codes: 0 created and validated; 1 created but validation failed (a bug
in this template, please report); 2 refused (bad name, file exists, bad args).
"""

from __future__ import annotations

import argparse
import json
import re
import stat
import subprocess
import sys
from pathlib import Path

# The runner's own rule for tool names (SPEC_SCHEMA in qat.py), repeated here so
# a bad name is refused before anything is written.
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DESC_MIN, DESC_MAX = 20, 400  # qat.py SPEC_SCHEMA description bounds
RUNTIMES = ("chatgpt", "skill")

# Default contract for a new tool: one input, two outputs. Deliberately small
# (ToolSmith reflex "smallest-first"); grow it only when an eval case needs it.
DEFAULT_OUTPUTS = [
    # (key, type, heading, format phrase used in runtime stubs)
    ("result", "claims", "Result", "bullets"),
    ("limits", "claims", "Limits", "bullets"),
]


def title_case(name: str) -> str:
    """'effort-cost' -> 'EffortCost', the display name used in spec bodies."""
    return "".join(part.capitalize() for part in name.split("-"))


# ---------------------------------------------------------------------------
# Templates. Each returns the file text. Placeholders are TODO lines that are
# still valid YAML/markdown, so the spec validates before anyone edits it.
# ---------------------------------------------------------------------------

def spec_text(name: str, description: str) -> str:
    outputs = "\n".join(
        f'  {key}: {{type: {typ}, heading: {heading}, doc: "TODO: what the reader uses this section for"}}'
        for key, typ, heading, _ in DEFAULT_OUTPUTS
    )
    return f"""---
name: {json.dumps(name)}
version: 0.1.0
description: {json.dumps(description)}
inputs:
  input: {{type: text, required: true, doc: "TODO: what the user supplies"}}
outputs:
{outputs}
reflexes:
  todo-first-failure-mode: "TODO: one rule per failure mode (ToolSmith step 5); each must be tested by an eval case"
handoffs: []
---

# {title_case(name)}

TODO: two or three sentences. Who runs this, on what, and what they do with the result.

## Procedure
1. TODO
2. TODO

Write the output with exactly the `##` headings in the contract above, in that order. Every section is bullets.
"""


def eval_text(name: str) -> str:
    return f"""# Eval cases for {name}. Output files go in OUTPUT_DIR/<id>.md.
# Pattern checks: regex (case-insensitive, multiline), optionally scoped to one output section.
# Judge checks: graded by a model, one line each. Mark who wrote each case (design-time vs independent)
# and keep the author's own judge grades provisional until someone independent grades them (QAT-R-create).
#
# Fixture: cases/fixtures/{name}.example.md (constructed; never a real conversation in this public repo).
# What the fixture plants (the key; do not show this to the model under test):
#   TODO: one line per planted failure mode
tool: {json.dumps(name)}
cases:
  - id: ordinary
    # written by: TODO (design-time)
    input:
      input: "file: cases/fixtures/{name}.example.md"
    must_include:
      - section: result
        pattern: "TODO"
        why: TODO
    must_avoid:
      - judge: "TODO: the most likely fluent-but-wrong output"

  - id: failure-mode-1
    # written by: TODO (design-time)
    # tests reflex: todo-first-failure-mode
    input:
      input: "file: cases/fixtures/{name}.example.md"
    must_include:
      - judge: "TODO: what a correct output does here"
    must_avoid:
      - judge: "TODO: the failure this case is planted to catch"
"""


def fixture_text(name: str) -> str:
    return f"""# Example input for {name}
<!-- Constructed test fixture (not a real conversation or document). Plant each failure mode
     listed in cases/{name}.eval.yaml here, and keep the key in that file, not in this one. -->

TODO: the input text.
"""


def design_text(name: str) -> str:
    return f"""# {name}: design notes

Kit-owned and ungoverned (Telosmith governs the creation machinery, not tools).
Write this only when real choices were made; delete the sections that stay empty.

## Why it exists
- TODO: origin, in the requester's words, with date
- TODO: why it is separate from its nearest neighbors

## Choices and the alternatives rejected
- TODO

## Distinctions that must survive revisions
- TODO

## Evidence
- TODO: sources with dates; cold-run results (qat/eval-runs/...)

## Open questions
- TODO
"""


def headings_block() -> str:
    """The verbatim heading list every runtime stub carries (see LESSONS above)."""
    return "\n".join(f"- `## {heading}`: {fmt}" for _, _, heading, fmt in DEFAULT_OUTPUTS)


def chatgpt_text(name: str) -> str:
    return f"""<!-- ChatGPT paste block for {name} v0.1.0, hand-adapted from qat/tools/{name}.qat.md.
     Paste everything below the line into any ChatGPT thread. Keep it short enough to paste repeatedly.
     When the spec's outputs change, update the heading list below in the same commit. -->
---
{title_case(name).upper()} (TODO: one line on what this does; say what NOT to do, e.g. don't answer my underlying question).

TODO: the procedure, inlined. ChatGPT cannot run scripts or read the repo: inline any tables.

Use these headings, in order, with this format under each:
{headings_block()}
"""


def skill_text(name: str, description: str) -> str:
    return f"""---
name: {json.dumps(name)}
description: {json.dumps("TODO: say WHEN to use this (the description is what triggers a skill). " + description)}
---
<!-- Claude skill for {name} v0.1.0, adapted from qat/tools/{name}.qat.md. Update together with the spec. -->

# {title_case(name)}

TODO: the procedure and reflexes from the spec.

## Output
Use these headings, in order, with this format under each:
{headings_block()}
"""


# ---------------------------------------------------------------------------

def plan(root: Path, name: str, description: str, runtimes: list[str], design: bool) -> dict[Path, str]:
    """Map every file to create -> its text. Pure; writes nothing."""
    files = {
        root / "tools" / f"{name}.qat.md": spec_text(name, description),
        root / "cases" / f"{name}.eval.yaml": eval_text(name),
        root / "cases" / "fixtures" / f"{name}.example.md": fixture_text(name),
    }
    if design:
        files[root / "tools" / f"{name}.DESIGN.md"] = design_text(name)
    if "chatgpt" in runtimes:
        files[root / "runtimes" / "chatgpt" / f"{name}.paste.md"] = chatgpt_text(name)
    if "skill" in runtimes:
        files[root / "runtimes" / "claude" / name / "SKILL.md"] = skill_text(name, description)
    return files


def preflight(root: Path, files: dict[Path, str]) -> str | None:
    """Reject occupied targets and unsafe parents before creating anything.

    lstat sees dangling symlinks too. Reject directory symlinks under the
    resolved root, even if they currently point inside it, so an existing link
    cannot redirect scaffold files elsewhere.
    """
    parents = {root}
    for path in files:
        parents.update(parent for parent in path.parents if parent.is_relative_to(root))
    for parent in sorted(parents, key=lambda p: (len(p.parts), str(p))):
        try:
            mode = parent.lstat().st_mode
        except FileNotFoundError:
            continue
        if not stat.S_ISDIR(mode):
            return f"not a real directory, nothing written: {parent.relative_to(root)}"
    existing = []
    for path in files:
        try:
            path.lstat()
        except FileNotFoundError:
            continue
        existing.append(str(path.relative_to(root)))
    if existing:
        return "already exists, nothing written: " + ", ".join(existing)
    return None


def write_scaffold(files: dict[Path, str]) -> None:
    """Create exclusively; undo our own new files and directories on I/O failure.

    This is not an atomic multi-file transaction. Run in a trusted workspace,
    not one whose directories are being concurrently replaced by another actor.
    """
    created_files: list[Path] = []
    created_dirs: list[Path] = []

    def mkdir(path: Path) -> None:
        if path.is_dir():
            return
        mkdir(path.parent)
        path.mkdir()
        created_dirs.append(path)

    try:
        for path, text in files.items():
            mkdir(path.parent)
            # Unlike write_text, exclusive creation cannot follow a late target
            # symlink or truncate a file created after preflight.
            with path.open("x", encoding="utf-8") as output:
                created_files.append(path)
                output.write(text)
    except OSError as error:
        cleanup_errors = []
        for path in reversed(created_files):
            try:
                path.unlink()
            except OSError as cleanup_error:
                cleanup_errors.append(str(cleanup_error))
        for path in reversed(created_dirs):
            try:
                path.rmdir()
            except OSError as cleanup_error:
                cleanup_errors.append(str(cleanup_error))
        if cleanup_errors:
            raise OSError(f"{error}; cleanup incomplete: {'; '.join(cleanup_errors)}") from error
        raise


def run_validate(root: Path, spec: Path) -> dict:
    """Validate with the unchanged runner. The runner resolves handoffs against its
    own tools/ directory, so it is run from `root`, with this file's sibling qat.py."""
    runner = Path(__file__).resolve().parent / "qat.py"
    proc = subprocess.run(
        [sys.executable, "-I", str(runner), "validate", str(spec)],
        cwd=root, capture_output=True, text=True,
    )
    out = (proc.stdout + proc.stderr).strip()
    return {"ok": proc.returncode == 0, "exit_code": proc.returncode, "output": out}


def next_steps(name: str, runtimes: list[str]) -> list[str]:
    steps = [
        f"Fill tools/{name}.qat.md by following ToolSmith (tools/toolsmith.qat.md): brief, failure modes, contract, reflexes, method.",
        f"Plant the failure modes in cases/fixtures/{name}.example.md and write one eval case per reflex in cases/{name}.eval.yaml.",
        f"Validate: python3 -I scripts/qat.py validate tools/{name}.qat.md",
        f"Cold run: an actor who has not seen the eval file runs the spec on the fixture into eval-runs/<date>/{name}/.",
        f"Score: python3 -I scripts/qat.py eval cases/{name}.eval.yaml eval-runs/<date>/{name}",
    ]
    if runtimes:
        steps.append("Update the runtime stubs' heading lists whenever the spec's outputs change.")
    steps.append("Record the creation-study metrics in docs/creation-study.md (arm B).")
    return steps


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Scaffold a new QAT tool (spec, eval stub, fixture, optional runtimes).")
    ap.add_argument("name", help="tool name: lowercase words joined by hyphens, e.g. effort-cost")
    ap.add_argument("--description", default=None,
                    help=f"one sentence, {DESC_MIN}-{DESC_MAX} characters (default: a TODO placeholder)")
    ap.add_argument("--runtime", action="append", choices=RUNTIMES, default=[],
                    help="add a runtime stub; repeatable")
    ap.add_argument("--design", action="store_true", help="also create tools/<name>.DESIGN.md")
    ap.add_argument("--root", type=Path, default=Path.cwd(), help="the qat/ directory to write into (default: cwd)")
    ap.add_argument("--json", action="store_true", help="print a machine-readable result")
    args = ap.parse_args(argv)

    result = {"ok": False, "tool": args.name, "created": [], "validate": None, "next": [], "error": None}

    def finish(code: int) -> int:
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["error"]:
                print(f"REFUSED  {result['error']}")
            for p in result["created"]:
                print(f"created  {p}")
            if result["validate"]:
                print(f"validate {'OK' if result['validate']['ok'] else 'FAILED'}")
                if not result["validate"]["ok"]:
                    print(result["validate"]["output"])
            for i, s in enumerate(result["next"], 1):
                print(f"next {i}. {s}")
        return code

    if not NAME_RE.match(args.name):
        result["error"] = f"name '{args.name}' must be lowercase words joined by hyphens (e.g. effort-cost)"
        return finish(2)
    description = args.description or f"TODO: one sentence on what {args.name} does and for whom."
    if not DESC_MIN <= len(description) <= DESC_MAX:
        result["error"] = f"--description must be {DESC_MIN}-{DESC_MAX} characters (got {len(description)})"
        return finish(2)
    try:
        root = args.root.resolve()
    except (OSError, RuntimeError) as error:
        result["error"] = f"cannot resolve --root: {error}"
        return finish(2)
    if not (root / "scripts" / "qat.py").exists() and not (Path(__file__).resolve().parent / "qat.py").exists():
        result["error"] = "cannot find scripts/qat.py; run from the qat/ directory or pass --root"
        return finish(2)

    files = plan(root, args.name, description, args.runtime, args.design)
    try:
        result["error"] = preflight(root, files)
        if result["error"]:
            return finish(2)
        write_scaffold(files)
    except OSError as error:
        result["error"] = f"could not create scaffold: {error}"
        return finish(2)
    result["created"] = [str(path.relative_to(root)) for path in files]

    result["validate"] = run_validate(root, root / "tools" / f"{args.name}.qat.md")
    result["next"] = next_steps(args.name, args.runtime)
    result["ok"] = result["validate"]["ok"]
    return finish(0 if result["ok"] else 1)


if __name__ == "__main__":
    sys.exit(main())
