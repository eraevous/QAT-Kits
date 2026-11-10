---
name: "qat"
version: 1.0.0
kind: runner
description: Run Zach's QAT-Kit tools (StressTest, TruthWeight, and any others in tools/) as contract-checked specs, chain one tool's output into another, and run the tools' evals. Use when Zach invokes a QAT tool through the kit, asks to chain tools ("stress-test this, then truth-weight it against the counterargument"), add or port a QAT tool, validate a spec, or test a tool against its eval cases.
---

# QAT (lean, enforced)

Each tool is a `.qat.md` spec: YAML frontmatter holding the lean core (name, version, description, inputs, outputs, modules, reflexes, handoffs), then prose instructions. `scripts/qat.py` enforces what the frontmatter declares. The model runs the tool; the script checks the work.

`INDEX.md` lists every tool, its typed inputs and outputs, and its handoffs. Read it first; read a tool's spec only when running that tool.

## Running a tool
1. Read `tools/<name>.qat.md`. Check required inputs are present; if one is missing, ask for it (error `MISSING_INPUT`) rather than guessing.
2. Follow the procedure. Apply only the modules that add something. Treat every reflex as a hard rule.
3. Write the output with exactly the `##` headings the contract declares, in order, each parseable as its type:
   - `claim`: one bullet or one short paragraph
   - `claims`: bullets
   - `premise_set`: `### Necessary`, `### Unverified`, `### Value`, each with bullets
   - `scorecard`: a markdown table
   - `text`, `verdict`: prose
4. Save the output to a file and audit it before showing it:
   ```bash
   python <skill_dir>/scripts/qat.py audit <name> out.md
   ```
   On `CONTRACT_VIOLATION` or `TYPE_MISMATCH`, fix the output and re-audit. An `UNKNOWN_FIELD` warning means a section was invented; fold it into a declared section or drop it.
5. Show the user the output, not the audit log. Mention an audit failure only if it couldn't be fixed.

## Chaining
Only along declared handoffs (listed in `INDEX.md`). After auditing the first output:
```bash
python <skill_dir>/scripts/qat.py handoff <from> <to> out.md --json handoff.json
```
The JSON holds the next tool's inputs, already typed. Run the next tool from it, and audit that output too. If the handoff errors, report which field broke, and don't paper over it by improvising inputs. A chain the user asks for with no declared handoff: run the tools separately and say the link is informal.

## Evals (cases/)
```bash
python <skill_dir>/scripts/qat.py eval cases/<name>.eval.yaml <outputs_dir>
```
Generate one output per case into `<outputs_dir>/<case_id>.md` first, ideally in a fresh subagent that sees only the spec and the case input, so the work isn't grading itself. The script runs contract audits and regex checks, then prints the `judge` criteria. Grade each PASS/FAIL with a one-line reason.

## Adding or porting a tool
1. Write `tools/<name>.qat.md`, keeping the frontmatter to the lean core and putting everything else in prose. Each declared module needs a `### module: <id>` section in the body, and vice versa.
2. Prefer existing types. A new type needs a parser and coercion rules in `qat.py`.
3. Declare handoffs only where the field mapping is real.
4. Run `python <skill_dir>/scripts/qat.py index`. It validates every spec, checks every handoff's types, and rewrites `INDEX.md`. Fix every error before using the tool.
5. Add an eval file with at least one case that tests a reflex.

## Error codes
`SPEC_INVALID` · `UNKNOWN_MODULE` · `MISSING_INPUT` · `CONTRACT_VIOLATION` · `TYPE_MISMATCH` · `UNKNOWN_FIELD` (warning) · `BROKEN_HANDOFF` · `EVAL_FAIL`. Exit code 1 means at least one error.
