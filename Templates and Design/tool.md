# 🛠️ Tool Specification · `<tool.name>`  

@module-type: tool  
@ai-role: <insert from ontology list>  
@ai-path: <folder.path.to_tool>  
@ai-toolkit: <associated.toolkit.name>  
@ai-version: 0.1.0  
@ai-generated: true  
@human-reviewed: false

---

## 🔍 Summary

**Purpose:**  
<1–3 sentence description of what this tool does, in LLM-friendly terms. Emphasize intent and situational use.>

**Design Pattern:**  
<select: standalone | composable | orchestration-bound | passive hook>

---

## 📥 Inputs

| Name      | Type                           | Required | Description                        |
|-----------|--------------------------------|----------|------------------------------------|
| `...`     | `str` / `List` / `Dict` / etc. | yes/no   | What this tool expects             |

---

## 📤 Outputs

| Name      | Type                                             | Description                    |
|-----------|--------------------------------------------------|--------------------------------|
| `...`     | `List[SegmentSummary]` / `Dict[str, Any]` / etc. | How the tool emits its results |

---

## 🧭 Coordination

**Trigger:**  
<When or how this tool is invoked — e.g., called by `synthesis.pipeline.merge`, or triggered after `retrieval.selector`.>

**Downstream Use:**  
<Which tools, pipelines, or outputs consume this data?>

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

## 🧠 Internal Notes

- Idempotent: <yes/no>
- Heavy IO: <yes/no> (for Codex budget awareness)
- Stateless or Stateful: <brief explanation>
- Inference Profile:
    <What the LLM is expected to infer or assume if under-specified?>

## 🧩 Design Rationale

<Why this tool is structured this way — tradeoffs, drift-protection, fallback logic, extensibility.>

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

## 📚 Metadata

``` yaml
created: 2025-07-13
last_updated: 2025-07-13
tags: [inference, summarization, modular, Codex-safe]
```
