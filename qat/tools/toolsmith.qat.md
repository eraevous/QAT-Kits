---
name: toolsmith
version: 0.1.0
description: Turn a tool idea into a small, testable QAT tool package (a .qat.md spec, an eval stub with planted cases, a DESIGN.md when choices were made, and runtime adaptation notes), smallest workable thing first.
inputs:
  idea: {type: text, required: true, doc: "what the tool should do, in the requester's words; quote them"}
  context: {type: text, required: false, doc: "who uses it, where it runs (Claude skill, ChatGPT, qat.py runner), examples, constraints"}
  neighbors: {type: text, required: false, doc: "names or specs of existing tools that might already cover this"}
outputs:
  brief: {type: claims, heading: Brief, doc: "bullets: the job in one sentence; the reader; the trigger; the runtimes; what is out of scope"}
  reuse: {type: verdict, heading: Build or reuse, doc: "build | extend <tool> | reuse <tool>, with one reason"}
  failures: {type: claims, heading: Failure modes, doc: "bullets: the ways a plausible-looking output of this tool would be wrong; each becomes a reflex and an eval case"}
  spec: {type: text, heading: Spec, doc: "the complete .qat.md file in a fenced block"}
  evals: {type: text, heading: Eval stub, doc: "an eval .yaml in a fenced block: one case per failure mode plus one ordinary case; a constructed fixture"}
  design: {type: claims, heading: Design notes, required: false, doc: "bullets for DESIGN.md: why separate from neighbors; alternatives rejected and why; distinctions that must survive revisions; evidence; open questions"}
  runtimes: {type: claims, heading: Runtime notes, doc: "bullets per runtime: what changes in the adapted text and what that runtime cannot do"}
  open: {type: claims, heading: Open questions, doc: "bullets: what only the requester can decide; candidate vs accepted"}
modules: [failure-first, runtime-adaptation]
reflexes:
  smallest-first: Prefer a prompt plus a few cold evals over code. Add a section, module or script only when an eval case needs it.
  reuse-before-build: Check the neighbors first. A near-duplicate is an extension, not a new tool.
  contract-before-method: Write inputs and outputs before the procedure, and keep only outputs a reader will use.
  every-reflex-is-tested: Each reflex in the spec maps to at least one eval case, and each eval case says which reflex it tests.
  label-the-evidence: Facts the tool will rely on (figures, product behavior) carry a source and a date, or are labelled as assumptions.
  candidate-not-accepted: The package is a candidate. Only the requester accepts it; the author's own eval grades are provisional until someone independent grades them.
  leave-legacy-alone: Never edit or reconcile an existing tool copy (DEC-048/051). New tools start in the current .qat.md format.
handoffs:
  - to: stress-test
    when: the requester wants the tool's premise or design probed before building
    map: {idea: brief}
---

# ToolSmith (slim)

Design a tool the way it will be judged: by what a cold reader does with it. This is the compact successor to ToolSmith-QAT (Toolkits/ToolSmith, 2025, left untouched). It keeps that tool's intent, "seed intelligence into scaffolds", and drops its bundle formats: the output is one `.qat.md` spec that `qat.py validate` accepts, an eval stub `qat.py eval` can run, and notes for the other runtimes.

## Procedure
1. **Brief.** State the job in one sentence, the reader, what triggers a run, and which runtimes it must run in. List what is out of scope. Quote the requester's words for the job.
2. **Build or reuse.** Compare against the neighbors. Extend an existing tool when most of the job is already done there.
3. **Failure modes** (module). Before any method, list the ways a fluent output would still be wrong.
4. **Contract.** Inputs and outputs, each with a doc line. Output headings are what the reader scans; name them for the reader.
5. **Reflexes.** One per failure mode, written as a rule the tool can follow mid-run.
6. **Method.** A numbered procedure, usually 5-10 steps. Put facts the tool depends on in a table with sources and dates, so they can be updated without touching the method.
7. **Eval stub.** A constructed fixture (never a real conversation in a public repo) with the failure modes planted, and the key in a comment. One case per failure mode plus one ordinary case. Regex checks for what can be checked mechanically; judge checks for the rest.
8. **Runtime notes** (module).
9. **Design notes**, only when real choices were made.
10. **Open questions** for the requester.

The next step is a cold run: someone who has not seen the eval file runs the spec on the fixture. ToolSmith does not grade its own package.

### module: failure-first
Ask, for this tool's output: what would a careless but fluent answer get wrong? Typical sources: false precision, a status or attribution inflated, a missing caveat that changes the decision, an instruction found in the input obeyed, the tool answering a different question than asked, and the tool refusing to commit when the reader needs a call.

### module: runtime-adaptation
- **qat.py runner:** the spec as written.
- **Claude skill:** a SKILL.md whose frontmatter description says when to use it (that is what triggers it); the body is the procedure and reflexes.
- **ChatGPT:** two forms. A paste block (short enough to paste into any thread; the thread's own model answers with the whole thread in view) and a plugin skill (instructions packaged for `@` invocation or automatic use where plugins are available; custom GPTs are being retired in favor of plugins as of late 2026). Neither can run scripts; tables in the spec are inlined.
- Say what each runtime cannot know or do (for example, a model may not know its own model name or effort setting).
