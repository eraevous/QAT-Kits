#!/usr/bin/env python3
"""
qat.py — the enforcement layer for QAT tool specs.

The old QAT problem: contracts were declarations the model might or might not
honour, and nothing checked that one tool's output fit the next tool's input.
This script is that check. It never runs a tool; the model does. It validates
specs, audits outputs against their contract, builds handoff payloads, and
scores eval cases.

Commands
  index    [--tools DIR]                 validate every spec, write INDEX.md, check every handoff
  validate SPEC                          validate one spec file
  audit    TOOL OUTPUT.md [--json OUT]   check an output against TOOL's output contract
  handoff  FROM TO OUTPUT.md [--json OUT]  map FROM's audited output onto TO's inputs
  eval     EVAL.yaml OUTPUT_DIR [--judgments FILE]
                                         run must_include / must_avoid checks per case;
                                         judged checks are graded only from FILE

Exit code 0 = no errors (warnings allowed), 1 = errors, 2 = usage or configuration
problem (bad arguments, unreadable eval file, malformed judgments file), 3 = incomplete
eval (no errors, but not everything was checked: no cases, a case SKIPped because its
output is missing, or a judged check with no valid recorded judgment). A known failure
wins: a run with an error exits 1 even if it is also incomplete, and says so.

Judgments file (JSON): {"judgments": [{"case": ID, "kind": "must_include"|"must_avoid",
  "check": N (1-based, as printed), "verdict": "PASS"|"FAIL", "reason": TEXT,
  "grader": TEXT, "grader_is_author": BOOL, "output_sha256": HEX, "criterion_sha256": HEX}]}
  output_sha256 binds the judgment to the exact output file graded, and criterion_sha256
  (sha256 of the judge: text, as UTF-8) to the exact criterion; a judgment whose hashes
  don't match the current output and criterion is stale and counts as missing.

Error codes (typed, so a caller can branch on them)
  SPEC_INVALID      spec frontmatter fails the schema
  UNKNOWN_MODULE    body references a module the spec doesn't declare, or vice versa
  MISSING_INPUT     a required input is absent
  CONTRACT_VIOLATION  a required output section is missing
  TYPE_MISMATCH     a section exists but doesn't parse as its declared type
  UNKNOWN_FIELD     output has a section the contract doesn't declare (warning: the
                    "model invented a field" failure)
  BROKEN_HANDOFF    handoff target or mapped field doesn't exist, or types can't coerce
  EVAL_FAIL         a deterministic eval check failed, or a judged check was graded FAIL
  EVAL_INCOMPLETE   (incomplete, exit 3) a case or judged check was not graded
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
DEFAULT_TOOLS = HERE.parent / "tools"

# ---------------------------------------------------------------------------
# Types. Each has a parser from a markdown section body; a parse that returns
# None is a TYPE_MISMATCH. COERCE lists which output types may feed which inputs.
# ---------------------------------------------------------------------------
BULLET = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*\S)")


def _bullets(body: str) -> list[str]:
    return [m.group(1) for line in body.splitlines() if (m := BULLET.match(line))]


def parse_text(body):
    t = body.strip()
    return t or None


def parse_claim(body):
    t = body.strip()
    if not t:
        return None
    items = _bullets(t)
    return items[0] if len(items) == 1 else t


def parse_claims(body):
    items = _bullets(body)
    return items or None


def parse_premise_set(body):
    """Expects ### Necessary / ### Unverified / ### Value (any order) with bullets,
    or bullets prefixed 'Necessary:' etc."""
    groups = {"necessary": [], "unverified": [], "value": []}
    current = None
    for line in body.splitlines():
        h = re.match(r"^\s*(?:###\s*|\*\*)(necessary|unverified|value)", line, re.I)
        if h:
            current = h.group(1).lower()
            continue
        m = BULLET.match(line)
        if m:
            text = m.group(1)
            tag = re.match(r"\**\s*(necessary|unverified|value)[^:]*:\**\s*(.*)", text, re.I)
            if tag:
                groups[tag.group(1).lower()].append(tag.group(2))
            elif current:
                groups[current].append(text)
    return groups if any(groups.values()) else None


def parse_scorecard(body):
    rows = [l for l in body.splitlines() if l.strip().startswith("|")]
    rows = [r for r in rows if not re.match(r"^\s*\|[\s|:-]+\|\s*$", r)]
    if len(rows) < 2:
        return None
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    header, data = cells[0], cells[1:]
    return [dict(zip(header, r)) for r in data]


TYPES = {
    "text": parse_text,
    "claim": parse_claim,
    "claims": parse_claims,
    "premise_set": parse_premise_set,
    "scorecard": parse_scorecard,
    "verdict": parse_text,
}

# output type -> input types it can feed
COERCE = {
    "text": {"text"},
    "claim": {"claim", "text", "claims"},
    "claims": {"claims", "text"},
    "premise_set": {"premise_set", "claims", "text"},
    "scorecard": {"scorecard", "text"},
    "verdict": {"verdict", "text", "claim"},
}


def coerce(value, src: str, dst: str):
    if src == dst:
        return value
    if dst == "text":
        if isinstance(value, list):
            return "\n".join(f"- {v}" if isinstance(v, str) else f"- {json.dumps(v)}" for v in value)
        if isinstance(value, dict):
            return "\n".join(f"{k}: " + "; ".join(v) for k, v in value.items() if v)
        return value
    if dst == "claims":
        if isinstance(value, dict):
            return [f"[{k}] {v}" for k, vs in value.items() for v in vs]
        return [value]
    if dst == "claim":
        return value
    return value

# ---------------------------------------------------------------------------
# Spec schema: the lean core. name, description, inputs, outputs, modules,
# reflexes, handoffs. Everything else is prose in the body.
# ---------------------------------------------------------------------------
TYPE_ENUM = sorted(TYPES)
SPEC_SCHEMA = {
    "type": "object",
    "required": ["name", "version", "description", "inputs", "outputs"],
    "additionalProperties": False,
    "properties": {
        "name": {"type": "string", "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"},
        "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
        "description": {"type": "string", "minLength": 20, "maxLength": 400},
        "inputs": {
            "type": "object", "minProperties": 1,
            "additionalProperties": {
                "type": "object", "required": ["type"], "additionalProperties": False,
                "properties": {"type": {"enum": TYPE_ENUM}, "required": {"type": "boolean"},
                               "doc": {"type": "string"}},
            },
        },
        "outputs": {
            "type": "object", "minProperties": 1,
            "additionalProperties": {
                "type": "object", "required": ["type", "heading"], "additionalProperties": False,
                "properties": {"type": {"enum": TYPE_ENUM}, "heading": {"type": "string"},
                               "required": {"type": "boolean"}, "doc": {"type": "string"}},
            },
        },
        "modules": {"type": "array", "items": {"type": "string", "pattern": "^[a-z0-9-]+$"},
                    "uniqueItems": True},
        "reflexes": {"type": "object", "additionalProperties": {"type": "string"}},
        "handoffs": {
            "type": "array",
            "items": {
                "type": "object", "required": ["to", "when", "map"], "additionalProperties": False,
                "properties": {"to": {"type": "string"}, "when": {"type": "string"},
                               "map": {"type": "object", "additionalProperties": {"type": "string"}}},
            },
        },
    },
}
VALIDATOR = Draft202012Validator(SPEC_SCHEMA)


class ConfigError(Exception):
    """A usage or configuration problem (exit 2), kept apart from failed or incomplete evals."""


@dataclass
class Report:
    errors: list[tuple[str, str]] = field(default_factory=list)
    warnings: list[tuple[str, str]] = field(default_factory=list)
    incomplete: list[tuple[str, str]] = field(default_factory=list)

    def err(self, code, msg):
        self.errors.append((code, msg))

    def warn(self, code, msg):
        self.warnings.append((code, msg))

    def gap(self, code, msg):
        """Something that should have been checked wasn't (exit 3 unless there are errors)."""
        self.incomplete.append((code, msg))

    def extend(self, other: "Report", prefix=""):
        self.errors += [(c, prefix + m) for c, m in other.errors]
        self.warnings += [(c, prefix + m) for c, m in other.warnings]
        self.incomplete += [(c, prefix + m) for c, m in other.incomplete]

    def print(self):
        for c, m in self.errors:
            print(f"ERROR   {c:<18} {m}")
        for c, m in self.incomplete:
            print(f"INCOMPL {c:<18} {m}")
        for c, m in self.warnings:
            print(f"WARN    {c:<18} {m}")
        if self.errors and self.incomplete:
            print(f"FAILED, and also INCOMPLETE: {len(self.incomplete)} item(s) not graded")
        elif self.incomplete:
            print(f"INCOMPLETE: no errors, but {len(self.incomplete)} item(s) not graded; not a pass")
        elif not self.errors and not self.warnings:
            print("OK")

    @property
    def code(self):
        if self.errors:
            return 1
        return 3 if self.incomplete else 0


