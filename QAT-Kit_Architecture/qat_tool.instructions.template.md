# 🧠 Tool: {Tool_Name} (Required)

---

## AI Tags (Required)

@ai-role: Which agent types this tool binds to - populate from ontology list
@ai-path: {folder.path.to_tool}
@ai-toolkit: {associated.toolkit.name }
@template-version: 2.1.0
@field-mode: strict+inferred
@ai-generated: true
@human-reviewed: true
@ai-mode: Control switch for tool reasoning style or mode intention - populate from ontology list
@ai-risk: {low/medium/high/experimental}
@ai-intent`: Natural language explanation of task or reasoning

## 🔍 Summary (Required)

> _{1–6 sentence description}_  
> Cognitive function or transformation this tool performs within the larger Clowder ecosystem. Include natural-language framing and purpose.
> Emphasize intent and situational use - what this tool does, in LLM-friendly terms.
---

## 🧾 Tool Metadata (Required)

| Field            | Value                          | Required | Flexibility |
|------------------|--------------------------------|----------|-------------|
| Tool ID          | `[toolkit_id].[tool_id]`       | Yes      | 🔴          |
| Version          | `0.1.0`                        | No       | 🟡          |
| Author           | `[name_1, name_2]`             | No       | 🟡          |
| Maintainer       | `@your_handle_or_email`        | No       | 🟢          |
| Tags             | `[nlp, synthesis, embedding]`  | No       | 🟢          |
| License          | MIT / Apache-2.0 / NA / etc.   | Yes      | 🟡          |

---

## Natural Language Logic (Required)

### 🌟 Purpose (Required)

> Why this tool exists, who it helps, and what gap it fills.

**Describe the tool’s purpose in clear natural language.**  
Use metaphor or examples if helpful. Avoid dry summaries.

### Intention Matrix (Required)

| Field       | Type       | Description                                  | Required | Flexibility |
|-------------|------------|----------------------------------------------|----------|-------------|
| `problem`   | string     | User-facing issue or gap                     | Yes      |🟢           |
| `gain`      | string     | What benefit the user gets                   | No       |🟢           |
| `why-now`   | string     | Why this matters in current context/system   | No       |🟢           |

---

### 🧰 Capabilities Matrix (Optional)

| Capability         | Description                                            | Required | Flexibility        |
|--------------------|--------------------------------------------------------|----------|--------------------|
| Decomposes         | What kinds of input it can parse or segment            | No       | 🟢                 |
| Synthesizes        | Whether it fuses multiple sources                      | No       | 🟢                 |
| Evaluates          | Applies scoring, ranking, heuristics                   | No       | 🟡                 |
| Orchestrates       | Can direct downstream tools or agents                  | No       | 🟡                 |
| Self-reflects      | Supports `self_applicable: true` usage                 | No       | 🔴 (Boolean)       |
| Memory-linked      | Accesses `.intent.md`, `.purpose.md`, `context_bundle` | No       | 🟡                 |
| `...`              | {What abstract actions this tool can perform}          | {Yes/No} | {🟢/🟡/🔴 (Enum)} |

> ✅ Use boolean or enum tags where clarity helps runtime behavior.
<!-- hint: Write each capability as a short declarative phrase. Example: "Summarizes code paths using vector clusters." -->

---

### 🧠 Internal Notes (Optional)

- Idempotent: {yes/no}
- Heavy IO: {yes/no}
- Stateless or Stateful: {brief explanation}
- Inference Profile:
    {What the LLM is expected to infer or assume if under-specified?}

### 🧩 Design Rationale (Optional)

{Why this tool is structured this way — tradeoffs, drift-protection, fallback logic, extensibility.}

### 🧭 Coordination (Optional)

#### 🧪 Invocation Schema & Trigger (Optional)

<When or how this tool is invoked — e.g., called by `synthesis.pipeline.merge`, or triggered after `retrieval.selector`.>

##### 📎 Example Invocation 1 (Optional)

```markdown
You are running `ToolName`, a QAT tool built to analyze semantic clusters in research files.
Use mode: `exploratory`, intent: `cluster`.
Generate a modular_output with `summary`, `topics`, and `relevance_ranking`.
If input is ambiguous, run FrameShift and reroute output to ForkAgent.
```

##### 📎 Example Invocation 2 (Optional)

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

### 🧱 Reasoning Scaffolding (Optional)

> How the LLM should think.

- Preferred structure: `Observation → Analysis → Reflection → Output`
- Fallback path: `retry with adjusted filter`, `invoke subtool`, or `fork agent`
- Reflective steps: `Check drift from user intent`, `log design memory`

| Element                   | Required | Flexibility  |
|---------------------------|----------|--------------|
| Recursive reasoning       | No       | 🟡           |
| Pattern match to context  | No       | 🟡           |
| Self-Applicable           | No       | 🟡           |
| Dialogic/Dialogue         | No       | 🟢           |
| {Cognitive Pattern/Mode}  | {Yes/No} | {🟢/🟡/🔴}  |

---

## IO (Required)

### 📥 Inputs (Required)

> Describe expected fields, constraints, and reasoning roles.

| Field         | Type                        | Description                                  | Required | Default   | Flexibility        |
|---------------|-----------------------------|----------------------------------------------|----------|-----------|--------------------|
| `input_text`  | Text                        | Natural language prompt                      | Yes      | —         | 🟢                 |
| `intent_tag`  | Text                        | e.g. “summarize”, “rank”, “interlink”        | Yes      | —         | 🔴 (Enum)          |
| `fileset`     | List                        | Source files to analyze                      | No       | null      | 🟡                 |
| `params`      | Pair List                   | Execution config                             | No       | null      | 🟡                 |
| `context`     | object                      | Design memory or prior output                | No       | null      | 🟡                 |
| `mode`        | Text                        | e.g. “strict”, “exploratory”                 | No       | "strict"  | 🔴 (Enum)          |
| `...`         | {Text / List / Data / etc.} | {What this tool expects}                     | {Yes/No} | {default} | {🟢/🟡/🔴 (Enum)} |

> Structs may reference entries from `qat_struct.md` if reused.

#### 🔐 Appendix: Valid `intent_tag` and `mode` values

- `intent_tag`: `summarize`, `cluster`, `critique`, `rank`, `trace`, `decompose`, `synthesize`
- `mode`: `strict`, `drift`, `fork`, `reflect`, `guided`

---

### 📤 Outputs (Required)

| Name             | Type                          | Description                              | Required | Default                        | Flexibility        |
|------------------|-------------------------------|------------------------------------------|----------|--------------------------------|--------------------|
| `summary`        | Text                          | Human-facing main prose block & output   | Yes      | "{Tool_Name} ran successfully" | 🟢                 |
| `results`        | List                          | Structured output for downstream use     | No       | —                              | 🟡                 |
| `signals`        | `DriftSignal`                 | Flags for reflection/evaluation          | No       | —                              | 🔴                 |
| `modular_output` | Data                          | Block-labeled fields                     | No       | —                              | 🔴                 |
| `raw_json`       | Data                          | Structured payload                       | No       | —                              | 🟡                 |
| `citation_map`   | List                          | Optional source references               | No       | —                              | 🟡                 |
| `...`            | {List / Data / String / etc.} | How the tool emits its results           | {Yes/No} | {default}                      | {🟢/🟡/🔴 (Enum)} |

> 💡 Encourage output tagging by intended use: `@for:cli`, `@for:docgen`, `@for:rerun`.

---

## 🔄 Pipeline Role (Optional)

> See flow.md

### Upstream Tools (Optional)

- `embedding_validator`
- `topic_mapper`
- <Which tools, pipelines, or outputs contribute input?>

### Downstream Consumers (Optional)

- `topic_synthesizer`
- `concept_graph_builder`
- <Which tools, pipelines, or outputs consume this output?>

### Message Shape (Optional)

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

## 🔄 MCP Contract (Mission–Coordination–Payload) (Required)

### 🧭 Mission (Required)

- Clarify design purpose, transformation goal, and user intent this tool addresses.
- Ex: “Summarizes code clusters across files using topic similarity and structural tags.”

### 🔧 Coordination Contract (Required)

- Trigger Conditions: `called within flow 'embedding_synth'`
- Required Precursor: `embedding_mapper`, `topic_chunker`
- Produces Output For: `topic_synth`, `fork_agent`, `pipeline.logger`

### 🧠 Payload & Fidelity Notes (Required)

- Critical IO assumptions: embedding space must be pre-validated
- Safety net: fallback on `drift_signal` if coverage < 70%
- Budget-awareness: if `params['cost_estimate']` > threshold → raise

---

## Logic Structure

### 🧵 Reflex Path (Optional)

| Condition                        | Action                                  |
|----------------------------------|-----------------------------------------|
| Output mismatches prior summary  | Trigger `.intent.md` fork               |
| Drift in embedding topic space   | Emit `DriftSignal` with confidence score|
| Missing struct compatibility     | Flag in `audit.md`                      |
| `...`                            | 
---

### 🧱 Logic Modules (Optional)

> See `tool.modules.md` for complete logic graph. Summary:

- `embed_normalizer` → `cluster_topics` → `retrieve_similar_segments` → `compose_response`

> List core functions + IO sketch.

| Module ID          | Description                              | Output Block                 |
|--------------------|------------------------------------------|------------------------------|
| `extract_concepts` | Identifies latent structure in input | `modular_output["concepts"]` |
| `summarize_path`   | Builds summary + relevance map       | `summary`, `citation_map`    |
| `...`              |

> Validate against `qat_tool.modules.json`. Each `Module ID` must match there.

---

### 🪞 Reflex Notes (Optional)

> Notes on execution, mitigation, and LLM execution intricacies

## 🛡️ Risk & Evaluation (Required)

### ⚠️ Known Risks & Failure Modes  (Required)

| Risk Type          | Likely Failure                 | Mitigation Strategy                    |
|--------------------|--------------------------------|----------------------------------------|
| Fuzzy input        | Misclassification              | Require mode: `strict`                 |
| Overgeneration     | Summary too verbose            | Enforce modular blocks                 |
| Hallucinated logic | Confabulated links             | Apply `TruthWeight` post-pass          |
| Spec mismatch      | Wrong IO format                | Validate against `.modules.json`       |
| `...`              |

---

### ❌ Edge Cases (Optional)

| Situation               | Handling Strategy                           |
| ----------------------- | ------------------------------------------- |
| Missing fields          | Default to schema guard; emit warning       |
| IO mismatch             | Raise structured validation error           |
| No matches or empty set | Return stubbed summary or fallback response |

### ✅ Test Guarantees (Optional)

- <Example: Produces valid summaries for 10MB+ text input>
- <Example: Rejects malformed metadata with clear trace>
- <Example: Operates under zero-config fallback>

### 🌟 Mitigation (Optional)

| Area               | Status                        | Notes                            |
| ------------------ | ----------------------------- | -------------------------------- |
| Human Review       | ❌                            |                                  |
| Trust Level        | `ai-generated`                | Confirmed output fidelity needed |
| Critical Drift Tag | `embedding.cluster_drift`     | Requires test probes             |
| Eval Scenarios     | Linked in `eval.md` (pending) |                                  |


## 🔗 Related (Optional)

- Modules: <toolkit_modules.name>
- Pipelines: <pipeline.name>
- Related Tools: <tool.name.other>, <retriever.selector>, etc.

## 📚 Maintenance Metadata  (Required)

``` yaml
created: 2025-07-13
last_updated: 2025-07-13
tags: [inference, summarization, modular, Codex-safe]
```
