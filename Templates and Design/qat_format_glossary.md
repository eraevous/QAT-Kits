# 📗 QAT-Kit Format Glossary

> A shared semantic dictionary for tags, annotations, metadata fields, and structured comments used across the Clowder architecture.

Each format element is designed for **clarity, interoperability, and Codex comprehension** — ensuring that natural language engines, pipelines, and agents operate on a **shared symbolic grammar**.

---

## 🔖 Global Prefixes and Namespaces

| Prefix         | Meaning                                          | Notes                         |
|----------------|--------------------------------------------------|-------------------------------|
| `@ai-*`        | LLM-assigned semantic fields                     | Used by Codex/QAT agents      |
| `@human-*`     | Explicit human annotations                       | Useful for review checkpoints |
| `@drift-*`     | Fields related to cadence, drift, and reflection | Run/Drift protocol            |
| `@codex-*`     | Codex-specific hints or scaffolds                | Not evaluated by runtime      |

---

## 🔩 Structural Tags

| Tag                  | Description                                                       |
|----------------------|-------------------------------------------------------------------|
| `@ai-path:`          | Canonical dotted path of the module/tool/agent                    |
| `@ai-role:`          | Agent/tool role (from `roles.ontology.md`)                        |
| `@ai-intent:`        | Natural-language summary of function/purpose                      |
| `@ai-version:`       | SemVer-style version control for tools/modules                    |
| `@ai-tags:`          | Comma-separated keyword hints (for search, categorization)        |
| `@ai-generated:`     | Flag indicating system-generated content                          |
| `@ai-verified:`      | True/false — verified against expected schema                     |
| `@ai-risk:`          | Coded risk rating (`low`, `medium`, `high`, `unknown`)            |
| `@ai-used-by:`       | Downstream modules/tools using this component                     |
| `@ai-depends-on:`    | Explicit dependencies not captured in imports                     |
| `@ai-output:`        | Declared output schema (format, type, role)                       |
| `@ai-pipeline-order:`| Declares non-default execution order if needed (`inverse`)        |

---

## 🧠 Drift & Memory Tags

| Tag                 | Meaning                                                              |
|---------------------|----------------------------------------------------------------------|
| `@drift-tag:`       | Label for content needing review/reflection                          |
| `@drift-candidate:` | Suggests future module/tool/agent for upgrade or retirement          |
| `@cadence:`         | Indicates whether this interaction is `run`, `drift`, or `sync`      |
| `@intent-timestamp:`| ISO 8601 timestamp for `.intent.md` trail capture                    |

---

## 🧾 Human & Review Tags

| Tag                   | Purpose                                                             |
|-----------------------|---------------------------------------------------------------------|
| `@human-reviewed:`    | Boolean — has a human signed off?                                   |
| `@human-notes:`       | Free-form notes intended for collaborators, not Codex               |
| `@human-author:`      | Name/email/alias of original contributor                            |
| `@human-edited:`      | Boolean — was this template or entry manually adjusted              |

---

## 🎯 Function-Specific Tags

| Tag                  | Notes                                                                |
|----------------------|----------------------------------------------------------------------|
| `@test-cases:`       | Link or describe where tests live or how this module is validated    |
| `@output-format:`    | Precise structure returned (`List[Dict[str, Any]]`, `JSON`, etc.)    |
| `@integration-mode:` | Whether it’s `standalone`, `loopable`, `agent-coordinated`, etc.     |
| `@indexable:`        | Whether this should be stored/referenced in manifest or search graph |
| `@scaffold:`         | This module/tool is a placeholder awaiting elaboration               |

---

## 🧪 Example Block

- @ai-path: core.synthesis.concept_indexer
- @ai-role: agent.indexer
- @ai-intent: "Clusters document embeddings by topic, retrieves matches, and synthesizes a relevance-weighted index."
- @ai-tags: synthesis, retrieval, embedding, topic-modeling
- @ai-risk: medium
- @ai-version: 0.4.2
- @ai-output: List[Dict[str, Union[str, float]]]
- @ai-used-by: core.pipeline.topic_synth
- @drift-tag: coherence-review
- @human-reviewed: false
- @scaffold: true

## 🧠 Codex Interpretation Notes

- All @ai-* and @drift-* tags are parsed and contextualized by Codex under the QAT-Kit protocol.
- Tools like DriftDiff, PurposeWeaver, and CodexWeaver enforce consistency, completion, and reflection across tags.
= Tags do not require strict ordering but must appear in the metadata section of each template.
