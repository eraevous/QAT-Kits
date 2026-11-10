# Contributing to QAT-Kits

QAT-Kits holds conversational tools for chat and thread work. It is not a home for general development tooling. The one script for Claude skills (`qat/scripts/skills.py`) exists to generate, check and package those tools, and stays standard-library only.

## Changing a tool's spec (eval-gated, DEC-193)

A spec is `qat/tools/<name>.skill.md` (a Claude skill's source) or `qat/tools/<name>.qat.md` (a runner contract). Change one only through a pull request that does all of these:

1. **Bump the version** in the spec's frontmatter (semver; see `qat/runtimes/claude/README.md`).
2. **Run its eval cases.** From `qat/`, generate one output per case in `qat/cases/<name>.eval.yaml`. Use synthetic inputs only. Ideally produce each output in a fresh session that sees only the new spec and the case. Then run:

       python3 -I scripts/qat.py eval cases/<name>.eval.yaml eval-runs/<date>/<name>

   Grade the `judge` criteria PASS/FAIL with a one-line reason each.
3. **Record the run**: commit the outputs and a `RESULTS.md` under `qat/eval-runs/<date>/<name>/`. State the spec version, the automated results and the judge grades. A failing case can still merge if the pull request explains why. Hiding a failure is not allowed.
4. **Rebuild and bump the bundle**: `python3 -I qat/scripts/skills.py build`, and raise `qat/runtimes/claude/BUNDLE_VERSION`.

A tool with no `qat/cases/<name>.eval.yaml` gets cases before its first change. Add at least one case that tests a reflex or a stated rule of the tool. Adding a new spec is not gated, because there is no earlier version to compare it with. Its cases still belong in the same pull request.

CI (`qat-skills`) checks steps 1, 3 and 4: the version bump, a recorded run under a path naming the tool, and the bundle bump. It also checks that no generated file is stale. CI cannot judge whether the recorded run is any good. That judgment is the reviewer's.

## Reviews and merging

Kate reviews first (DEC-038), then a fresh-context execution review. Zach merges. Agents never merge or force-push.

## Content

The repository is public. Keep personal and employer-related material out of specs, cases and eval runs, including links to private documents.
