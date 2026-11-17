#!/usr/bin/env python3
"""Tests for the runner's pure core in qat.py (stdlib unittest).
Run from the repo root: python3 -I qat/scripts/test_qat.py -v   (needs pyyaml and jsonschema)

qat.py checks other tools' outputs, so a silent change in how it reads markdown would make
every audit and handoff wrong without any eval failing. These tests pin the behaviour the
error codes in its docstring promise: the section parsers, fenced-code handling in
split_sections, the coercion table, spec validation, handoff checks and the output audit.
They build specs in memory and never touch qat/tools/, so they don't depend on any tool's
current text."""

import contextlib
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qat  # noqa: E402


def spec(name, inputs, outputs, body="", **extra):
    meta = {"name": name, "version": "1.0.0",
            "description": "A test tool used only by test_qat.py fixtures.",
            "inputs": inputs, "outputs": outputs, **extra}
    return qat.Spec(Path(f"{name}.qat.md"), meta, body)


def codes(report):
    return [c for c, _ in report.errors], [c for c, _ in report.warnings]


SRC = spec("src", {"idea": {"type": "text"}},
           {"premises": {"type": "premise_set", "heading": "Premises"},
            "verdict": {"type": "verdict", "heading": "Verdict"},
            "notes": {"type": "text", "heading": "Notes", "required": False}},
           handoffs=[{"to": "tgt", "when": "always", "map": {"claims": "premises", "summary": "verdict"}}])
TGT = spec("tgt", {"claims": {"type": "claims"}, "summary": {"type": "text"}},
           {"out": {"type": "text", "heading": "Out"}})
REGISTRY = {"src": SRC, "tgt": TGT}


class ParserTest(unittest.TestCase):
    def test_text_blank_is_mismatch(self):
        self.assertIsNone(qat.parse_text("  \n\t"))
        self.assertEqual(qat.parse_text("\n hello \n"), "hello")

    def test_claim_single_bullet_unwrapped(self):
        self.assertEqual(qat.parse_claim("- only one"), "only one")
        self.assertEqual(qat.parse_claim("- a\n- b"), "- a\n- b")
        self.assertIsNone(qat.parse_claim(""))

    def test_claims_accepts_all_bullet_styles(self):
        body = "- dash\n* star\n+ plus\n1. dot\n2) paren\nplain prose"
        self.assertEqual(qat.parse_claims(body), ["dash", "star", "plus", "dot", "paren"])
        self.assertIsNone(qat.parse_claims("prose only"))

    def test_premise_set_headings_and_tags(self):
        body = ("### Necessary\n- n1\n### Value judgements\n- v1\n"
                "- Unverified: u1\n- **Necessary:** n2")
        self.assertEqual(qat.parse_premise_set(body),
                         {"necessary": ["n1", "n2"], "unverified": ["u1"], "value": ["v1"]})

    def test_premise_set_untagged_bullets_before_heading_dropped(self):
        self.assertIsNone(qat.parse_premise_set("- floating\n- bullets"))

    def test_scorecard_skips_separator_row(self):
        body = "| Lens | A | B |\n|---|:-:|--:|\n| Empirical | 3 | 4 |\n| Ethical | 2 | 5 |"
        self.assertEqual(qat.parse_scorecard(body),
                         [{"Lens": "Empirical", "A": "3", "B": "4"},
                          {"Lens": "Ethical", "A": "2", "B": "5"}])

    def test_scorecard_header_only_is_mismatch(self):
        self.assertIsNone(qat.parse_scorecard("| Lens | A |\n|---|---|"))

    def test_every_type_has_parser_and_coercion_row(self):
        self.assertEqual(set(qat.TYPES), set(qat.COERCE))
        for src, dsts in qat.COERCE.items():
            self.assertIn(src, dsts, f"{src} must feed itself")
            self.assertLessEqual(dsts, set(qat.TYPES))


