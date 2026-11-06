# effort-cost: design notes

Kit-owned and ungoverned (no Telosmith records), per the Telosmith scope agreed on 2026-11-05/06.

## Why it exists

- **Origin.** Zach (2026-11-06, QAT lane). A conversation with his partner about literary analysis: he suggested setting the effort to high, and she was reluctant because the environmental and social costs are unknown. His idea: a thread knows enough about place, time and the conversation to give a heuristic evaluation of the cost of bumping the effort.
- **First tool of the creation feasibility study.** Arm A: slim ToolSmith, the validator, and hand-adapted runtimes. See [docs/creation-study.md](../../docs/creation-study.md).
- **No neighbor covers it.** No QAT tool estimates costs or compares one model setting with another.

## Choices and the alternatives rejected

- **Location is an optional scenario, not the default (v0.3).** Revised at Zach's request on 2026-11-06 at 11:17 CT: "Chicago, which has access both to plentiful water, nuclear power, and other differences vs if I were in Silicon Valley".
  - v0.1–0.2 used location for nothing but the country.
  - v0.3 adds a labelled row, "at proposed if served near you", that uses the user's state grid average and a water note. It never replaces the default rows, because consumer ChatGPT routing is undisclosed. OpenAI offers inference residency by region only to Enterprise and Edu customers.
  - Rejected: replacing the default with the local grid. That would give precise-looking numbers for a grid that may not be the one serving the request.
  - **What the figures show:**
    - Carbon: Illinois (0.23 g/Wh) is not cleaner than California (0.18 g/Wh, in-state generation) on EIA's 2024 state averages.
    - Water: the Great Lakes advantage is real but finite. Illinois is still among the five states with the most new datacenters in high water-stress locations.
    - So "Chicago vs Silicon Valley" splits by measure: probably better on water, not on carbon.
  - Only Illinois and California are in the table so far. EIA pages for Texas and Virginia could not be fetched in this session.
- **Time of day adjusts the default carbon factor**, because US datacenters share the evening peak. The bands are 10 am–4 pm 0.30, 4–10 pm 0.45, and 0.35 otherwise. These are assumptions.
- **The check tells the user to run it on the lightest setting.** A live ChatGPT test showed the check itself ran for 51 seconds at High, so it cost about what it measured.
- **The setting is a fill-in.** In the same live test, ChatGPT could not see its own effort setting.
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

- **Absolute menu, not current-vs-proposed (v0.4).** Zach, 2026-11-06 11:42 CT: "if it's already at high, you can do what it would cost at high. If it's at low, you can also do what it would cost at high … including different model options."
  - Every setting is priced for the request, and a named setting only marks a row.
  - This also removes the dependence on the current setting, which ChatGPT cannot see.
- **The check must cost less than what it informs (v0.4).** Zach: "evaluating should not cost more than the thing it's evaluating."
  - The check states its own cost: about 0.24 Wh on Instant, about 9 Wh on Thinking high.
  - It counts as worth running only at 10× or more. The live runs confirmed the arithmetic: a 14 Wh gap is worth checking on Instant, not on High.
  - The pocket card answers the common case at zero cost.
- **Perspective scales with size (v0.4).** Zach asked for household, car and computer comparisons when numbers get large.
  - Anchors are tiered from Wh to GWh, g to t, and mL to Olympic pools, plus a "million answers like this" line.
  - **v0.5:** that line now uses fixed multipliers (0.095, 0.22, 0.91). ChatGPT Instant mis-converted the units in both live v0.4 runs: 37,000 household-days instead of 37, and 0.0012 car-years instead of about 1.3.
- **Estimated place and time are allowed (v0.5).** ChatGPT supplied an approximate location and time from its own context, even in a Temporary chat. They may be used if labelled "estimated".

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
