#!/usr/bin/env python3
"""Lint and score /goal prompts as executable mission contracts.

The linter is deliberately heuristic: it does not try to understand every task,
but it catches the failure modes that make autonomous coding goals unsafe or
unproductive: vague missions, missing verification, unbounded authority, weak
stop rules, no evidence matrix, marathon prompts without durable state, and
runtime-hardened prompts without anchors, assertions, telemetry, or anti-sandbagging gates.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

CANONICAL_SECTIONS = {
    "mission": ("MISSION", "GOAL"),
    "context": ("CONTEXT",),
    "constraints": ("CONSTRAINTS", "RISK + ACTION POLICY", "RISK AND ACTION POLICY"),
    "success_criteria": ("SUCCESS CRITERIA",),
    "evidence_matrix": ("EVIDENCE MATRIX",),
    "execution_loop": ("EXECUTION LOOP", "PLAN"),
    "verify": ("VERIFY", "VERIFICATION"),
    "stop": ("STOP", "STOP RULES", "DONE WHEN"),
    "output": ("OUTPUT",),
}

MARATHON_SECTIONS = {
    "long_horizon_intent": ("LONG-HORIZON INTENT", "LONG HORIZON INTENT"),
    "target_runtime": ("TARGET RUNTIME", "CYCLE BUDGET", "RUNTIME"),
    "persistent_state": ("PERSISTENT STATE", "DURABLE STATE"),
    "soft_hard_blockers": ("SOFT VS HARD BLOCKERS", "SOFT AND HARD BLOCKERS"),
    "failure_recovery": ("FAILURE RECOVERY",),
    "quality_ratchet": ("QUALITY RATCHET",),
    "phased_execution": ("PHASED EXECUTION",),
}

ANTI_PATTERNS = {
    "make no mistakes": "replaces verification with aspiration",
    "make it perfect": "creates unbounded polishing pressure",
    "do whatever it takes": "removes authority boundaries",
    "use every tool": "encourages indiscriminate tool use",
    "keep going until everything is fixed": "creates unbounded scope",
    "no need to run tests": "weakens the verification oracle",
    "skip tests": "weakens the verification oracle",
}

EVIDENCE_TERMS = (
    "required proof",
    "evidence found",
    "pass/fail",
    "confidence",
    "source",
    "remaining gap",
    "next action",
)

RISK_TERMS = (
    "allowed without approval",
    "approval required",
    "forbidden",
    "external side effect",
    "production",
    "secrets",
    "irreversible",
)

VERIFY_TERMS = (
    "test",
    "lint",
    "typecheck",
    "build",
    "check",
    "manual",
    "evidence",
    "oracle",
)

RUNTIME_ANCHOR_TERMS = (
    "goal anchor",
    "goal_anchor",
    ".agent/goal_anchor.md",
    "compacted state",
    "cst_start",
)

RUNTIME_ASSERTION_TERMS = (
    ".agent/goal.json",
    "assertions",
    "verification_command",
    "primary_command",
    ".agent/verify_step.py",
    "deterministic assertion",
)

ADVERSARIAL_TERMS = (
    "anti-sandbagging",
    "do not delete",
    "do not comment out",
    "test assertions",
    "skip markers",
    "mocking",
    "git_delta",
)

TELEMETRY_TERMS = (
    ".agent/goal_telemetry.jsonl",
    ".agent/interrupted_state.md",
    "telemetry",
    "handoff",
    "intervention gates",
    "state handoff",
)

TERMINAL_STATES = (
    "DONE",
    "PARTIAL DONE",
    "BLOCKED",
    "UNSAFE",
    "BUDGET EXHAUSTED",
    "NEEDS HUMAN DECISION",
)

@dataclass
class Finding:
    code: str
    severity: str
    message: str
    recommendation: str

@dataclass
class CategoryScore:
    name: str
    score: int
    max_score: int
    notes: list[str]

@dataclass
class LintReport:
    path: str
    mode: str
    score: int
    max_score: int
    passed: bool
    category_scores: list[CategoryScore]
    findings: list[Finding]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def has_heading(text: str, headings: Iterable[str]) -> bool:
    for heading in headings:
        pattern = rf"(?im)^\s*{re.escape(heading)}\s*:"
        if re.search(pattern, text):
            return True
    return False


def has_any(text: str, terms: Iterable[str]) -> bool:
    low = text.lower()
    return any(term.lower() in low for term in terms)


def term_count(text: str, terms: Iterable[str]) -> int:
    low = text.lower()
    return sum(1 for term in terms if term.lower() in low)


def count_success_criteria(text: str) -> int:
    match = re.search(r"(?ims)^\s*SUCCESS CRITERIA\s*:\s*(.*?)(?:^\s*[A-Z][A-Z /+\-]{2,}\s*:|\Z)", text)
    if not match:
        return 0
    block = match.group(1)
    numbered = re.findall(r"(?m)^\s*(?:\d+\.|[-*])\s+\S", block)
    return len(numbered)


def mission_text(text: str) -> str:
    match = re.search(r"(?ims)^\s*(?:MISSION|GOAL)\s*:\s*(.*?)(?:^\s*[A-Z][A-Z /+\-]{2,}\s*:|\Z)", text)
    return match.group(1).strip() if match else ""


def score_bool(name: str, value: bool, notes: list[str], weight: int = 5) -> CategoryScore:
    return CategoryScore(name=name, score=weight if value else 0, max_score=weight, notes=notes)


def infer_mode(text: str, explicit: str | None) -> str:
    if explicit:
        return explicit
    if has_any(text, ["LONG-HORIZON INTENT", "PERSISTENT STATE", "SOFT VS HARD BLOCKERS"]):
        return "marathon"
    return "frontier"


def wants_runtime_hardening(text: str, mode: str) -> bool:
    return mode == "marathon" or has_any(text, [".agent/", "GOAL ANCHOR", "COMPACTED STATE", "CST_START", "anti-sandbagging", "telemetry", "verify_step.py"])


def score_goal(text: str, path: str = "<memory>", mode: str | None = None) -> LintReport:
    findings: list[Finding] = []
    categories: list[CategoryScore] = []
    low = normalize(text)
    inferred_mode = infer_mode(text, mode)

    if "/goal" not in low:
        findings.append(Finding("MISSING_GOAL_PREFIX", "error", "Prompt does not contain /goal.", "Start the prompt with /goal."))
        categories.append(score_bool("goal_prefix", False, ["missing /goal"], 3))
    else:
        categories.append(score_bool("goal_prefix", True, ["contains /goal"], 3))

    miss = mission_text(text)
    vague_terms = ("better", "improve", "fix stuff", "make it good", "perfect", "everything")
    mission_ok = bool(miss) and len(miss.split()) >= 6 and not any(t in miss.lower() for t in vague_terms)
    if not mission_ok:
        findings.append(Finding("WEAK_MISSION", "error", "Mission is missing, too short, or vague.", "Define one measurable durable outcome with a clear scope boundary."))
    categories.append(score_bool("mission_singularity", mission_ok, ["mission is concrete" if mission_ok else "mission is vague or missing"], 8))

    criteria_count = count_success_criteria(text)
    criteria_ok = criteria_count >= 2
    if not criteria_ok:
        findings.append(Finding("WEAK_SUCCESS_CRITERIA", "error", f"Found {criteria_count} success criteria.", "Add at least two observable, testable success criteria."))
    categories.append(score_bool("measurable_success_criteria", criteria_ok, [f"criteria_count={criteria_count}"], 8))

    missing_sections = []
    for name, headings in CANONICAL_SECTIONS.items():
        if not has_heading(text, headings):
            missing_sections.append(name)
    if missing_sections:
        findings.append(Finding("MISSING_CORE_SECTIONS", "error", "Missing core sections: " + ", ".join(missing_sections), "Add the missing execution-contract sections."))
    section_score = max(0, 12 - len(missing_sections) * 2)
    categories.append(CategoryScore("contract_completeness", section_score, 12, ["missing=" + ",".join(missing_sections) if missing_sections else "all core sections present"]))

    evidence_score = term_count(text, EVIDENCE_TERMS)
    evidence_ok = has_heading(text, CANONICAL_SECTIONS["evidence_matrix"]) and evidence_score >= 5
    if not evidence_ok:
        findings.append(Finding("WEAK_EVIDENCE_MATRIX", "error", "Evidence matrix is missing or underspecified.", "Include required proof, evidence found, pass/fail/unknown, confidence, source, remaining gap, and next action."))
    categories.append(CategoryScore("evidence_matrix", min(10, evidence_score + (3 if has_heading(text, CANONICAL_SECTIONS["evidence_matrix"]) else 0)), 10, [f"evidence_terms={evidence_score}"]))

    risk_score = term_count(text, RISK_TERMS)
    risk_ok = risk_score >= 4
    if not risk_ok:
        findings.append(Finding("WEAK_RISK_POLICY", "error", "Risk policy does not clearly bound authority.", "Separate allowed, rollback-required, approval-required, and forbidden actions."))
    categories.append(CategoryScore("risk_policy", min(10, risk_score * 2), 10, [f"risk_terms={risk_score}"]))

    verify_score = term_count(text, VERIFY_TERMS)
    verify_ok = has_heading(text, CANONICAL_SECTIONS["verify"]) and verify_score >= 3
    if not verify_ok:
        findings.append(Finding("WEAK_VERIFICATION_ORACLE", "error", "Verification is absent or too weak.", "Name the narrow checks, broader checks, and evidence mapping required for DONE."))
    categories.append(CategoryScore("verification_oracle", min(10, verify_score * 2), 10, [f"verify_terms={verify_score}"]))

    terminal_count = sum(1 for state in TERMINAL_STATES if state.lower() in low)
    stop_ok = has_heading(text, CANONICAL_SECTIONS["stop"]) and terminal_count >= 3
    if not stop_ok:
        findings.append(Finding("WEAK_STOP_RULES", "error", "Stop rules or terminal states are missing.", "Define DONE/BLOCKED/UNSAFE/BUDGET EXHAUSTED/NEEDS HUMAN DECISION as applicable."))
    categories.append(CategoryScore("stop_conditions", min(8, terminal_count + (3 if has_heading(text, CANONICAL_SECTIONS["stop"]) else 0)), 8, [f"terminal_states={terminal_count}"]))

    anti_hits = [phrase for phrase in ANTI_PATTERNS if phrase in low]
    if anti_hits:
        findings.append(Finding("ANTI_PATTERNS", "error", "Detected anti-patterns: " + ", ".join(anti_hits), "Replace motivational or unbounded language with evidence, authority, and stop rules."))
    categories.append(CategoryScore("anti_patterns", 0 if anti_hits else 7, 7, ["hits=" + ",".join(anti_hits) if anti_hits else "none detected"]))

    if inferred_mode == "marathon":
        missing_marathon = [name for name, headings in MARATHON_SECTIONS.items() if not has_heading(text, headings)]
        if missing_marathon:
            findings.append(Finding("MISSING_MARATHON_SECTIONS", "error", "Missing marathon sections: " + ", ".join(missing_marathon), "Add runtime budget, persistent state, blocker policy, failure recovery, phases, and quality ratchet."))
        marathon_score = max(0, 15 - len(missing_marathon) * 3)
        categories.append(CategoryScore("marathon_protocol", marathon_score, 15, ["missing=" + ",".join(missing_marathon) if missing_marathon else "all marathon sections present"]))

        durable_state_ok = has_any(text, [".goal/", ".agent/", "state.md", "evidence.md", "handoff.md"])
        if not durable_state_ok:
            findings.append(Finding("WEAK_DURABLE_STATE", "error", "Marathon prompt does not specify durable state artifacts.", "Use .goal/ or .agent/ state artifacts for state, evidence, failures, commands, and handoff."))
        categories.append(score_bool("durable_memory", durable_state_ok, ["durable state specified" if durable_state_ok else "durable state missing"], 7))

    if wants_runtime_hardening(text, inferred_mode):
        anchor_score = term_count(text, RUNTIME_ANCHOR_TERMS)
        anchor_ok = anchor_score >= 2
        if not anchor_ok:
            findings.append(Finding("WEAK_GOAL_ANCHOR", "error", "Runtime-hardened prompt lacks a compact goal anchor.", "Add GOAL ANCHOR or .agent/goal_anchor.md with objective, target refs, constraints, verification, and stop gates."))
        categories.append(CategoryScore("compaction_resistance", min(8, anchor_score * 3), 8, [f"anchor_terms={anchor_score}"]))

        assertion_score = term_count(text, RUNTIME_ASSERTION_TERMS)
        assertion_ok = assertion_score >= 2
        if not assertion_ok:
            findings.append(Finding("WEAK_RUNTIME_ASSERTIONS", "error", "Runtime-hardened prompt lacks deterministic assertion wiring.", "Reference .agent/goal.json assertions and/or .agent/verify_step.py verification commands."))
        categories.append(CategoryScore("deterministic_assertions", min(8, assertion_score * 3), 8, [f"assertion_terms={assertion_score}"]))

        adversarial_score = term_count(text, ADVERSARIAL_TERMS)
        adversarial_ok = adversarial_score >= 3
        if not adversarial_ok:
            findings.append(Finding("WEAK_ADVERSARIAL_HARDENING", "error", "Prompt lacks anti-sandbagging gates.", "Forbid deleted/muted tests, skip markers, unjustified mocks, public API drift, and weak self-assessment."))
        categories.append(CategoryScore("adversarial_hardening", min(10, adversarial_score * 2), 10, [f"adversarial_terms={adversarial_score}"]))

        telemetry_score = term_count(text, TELEMETRY_TERMS)
        telemetry_ok = telemetry_score >= 2
        if not telemetry_ok:
            findings.append(Finding("WEAK_TELEMETRY_HANDOFF", "error", "Prompt lacks runtime telemetry or interrupted-state handoff.", "Add .agent/goal_telemetry.jsonl and .agent/interrupted_state.md or equivalent handoff artifacts."))
        categories.append(CategoryScore("telemetry_handoff", min(8, telemetry_score * 3), 8, [f"telemetry_terms={telemetry_score}"]))

    max_score = sum(c.max_score for c in categories)
    total_score = sum(c.score for c in categories)
    threshold = int(max_score * (0.82 if inferred_mode == "marathon" else 0.78))
    has_errors = any(f.severity == "error" for f in findings)
    passed = total_score >= threshold and not has_errors

    return LintReport(path=path, mode=inferred_mode, score=total_score, max_score=max_score, passed=passed, category_scores=categories, findings=findings)


def render_text(report: LintReport) -> str:
    status = "PASS" if report.passed else "FAIL"
    lines = [f"{status} {report.path}", f"mode: {report.mode}", f"score: {report.score}/{report.max_score}", ""]
    lines.append("Category scores:")
    for category in report.category_scores:
        note = "; ".join(category.notes)
        lines.append(f"- {category.name}: {category.score}/{category.max_score} ({note})")
    if report.findings:
        lines.append("")
        lines.append("Findings:")
        for finding in report.findings:
            lines.append(f"- [{finding.severity}] {finding.code}: {finding.message}")
            lines.append(f"  Recommendation: {finding.recommendation}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint /goal prompts as mission contracts.")
    parser.add_argument("paths", nargs="+", help="Prompt files to lint")
    parser.add_argument("--mode", choices=["compact", "frontier", "marathon"], default=None, help="Override inferred mode")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = parser.parse_args(argv)

    reports = []
    for raw_path in args.paths:
        path = Path(raw_path)
        text = path.read_text(encoding="utf-8")
        reports.append(score_goal(text, path=str(path), mode=args.mode))

    if args.json:
        print(json.dumps([asdict(r) for r in reports], indent=2))
    else:
        for index, report in enumerate(reports):
            if index:
                print("\n" + "-" * 72 + "\n")
            print(render_text(report))

    return 0 if all(report.passed for report in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
