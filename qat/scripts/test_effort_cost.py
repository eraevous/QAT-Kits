"""Regression tests for effort-cost carbon/water ranges and runtime copies.

Run from qat/: python3 -I -B -m unittest discover -s scripts -p 'test_*.py'
"""
import importlib.util
import subprocess
import sys
import unittest
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtimes" / "chatgpt"
GENERATOR = RUNTIME / "effort-cost.card.py"
module_spec = importlib.util.spec_from_file_location("effort_cost_card", GENERATOR)
card = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(card)


def expected_number(value):
    """Independent two-significant-figure Decimal rounding for expected cells."""
    quantum = Decimal(1).scaleb(value.adjusted() - 1)
    rounded = value.quantize(quantum, rounding=ROUND_HALF_EVEN)
    places = max(0, -quantum.as_tuple().exponent)
    return f"{rounded:,.{places}f}"


class EffortCostTests(unittest.TestCase):
    def test_known_short_context_cells(self):
        cells = card.conversion_cells((0.2, 0.4, 1.2), 0.3, False, (0, 0, 0))
        self.assertEqual(cells[0], "0.042 (0.021–0.13)")
        self.assertEqual(cells[2], "0.054 (0.027–0.16)")
        self.assertEqual(cells[3], "0.028 (0.014–0.083)")
        self.assertEqual(cells[4], "0.022 (0.011–0.065)")
        self.assertEqual(cells[-1], "0.36 (0.060–1.8)")

    def test_long_context_water_includes_both_uncertainties(self):
        cells = card.conversion_cells((0.2, 0.4, 1.2), 0.1, False, (20, 30, 40))
        self.assertEqual(cells[0], "11 (7.0–14)")
        self.assertEqual(cells[-1], "90 (20–200)")

    def test_reasoning_floor_and_unrounded_energy(self):
        short = card.conversion_cells((0.7, 2.5, 6), 0.1, True, (0, 0, 0))
        paragraph = card.conversion_cells((0.7, 2.5, 6), 0.3, True, (0, 0, 0))
        self.assertEqual(short, paragraph)
        page = card.conversion_cells((0.7, 2.5, 6), 0.7, True, (0, 0, 0))
        self.assertEqual(page[0], "0.61 (0.17–1.5)")  # 1.75 Wh, not rounded 1.8 Wh

    def test_every_conversion_and_two_significant_figures(self):
        for tier, context in card.CONTEXTS:
            for name, vals, reasoning in card.T1:
                for length, factor in card.LENGTHS:
                    with self.subTest(tier=tier, setting=name, length=length):
                        scale = Decimal(str(factor))
                        if reasoning:
                            scale = max(scale, Decimal("0.5"))
                        energy = [Decimal(str(v)) * scale + Decimal(str(c)) for v, c in zip(vals, context)]
                        expected = []
                        for coefficients in [(f, f, f) for _, f in card.CARBON_FACTORS] + [(1, 3, 5)]:
                            values = [expected_number(v * Decimal(str(f))) for v, f in zip(energy, coefficients)]
                            expected.append(f"{values[1]} ({values[0]}–{values[2]})")
                        self.assertEqual(card.conversion_cells(vals, factor, reasoning, context), expected)

    def test_all_settings_lengths_and_contexts_are_rendered(self):
        table = card.conversion_tables()
        for tier, _ in card.CONTEXTS:
            section = table.split(f"Context: {tier}\n", 1)[1].split("\nContext:", 1)[0]
            rows = [line for line in section.splitlines() if line.startswith("| ")][1:]
            self.assertEqual(len(rows), len(card.T1) * len(card.LENGTHS))
            for name, _, _ in card.T1:
                for length, _ in card.LENGTHS:
                    prefix = f"| {name.split(' (')[0]} | {length.split(' (')[0]} |"
                    self.assertEqual(sum(row.startswith(prefix) for row in rows), 1)

    def test_published_runtime_tables_and_instructions_match(self):
        runtimes = [(RUNTIME / f"effort-cost.{kind}.md").read_text() for kind in ("paste", "skill")]
        for text in runtimes:
            self.assertEqual(text.count(card.CONVERSIONS_START), 1)
            self.assertEqual(text.count(card.CONVERSIONS_END), 1)
            block = text[text.index(card.CONVERSIONS_START):text.index(card.CONVERSIONS_END) + len(card.CONVERSIONS_END)]
            self.assertEqual(block, card.conversion_tables())
            instruction = next(line for line in text.splitlines() if line.startswith("2. Cost by setting:"))
            self.assertIn("copy the full central (low–high) cells from Table D", instruction)
            self.assertIn("its range includes 1–5 mL/Wh uncertainty", instruction)
            self.assertNotIn("central Wh ×", instruction)
        self.assertEqual(*(text.split("EFFORT CHECK (heuristic).", 1)[1] for text in runtimes))

    def test_conversion_cli_emits_the_shared_block(self):
        result = subprocess.run([sys.executable, "-I", "-B", str(GENERATOR), "--conversions"],
                                check=True, capture_output=True, text=True)
        self.assertEqual(result.stdout, card.conversion_tables() + "\n")


if __name__ == "__main__":
    unittest.main()
