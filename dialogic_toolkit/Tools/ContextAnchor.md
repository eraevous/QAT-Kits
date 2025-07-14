# 🧠 ContextAnchor Instructions

## Purpose

ContextAnchor is designed to preserve, compress, and reactivate the core ideas, reasoning threads, and identity-level scaffolds of a conversation. It enables robust context retrieval by distilling threads into cognitively meaningful segments that can be stored, indexed, reloaded, or cross-referenced by future tools.

It serves as a **bridge** between exploratory conversation and structured memory — helping users avoid idea drift, context loss, or rework by anchoring important insights and thread contours.

---

## Invoked When:

* A conversation becomes long, recursive, or layered
* User wants to **“remember this for later”** or **“package this for reuse”**
* Preparing to fork, clone, or migrate context
* Starting a new phase of a project and need summary memory

---

## Input

* Full thread transcript, Markdown export, or self-reference to current thread
* Optional summary objective (e.g., “retain design heuristics,” “preserve reasoning path,” “capture strategic decision points”)
* Optional thread title or future use-case signal

---

## Output

* A structured distillation organized by:

  1. **High-Level Topics**
  2. **Key Vocabulary / Concepts**
  3. **Actionable Insights**
  4. **Frameworks / Methods**
  5. **Unresolved Questions**
  6. **Applications / Forking Points**

* Also returns: a narrative map and a retrieval hook (summary phrase, timestamp, or mnemonic).

* Optionally includes:

  * Layered summaries (zoomed-in / zoomed-out)
  * Compression signal (e.g. “This anchors 11.2k tokens of prior content”)

---

## Behavior

ContextAnchor uses a hybrid distillation model:

1. **Thematic Segmentation** – Group conversation into cognitive modules based on topic, purpose, and rhythm.

2. **Memory-Preserving Summarization** – Extract insight without over-compressing nuance. Balance core takeaways with conceptual scaffolding.

3. **Reactivation Hooks** – Embed references, mnemonics, or labels that will help the user reconnect emotionally or cognitively in future sessions.

4. **Promptable Format Generation** – Package the output into a form easily referenceable by other tools or prompts.

---

## Best Practices

* **Anchor identity-forming ideas** (e.g. values, self-assignments, concept metaphors)
* **Capture reasoning pivots** and logic forks
* **Map tooling decisions or framework evolution**
* **Include invented language or coined frames**
* Flag **points of ambiguity**, friction, or potential drift

---

## Example Prompts

* “Distill this thread into memory anchors for future scaffolding.”
* “Summarize this dialogue into reactivatable context for tool reuse.”
* “Create scaffolds for forking this session into new design phases.”
* “Anchor the key heuristics and working assumptions that defined this project.”

---

## Cross-Tool Synergy

* Use alongside `TokenMap` to segment long conversations
* Pair with `MetaDistill` to extract patterns of method
* Feed into `TruthWeight`, `BraidedExplanations`, or future forks via structured prompt prefixes

---

## Invocation Tags

* context-anchor
* memory-scaffold
* thread-fork-ready
* recall-kit

---

## Thread Types

* architect
* thinker
* designer
* system-crafter
* memory-integrator

---

## Known Limitations

* May require tuning for emotional nuance or narrative drift
* Should not overwrite divergent interpretations without flagging them
* Does not replace TokenMap; they serve complementary cognitive roles

---

## Authors

Zach Rhodes & GPT Collaboration – 2025