class CoerceTest(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(qat.coerce(["a"], "claims", "claims"), ["a"])

    def test_list_to_text(self):
        self.assertEqual(qat.coerce(["a", {"k": 1}], "scorecard", "text"), '- a\n- {"k": 1}')

    def test_premise_set_to_claims_and_text(self):
        ps = {"necessary": ["n"], "unverified": [], "value": ["v1", "v2"]}
        self.assertEqual(qat.coerce(ps, "premise_set", "claims"),
                         ["[necessary] n", "[value] v1", "[value] v2"])
        self.assertEqual(qat.coerce(ps, "premise_set", "text"), "necessary: n\nvalue: v1; v2")

    def test_claim_to_claims_wraps(self):
        self.assertEqual(qat.coerce("one", "claim", "claims"), ["one"])


class SplitSectionsTest(unittest.TestCase):
    def test_basic_and_closing_hashes(self):
        md = "# Title\nintro\n## One ##\nbody 1\n### sub\nstill 1\n## Two\nbody 2"
        self.assertEqual(qat.split_sections(md), {"One": "body 1\n### sub\nstill 1", "Two": "body 2"})

    def test_h1_ends_section(self):
        self.assertEqual(qat.split_sections("## A\na\n# New doc\nlost"), {"A": "a"})

    def test_heading_inside_fence_is_body(self):
        md = "## A\n```md\n## Not a heading\n```\nafter\n## B\nb"
        self.assertEqual(qat.split_sections(md), {"A": "```md\n## Not a heading\n```\nafter", "B": "b"})

    def test_fence_closes_only_on_same_char_and_length(self):
        md = "## A\n````\n```\n## inside\n~~~\n````\n## B\nb"
        out = qat.split_sections(md)
        self.assertEqual(set(out), {"A", "B"})
        self.assertIn("## inside", out["A"])

    def test_unclosed_fence_swallows_rest(self):
        self.assertEqual(set(qat.split_sections("## A\n~~~\n## B\n")), {"A"})


class ValidateSpecTest(unittest.TestCase):
    def test_valid_spec_with_registry(self):
        errs, warns = codes(qat.validate_spec(SRC, REGISTRY))
        self.assertEqual(errs, [])
        # premise_set -> claims and verdict -> text are lossy
        self.assertEqual(warns.count("TYPE_MISMATCH"), 2)

    def test_schema_error_stops_early(self):
        bad = spec("bad", {}, {"o": {"type": "nope", "heading": "O"}})
        errs, _ = codes(qat.validate_spec(bad))
        self.assertTrue(errs and set(errs) == {"SPEC_INVALID"})

    def test_filename_must_match_name(self):
        s = spec("good", {"i": {"type": "text"}}, {"o": {"type": "text", "heading": "O"}})
        s.path = Path("other.qat.md")
        self.assertIn("SPEC_INVALID", codes(qat.validate_spec(s))[0])

    def test_modules_declared_vs_defined(self):
        s = spec("mods", {"i": {"type": "text"}}, {"o": {"type": "text", "heading": "O"}},
                 body="### module: used\n### module: extra\n", modules=["used", "ghost"])
        msgs = [m for c, m in qat.validate_spec(s).errors if c == "UNKNOWN_MODULE"]
        self.assertEqual(len(msgs), 2)
        self.assertTrue(any("'ghost' declared" in m for m in msgs))
        self.assertTrue(any("'extra' defined" in m for m in msgs))

    def test_duplicate_headings_case_insensitive(self):
        s = spec("dup", {"i": {"type": "text"}},
                 {"a": {"type": "text", "heading": "Verdict"}, "b": {"type": "text", "heading": "verdict"}})
        self.assertIn("SPEC_INVALID", codes(qat.validate_spec(s))[0])


class HandoffTest(unittest.TestCase):
    def check(self, mapping, tgt=TGT):
        return codes(qat.check_handoff(SRC, {"to": tgt.name, "when": "x", "map": mapping}, {"src": SRC, tgt.name: tgt}))

    def test_unknown_target(self):
        r = qat.check_handoff(SRC, {"to": "nowhere", "when": "x", "map": {}}, REGISTRY)
        self.assertEqual(codes(r)[0], ["BROKEN_HANDOFF"])

    def test_unknown_fields_and_bad_type(self):
        errs, _ = self.check({"claims": "nope", "ghost": "verdict", "summary": "verdict"})
        self.assertEqual(errs.count("BROKEN_HANDOFF"), 2)
        sc = spec("sc", {"table": {"type": "scorecard"}}, {"o": {"type": "text", "heading": "O"}})
        errs, _ = self.check({"table": "verdict"}, sc)
        self.assertEqual(errs, ["BROKEN_HANDOFF"])  # verdict cannot feed scorecard

    def test_unmapped_required_input(self):
        errs, _ = self.check({"claims": "premises"})
        self.assertEqual(errs, ["MISSING_INPUT"])

    def test_optional_output_warns(self):
        _, warns = self.check({"claims": "premises", "summary": "notes"})
        self.assertIn("BROKEN_HANDOFF", warns)


class AuditAndBuildTest(unittest.TestCase):
    GOOD = "## Premises\n### Necessary\n- p1\n## verdict:\nA holds.\n## Extra\nx"

    def test_audit_normalises_headings_and_warns_unknown(self):
        r, payload = qat.audit_output(SRC, self.GOOD)
        self.assertEqual(codes(r), ([], ["UNKNOWN_FIELD"]))
        self.assertEqual(payload, {"premises": {"necessary": ["p1"], "unverified": [], "value": []},
                                   "verdict": "A holds."})

    def test_audit_missing_and_mismatch(self):
        r, _ = qat.audit_output(SRC, "## Premises\nno bullets here\n## Notes\nfine")
        self.assertEqual(sorted(codes(r)[0]), ["CONTRACT_VIOLATION", "TYPE_MISMATCH"])

    def test_optional_section_may_be_absent(self):
        r, payload = qat.audit_output(SRC, "## Premises\n- Value: v\n## Verdict\nok")
        self.assertEqual(r.errors, [])
        self.assertNotIn("notes", payload)

    def test_build_handoff_coerces(self):
        r, out = qat.build_handoff(SRC, TGT, self.GOOD, REGISTRY)
        self.assertEqual(r.errors, [])
        self.assertEqual(out, {"tool": "tgt", "from": "src",
                               "inputs": {"claims": ["[necessary] p1"], "summary": "A holds."}})

    def test_build_handoff_empty_input_is_error(self):
        r, out = qat.build_handoff(SRC, TGT, "## Premises\n- Value: v", REGISTRY)
        self.assertIn("MISSING_INPUT", codes(r)[0])
        self.assertNotIn("summary", out["inputs"])

    def test_build_handoff_undeclared(self):
        r, out = qat.build_handoff(TGT, SRC, "## Out\nx", REGISTRY)
        self.assertEqual((codes(r)[0], out), (["BROKEN_HANDOFF"], {}))


class EvalExitTest(unittest.TestCase):
    """Exit status of `eval` (ChatGPT port finding, HO-QAT-20261116-Y0HJ): a run where nothing was graded
    used to exit 0 with every case SKIP, and judged checks were printed but never recorded. Now
    1 = a known failure (wins over incomplete), 3 = incomplete, 2 = configuration, 0 = everything graded."""

    EVAL = {"tool": "tgt", "cases": [
        {"id": "a", "must_include": [{"pattern": "hello"}, {"judge": "it is polite"}]},
        {"id": "b", "must_include": [{"pattern": "hello"}]}]}

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.out = self.tmp / "out"
        self.out.mkdir()
        self.write_eval(self.EVAL)

    def write_eval(self, cfg):
        import yaml
        (self.tmp / "tgt.eval.yaml").write_text(yaml.safe_dump(cfg))

    def output(self, cid, text="## Out\nhello there\n"):
        (self.out / f"{cid}.md").write_text(text)
        return hashlib.sha256(text.encode()).hexdigest()

    def judgment(self, sha, **over):
        j = {"case": "a", "kind": "must_include", "check": 1, "verdict": "PASS", "reason": "polite",
             "grader": "test", "grader_is_author": False, "output_sha256": sha}
        j.update(over)
        return j

    def run_eval(self, judgments=None):
        jp = None
        if judgments is not None:
            jp = self.tmp / "judgments.json"
            jp.write_text(json.dumps({"judgments": judgments}))
        with contextlib.redirect_stdout(io.StringIO()):
            return qat.run_eval(self.tmp / "tgt.eval.yaml", self.out, REGISTRY, jp)

    def test_all_outputs_missing_is_incomplete_not_success(self):
        r = self.run_eval()
        self.assertEqual((r.errors, r.code), ([], 3))
        self.assertEqual(len([c for c, _ in r.incomplete if c == "EVAL_INCOMPLETE"]), 2)  # one per SKIPped case

    def test_zero_cases_is_incomplete(self):
        self.write_eval({"tool": "tgt", "cases": []})
        self.assertEqual(self.run_eval().code, 3)

    def test_ungraded_judged_check_is_incomplete(self):
        self.output("a"); self.output("b")
        r = self.run_eval()
        self.assertEqual((r.errors, r.code), ([], 3))
        self.assertIn("a must_include#1", r.incomplete[0][1])

    def test_all_graded_is_success(self):
        sha = self.output("a"); self.output("b")
        self.assertEqual(self.run_eval([self.judgment(sha)]).code, 0)

    def test_failure_wins_over_incomplete(self):
        self.output("a", "## Out\ngoodbye\n")           # deterministic fail; b missing; judged ungraded
        r = self.run_eval()
        self.assertEqual(r.code, 1)
        self.assertTrue(r.incomplete)                     # still reported alongside the failure

    def test_judged_fail_is_failure(self):
        sha = self.output("a"); self.output("b")
        r = self.run_eval([self.judgment(sha, verdict="FAIL", reason="rude")])
        self.assertEqual(r.code, 1)
        self.assertIn("judged FAIL", r.errors[0][1])

    def test_judgment_for_other_output_is_stale(self):
        self.output("a"); self.output("b")
        r = self.run_eval([self.judgment("0" * 64)])
        self.assertEqual(r.code, 3)
        self.assertIn("different output", r.incomplete[0][1])

    def test_malformed_judgments_are_config_errors(self):
        sha = self.output("a"); self.output("b")
        bad = [[self.judgment(sha, verdict="ok")],          # not PASS/FAIL
               [self.judgment(sha, reason="")],             # empty reason
               [{"case": "a", "verdict": "PASS"}],          # missing keys
               [self.judgment(sha), self.judgment(sha)],    # duplicate
               [self.judgment(sha, check=2)]]               # no such judged check
        for judgments in bad:
            with self.subTest(judgments=judgments), self.assertRaises(qat.ConfigError):
                self.run_eval(judgments)

    def test_cli_exit_codes(self):
        script = Path(qat.__file__)
        tools = self.tmp / "tools"
        tools.mkdir()
        (tools / "tgt.qat.md").write_text(
            "---\nname: tgt\nversion: 1.0.0\ndescription: A test tool used only by test_qat.py fixtures.\n"
            "inputs:\n  summary: {type: text}\noutputs:\n  out: {type: text, heading: Out}\n---\nBody.\n")
        def run(*extra):
            return subprocess.run([sys.executable, "-I", str(script), "--tools", str(tools), "eval",
                                   str(self.tmp / "tgt.eval.yaml"), str(self.out), *extra],
                                  capture_output=True, text=True)
        p = run()
        self.assertEqual(p.returncode, 3, p.stdout + p.stderr)
        self.assertIn("INCOMPLETE", p.stdout)
        sha = self.output("a"); self.output("b")
        jp = self.tmp / "j.json"
        jp.write_text(json.dumps({"judgments": [self.judgment(sha)]}))
        self.assertEqual(run("--judgments", str(jp)).returncode, 0)
        jp.write_text("not json")
        self.assertEqual(run("--judgments", str(jp)).returncode, 2)


if __name__ == "__main__":
    unittest.main()