@dataclass
class Spec:
    path: Path
    meta: dict
    body: str

    @property
    def name(self):
        return self.meta.get("name", self.path.stem)


def load_spec(path: Path) -> Spec:
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{path.name}: no YAML frontmatter")
    return Spec(path, yaml.safe_load(m.group(1)) or {}, m.group(2))


def load_all(tools_dir: Path) -> dict[str, Spec]:
    specs = {}
    for p in sorted(tools_dir.glob("*.qat.md")):
        s = load_spec(p)
        specs[s.name] = s
    return specs


def validate_spec(spec: Spec, registry: dict[str, Spec] | None = None) -> Report:
    r = Report()
    for e in sorted(VALIDATOR.iter_errors(spec.meta), key=lambda e: list(e.path)):
        loc = "/".join(map(str, e.path)) or "(root)"
        r.err("SPEC_INVALID", f"{spec.path.name}: {loc}: {e.message}")
    if r.errors:
        return r
    if spec.path.name != f"{spec.meta['name']}.qat.md":
        r.err("SPEC_INVALID", f"{spec.path.name}: filename must be {spec.meta['name']}.qat.md")

    # modules: declared <-> defined in body as '### module: <id>'
    declared = set(spec.meta.get("modules", []))
    defined = set(re.findall(r"^###\s+module:\s*([a-z0-9-]+)", spec.body, re.M))
    for m in sorted(declared - defined):
        r.err("UNKNOWN_MODULE", f"{spec.name}: module '{m}' declared but never defined in body")
    for m in sorted(defined - declared):
        r.err("UNKNOWN_MODULE", f"{spec.name}: module '{m}' defined in body but not declared")

    headings = [o["heading"] for o in spec.meta["outputs"].values()]
    if len(set(h.lower() for h in headings)) != len(headings):
        r.err("SPEC_INVALID", f"{spec.name}: duplicate output headings")

    if registry is not None:
        for h in spec.meta.get("handoffs", []):
            r.extend(check_handoff(spec, h, registry))
    return r


