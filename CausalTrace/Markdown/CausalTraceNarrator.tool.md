# 🛠️ Tool Definition: CausalTraceNarrator

**Version:** 0.1  
**Authors:** ToolSmith-QAT, Zach Rhodes, Toolbox Program GPT  
**Backend:** `chatgpt`  
**Entrypoint:** inline  
**Output Type:** modular_report

---

## 🧠 Description

Simulates and narrates codebase execution in natural language using AST relationships and design intent.

---

## 🧩 Inputs

- `prompt`: Natural-language entrypoint or debug/design intent  
- `edge_graph`: AST or code dependency edge graph  
- `purpose_files`: Module purpose metadata like `.purpose.md`

---

## 📤 Outputs

- `nl_trace_report`: Step-by-step natural language trace  
- `structured_thought_chain`: Machine-readable CoT for downstream LLMs

---

## 🧱 Scaffold Goals

1. Simulate causal code execution from entrypoints  
2. Enrich traces with architectural purpose and prompt alignment

---

## 🧪 Prompts

- “If I invoke `command X`, what happens?”
- “What part of the code does Y when I change Z?”
- “Explain what leads to this line being hit in a trace”

---

## 🔄 Reflex Paths

- `clarify_input_if_missing`  
- `fallback_to_static_analysis`

---

## 📏 MCP Contract

- **Preconditions:** Valid graph and at least one entrypoint
- **Fallback:** Guess intent from known tool patterns
- **Constraints:** No fabrication of unsupported behaviors
- **Verified by:** ToolSmith-QAT

---

## 🔧 Flags

- Requires input: ✅  
- Pipeline node: ✅  
- Invocable by other tools: ✅  
- Self-applicable: ❌

---

## 🧬 Modules

- `entrypoint_resolver`
- `causal_chain_tracer`
- `architecture_contextualizer`
- `trace_output_formatter`
- `intent_reconciler`
