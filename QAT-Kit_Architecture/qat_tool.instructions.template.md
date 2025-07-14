# 🧠 `ToolName` · QAT Tool Instruction Template (LLM-Aware + Malleability-Aware)

> **Use Case:** This file provides grounding for LLM-based agents using or generating QAT tools.  
> It defines purpose, cognitive scaffolding, IO shape, reasoning constraints, and invocation norms.

---

## 🗭 Overview

| Field           | Description                                                                 | Flexibility           |
|----------------|------------------------------------------------------------------------------|-----------------------|
| `tool_name`     | Human-readable title                                                        | 🟢 Inference-Friendly |
| `qat_id`        | Unique identifier for the QAT system                                        | 🔴 Fixed Schema       |
| `version`       | Version of tool instructions                                                | 🔴 Fixed Schema       |
| `associated_files` | Tool file(s) this governs (e.g., `.tool.json`, `.modules.json`)          | 🟡 Soft-Guarded       |

---

## 🌟 Purpose

> Why this tool exists, who it helps, and what gap it fills.

**Describe the tool’s purpose in clear natural language.**  
Use metaphor or examples if helpful. Avoid dry summaries.

| Field       | Type       | Description                                  | Flexibility       |
|-------------|------------|----------------------------------------------|-------------------|
| `problem`   | string     | User-facing issue or gap                     | 🟢                |
| `gain`      | string     | What benefit the user gets                   | 🟢                |
| `why-now`   | string     | Why this matters in current context/system   | 🟢                |

---

## 🧰 Capabilities Matrix

| Capability         | Description                                                      | Required? | Flexibility  |
|--------------------|------------------------------------------------------------------|-----------|--------------|
| Decomposes         | What kinds of input it can parse or segment                      | Optional  | 🟢           |
| Synthesizes        | Whether it fuses multiple sources                                | Optional  | 🟢           |
| Evaluates          | Applies scoring, ranking, heuristics                             | Optional  | 🟡           |
| Orchestrates       | Can direct downstream tools or agents                            | Optional  | 🟡           |
| Self-reflects      | Supports `self_applicable: true` usage                           | Optional  | 🔴 (Boolean) |
| Memory-linked      | Accesses `.intent.md`, `.purpose.md`, `context_bundle`           | Optional  | 🟡           |

> ✅ Use boolean or enum tags where clarity helps Codex behavior.

---

## 🔣 Inputs

> Describe expected fields, constraints, and reasoning roles.

| Field         | Type     | Description                                   | Required | Default | Flexibility |
|---------------|----------|-----------------------------------------------|----------|---------|-------------|
| `input_text`  | string   | Raw input (file, block, segment, etc.)        | Yes      | —       | 🟢           |
| `intent_tag`  | string   | e.g. “summarize”, “rank”, “interlink”         | Yes      | —       | 🔴 (Enum)    |
| `context`     | object   | Design memory or prior output                 | Optional | null    | 🟡           |
| `mode`        | string   | e.g. “strict”, “exploratory”                  | Optional | "strict"| 🔴 (Enum)    |

### 🔐 Appendix: Valid `intent_tag` and `mode` values

- `intent_tag`: `summarize`, `cluster`, `critique`, `rank`, `trace`, `decompose`, `synthesize`
- `mode`: `strict`, `drift`, `fork`, `reflect`, `guided`

---

## 📄 Outputs

| Field            | Type     | Description                                        | Flexibility |
|------------------|----------|----------------------------------------------------|-------------|
| `summary`        | string   | Main prose block                                   | 🟢          |
| `modular_output` | object   | Block-labeled fields like `key_findings`, `io_map` | 🟡          |
| `raw_json`       | dict     | Structured payload                                 | 🔴          |
| `citation_map`   | list     | Optional source references                         | 🟡          |

> 💡 Encourage output tagging by intended use: `@for:cli`, `@for:docgen`, `@for:rerun`.

---

## 🧱 Reasoning Scaffolding

> How the LLM should think.

- Preferred structure: `Observation → Analysis → Reflection → Output`
- Fallback path: `retry with adjusted filter`, `invoke subtool`, or `fork agent`
- Reflective steps: `Check drift from user intent`, `log design memory`

| Element                  | Required | Flexibility  |
|--------------------------|----------|--------------|
| Recursive reasoning      | Yes      | 🟡           |
| Pattern match to context | Yes      | 🟡           |
| FrameShift applicable?   | Optional | 🔴 (Boolean) |

---

## 🧹 Modules

> List core functions + IO sketch.

| Module ID      | Description                              | Output Block                 |
|----------------|------------------------------------------|------------------------------|
| `extract_concepts` | Identifies latent structure in input | `modular_output["concepts"]` |
| `summarize_path`   | Builds summary + relevance map       | `summary`, `citation_map`    |

> Validate against `qat_tool.modules.json`. Each `Module ID` must match there.

---

## 🔄 Pipeline Role

| Field       | Value                                        | Flexibility  |
|-------------|----------------------------------------------|--------------|
| `feeds_to`  | Tools that depend on this output             | 🟡           |
| `used_by`   | Tools or agents invoking this one            | 🟡           |
| `stage_tag` | e.g. `preprocessing`, `synthesis`, `reflect` | 🔴 (Enum)    |

---

## 🧪 Invocation Schema

> Provide invocation examples *for Codex-like agents*:

```markdown
You are running `ToolName`, a QAT tool built to analyze semantic clusters in research files.
Use mode: `exploratory`, intent: `cluster`.
Generate a modular_output with `summary`, `topics`, and `relevance_ranking`.
If input is ambiguous, run FrameShift and reroute output to ForkAgent.
```

---

## ⚠️ Known Risks & Failure Modes

| Risk Type         | Likely Failure                 | Mitigation Strategy                    |
|-------------------|--------------------------------|----------------------------------------|
| Fuzzy input       | Misclassification              | Require mode: `strict`                 |
| Overgeneration    | Summary too verbose            | Enforce modular blocks                 |
| Hallucinated logic| Confabulated links             | Apply `TruthWeight` post-pass          |
| Spec mismatch     | Wrong IO format                | Validate against `.modules.json`       |

---

## 🧬 Cognitive & System Tags

```yaml
tags:
  - toolkit:qat
  - agent:architect
  - category:summarizer
  - semantic_unit:topic_bundle
  - risk:medium
```

> 🧠 Use these for filtering, search, UI anchors, or drift recovery.

---

## 📘 Dictionary Appendix

| Field          | Description                                                             |
|----------------|-------------------------------------------------------------------------|
| `@ai-intent`   | Natural language explanation of task or reasoning mode                  |
| `@ai-role`     | Which agent types this tool binds to (`synthesizer`, `fork_agent`, etc) |
| `mode`         | Control switch for tool behavior (`drift`, `strict`, etc.)              |
| `intent_tag`   | Operation context (`summarize`, `cluster`, `trace`)                     |
