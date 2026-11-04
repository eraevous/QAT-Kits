# Implementation comparison: MetaDistill and ThreadMap, 2026-11-04

Authority: DEC-048 with Kate's amendment. This compares what each copy asks the model to do. It does not pick one. Inventory and sources: `docs/DRIFT_INVENTORY_2026-11-04.md`. Neither tool has a `.qat.md` spec. Vault copies are visible only to line 25 unless stated.

## MetaDistill

Copies: repo `Tools/MetaDistill.md` (775 B), which the vault's `Prompts/MetaDistill/MetaDistill.md` equals in full text; vault `MetaDistill Refinement 1.md` (638 B, 2025-06-18); skill `meta-distill/SKILL.md` (2,760 B).

| Step | Repo and vault text | Vault Refinement 1 | Skill |
|---|---|---|---|
| Scope | "The preceding conversational dialogue" | A proposed extension to meta-prompts | Current conversation up to invocation by default; if too short to hold a method, say so and ask |
| Effectiveness | What made it effective: structure, tone, pacing, intent alignment | none | Effective or ineffective: structure, pacing, tone, alignment with the original goal |
| Tactics | Name tactics (recursion, role-shift, metaphor) | none | Only tactics actually observed (adds context anchoring, dialectic) |
| Method | Extract a reusable method, as prompt or process | none | Same; if the user names an objective, lead with that output |
| Future use | Optional: what could it generate later | none | Optional: plausible uses elsewhere |
| Drift | Clarity or abstraction drift? One way to sharpen | none | Same, "one concrete adjustment" |
| Ownership checkpoint | Three first-person questions the user can ask the model: summarize what we built; which parts did I generate vs you; leaps to slow down | The same three, as a "Midpoint Validation Ritual" in a conversation | The model performs it: summarize; split user-originated, model-originated and joint; flag unsupported leaps |
| Attribution rule | none | none | No authorship claim without evidence; quote the turn where an idea first appears; do not credit yourself for the user's ideas |
| Output | Unspecified | Unspecified | Six named parts: object of analysis, successful tactics, reusable method, ownership/lineage, drift check, one refinement |

Net: the repo asks the model to answer five analytic prompts and leaves the checkpoint as questions for the user to pose, while the skill turns the checkpoint into a required attribution analysis with an evidence rule. The only text the repo has and the skill does not is the question wording and its mid-conversation timing.

## ThreadMap

Copies: repo `Tools/ThreadMap.md` (1,892 B; the vault's `ThreadMap1.md` equals it by size and visible head); vault `Prompts/ThreadMap.md` (1,991 B, 2026-04-22); vault `kAIros/.md` (2,939 B, 2025-09-16, tail unseen); skill `thread-map/SKILL.md` (2,843 B).

| Step | Repo | Vault 2026-04-22 | Vault `kAIros/.md` | Skill |
|---|---|---|---|---|
| Input | Attached log (Markdown, CSV, text); optional objective | "One of": attached log, or the current conversation where this prompt was used | "The entire conversation so far" | Log or excerpts; with no log, map the current conversation if long enough, else ask; optional goal |
| Segmentation | Rhythm, prompt-conclusion seams, AI confusion signs, topic shifts, ~1.5k-token fade signs | Same as repo (+99 B is fully explained by the two input edits) | Same cues plus rhythm change (intro, list "slide" mode, TL;DR); blocks over 1.5k tokens are compression candidates | Topic changes, decisions, intent changes, correction loops, reasoning shifts |
| Per segment | Title, token estimate, where fade-out likely begins, degradation flag, cognitive purpose | Same as repo | Table: Segment, Tokens, Title, Cognitive Function, Fade Warning | Title, purpose, key claims or decisions, links to adjacent sections |
| Size and decay | Estimated tokens; fade zones marked with a warning emoji | Same as repo | Rough token counts; warning when fade is likely | Length only if measured or approximated (words x ~1.3, labelled); no claim to detect hidden context loss |
| Warnings | Heuristic fade zones | Same as repo | Fade and coherence risk | Evidence only: dropped requirement, contradicted decision, unanswered question; speculative fades kept separate |
| Output | Table plus narrative outline; example rows given | Same as repo | Table, narrative (tagged conversational / slide-style / conclusion), then compressed `memory_nodes` | Table plus narrative reconstruction plus "context to carry forward" |
| Extra | Bonus: segmentation for thread stitching | Same as repo (tail unseen) | Step 2 compresses each segment into YAML-compatible nodes | Optional stitching map; by default when moving to a new thread |
| Checks | Manifest caveat: fade estimates heuristic | none visible | "Rigorous, multi-step, YAML-compatible" | Do not pretend to see unsupplied segments; mark uncertain segmentation and inferred links |

Net: three prompts ask for a token-aware fade map; the skill asks for an evidence-only continuity map and a carry-forward list, and says it dropped the 1.5k threshold because current models do not degrade at that length (its own provenance claim, not tested here). The `kAIros/.md` variant alone continues into compression.
