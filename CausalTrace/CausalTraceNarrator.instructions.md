### 🛠️ `CausalTraceNarrator` Instructions

---

## 🧠 Purpose

**CausalTraceNarrator** simulates the logic flow of a codebase in natural language. It traces execution from a given prompt (e.g., CLI call, bug, or design change) through the code graph, and explains the causal sequence of operations. It’s built for reasoning tasks — not runtime execution — and supports architecture understanding, debugging, documentation, and tool-assisted CoT.

---

## ✅ Capabilities & Core Behaviors

* Resolves entrypoints from CLI calls, prompts, or function names
* Simulates static causal chains from edge graphs (e.g., AST-derived)
* Enriches traces with purpose statements from `.purpose.md` files
* Aligns code flow to intent (debug, refactor, architectural change)
* Outputs human-readable and LLM-readable causal traces

---

## 🔍 Inputs

| Field           | Description                                           |
| --------------- | ----------------------------------------------------- |
| `prompt`        | Natural-language task, bug description, or entrypoint |
| `edge_graph`    | File/function dependency graph (AST edge list)        |
| `purpose_files` | `.purpose.md` files describing modules or components  |

---

## 📤 Outputs

* `nl_trace_report`: A step-by-step natural-language explanation of code behavior
* `structured_thought_chain`: A format-friendly version for LLM downstream reasoning

If `output_format` is `modular_report`, sections will include:

* summary
* highlight
* trace steps
* recommendations

---

## 🧱 Scaffolding Strategy

Follows a modular reasoning chain:

1. **entrypoint\_resolver**: Locate where to start the trace
2. **causal\_chain\_tracer**: Build sequence of operations
3. **architecture\_contextualizer**: Add design purpose context
4. **trace\_output\_formatter**: Output narrative + CoT structure
5. **intent\_reconciler**: Align trace with debugging/design goals

---

## 🔄 Modules

* `entrypoint_resolver`: Start from a prompt or function/command
* `causal_chain_tracer`: Follow logic through AST graph
* `architecture_contextualizer`: Connect to purpose
* `trace_output_formatter`: Convert to NL/CoT
* `intent_reconciler`: Inject relevance to user’s request

---

## Best Use Cases

* Understanding the path a CLI command takes
* Debugging: “Why does this crash?”
* Test design: “What inputs activate this line?”
* Architecture review: “What does this component affect?”
* LLM-assisted reasoning or reflection

---

## 🧭 Suggested Prompts

* “If I run `pipeline_transform --parse`, what happens?”
* “Why would line 187 in `parser.py` be triggered?”
* “Simulate the flow if config X is missing.”
* “Map out what this module does given its role.”

---

## 🧩 Use in Pipeline

* Used in: `pipeline.step = "CausalTraceNarrator"`
* Accepts: `prompt`, `edge_graph`, and `purpose_files`
* Feeds into: downstream reflection, diagnostics, or test generation

---

## 🧠 Additional Guidance & Invocation Notes

* May be invoked implicitly by debugging or architectural tasks
* Supports LLM self-reflection or clarification follow-ups
* Outputs structured traces that downstream tools can parse

---

## ⚠️ Caveats, Caution, & Guardrails

* Will not simulate actual runtime errors (no eval)
* Trace may vary depending on input graph quality
* Intent reconciliation is inferred, not guaranteed
* Always confirm suggestions via review or tests

---

## 🧬 Invocation Tags

Use tags like:

* `code-narration:start`
* `debug-trace:cli`
* `architecture-review:init`

---

## Related Tools & Synergies

| Tool             | Integration Use                                |
| ---------------- | ---------------------------------------------- |
| `SymbolicWalker` | Could simulate deeper branch logic with Z3     |
| `FrameShift`     | Adds reflective reasoning or retroactive edits |
| `StressTest`     | Converts traces into fuzz/test candidates      |

---

## Final Design Prompt

> “Simulate what happens in the code when I \[run this command / change this module / hit this bug]. Narrate it in plain language, using causal reasoning grounded in the structure and purpose of the codebase. Focus on paths, transitions, and underlying design logic.”
