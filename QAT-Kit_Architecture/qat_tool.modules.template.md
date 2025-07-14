# 🧩 QAT Tool Modules Template (Markdown)

@template-version: 2.1
@format-type: template
@ai-role: modules.subroutine\_graph
@field-mode: strict+inferred
@ai-hint: Generate in blocks. Treat each module as independently invocable.

---

## 🧠 Module Graph Overview

> *Explain what these modules represent in your tool.*
> This is a named list of logic units that form the execution graph of your tool.
> Each should be composable, idempotent (if possible), and have well-scoped IO.

---

### 📄 Module Index

> Use the table below to list modules in sequence order.

| ID (module\_id) | Type       | Description            | Order |
| --------------- | ---------- | ---------------------- | ----- |
| `{{module_id}}` | `{{type}}` | {{1-sentence purpose}} | #     |

---

## 🔧 Module Definitions

> Copy this structure per module.

### 🧩 `{{module_id}}`

* **Type**: `transform` | `analyze` | `dispatch` | `filter` | `synthesize` | `fork` | `visualize`
* **Description**: *Sentence about the module's role in the pipeline.*
* **Inputs**:

  * `{{input_name}}`: `{{Type}}` — {{purpose}}
* **Outputs**:

  * `{{output_name}}`: `{{Type}}` — {{purpose}}
* **Order**: `#` *(Integer - defines execution position)*
* **Optional Notes**:

  * Heuristics: *{min\_size, tolerance, etc.}*
  * Flags: *e.g., `skip_if_empty`, `emits_drift_signal`*

---

## 🪞 Module Reflex Flags (Optional)

| Module ID       | Reflex Trigger | Action Taken                          |
| --------------- | -------------- | ------------------------------------- |
| `{{module_id}}` | `{{event}}`    | `{{emit DriftSignal / fork / retry}}` |

---

## 🧱 Schema Reference

> List all IO types that must exist in `qat_struct.md`.
> These must be semantically stable types for Codex/ToolSmith reuse.

* `{{CustomType}}`: used in `inputs[]` of `{{module_id}}`
* `SegmentSummary`, `DriftSignal`, etc.

---

## 🧩 Assembly Graph (Optional)

```mermaid
graph TD;
  A[{{module_1}}] --> B[{{module_2}}]
  B --> C[{{module_3}}]
```

---

## 🧠 Design Hints for ToolSmith

| Principle             | Practice                                                                 |
| --------------------- | ------------------------------------------------------------------------ |
| Single Responsibility | Keep module functions tightly scoped (avoid multi-action blocks)         |
| Clear Naming          | Prefer `verb_object` like `generate_summary`, `fetch_segments`           |
| Order Matters         | Sequence should match logical execution → `normalize → cluster → output` |
| Self-contained        | Modules should be invocable in isolation for testing                     |

---

## ✅ Module Checklist

* [ ] All modules have unique `module_id`
* [ ] All inputs/outputs are typed (or reference `qat_struct`)
* [ ] Modules are ordered logically
* [ ] Reflex triggers noted if applicable
* [ ] Mermaid graph added if flow is complex

---

## 📌 Template Notes

> This file may be generated or extended by ToolSmith agents.
> All fields marked `{{...}}` must be filled, but generation may use `@inferred` values for most defaults.
> Runtime agents may evaluate IO fidelity based on declared types and coordinate with upstream tools.

## 🔗 Related

- Instructions: <toolkit_instructions.name>
- Pipelines: <pipeline.name>
- Related Tools: <tool.name.other>, <retriever.selector>, etc.

## 📚 Maintenance Metadata

``` yaml
created: 2025-07-13
last_updated: 2025-07-13
tags: [inference, summarization, modular, Codex-safe]
```
