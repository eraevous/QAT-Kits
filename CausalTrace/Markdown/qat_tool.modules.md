# 🔄 Module Definitions for CausalTraceNarrator

---

## 1. `entrypoint_resolver`

- **Type:** resolution  
- **Inputs:** `prompt`, `edge_graph`  
- **Outputs:** `entrypoint_node`  
- **Order:** 1  
- **Role:** Maps prompt to start node in AST

---

## 2. `causal_chain_tracer`

- **Type:** static_flow_analysis  
- **Inputs:** `entrypoint_node`, `edge_graph`  
- **Outputs:** `causal_sequence`  
- **Order:** 2  
- **Role:** Simulates flow through AST structure

---

## 3. `architecture_contextualizer`

- **Type:** semantic_enrichment  
- **Inputs:** `causal_sequence`, `purpose_files`  
- **Outputs:** `annotated_trace`  
- **Order:** 3  
- **Role:** Links each node to its purpose/intent

---

## 4. `trace_output_formatter`

- **Type:** nl_generation  
- **Inputs:** `annotated_trace`  
- **Outputs:** `nl_trace_report`, `structured_thought_chain`  
- **Order:** 4  
- **Role:** Generates NL narrative + structured output

---

## 5. `intent_reconciler`

- **Type:** intent_alignment  
- **Inputs:** `prompt`, `annotated_trace`  
- **Outputs:** `goal_aligned_trace`  
- **Order:** 5  
- **Role:** Aligns flow with design/debug purpose
