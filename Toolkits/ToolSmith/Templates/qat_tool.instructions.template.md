# 🛠️ ToolName Instructions

## 🧠 Purpose

Brief summary of this tool’s purpose — what cognitive function it serves, what kind of user problem it solves, and what input/output behavior it supports.

---

## ✅ Capabilities & Core Behaviors

- Breaks down: [task or object]
- Outputs: [what type of results]
- Handles: [vague input? format detection?]
- Tailors output: [optional — for user goals or context]

---

## 🔍 Inputs

| Field         | Description                       |
|--------------|-----------------------------------|
| input_1       | Describe what this is             |
| input_2       | Optional — explain how it helps   |

---

## 📤 Outputs

- `output_1`: [Short description]
- `output_2`: [Optional or alternative outputs]

If output_format is `modular_report`, define likely sections.

---

## Scaffolding Strategy

Information on what additional logic should be followed by the LLM to reliably execute your tool.

---

## 🔄 Modules (if any)

If present in `.tool.json.modules[]`, list and briefly describe them.

- `module_1`: Short explanation
- `module_2`: Optional subroutine behavior

---

## Best Use Cases

- Use Case 1
- Use Case 2


---

## 🧭 Suggested Prompts

- “Run ToolName on this [X]”
- “What does this [X] reveal?”
- “Tailor my [resume/goals/input] using ToolName”

---

## 🧩 Use in Pipeline

- Used in: `pipeline.json.step`
- Accepts: `provides[]` from prior tool(s)
- Feeds into: `next tool or stage`

---

## 🧠 Additional Guidance & Invocation Notes

- May invoke: `invocable_tools[]`
- Supports: feedback loop / reflection / chaining (based on flags)
- Output will influence downstream prep or user action

---

## ⚠️ Caveats, Caution , & Guardrails

- Tool may misinterpret if input is poorly structured.
- Always verify tailored suggestions before submission.
- Red flags are advisory, not definitive.

---

## 🧬 Invocation Tags

Use tags for memory anchors (e.g., `job-hunter:start`, `toolsmith:reflect`, etc.)
---

## Related Tools & Synergies

| Tool              | Integration Use                                   |
|-------------------|---------------------------------------------------|
| `Tool 1`          | Notes on purpose and relation                     |
| `Tool 2`          | Notes on purpose and relation                     |

---

## Final Design Prompt

Text intended to ground the LLM while invoking your tool.
This can include intentions, guidance, mission statement, narrative, etc