def check_handoff(src: Spec, h: dict, registry: dict[str, Spec]) -> Report:
    r = Report()
    tgt = registry.get(h["to"])
    if tgt is None:
        r.err("BROKEN_HANDOFF", f"{src.name} -> {h['to']}: target tool not found")
        return r
    outs, ins = src.meta["outputs"], tgt.meta["inputs"]
    for in_field, out_field in h["map"].items():
        if in_field not in ins:
            r.err("BROKEN_HANDOFF", f"{src.name} -> {tgt.name}: target has no input '{in_field}'")
            continue
        if out_field not in outs:
            r.err("BROKEN_HANDOFF", f"{src.name} -> {tgt.name}: source has no output '{out_field}'")
            continue
        st, dt = outs[out_field]["type"], ins[in_field]["type"]
        if dt not in COERCE[st]:
            r.err("BROKEN_HANDOFF", f"{src.name}.{out_field} ({st}) cannot feed {tgt.name}.{in_field} ({dt})")
        elif st != dt:
            r.warn("TYPE_MISMATCH", f"{src.name}.{out_field} ({st}) -> {tgt.name}.{in_field} ({dt}) is a lossy coercion")
        if not outs[out_field].get("required", True):
            r.warn("BROKEN_HANDOFF", f"{src.name}.{out_field} is optional; handoff to {tgt.name} may arrive empty")
    for name, spec in ins.items():
        if spec.get("required", True) and name not in h["map"]:
            r.err("MISSING_INPUT", f"{src.name} -> {tgt.name}: required input '{name}' not mapped")
    return r

# ---------------------------------------------------------------------------
# Output audit
# ---------------------------------------------------------------------------
def split_sections(md: str) -> dict[str, str]:
    """'## Heading' -> body (until next ## or #)."""
    sections, current, buf, fence = {}, None, [], None
    for line in md.splitlines():
        if fence is not None:
            close = re.match(r"^ {0,3}(`{3,}|~{3,})[ \t]*$", line)
            if close and close.group(1)[0] == fence[0] and len(close.group(1)) >= fence[1]:
                if current is not None:
                    buf.append(line)
                fence = None
            elif current is not None:
                buf.append(line)
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if opening:
            if current is not None:
                buf.append(line)
            fence = (opening.group(1)[0], len(opening.group(1)))
            continue
        m = re.match(r"^##\s+(.+?)\s*#*\s*$", line)
        if m and not line.startswith("###"):
            if current is not None:
                sections[current] = "\n".join(buf)
            current, buf = m.group(1).strip(), []
        elif re.match(r"^#\s", line):
            if current is not None:
                sections[current] = "\n".join(buf)
            current, buf = None, []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf)
    return sections


