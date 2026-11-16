# Selective Self-Distillation: partial-adoption.txt

Input: one pasted conversation, 2 user turns (L1-2, L7-8), 1 model turn (L4-5). No paste delimiters, quoted lines or role inversions; no turns flagged. Extraction script not run (optional for this input).

## 1. Evidence table

| Claim | His words (verbatim) | Source | Label |
|---|---|---|---|
| He wants a plan for learning to cook on weeknights | "I need a plan for learning to cook on weeknights." | L2 | Direct |
| Cook three recipes on rotation for a month | "Yes to the three-recipe rotation" | L8 (proposal: model, L5 part A) | Adopted, with a condition |
| One of the three recipes must be vegetarian | "but only if one of them is vegetarian" | L8 | Revised (his condition on proposal A) |
| Batch-cook everything on Sunday | "No to Sunday batch cooking" | L8 (proposal: model, L5 part B) | AI proposal, rejected |
| The point is cooking on weeknights, not reheating | "I want to actually cook on weeknights, that's the point." | L8 | Direct |

Minimal context (model text, L5): "(A) cook the same three recipes on rotation for a month, and (B) batch-cook everything on Sunday so weeknights are just reheating."

## 2. Reconstruction

I want to learn to cook on weeknights (L2). A three-recipe rotation for a month works, as long as one recipe is vegetarian (L8). Sunday batch cooking doesn't: if weeknights are just reheating, I'm not learning to cook on weeknights, and that's the point (L8).

Not his: the one-month length and the idea of a rotation came from the model (L5). His "yes" to the rotation adopts them, but only the vegetarian condition and the rejection of batch cooking are his own additions.

## 3. Changes of mind

None. He states one goal (L2) and holds it; his L8 turn applies that goal to sort the model's proposals rather than revising it.

## 4. How he works (keyword counts, 1 short exchange)

- Split verdict on a bundled proposal (1): accepts one part and rejects the other in one turn. Example: "Yes to the three-recipe rotation ... No to Sunday batch cooking" (L8).
- Conditional acceptance (1): "only if". Example: "but only if one of them is vegetarian" (L8).
- Rejects a proposal by appeal to the original goal (1). Example: "that's the point" (L8).

## 5. Unresolved attribution

- Whether he accepts the "for a month" duration specifically. "Yes to the three-recipe rotation" names the rotation, not its length. Check: ask him, or look for a later turn that mentions the month.
- Coinage: the labels "three-recipe rotation" and "Sunday batch cooking" are his phrasing of the model's ideas (A) and (B); the ideas themselves are the model's.

## Verification

7 distinct quotations (6 his, 1 model; the ellipsis quote checked as its two parts) checked programmatically against the source with whitespace normalized: 7 passed, 0 failed. Corpus file (item 6) skipped: no files given.
