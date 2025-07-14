# QAT Cognitive Tool Specification (v2.1)

---

@ai-path: <insert from ontology list>
@ai-role: <folder.path.to_tool> 
@ai-toolkit: <associated.toolkit.name>  
@template-version: 2.1.0
@field-mode: strict+inferred
@ai-generated: true
@human-reviewed: true

---

# 🧠 Tool: [Tool Name]

## 🔍 Summary

> _[1–3 sentence description]_  
> Cognitive function or transformation this tool performs within the larger Clowder ecosystem. Include natural-language framing and purpose.
> Emphasize intent and situational use - what this tool does, in LLM-friendly terms.

---

## 🧾 Tool Metadata

| Field             | Value                         |
|------------------|-------------------------------|
| Tool ID          | `[toolkit_id].[tool_id]`      |
| Version          | `0.1.0`                        |
| Maintainer       | `@your_handle_or_email`        |
| Tags             | `[nlp, synthesis, embedding]` |
| License          | MIT / Apache-2.0 / etc.        |

---

## 📥 Inputs

| Name        | Type                           | Description                                  | Required |
|-------------|--------------------------------|----------------------------------------------|----------|
| `input_1`   | `str`                          | Natural language prompt                      | yes      |
| `fileset`   | `List[FileBlob]`               | Source files to analyze                      | no       |
| `params`    | `Dict[str, Any]`               | Execution config                             | no       |
| `...`       | `str` / `List` / `Dict` / etc. | What this tool expects                       | yes/no   |

> Structs may reference entries from `qat_struct.md` if reused.

---

## 📤 Outputs

| Name        | Type                                             | Description                              |
|-------------|--------------------------------------------------|------------------------------------------|
| `summary`   | `str`                                            | Human-facing output                      |
| `results`   | `List[AnalysisBlock]`                            | Structured output for downstream use     |
| `signals`   | `Optional[DriftSignal]`                          | Flags for reflection/evaluation          |
| `...`       | `List[SegmentSummary]` / `Dict[str, Any]` / etc. | How the tool emits its results           |

---

## 🧭 Natural Language Coordination

### Trigger

<When or how this tool is invoked — e.g., called by `synthesis.pipeline.merge`, or triggered after `retrieval.selector`.>

### Upstream Tools

- `embedding_validator`
- `topic_mapper`
- <Which tools, pipelines, or outputs contribute input?>

### Downstream Consumers

- `topic_synthesizer`
- `concept_graph_builder`
- <Which tools, pipelines, or outputs consume this output?>

**Message Shape:**  

```json
{
  "role": "<tool/agent>",
  "input": "<varies>",
  "output": "<varies>",
  "context": {
    "pipeline_id": "...",
    "user_intent": "...",
    "priority": "high"
  }
}
```

---

## 🔄 MCP Contract (Mission–Coordination–Payload)

### 🧭 Mission

- Clarify design purpose, transformation goal, and user intent this tool addresses.
- Ex: “Summarizes code clusters across files using topic similarity and structural tags.”

### 🔧 Coordination Contract

- Trigger Conditions: `called within flow 'embedding_synth'`
- Required Precursor: `embedding_mapper`, `topic_chunker`
- Produces Output For: `topic_synth`, `fork_agent`, `pipeline.logger`

### 🧠 Payload & Fidelity Notes

- Critical IO assumptions: embedding space must be pre-validated
- Safety net: fallback on `drift_signal` if coverage < 70%
- Budget-awareness: if `params['cost_estimate']` > threshold → raise

---

## 🧵 Reflex Path

| Condition                         | Action                                  |
|----------------------------------|-----------------------------------------|
| Output mismatches prior summary  | Trigger `.intent.md` fork               |
| Drift in embedding topic space   | Emit `DriftSignal` with confidence score|
| Missing struct compatibility     | Flag in `audit.md`                      |

---

## 🧱 Logic Modules

> See `tool.modules.md` for complete logic graph. Summary:

- `embed_normalizer` → `cluster_topics` → `retrieve_similar_segments` → `compose_response`

---

## 🧑‍💻 Codex Runtime Tips

- Output must be Markdown or JSON serializable
- Avoid `eval()` or file writes unless inside `CodexContext`
- Return objects using field headers only, not prose
- Use `params` dictionary for all tunable runtime switches

## 🧠 Internal Notes

- Idempotent: <yes/no>
- Heavy IO: <yes/no> (for Codex budget awareness)
- Stateless or Stateful: <brief explanation>
- Inference Profile:
    <What the LLM is expected to infer or assume if under-specified?>

## 🧩 Design Rationale

<Why this tool is structured this way — tradeoffs, drift-protection, fallback logic, extensibility.>

---

## 📎 Example Invocation

```json
{
  "input_1": "Summarize all concepts related to memory scaffolding.",
  "fileset": ["memory_hooks.py", "intent_tracker.py"],
  "params": {
    "embedding_model": "text-embedding-ada-002",
    "match_threshold": 0.78,
    "output_mode": "clustered"
  }
}
```

## 🪞 Reflex Notes

When invoked with conflicting upstream embeddings and mismatched clusters, this tool may enter meta-review mode.
In such cases, it must emit a .intent.md record describing the decision edge encountered.

## 🛡️ Risk & Evaluation

| Area               | Status                        | Notes                            |
| ------------------ | ----------------------------- | -------------------------------- |
| Human Review       | ❌                            |                                  |
| Trust Level        | `ai-generated`                | Confirmed output fidelity needed |
| Critical Drift Tag | `embedding.cluster_drift`     | Requires test probes             |
| Eval Scenarios     | Linked in `eval.md` (pending) |                                  |

---

## ❌ Edge Cases

| Situation               | Handling Strategy                           |
| ----------------------- | ------------------------------------------- |
| Missing fields          | Default to schema guard; emit warning       |
| IO mismatch             | Raise structured validation error           |
| No matches or empty set | Return stubbed summary or fallback response |

## ✅ Test Guarantees

- <Example: Produces valid summaries for 10MB+ text input>
- <Example: Rejects malformed metadata with clear trace>
- <Example: Operates under zero-config fallback>

## 🔗 Related

- Toolkit: <toolkit.name>
- Pipelines: <pipeline.name>
- Related Tools: <tool.name.other>, <retriever.selector>, etc.

---

## 📚 Related Files

- tool.modules.md
- qat_struct.md
- eval.md
- instructions.md

## 📚 Maintenance Metadata

``` yaml
created: 2025-07-13
last_updated: 2025-07-13
tags: [inference, summarization, modular, Codex-safe]
```