def _norm(h: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", h.lower()).strip()


def audit_output(spec: Spec, md: str) -> tuple[Report, dict]:
    r, payload = Report(), {}
    found = {_norm(h): (h, b) for h, b in split_sections(md).items()}
    expected = {_norm(o["heading"]): k for k, o in spec.meta["outputs"].items()}
    for key, o in spec.meta["outputs"].items():
        hit = found.get(_norm(o["heading"]))
        if hit is None:
            if o.get("required", True):
                r.err("CONTRACT_VIOLATION", f"missing section '## {o['heading']}' ({key}: {o['type']})")
            continue
        value = TYPES[o["type"]](hit[1])
        if value is None:
            r.err("TYPE_MISMATCH", f"'## {o['heading']}' doesn't parse as {o['type']}")
            continue
        payload[key] = value
    for n, (h, _) in found.items():
        if n not in expected:
            r.warn("UNKNOWN_FIELD", f"section '## {h}' is not in {spec.name}'s output contract")
    return r, payload


def build_handoff(src: Spec, tgt: Spec, md: str, registry) -> tuple[Report, dict]:
    h = next((h for h in src.meta.get("handoffs", []) if h["to"] == tgt.name), None)
    r = Report()
    if h is None:
        r.err("BROKEN_HANDOFF", f"{src.name} declares no handoff to {tgt.name}")
        return r, {}
    r.extend(check_handoff(src, h, registry))
    ar, payload = audit_output(src, md)
    r.extend(ar, prefix=f"[{src.name} output] ")
    out = {}
    for in_field, out_field in h["map"].items():
        if out_field in payload and in_field in tgt.meta["inputs"]:
            out[in_field] = coerce(payload[out_field], src.meta["outputs"][out_field]["type"],
                                   tgt.meta["inputs"][in_field]["type"])
    for name, spec in tgt.meta["inputs"].items():
        if spec.get("required", True) and name not in out:
            r.err("MISSING_INPUT", f"{tgt.name}.{name} would arrive empty")
    return r, {"tool": tgt.name, "from": src.name, "inputs": out}

# ---------------------------------------------------------------------------
# Evals
# ---------------------------------------------------------------------------
JUDGMENT_KEYS = {"case", "kind", "check", "verdict", "reason", "grader", "grader_is_author",
                 "output_sha256", "criterion_sha256"}


def load_judgments(path: Path | None) -> dict[tuple[str, str, int], dict]:
    """Read a judgments file into {(case, kind, check): judgment}. Raises ConfigError if malformed."""
    if path is None:
        return {}
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError) as e:
        raise ConfigError(f"judgments file {path}: {e}")
    items = data.get("judgments") if isinstance(data, dict) else None
    if not isinstance(items, list):
        raise ConfigError(f"judgments file {path}: expected an object with a 'judgments' list")
    out = {}
    for i, j in enumerate(items):
        where = f"judgments file {path}, item {i + 1}"
        if not isinstance(j, dict) or set(j) != JUDGMENT_KEYS:
            got = sorted(j) if isinstance(j, dict) else type(j).__name__
            raise ConfigError(f"{where}: needs exactly the keys {sorted(JUDGMENT_KEYS)}, got {got}")
        if j["kind"] not in ("must_include", "must_avoid"):
            raise ConfigError(f"{where}: kind must be must_include or must_avoid")
        if not isinstance(j["check"], int) or isinstance(j["check"], bool) or j["check"] < 1:
            raise ConfigError(f"{where}: check must be a positive integer (1-based, as printed)")
        if j["verdict"] not in ("PASS", "FAIL"):
            raise ConfigError(f"{where}: verdict must be PASS or FAIL")
        if not isinstance(j["grader_is_author"], bool):
            raise ConfigError(f"{where}: grader_is_author must be true or false")
        for k in ("case", "reason", "grader"):
            if not isinstance(j[k], str) or not j[k].strip():
                raise ConfigError(f"{where}: {k} must be a non-empty string")
        for k in ("output_sha256", "criterion_sha256"):
            if not isinstance(j[k], str) or not re.fullmatch(r"[0-9a-f]{64}", j[k]):
                raise ConfigError(f"{where}: {k} must be 64 lowercase hex digits")
        key = (j["case"], j["kind"], j["check"])
        if key in out:
            raise ConfigError(f"{where}: duplicate judgment for {key[0]} {key[1]}#{key[2]}")
        out[key] = j
    return out


