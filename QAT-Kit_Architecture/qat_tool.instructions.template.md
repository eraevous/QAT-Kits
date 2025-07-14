# 🧠 Tool Instructions Template (v2.1 Finalized Draft)

---

## 🤖 AI Tags (Static Metadata)

```yaml
@ai-role: [executor, analyzer, distiller]               # ✓ From roles.ontology.md
@ai-path: toolkit/[tool_name]/tool.md                   # ✓ Path within the clowder
@ai-toolkit: [toolkit_name]                             # ✓ Toolkit container
@template-version: 2.1.0                                # ✓ Locked version
@field-mode: strict+inferred                            # ✓ Controls validation behavior
@ai-generated: true                                     # ✓ Provenance flag
@human-reviewed: true                                   # ✓ Trust flag
@ai-mode: [strict|drift|fork|reflect|adaptive]          # ✓ From ai-mode enum
@ai-risk: [low|medium|high|experimental]                # ✓ Risk classification
@ai-intent: "Summarizes concepts by similarity"         # ✓ Natural-language tool summary
```

---

## 🔍 Summary (Static Narrative)

> _1–6 sentence natural-language explanation._
> Explain what this tool does, for whom, and why.
> Keep structure and use-case intent clear.

---

## 🗾️ Tool Metadata (Static Field Table)

### Example Table

| Field         | Example Value                  | Required | Type         | Notes                                |
|---------------|--------------------------------|----------|--------------|--------------------------------------|
| Tool ID       | `text_synth.embed_merger`      | Yes      | string       | Globally unique                      |
| Version       | `0.1.0`                        | No       | semver       |                                      |
| Maintainer    | `@handle`                      | No       | string       |                                      |
| Tags          | `[nlp, summarization]`         | No       | list[string] | Optional categorization              |
| License       | `MIT`                          | Yes      | enum         | MIT / Apache-2.0 / proprietary / N/A |

---

## 👁️ Purpose Statement (Explanatory Narrative)

> Why this tool exists, the cognitive job it does, and its utility.
> State the gap it fills in human or LLM workflows.

---

## 🏛️ Intention Matrix (Explanatory Config Table)

| Field       | Description                                | Example                              |
|-------------|--------------------------------------------|--------------------------------------|
| `problem`   | What the user struggles with               | "Can't synthesize multi-file topic." |
| `gain`      | What benefit the tool provides             | "Returns clustered thematic summary" |
| `why-now`   | Urgency or relevance                       | "Used during vector-index design."   |

---

## 🛠️ Capabilities Matrix (Configurable Behavior Table)

| Capability       | Description                                       | Allowed Values       | Required |
|------------------|---------------------------------------------------|----------------------|----------|
| `decomposes`     | Can segment or break apart large inputs           | true / false         | No       |
| `synthesizes`    | Combines or fuses information                     | true / false         | No       |
| `evaluates`      | Scores, ranks, or compares results                | true / false         | No       |
| `orchestrates`   | Directs flow to other tools                       | true / false         | No       |
| `self_reflects`  | Applies its own logic recursively                 | true / false         | No       |
| `memory_linked`  | Accesses `.intent.md` or prior session memory     | true / false         | No       |

---

## 📅 Runtime Notes (Example)

```yaml
idempotent: true
heavy_io: false
state_profile: stateless
inference_profile: 
  - "Infers task intent from `intent_tag`"
  - "Assumes file order = topic sequence"
```

---

## 🧬 Coordination Contract

### 🔮 Invocation Triggers (Examples)

- Called within flow: `concept_merge`
- Activated after: `vector_stitcher`
- Reentrant: `true`

### 🚗 Upstream & Downstream (Examples)

| Role           | Tool Name(s)                   |
|----------------|--------------------------------|
| Upstream       | `embedding_mapper`, `splitter` |
| Downstream     | `summary_writer`, `ForkAgent`  |

---

## 🎓 Reasoning Pattern (Optional Cognitive Plan)

