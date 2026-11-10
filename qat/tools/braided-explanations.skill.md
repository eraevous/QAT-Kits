---
name: "braided-explanations"
version: 1.0.0
description: "Teach a concept through braided strands (formal, poetic, analogical, skeptical, historical, experiential) built from WWH micro-chunks. Use when the user invokes BraidedExplanations or wants a concept explained from several angles rather than one."
---

# BraidedExplanations

## Purpose
Support learners who synthesize understanding through multiple explanatory styles. Present a topic through distinct, parallel explanatory **strands** that together form a rich, dynamic grasp of one conceptual core, rather than repeating the same explanation in different words.

Each strand is made of one or more **strings**. The default string for a strand is a native explanation in that strand's mode. Additional strings come from the WWH Braiding method below.

Assume the user is an intelligent, nonlinear thinker who values texture over polish.

Use a sibling skill instead when the user wants an idea challenged rather than explained (stress-test) or two positions weighed (truth-weight).

## Invocation
If invoked with no topic, give a one-line summary, list the six strands and the WWH strings, and ask what to explain.

## Default strands
- 🧪 **Technical/Formal**: precise, structured, system-level explanation
- 🎭 **Poetic/Intuitive**: evocative, aesthetic, emotionally resonant description
- 🧩 **Metaphorical/Analogical**: illustrative comparisons and mental models
- 🧐 **Skeptical/Challenger**: critical inquiry, edge cases, failure points
- 🧵 **Contextual/Historical**: origins, evolution, surrounding influences
- 🧠 **Experiential/Cognitive**: how it feels to use or apply the concept in practice

## Choosing a path
- **Quick path** (a single concept, a short question, or a follow-up in an ongoing exchange): don't open with questions. Give a one-line interpretation, braid a compact version with the 2–3 strands that add the most, and end with one line offering adjustments (more depth, other strands, harmony vs. contrast, sequential chunks).
- **Full path** (an involved tutorial, a broad topic, or a learning plan, where a wrong guess would waste a long answer): follow the full workflow below, including clarifying questions.

When unsure, take the quick path; the closing line lets the user steer.

## Full workflow
1. **Interpret.** Begin by relaying your understanding of what you're being asked to explain and the learning goal. In the same interpretation, say which strands you'll use and which WWH strings you'll add to each, with a brief reason.
2. **Clarify.** Ask brief questions to set:
   - preferred length and depth
   - desired strands (on/off or prioritized)
   - whether to chunk into sequential sub-parts
   - harmony or productive contrast between voices
   - related concepts or directions to explore or avoid
   Skip any or all of these when (a) the user has already answered them explicitly, implicitly, or by derivation, or (b) your interpretation already settles most of them. You may add your own questions in service of the learning goal.
3. **Braid.** Return the explanation with each strand clearly labeled and well-formed, all focused on the same core. Build complete WHAT–WHY–HOW loops before moving to the next conceptual unit. Strands may reinforce, contrast, or enrich one another; where they genuinely differ, contrast them. Use clear transitions between strands. Stay concise in each strand unless longer exploration is requested.
4. **Integrate.** Offer a summary, synthesis, or reweaving into one working mental model, plus limits or common misconceptions and an optional practice example. Offer related conceptual paths only when they serve the stated goal.

## WWH Braiding (strings)
Rather than long isolated passes (all the WHAT, then all the WHY, then all the HOW), interleave them in **micro-chunks**, closing each loop before moving on:

- 🔹 **WHAT** (definition / structure): define the idea as clearly and succinctly as possible; establish boundaries, role, essential identity. *e.g. "Temptation bundling is pairing something you need to do with something you want to do."*
- 🔸 **WHY** (cause / motivation / function): why it exists, what problem it solves, what role it plays; root it in internal logic, external constraints, or personal context. *e.g. "It works because it anchors a less-rewarding task to a dopaminergic boost."*
- 🔹 **HOW** (operation / behavior / examples): how it behaves in practice or over time; interactions, pitfalls, example flows. *e.g. "I play a specific playlist only while doing dishes; now dishes cue the music and vice versa."*

Each chunk is complete and actionable by itself; over time the loops stack into a full dynamic system model.

**Optional add-ons:**
- ▪️ **WHERE / WHO / WHEN**: social, historical, or narrative grounding; identity, role models, developmental timeline.
- 🪞 **REFLECTION**: "How does this show up in my life?" "When does it fail?" "How would I teach it to someone like me?"

**Why it works** (the method was designed for AuDHD learning): it closes loops fast for working memory; frequent closure keeps tangents from leaking attention; it favors system-mapping over rote procedure; each WHY/WHAT resolves ambiguity quickly; and it builds a layered graph of understanding instead of linear piles.

### Chunk template
```
## Topic: [topic]
### 🔹 WHAT: [definition or structure]
### 🔸 WHY: [function, principle, problem solved]
### 🔹 HOW: [behavior, application, edge cases, examples]
### ▪️ (Optional) WHERE / WHO / WHEN: [historical, social, personal anchor]
### 🪞 (Optional) Reflection: [relationship to the idea; what changed]
```

## Output
**Interpretation of the learning goal**, **braided explanation**, **integrated model**, **limits or misconceptions**, **optional practice/example** (full path); interpretation line, compact braid, and adjustment offer (quick path).

## Checks
- Every strand must advance understanding, not rephrase the same paragraph. Don't force all six strands on a short question.
- The Poetic/Intuitive strand must still carry a real idea; evocative but empty is a failure.
- Label analogies as analogies and say where they break down.

## Provenance
Restored from the user's original BraidedExplanations_Full.md (QAT-Kit), including the embedded WWH Braiding method: (in the owner's Drive; link not published). Added in adaptation and review: the integration step, output list, checks, and the quick/full path split (the original already allowed skipping clarifying questions when answers were inferable).