def run_eval(eval_path: Path, out_dir: Path, registry, judgments_path: Path | None = None) -> Report:
    try:
        cfg = yaml.safe_load(eval_path.read_text())
    except (OSError, yaml.YAMLError) as e:
        raise ConfigError(f"eval file {eval_path}: {e}")
    if not isinstance(cfg, dict) or not isinstance(cfg.get("cases", []), list):
        raise ConfigError(f"eval file {eval_path}: expected a mapping with 'tool' and a 'cases' list")
    if cfg.get("tool") not in registry:
        raise ConfigError(f"eval file {eval_path}: unknown tool {cfg.get('tool')!r}; known: {', '.join(registry)}")
    spec = registry[cfg["tool"]]
    judgments = load_judgments(judgments_path)
    r = Report()
    judge = []
    rows = []
    known = set()                                # (case, kind, check) that exist in this eval
    cases = cfg.get("cases") or []
    if not cases:
        r.gap("EVAL_INCOMPLETE", f"{eval_path.name}: no cases selected")
    for case in cases:
        cid = case["id"]
        f = out_dir / f"{cid}.md"
        n = {"must_include": 0, "must_avoid": 0}
        judged_here = []
        for kind in ("must_include", "must_avoid"):
            for chk in case.get(kind, []):
                if "judge" in chk:
                    n[kind] += 1
                    known.add((cid, kind, n[kind]))
                    judged_here.append((kind, n[kind], chk["judge"]))
        if not f.exists():
            r.gap("EVAL_INCOMPLETE", f"{cid}: no output file {f.name}; skipped")
            rows.append((cid, "SKIP"))
            continue
        raw = f.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        md = raw.decode("utf-8")
        ar, payload = audit_output(spec, md)
        r.extend(ar, prefix=f"{cid}: ")
        fails = len(ar.errors)
        ungraded = 0
        sections = {_norm(h): b for h, b in split_sections(md).items()}
        for kind in ("must_include", "must_avoid"):
            for chk in case.get(kind, []):
                if "judge" in chk:
                    continue
                scope = md
                if "section" in chk:
                    head = spec.meta["outputs"].get(chk["section"], {}).get("heading", chk["section"])
                    scope = sections.get(_norm(head), "")
                hit = re.search(chk["pattern"], scope, re.I | re.M) is not None
                if hit != (kind == "must_include"):
                    fails += 1
                    where = f" in {chk['section']}" if "section" in chk else ""
                    verb = "missing" if kind == "must_include" else "present"
                    r.err("EVAL_FAIL", f"{cid}: /{chk['pattern']}/ {verb}{where} — {chk.get('why', '')}".rstrip(" —"))
        for kind, i, text in judged_here:
            label = f"{cid} {kind}#{i}"
            j = judgments.get((cid, kind, i))
            if j is None:
                ungraded += 1
                judge.append((label, text, None))
                r.gap("EVAL_INCOMPLETE", f"{label}: judged check has no recorded judgment")
            elif j["output_sha256"] != digest:
                ungraded += 1
                judge.append((label, text, None))
                r.gap("EVAL_INCOMPLETE", f"{label}: judgment is for a different output "
                      f"(sha256 {j['output_sha256'][:12]}, file is {digest[:12]}); regrade it")
            elif j["criterion_sha256"] != hashlib.sha256(str(text).encode("utf-8")).hexdigest():
                ungraded += 1
                judge.append((label, text, None))
                r.gap("EVAL_INCOMPLETE", f"{label}: judgment is for a different criterion "
                      f"(the judge: text changed or the checks were reordered); regrade it")
            else:
                own = " (grader is the output's author)" if j["grader_is_author"] else ""
                judge.append((label, text, f"{j['verdict']} by {j['grader']}{own}: {j['reason']}"))
                if j["verdict"] == "FAIL":
                    fails += 1
                    r.err("EVAL_FAIL", f"{label}: judged FAIL by {j['grader']}{own} — {j['reason']}")
        status = f"FAIL ({fails})" if fails else "PASS"
        if ungraded:
            status += f", {ungraded} judged ungraded"
        rows.append((cid, status))
    for key in sorted(set(judgments) - known):
        raise ConfigError(f"judgments file {judgments_path}: no judged check {key[0]} {key[1]}#{key[2]} in {eval_path.name}")
    print(f"Eval: {cfg['tool']} — {eval_path.name}")
    for cid, status in rows:
        print(f"  {cid:<28} {status}")
    pending = [(label, text) for label, text, got in judge if got is None]
    graded = [(label, got) for label, _, got in judge if got is not None]
    if graded:
        print("\nJudged checks (from the judgments file):")
        for label, got in graded:
            print(f"  [{label}] {got}")
    if pending:
        print("\nNeeds model judgment (record PASS/FAIL with a one-line reason in a judgments file;"
              " until then the run is incomplete):")
        for label, text in pending:
            crit = hashlib.sha256(str(text).encode("utf-8")).hexdigest()
            print(f"  [{label}] (criterion_sha256 {crit}) {text}")
    print()
    return r

# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------
def write_index(registry: dict[str, Spec], tools_dir: Path) -> Report:
    r = Report()
    lines = ["# QAT tool index", "",
             "Generated by `qat.py index`. Load a tool by reading its spec file.", ""]
    for name, s in registry.items():
        rep = validate_spec(s, registry)
        r.extend(rep)
        m = s.meta
        status = "ok" if not rep.errors else "INVALID"
        lines += [f"## {name} v{m.get('version', '?')} — {status}", "",
                  m.get("description", ""), "",
                  f"- **file:** `tools/{s.path.name}`",
                  "- **inputs:** " + ", ".join(f"{k} ({v['type']}{'' if v.get('required', True) else ', optional'})"
                                              for k, v in m.get("inputs", {}).items()),
                  "- **outputs:** " + ", ".join(f"{k} ({v['type']})" for k, v in m.get("outputs", {}).items())]
        if m.get("modules"):
            lines.append("- **modules:** " + ", ".join(m["modules"]))
        for h in m.get("handoffs", []):
            lines.append(f"- **hands off to** `{h['to']}` when {h['when']}")
        lines.append("")
    (tools_dir.parent / "INDEX.md").write_text("\n".join(lines))
    return r


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tools", type=Path, default=DEFAULT_TOOLS)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("index")
    v = sub.add_parser("validate"); v.add_argument("spec", type=Path)
    a = sub.add_parser("audit"); a.add_argument("tool"); a.add_argument("output", type=Path); a.add_argument("--json", type=Path)
    h = sub.add_parser("handoff"); h.add_argument("src"); h.add_argument("dst"); h.add_argument("output", type=Path); h.add_argument("--json", type=Path)
    e = sub.add_parser("eval"); e.add_argument("eval", type=Path); e.add_argument("outputs", type=Path)
    e.add_argument("--judgments", type=Path, help="JSON file of recorded judgments for the judged checks")
    args = ap.parse_args()

    registry = load_all(args.tools)
    if args.cmd == "index":
        r = write_index(registry, args.tools)
        print(f"Indexed {len(registry)} tools -> {args.tools.parent / 'INDEX.md'}")
    elif args.cmd == "validate":
        r = validate_spec(load_spec(args.spec), registry)
    elif args.cmd in ("audit", "handoff"):
        name = args.tool if args.cmd == "audit" else args.src
        if name not in registry or (args.cmd == "handoff" and args.dst not in registry):
            print(f"unknown tool; known: {', '.join(registry)}", file=sys.stderr)
            sys.exit(2)
        md = args.output.read_text()
        if args.cmd == "audit":
            r, payload = audit_output(registry[name], md)
        else:
            r, payload = build_handoff(registry[name], registry[args.dst], md, registry)
        if args.json:
            args.json.write_text(json.dumps(payload, indent=2))
        else:
            print(json.dumps(payload, indent=2))
    else:
        try:
            r = run_eval(args.eval, args.outputs, registry, args.judgments)
        except ConfigError as e:
            print(f"ERROR   {'CONFIG':<18} {e}", file=sys.stderr)
            sys.exit(2)
    r.print()
    sys.exit(r.code)


if __name__ == "__main__":
    main()
