"""Offline contracts, provider parity and adversarial fixture checks; no model calls."""
import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('resume-tailor', 'interview-commander', 'reflective-job-note')
RUNS = ROOT / 'eval-runs/2026-11-23'
module_spec = importlib.util.spec_from_file_location('companion_qat', ROOT / 'scripts/qat.py')
qat = importlib.util.module_from_spec(module_spec)
sys.modules[module_spec.name] = qat
module_spec.loader.exec_module(qat)


class CompanionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = qat.load_all(ROOT / 'tools')

    def cases(self, name):
        return yaml.safe_load((ROOT / 'cases' / f'{name}.eval.yaml').read_text())['cases']

    def test_contracts_and_cold_start_inputs(self):
        for name in NAMES:
            with self.subTest(tool=name):
                spec = self.registry[name]
                self.assertEqual(qat.validate_spec(spec, self.registry).code, 0)
                self.assertFalse(spec.meta['inputs']['context']['required'])
                self.assertEqual(spec.meta['handoffs'], [])
                cases = self.cases(name)
                self.assertEqual(len(cases), 5)
                # Reflection's cold context contains only a direct user priority.
                self.assertNotIn('D1', str(cases[0]['input']))
                for case in cases:
                    self.assertLessEqual(set(case['input']), set(spec.meta['inputs']))
                    text = (RUNS / name / f"{case['id']}.md").read_text()
                    report, payload = qat.audit_output(spec, text)
                    self.assertEqual(report.code, 0, report.errors)
                    if name == 'interview-commander':
                        self.assertEqual([s.split(':', 1)[0] for s in payload['employer']], [
                            'Intellectual fit', 'Demonstrated qualifications', 'Organizational authority',
                            'Resources', 'Structure/sustainability', 'Compensation'])

    def test_adaptations_preserve_full_procedures(self):
        for name in NAMES:
            with self.subTest(tool=name):
                body = self.registry[name].body.strip()
                skill = (ROOT / 'tools' / f'{name}.skill.md').read_text().split('\n---\n', 1)[1].strip()
                paste = (ROOT / 'runtimes/chatgpt' / f'{name}.paste.md').read_text().split('-->', 1)[1].strip()
                self.assertEqual(body, skill)
                self.assertEqual(body, paste)

    def test_missing_sections_fail_audit(self):
        for name in NAMES:
            text = (RUNS / name / 'cold.md').read_text()
            for output in self.registry[name].meta['outputs'].values():
                with self.subTest(tool=name, heading=output['heading']):
                    broken = text.replace('## ' + output['heading'], '## Undeclared')
                    report, _ = qat.audit_output(self.registry[name], broken)
                    self.assertEqual(report.code, 1)
                    self.assertTrue(any(code == 'CONTRACT_VIOLATION' for code, _ in report.errors))

    def test_author_fixtures_cannot_claim_semantic_pass(self):
        for name in NAMES:
            with self.subTest(tool=name), redirect_stdout(io.StringIO()):
                report = qat.run_eval(ROOT / 'cases' / f'{name}.eval.yaml', RUNS / name, self.registry)
                self.assertEqual(report.errors, [])
                self.assertEqual(report.code, 3)
                self.assertEqual(len(report.incomplete), 10)

    def test_mutations_reject_grounding_and_control_regressions(self):
        mutations = [
            ('resume-tailor', 'cold', 'After: “Assisted', 'After: “Led'),
            ('resume-tailor', 'conflict', 'After: “Supported testing', 'After: “Managed the team'),
            ('resume-tailor', 'optional-context', 'source unavailable', 'verified source'),
            ('interview-commander', 'cold', 'measured impact unknown', 'measured impact was 40%'),
            ('interview-commander', 'rehearsal', 'Waiting for your answer', 'Your answer was excellent'),
            ('reflective-job-note', 'cold', 'approximately', 'verbatim'),
            ('reflective-job-note', 'silence', 'interpretation, not', 'fact, not'),
            ('reflective-job-note', 'optional-context', 'not edited or rerun', 'automatically updated'),
        ]
        mutations += [(name, 'injection', 'ignored', 'RED_KITE_APPROVED') for name in NAMES]
        for name, cid, old, new in mutations:
            with self.subTest(tool=name, case=cid, mutation=old), tempfile.TemporaryDirectory() as directory:
                folder = Path(directory)
                for case in self.cases(name):
                    text = (RUNS / name / f"{case['id']}.md").read_text()
                    if case['id'] == cid:
                        self.assertIn(old, text)
                        text = text.replace(old, new)
                    (folder / f"{case['id']}.md").write_text(text)
                with redirect_stdout(io.StringIO()):
                    report = qat.run_eval(ROOT / 'cases' / f'{name}.eval.yaml', folder, self.registry)
                self.assertEqual(report.code, 1)
                self.assertTrue(any(code == 'EVAL_FAIL' and msg.startswith(cid + ':')
                                    for code, msg in report.errors), report.errors)


if __name__ == '__main__':
    unittest.main()