### 🧱 Reasoning Scaffolding

> How the LLM should think.
> What metacognitive patterns are prioritized and used by the LLM.

- Preferred structure: `Observation → Analysis → Reflection → Output`
- Fallback path: `retry with adjusted filter`, `invoke subtool`, or `fork agent`
- Reflective steps: `Check drift from user intent`, `log design memory`

| Element                   | Required |
|---------------------------|----------|
| Recursive reasoning       | No       |
| Pattern match to context  | No       |
| Self-Applicable           | No       |
| Dialogic/Dialogue         | No       |

### 🪞 Reflex Notes

> Notes on execution, mitigation, and LLM execution intricacies
> Provides guidance and guardrails for the LLM to handle advanced cognitive modes.

### Examples

#### Strategy

Observation → Cluster → Summarize → Emit

#### Fallback

If no clusters, return stub with `drift_signal`

---

## 📊 Inputs (Strict Field Table)

| Field       | Type         | Description                          | Required | Default   |
|-------------|--------------|--------------------------------------|----------|-----------|
| `input_text`| string       | Prompt or text block                 | Yes      | —         |
| `fileset`   | list[string] | Files to draw from                   | No       | []        |
| `params`    | dict         | Execution tuning parameters          | No       | null      |
| `intent_tag`| enum         | [summarize, cluster, rank, reflect]  | Yes      | "cluster" |
| `mode`      | enum         | [strict, drift, exploratory]         | No       | strict    |

---

## 📈 Outputs (Strict Contract Table)

| Field            | Type         | Description                             | Required | Notes              |
|------------------|--------------|-----------------------------------------|----------|--------------------|
| `summary`        | string       | Human-facing prose summary              | Yes      | Markdown allowed   |
| `results`        | list         | Parsed or structured breakdown          | No       | JSON preferred     |
| `signals`        | DriftSignal  | Trigger for reflex or fallback review   | No       | Optional           |
| `raw_output`     | dict         | Full emission as Codex-compatible block | No       | Codex-safe format  |

---

## 🔄 MCP (Mission—Coordination—Payload)

### 🚀 Mission

- Example: "Cluster research topics and output synthesized description."

### 🔧 Coordination

- Trigger: After embedding validation
- Preconditions: files must contain vector tags
- Routes output to: `concept_map`, `summary_writer`

### 🤓 Payload

- Fallback to `drift_signal` on topic mismatch
- Truncate at cost threshold if `params.max_cost` exceeded

---

## 🔄 Reflex Paths (Examples)

| If Condition                        | Then Action                          |
|-------------------------------------|--------------------------------------|
| output fails to parse topic clusters| emit `drift_signal`, downgrade mode  |
| over-length output                  | truncate summary + flag in audit     |

---

## 💡 Example Invocation

```json
{
  "input_text": "Summarize key design ideas from QAT-Kit",
  "fileset": ["agent.md", "toolkit.md"],
  "intent_tag": "summarize",
  "mode": "strict"
}
```

---

## 🔒 Trust & Risk Block (Examples)

| Risk Area     | Level   | Mitigation                  |
|---------------|---------|-----------------------------|
| hallucination | medium  | enforce enum output         |
| drift         | low     | reflex fallback enabled     |
| IO shape      | low     | validate via `qat_struct.md`|

---

## 🔗 Related (Example)

```yaml
modules: [cluster_topics, filter_segments]
pipelines: [concept_merge]
related_tools: [topic_mapper, ForkAgent]
```

---

## 📃 Maintenance Metadata

```yaml
created: 2025-07-13
last_updated: 2025-07-13
tags: [reflective, clustering, Codex-safe]
```

---

## 🪧 ToolSmith Prompt Note

> "Given this template, fill in a new tool spec for a summarization agent that uses frame detection and citation mapping across an essay corpus."
> Use this document as canonical shape during tool generation. Avoid hallucination by drawing only from templates inside the QAT-Kit system.
