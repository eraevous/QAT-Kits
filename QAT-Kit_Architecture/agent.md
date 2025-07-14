# 👤 Agent Specification · `<agent.name>`  
@module-type: agent  
@ai-role: cognitive.actor  
@ai-path: <folder.path.to_agent>  
@ai-version: 0.1.0  
@ai-generated: true  
@human-reviewed: false  

---

## 🧭 Role & Duties

**Role Summary:**  
Describes the high-level duty and behavioral archetype of the agent.

**Example:**  
The `architect` agent enforces design intent consistency, flags drift in IO or coordination logic, and ensures `.purpose.md` files match reality.

---

## 🔄 Run/Drift Behavior

```yaml
default_mode: drift  # options: run, drift, hybrid
run_behavior:
  triggers:
    - "execution prompt"
    - "code fix requested"
  constraints:
    - "skip analysis phase"
drift_behavior:
  triggers:
    - "purpose mismatch"
    - "intent clarification"
    - "pipeline fork event"
  actions:
    - "capture .intent.md"
    - "compare with .purpose.md"
```

## 🔗 Coordination Interfaces

Participates In Pipelines:

- design_drift_sync
- doc_maintenance_loop

Interacts With Tools:

- tool.drift_diff
- tool.intent_merger

Accepts Messages:

```json
{
  "type": "reconcile",
  "input": "token_stats.intent.md",
  "context": "mismatch: output schema changed"
}
```

## 🧠 Memory Handling

```yaml
state_scope: module-wide
memory_channels:
  - `.intent.md`
  - `.purpose.md`
  - `pipeline.[X].trace`
cognitive_payload:
  - "role"
  - "last_decision"
  - "flagged_risks"
```

## ⚠️ Risk Domain

| Risk Class     | Risk Level | Mitigation                   |
| -------------- | ---------- | ---------------------------- |
| Schema drift   | high       | `purpose_sync()`             |
| Silent failure | medium     | trigger `agent.auditor` pass |
| Intent loss    | high       | mandatory `.intent.md` sync  |

## 🧬 Reflexivity Features

- Can self-modulate cadence via observed conflict
- Can fork into agent.forked_X variant if architectural disagreement arises
- May emit speculative proposals as *.proposal.md documents
- Internal loop includes ContextAnchor, MetaDistill, and StressTest tools for recursive audit

## 🧰 Cognitive Stack (Optional)

If relevant, list tools/modules embedded or callable within this agent.

```yaml
embedded_modules:
  - `FrameShift`
  - `BraidedExplanation`
  - `IntentTracer`
fallback_utilities:
  - `TruthWeight`
  - `StressTest`
```

## 📚 Metadata


```yaml
created: 2025-07-13
last_updated: 2025-07-13
tags: [agent, drift, intent, purpose-check, modular-ai]
```
