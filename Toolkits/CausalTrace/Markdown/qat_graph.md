# 🕸 Tool DAG Graph Node: CausalTraceNarrator

## 🧷 Node

- **ID:** CausalTraceNarrator  
- **Type:** reasoning_tool  
- **Entry:** true  
- **Description:** Simulates execution flow in natural language from code structure and prompt

---

## 🔗 Edges

1. `DesignIntentAnalyzer` → `CausalTraceNarrator`  
   - **Type:** context_flow  
   - **Description:** Passes architectural reasoning to guide narration

2. `CausalTraceNarrator` → `TestSynthesizer`  
   - **Type:** data_flow  
   - **Description:** Enables test hypothesis generation

3. `CausalTraceNarrator` → `ReflectiveAgent`  
   - **Type:** feedback_loop  
   - **Description:** Reflects on alignment between prompt and trace
