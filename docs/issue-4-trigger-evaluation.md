# Issue #4: evaluation of the trigger table

- **Handoff:** HO-QAT-20261109-4W88 (relay-kit-private), first bounded deliverable for [#4](https://github.com/eraevous/QAT-Kits/issues/4).
- **Author:** claude:qat#01GZK2KjF7UwySqjgiEQFBKD, 2026-11-14.
- **Read against:** QAT-Kits `main` at c981e8c (after #11 merged).
- **Status:** an evaluation note. It doesn't implement routing, change any spec, or designate a canonical tool source; #4 reserves that for Zach.

Claim labels: **[read]** checked in the repo for this note · **[proposal]** this lane's suggestion · **[untested]** a reasoned guess with no run behind it.

## 0. What exists today (this changed since #4 was written)

#4 says the typed `qat/` specs cover only stress-test and truth-weight. That is out of date. [read]

- **Typed specs** (`qat/tools/*.qat.md`, contract-checked by `qat.py`, with eval cases in `qat/cases/`):
  - stress-test 2.0.0
  - truth-weight 2.0.0
  - thread-distill 0.2.1
  - kind-check 0.1.0
  - real-problem 0.1.0
  - toolsmith 0.1.0 (its eval is the creation study, not a cases file)
  - effort-cost 0.6.0
- **Generated skills** (`qat/tools/*.skill.md`, from #11; versioned, not typed, no eval cases):
  - meta-distill 1.0.0
  - thread-map 1.0.0
  - thread-seed 1.0.0
  - negative-space **0.1.0-reconstruction**
  - selective-self-distillation 1.0.0
  - frame-shift, braided-explanations, legal-ease (not in the table)
- **Legacy prose only:** ContextAnchor (`Toolkits/dialogic_toolkit/Tools/ContextAnchor.md`). No spec, version or eval.

## 1. Row by row

Each row gives:
- which tool exists, and in what form;
- an **observable trigger**, something a lane can see in a message or record, not "when it would help";
- the **checked output**;
- **useful vs performative**: what a small trial would look at.

### Row 1. Multi-topic intake / loose brainstorming → ContextAnchor + MetaDistill

- **Exists:**
  - ContextAnchor: legacy prose only.
  - MetaDistill: a generated skill, but it analyses a conversation *as a method*, not as an intake sort.
  - The closest typed tool is **kind-check**. It classifies one item as decision · proposal · challenge · reminder · observation · question · tracking record · mixed · abstain, quoting the item's words as evidence. [read]
- **Observable trigger:** one incoming message carrying three or more distinct topics with no single explicit ask, such as a voice dump or a "thinking out loud" message.
- **Checked output:** each idea gets a kind, a speaker and a pointer. Count **incorrect promotions**: a musing or proposal recorded as a decision.
- **Useful vs performative:**
  - Useful: fewer incorrect promotions than a plain summary, with nothing dropped.
  - Performative: the same items as a summary, just re-labelled.
- **Gap:** the issue's Idea-to-Ontology candidate would be the real tool here, and it doesn't exist yet.

### Row 2. Long thread / successor startup → ThreadMap + ContextAnchor

- **Exists:**
  - **thread-distill** (typed, with eval cases containing planted facts).
  - thread-map and thread-seed (generated skills).
  - ContextAnchor overlaps thread-distill and adds nothing typed. [read]
- **Observable trigger:**
  - a request to start a successor thread; or
  - a thread past a set length (for example a context-limit warning, or a captured transcript over a set size).
- **Checked output:** thread-distill's status ledger (Item · Status · Held by · Pointer) against the thread itself:
  - decided and open items kept;
  - "relayed" kept distinct from "decided (user)";
  - compression notes saying what was cut.
- **Useful vs performative:**
  - Useful: the successor thread doesn't re-ask settled questions or lose open loops.
  - Performative: a polished distillate the successor never loads.

### Row 3. Architectural proposal or dependency change → StressTest

- **Exists:** **stress-test 2.0.0** (typed, with eval cases, including a must-avoid for manufacturing flaws in well-supported premises). [read]
- **Observable trigger:**
  - a handoff, PR or decision that adds a new subsystem, dependency or repository; or
  - one that changes a contract.
  - Kairos already requires a dissent review for this kind of "drift", so the trigger is already named in practice.
- **Checked output:**
  - Necessary vs Unverified assumptions.
  - The strongest counterargument.
  - Tests or falsifiers.
- **Useful vs performative:**
  - stress-test always produces findings. Its spec has no "nothing material" output, so it is the row most at risk of performative analysis. [read]
  - The measure: **did any finding change the proposal, add a test, or get an explicit "accepted risk"?**
  - Chaining into **real-problem** filters this. It turns each challenge into investigate now · monitor · propose accepting the risk · no action · insufficient information, and "no action" is a legitimate result. [proposal]

### Row 4. Two factual claims in genuine tension → TruthWeight

- **Exists:** **truth-weight 2.0.0** (typed, with eval cases). [read]
- **Observable trigger:** two sources or agents state incompatible facts about the same thing, for example a Claude lane and Kate, or two records.
- **Checked output:**
  - the scorecard and verdict;
  - the "Would reverse if" list;
  - the Positions section's "do they truly conflict?".
- **Useful vs performative:**
  - Useful: on known-answer synthetic pairs, it picks the better-supported claim, and on non-conflicts it says they don't conflict.
  - Performative: a 50-point scorecard on a question one lookup would settle.
- **Note:** genuine factual tension is probably rarer in coordination traffic than rows 2, 3 and 6. [untested]

### Row 5. Missing priorities, excluded alternatives → NegativeSpace

- **Exists:** negative-space, as a generated skill at version **0.1.0-reconstruction**. It is not the original tool and has no eval. #4's "where the intended tool copy is available" still applies. [read]
- **Observable trigger:** a plan or option list with no rejected alternatives stated, or a "should we do X?" with no "or Y".
- **Checked output:** one significant omitted option, plus the evidence that would show it matters.
- **Useful vs performative:**
  - Useful: on synthetic plans with one **planted** omission, it finds the planted option.
  - Performative: it lists generic omissions every plan has.

### Row 6. Erroneous attribution / authority → SSD / provenance audit

- **Exists:**
  - selective-self-distillation (a generated skill). It is scoped to extracting Zach's own contributions, which is a narrower job and touches his corpora.
  - The provenance job is better served by the typed tools:
    - **kind-check**: status taken from the item's own words, with "unknown" when they don't show it, plus an evidence section;
    - **thread-distill**: "Held by" and "relayed" as separate statuses, with pointers. [read]
- **Observable trigger:**
  - a record or message saying "Zach decided" or "approved" with no locator; or
  - a relayed instruction ("relayed by X") about to become a decision or a handoff's Authorized section.
- **Checked output:** speaker, decision status and locator for each authority claim, checked against the source.
- **Useful vs performative:**
  - Useful: on synthetic records with **planted misattributions**, it catches them and doesn't flag correct ones.
  - Performative: it flags everything as "unverified".
  - Ground truth is cheap to build, because the planted errors are known.

### Row 7. Repeated unmet cognitive need → ToolSmith + cold evaluation

- **Exists:**
  - **toolsmith 0.1.0** (typed).
  - `qat new` (scaffold).
  - The creation study (`docs/creation-study.md`) is already the trial for this row. [read]
- **Observable trigger:** the same manual procedure done three or more times, or a QAT-use line of the form "X would have fit; did it by hand".
  - `kairos/wake/qat-uses.md` already asks lanes to write that line, so the trigger can be counted.
- **Checked output:** a spec, an eval stub with planted cases, and a cold run.
- **Useful vs performative:**
  - Useful: the new tool is invoked again afterwards.
  - Performative: a spec nobody runs.

## 2. One trial shape for any row [proposal]

- **Inputs:** synthetic only, about 6–10 per row.
  - At least **two negative controls** per row, where no tool should help.
  - No real threads or corpora.
- **Arms** (from #4): A, an ordinary summary or no tool; B, the selected tool, zero or one per input.
- **Scoring:** blind, by a lane or model that didn't build the inputs.
  - Measures, from #4: priority retention · incorrect promotions · novel findings that changed the next action · missed key facts · time and tokens.
- **Decision rule:** a row earns a trigger if B beats A on at least one primary measure **without** more incorrect promotions, **and** on the negative controls it abstains, says "no action", or says "nothing material".
- **Records:** each invocation writes the QAT-use line (tool, version or source, what it changed), as #4 asks.

## 3. Rows worth trialling first

| Rank | Row | Why first | Cost |
|---|---|---|---|
| 1 | **Row 6, attribution/authority** (kind-check, thread-distill) | The most common error class in Kairos records ("relayed, not first-hand" labels; status drift); typed tools exist; planted errors give exact ground truth | Low: two typed specs, synthetic records |
| 2 | **Row 3, architectural proposal** (stress-test → real-problem) | The trigger is already defined (dissent review on drift); the row most at risk of performative output, so most worth measuring; real-problem gives the "no action" exit | Low–medium: needs a few synthetic proposals, including trivial ones as controls |
| 3 | **Row 2, successor thread** (thread-distill) | Happens often; typed, with planted-fact eval cases to build from | Low |

**Not first:**
- **Row 1:** waits for Idea-to-Ontology, or for kind-check to be shown on row 6 first.
- **Row 4:** ready, but the trigger is probably rare. [untested]
- **Row 5:** the tool is a reconstruction with no eval.
- **Row 7:** already under the creation study.

## 4. Points for Zach (none blocks this note)

- #4's "Existing capabilities" list is out of date (see §0). A comment would fix it; under this handoff, issue comments are Abigail's.
- Row 6 points at kind-check and thread-distill rather than SSD. That is a reading of what fits, not a canonical-source designation.

QAT: none run. stress-test and real-problem would fit as an alternative to §3's ranking; I ranked by hand from the specs.
