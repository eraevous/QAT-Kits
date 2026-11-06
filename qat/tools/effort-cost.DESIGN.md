# effort-cost: design notes

Kit-owned and ungoverned (no Telosmith records), per the Telosmith scope agreed on 2026-11-05/06.

## Why it exists

- **Origin.** Zach (2026-11-06, QAT lane). A conversation with his partner about literary analysis: he suggested setting the effort to high, and she was reluctant because the environmental and social costs are unknown. His idea: a thread knows enough about place, time and the conversation to give a heuristic evaluation of the cost of bumping the effort.
- **First tool of the creation feasibility study.** Arm A: slim ToolSmith, the validator, and hand-adapted runtimes. See [docs/creation-study.md](../../docs/creation-study.md).
- **No neighbor covers it.** No QAT tool estimates costs or compares one model setting with another.

## Choices and the alternatives rejected

- **The user's location barely moves the estimate.** The answer is computed in a datacenter, not on the user's home grid.
  - Zach's intuition that place and time help is partly right. Time of day shifts the carbon factor, because US datacenters share the evening peak.
  - Place mostly tells you which country's datacenters are likely.
  - Rejected: using the user's local grid intensity. It would produce precise-looking numbers for the wrong grid.
- **Ranges, not points.** Published per-query energy figures for comparable settings disagree by more than tenfold:
  - Google's measured fleet median is 0.24 Wh.
  - Modeled estimates for GPT-5 at high effort are 17–40 Wh.
  - Rejected: a single "best estimate". It would hide the most decision-relevant fact, which is that nobody outside the providers knows.
- **Coefficients live in a table in the spec**, so a refresh doesn't touch the method. The runtime texts inline the same table, so they must be updated together.
- **Cost sits next to value.** A cost figure alone invites either guilt or dismissal. The decision is whether *this request* benefits.
- **A lean, not a verdict.** The tool can say "bump for this message only", but the user decides. It never moralizes.
- **ChatGPT runtime: a paste block first, a plugin skill second.**
  - A paste block works in any thread today. It is answered by the thread's own model with the whole thread in view.
  - Custom GPTs are being retired in favor of plugins (new creation ended late Oct 2026; retirement Dec 11, 2026 / Feb 11, 2027 by plan). So the `@` path is a plugin skill.
  - Whether an `@`-invoked plugin sees the whole thread is unverified.

## Distinctions that must survive revisions

- Compute location ≠ user location.
- An assumed setting ≠ a stated setting. The model may not know its own effort level.
- Next answer, next N answers, and the difference are separate rows.
- On-site water ≠ water including power generation.
- Excluded from every figure: training, hardware manufacture, networking, the user's device.

## Evidence

- **Sources:**
  - OpenAI average query 0.34 Wh and 0.32 mL (Jun 2025).
  - Google Gemini median text prompt 0.24 Wh, 0.03 g, 0.26 mL (Aug 2025; arXiv 2508.15734).
  - Epoch AI, GPT-4o about 0.3 Wh plus long-context scaling (Feb 2025).
  - Jegham et al., "How Hungry is AI?" (arXiv 2505.09598 v6, Nov 2025): per-model tables, GPT-5 effort levels, Azure PUE 1.12, WUE 0.30 + 4.35 L/kWh, CIF 0.35.
  - University of Rhode Island GPT-5 estimate via Tom's Hardware / The Guardian (Aug 2025).
- **Assumptions, labelled in the spec:**
  - The medium-effort row (interpolated).
  - The Pro row (about 3× high).
  - The time-of-day carbon adjustments.
  - The context add-on bands, interpolated from Epoch's two points.
- **Cold-run results:** [qat/eval-runs/2026-11-06/RESULTS.md](../eval-runs/2026-11-06/RESULTS.md).

## Open questions

- Should social costs (water stress, local grid prices, labor) get more than one line? Zach asked about "environmental or social costs".
- The refresh cadence for the coefficient table.
- Whether to verify, in ChatGPT, that an `@`-invoked plugin sees the thread.
- Whether ChatGPT reliably knows its own effort level. If it does, the settings question can go.
