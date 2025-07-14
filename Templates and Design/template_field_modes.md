# 📘 QAT Field Modes Specification

> Field governance and cognitive affordance tagging for all core templates.

Each field in a QAT template is classified by its **flexibility** and **semantic sensitivity**.

---

## 🎛️ Field Modes (Tag Reference)

| Mode        | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| `@required` | Must be explicitly filled. Omission is an error.                            |
| `@optional` | May be omitted. Defaults or no-ops are acceptable.                          |
| `@inferred` | Derived by Codex from context, metadata, or connected modules.              |
| `@locked`   | Must not be modified unless human-verified or `@cadence:drift` is triggered.|
| `@dynamic`  | Expected to vary during execution or pipeline composition.                  |
| `@scaffold` | Structural field that frames or organizes but has no execution impact.      |
| `@codex-hint` | Helps LLMs infer behavior but is nonfunctional at runtime.                |

---

## 🧰 Field Mode Matrix by Template

### 🧩 `clowder.template.md`

| Field         | Mode        | Notes                                      |
|---------------|-------------|--------------------------------------------|
| `id`          | `@required` | Canonical namespace identifier             |
| `name`        | `@required` | Human-facing display name                  |
| `version`     | `@required` | Semver-style                               |
| `description` | `@required` | Summarizes scope and philosophy            |
| `toolkits`    | `@required` | Declares active toolkits                   |
| `pipelines`   | `@optional` | Not all clowders require pipelines         |
| `agents`      | `@optional` | May be implied by tool/pipeline assignment |
| `instructions`| `@optional` | Fallback to default if omitted             |
| `graph`       | `@optional` | Derivable from roles or manifest           |
| `audit`       | `@optional` | Will be filled after compliance pass       |
| `index`       | `@required` | Link to manifest                           |
| `metadata.*`  | `@inferred` | Often populated by PurposeWeaver           |

---

### 🧠 `agent.template.md`

| Field           | Mode        | Notes                                         |
|-----------------|-------------|-----------------------------------------------|
| `id`            | `@required` | Must match manifest + graph references        |
| `role`          | `@required` | Codex behavior pattern (use `roles.ontology`) |
| `cadence_mode`  | `@inferred` | From `@ai-cadence:` usage                     |
| `instructions`  | `@required` | Codex/LLM instruction block                   |
| `io_contract`   | `@required` | Declares expected shape of communication      |
| `drift_rules`   | `@optional` | Augments Run/Drift override logic             |
| `fields_locked` | `@locked`   | Prevents Codex from violating governance      |

---

### 🛠 `tool.template.md`

| Field         | Mode        | Notes                                      |
|---------------|-------------|--------------------------------------------|
| `id`          | `@required` | Canonical reference                        |
| `name`        | `@required` | Human label                                |
| `description` | `@required` | Short functional summary                   |
| `inputs`      | `@required` | Exact input shape                          |
| `outputs`     | `@required` | Must list fields + data types              |
| `integration` | `@optional` | Downstream/upstream coordination           |
| `tags`        | `@optional` | Surface hints (for search, clustering)     |
| `agent_role`  | `@inferred` | Often deduced from function                |
| `scaffolded_by`| `@scaffold`| Links to pipeline/toolkit scaffold         |
| `locked_fields`| `@locked`  | Prevent automated redefinition             |

---

### 🧪 `pipeline.template.md`

| Field           | Mode        | Notes                                    |
|-----------------|-------------|------------------------------------------|
| `id`            | `@required` | Unique reference                         |
| `name`          | `@required` | Human label                              |
| `steps`         | `@required` | Ordered actions/tools                    |
| `control_logic` | `@optional` | Branching, fallbacks                     |
| `shared_inputs` | `@optional` | Used in RAG / data prep loops            |
| `cadence`       | `@inferred` | Implied from context                     |
| `locked`        | `@locked`   | Stable flow for CI/CD                    |

---

### 🧱 `toolkit.template.md`

| Field       | Mode        | Notes                                 |
|-------------|-------------|---------------------------------------|
| `id`        | `@required` | Bundle ID                             |
| `tools`     | `@required` | List of tool IDs                      |
| `focus`     | `@optional` | Theme or intent area                  |
| `agents`    | `@optional` | Roles allowed in this bundle          |
| `integration`| `@optional`| Shared pre/post-processing guidance   |

---

## 📌 Usage in Toolchain

- `PurposeWeaver` will flag violations of `@required`, suggest defaults for `@optional`, and attempt inference of `@inferred` fields.
- `Codex` will treat `@codex-hint` as soft semantic scaffolds.
- `DriftDiff` alerts when `@locked` fields are unintentionally modified.
