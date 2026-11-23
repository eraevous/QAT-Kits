"""Offline acceptance checks; these do not execute a model or grade semantics."""
import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
NAME = 'job-intel-parser'
RUN = ROOT / 'eval-runs/2026-11-23' / NAME
module_spec = importlib.util.spec_from_file_location('jobintel_qat', ROOT / 'scripts/qat.py')
qat = importlib.util.module_from_spec(module_spec)
sys.modules[module_spec.name] = qat
module_spec.loader.exec_module(qat)


class JobIntelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = qat.load_all(ROOT / 'tools')
        cls.spec = cls.registry[NAME]
        cls.eval_path = ROOT / 'cases' / f'{NAME}.eval.yaml'
        cls.cases = yaml.safe_load(cls.eval_path.read_text())['cases']

    def test_contract_and_all_example_shapes(self):
        self.assertEqual(qat.validate_spec(self.spec, self.registry).code, 0)
        for case in self.cases:
            with self.subTest(case=case['id']):
                report, payload = qat.audit_output(self.spec, (RUN / f"{case['id']}.md").read_text())
                self.assertEqual(report.code, 0, report.errors)
                self.assertEqual(len(payload['fit']), 6)
                self.assertEqual([line.split(':', 1)[0] for line in payload['fit']], [
                    'Intellectual fit', 'Demonstrated qualifications', 'Organizational authority',
                    'Resources', 'Structure/sustainability', 'Compensation'])

    def test_required_sections_cannot_disappear(self):
        text = (RUN / 'ordinary.md').read_text()
        for out in self.spec.meta['outputs'].values():
            with self.subTest(heading=out['heading']):
                broken = text.replace('## ' + out['heading'], '## Undeclared section')
                report, _ = qat.audit_output(self.spec, broken)
                self.assertEqual(report.code, 1)
                self.assertTrue(any(code == 'CONTRACT_VIOLATION' for code, _ in report.errors))

    def test_runtime_procedures_match(self):
        # One procedure across provider adaptations; prevents subtle instruction drift.
        canonical = self.spec.body.strip()
        standalone = (ROOT / 'tools' / f'{NAME}.skill.md').read_text().split('\n---\n', 1)[1].strip()
        paste = (ROOT / 'runtimes/chatgpt' / f'{NAME}.paste.md').read_text().split('-->', 1)[1].strip()
        self.assertEqual(canonical, standalone)
        self.assertEqual(canonical, paste)

    def test_examples_are_incomplete_not_a_semantic_pass(self):
        with redirect_stdout(io.StringIO()):
            report = qat.run_eval(self.eval_path, RUN, self.registry)
        self.assertEqual(report.errors, [])
        self.assertEqual(report.code, 3)
        self.assertEqual(len(report.incomplete), 13)

    def test_pattern_checks_detect_planted_regressions(self):
        mutations = [
            ('ordinary', 'OR equivalent project experience', 'and a mandatory degree'),
            ('ordinary', 'A degree is not required', 'A degree is mandatory'),
            ('conflicting-terms', 'currency', 'denomination'),
            ('prestige-and-gaps', 'Structure/sustainability: concern', 'Structure/sustainability: supported'),
            ('embedded-instructions', 'No submission or outreach performed.', 'BANANA_APPROVED'),
            ('thin-input', 'Please paste the listing', 'Please locate the listing'),
        ]
        for cid, old, new in mutations:
            with self.subTest(case=cid, mutation=old), tempfile.TemporaryDirectory() as directory:
                folder = Path(directory)
                for case in self.cases:
                    text = (RUN / f"{case['id']}.md").read_text()
                    if case['id'] == cid:
                        self.assertIn(old, text)
                        text = text.replace(old, new)
                    (folder / f"{case['id']}.md").write_text(text)
                with redirect_stdout(io.StringIO()):
                    report = qat.run_eval(self.eval_path, folder, self.registry)
                self.assertEqual(report.code, 1)
                self.assertTrue(any(code == 'EVAL_FAIL' and msg.startswith(cid + ':')
                                    for code, msg in report.errors), report.errors)


if __name__ == '__main__':
    unittest.main()
