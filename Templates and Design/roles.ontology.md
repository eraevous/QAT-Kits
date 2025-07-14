# 🧠 QAT-Kit Role & Function Ontology

> A shared vocabulary and semantic schema for the functional behavior of tools, agents, and modules in the QAT-Kit and Clowder ecosystems.

---

## 📦 Overview

This ontology defines standardized roles and cognitive modes for all components — including tools, agents, pipelines, and templates — to enable:

- 🔁 Role-based execution within pipelines
- 🔐 Schema validation via `@ai-role`, `@agent-role`, `@module-type`, and other tags
- 🤝 Interop across Codex, Toolsmith, QAT-Kit, and custom forks

All roles are assumed to be **natural-language native**, semantically inferable by LLMs, and resolvable by either hard schema or contextual pattern matching.

---

## 🧱 Ontology Levels

| Layer      | Keyword          | Applies To             |
|------------|------------------|------------------------|
| Tool Role  | `@ai-role:`      | Toolkits, tools        |
| Agent Role | `@agent-role:`   | Codex behavior modules |
| Pipeline Step | `@step-type:` | Pipeline stages        |
| Module Type | `@module-type:` | Any file/template      |

---

## 🔧 Tool Roles (`@ai-role:`)

| Role                   | Description                                                                       |
|------------------------|-----------------------------------------------------------------------------------|
| `analysis.utility`     | Performs internal computation, parsing, inspection (e.g., token counts, AST diff) |
| `retrieval.selector`   | Gathers, ranks, or filters contextual information                                 |
| `synthesis.engine`     | Merges, generates, or summarizes structured knowledge                             |
| `diagnostic.lens`      | Applies heuristics, flags errors, or maps drift                                   |
| `transform.compiler`   | Converts between representations (e.g., graph → prompt)                           |
| `scaffold.generator`   | Builds templates, contracts, or purpose files                                     |
| `agent.interface`      | Exposes internal state/tools to a Codex agent                                     |
| `memory.recorder`      | Writes `.intent.md`, `.purpose.md`, or `.meta.json` entries                       |

---

## 🧠 Agent Roles (`@agent-role:`)

| Role                | Description                                                                |
|---------------------|----------------------------------------------------------------------------|
| `architect`         | Oversees schema adherence, module health, and semantic cohesion            |
| `executor`          | Implements code logic or resolves intent into artifacts                    |
| `drift_guard`       | Detects divergence from declared structure or intent                       |
| `toolsmith`         | Creates or modifies tools and templates, reconciles structure with need    |
| `memory_architect`  | Maintains `.intent.md` trails and `.purpose.md` alignment                  |
| `fork_agent`        | Preserves alternate reasoning branches or speculative designs              |
| `risk_auditor`      | Flags issues around cost, legality, ethics, or external dependencies       |

---

## 🔄 Pipeline Step Types (`@step-type:`)

| Type             | Description                                                            |
|------------------|------------------------------------------------------------------------|
| `ingest`         | Pull in and clean input data                                           |
| `analyze`        | Parse, tokenize, extract metrics or structure                          |
| `evaluate`       | Apply tests, heuristics, or constraints                                |
| `transform`      | Reformat, recompile, or reshape data                                   |
| `synthesize`     | Merge knowledge into summaries, insights, or master documents          |
| `route`          | Conditional logic for branching execution paths                        |
| `output`         | Deliver final artifact (e.g. JSON, Markdown, API call, plot)           |
| `reconcile`      | Sync or compare `.purpose.md` with source outputs                      |

---

## 🔖 Module Types (`@module-type:`)

| Type             | Description                                                 |
|------------------|-------------------------------------------------------------|
| `toolkit`        | A named collection of related tools                         |
| `tool`           | A single executable or callable logic unit                  |
| `pipeline`       | Declarative flow of tools and agents                        |
| `agent`          | Persistent behavior interface assumed by LLMs/Codex         |
| `instruction`    | Runtime configuration or execution rules for a clowder      |
| `graph`          | Node/edge maps of IO, semantic dependency, or coordination  |
| `manifest`       | Indexed list of all components and their current states     |
| `audit`          | Health check and mismatch report for templates or modules   |

---

## 🧪 Future Extensions

```yaml
# Experimental roles and future states

- ai-role: translation.bridge
  # Converts human intentions into pipelines or tool scaffolds

- agent-role: planner
  # Capable of decomposing intention into roadmap + MVP + CI stages

- step-type: introspect
  # Examines LLM outputs, traces, and behaviors recursively

- module-type: fork
  # Designated alt-path structure, auto-compared via `ForkDiff`
```

## 🧷 Validation

All templates must tag their modules with @module-type: and one or more of the above roles as applicable.

Use MetaChecker or SchemaGuard to enforce canonical values.

## 📘 Related Files

- clowder.md
- clowder.schema.json
- template_field_modes.md
- .purpose.md, .intent.md
