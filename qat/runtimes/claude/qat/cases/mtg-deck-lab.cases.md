---
tool: mtg-deck-lab
spec: qat/tools/mtg-deck-lab.skill.md
version: 1.0.0
---

# mtg-deck-lab: cases

Cases for the standalone skill (CONTRIBUTING.md, "Standalone skill"). Inputs are synthetic: no real
inventory workbook is needed or used. Run each case against the skill text in a fresh session, save the
output as `qat/eval-runs/<date>/mtg-deck-lab/<case id>.md`, and grade PASS/FAIL against "Must" and
"Must not".

## ML-01: Inventory-first, no commander picked early (§0, §2.9)

**Input:**
I've got a pile of sacrifice and token cards (Viscera Seer, Carrion Feeder, Bitterblossom, Skullclamp,
Blood Artist, Zulaport Cutthroat, Pitiless Plunderer, Ophiomancer, Village Rites, Deadly Dispute and about
40 more black and red cards). What can I build from what I own?

**Must:**
- Take the inventory-first path: a module census (what the owned cards require, produce and connect to)
  before naming any commander.
- Ask at most 3-4 targeted questions, or state assumptions if proceeding.

**Must not:**
- Open by recommending a specific commander.

## ML-02: Anti-cleverness check (§2.6)

**Input:**
For my Rakdos tokens deck, swap Lightning Greaves out for a three-card package: Ashnod's Altar, Nim
Deathmantle and Reassembling Skeleton. It makes so many triggers.

**Must:**
- Run the anti-cleverness questions: material advantage or just triggers; how often all pieces are present;
  whether each piece is useful alone; what breaks if one is removed.
- Trace the package to an outcome (cards, mana, damage, a win), not "more triggers".
- Give a recommendation class (e.g. PACKAGE-DEPENDENT, TEST) with an evidence level.

**Must not:**
- Call the loop verified without closing costs, timing and termination.
- Use made-up decimal precision.

## ML-03: Table cockpit (§3.4)

**Input:**
Mid-game, four players. I have 6 mana open and Blood Artist out. Opponent to my left has 18 power on board
and attacks next turn. What do I do right now?

**Must:**
- Answer with the live cockpit (CLOCK, GATE, JOB, REPLY, CONVERT, RESET), kept short enough to use at the
  table.
- Address the clock threat from the 18-power board first.
