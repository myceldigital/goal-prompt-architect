#!/usr/bin/env python3
"""Optional local verification harness for runtime-hardened /goal prompts.

This script provides conservative, dependency-free integrity checks that can be
referenced from generated `.agent/goal.json` assertions. It is intentionally
configurable and avoids assuming that every repository has the same toolchain.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence

DEFAULT_TIMEOUT = 120
ASSERTION_DELETION_TERMS = ("expect(", "assert ", "self.assert", "assert_", "should(", "toEqual(")
TEST_BLOCK_DELETION_TERMS = ("#[test]", "def test_", "it(", "describe(", "test(")
SKIP_ADDITION_TERMS = ("@pytest.mark.skip", "@unittest.skip", ".skip(", "describe.skip", "it.skip", "test.skip")


def run_command(cmd: Sequence[str], timeout: int = DEFAULT_TIMEOUT) -> tuple[int, str, str]:
    try:
        result = subprocess.run(list(cmd), capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError as exc:
        return 127, "", str(exc)
    except subprocess.TimeoutExpired as exc:
        return 124, exc.stdout or "", exc.stderr or f"Command timed out after {timeout}s"


def emit_json(target: str, status: str, message: str, evidence: dict | None = None) -> None:
    payload = {"target": target, "status": status, "message": message, "evidence": evidence or {}}
    print(json.dumps(payload, indent=2, sort_keys=True))


def git_diff() -> str:
    code, stdout, stderr = run_command(["git", "diff"], timeout=DEFAULT_TIMEOUT)
    if code != 0:
        emit_json("git_delta", "fail", "git diff failed", {"stderr": stderr})
        raise SystemExit(1)
    return stdout


def verify_git_delta(args: argparse.Namespace) -> None:
    diff = git_diff()
    violations: list[str] = []
    for line in diff.splitlines():
        stripped = line.strip()
        if stripped.startswith("---") or stripped.startswith("+++"):
            continue
        if stripped.startswith("-"):
            if any(term in line for term in ASSERTION_DELETION_TERMS):
                violations.append(f"deleted assertion: {line}")
            if any(term in line for term in TEST_BLOCK_DELETION_TERMS):
                violations.append(f"deleted test block: {line}")
        if stripped.startswith("+"):
            if any(term in line for term in SKIP_ADDITION_TERMS):
                violations.append(f"added skip/bypass marker: {line}")

    if violations:
        emit_json("git_delta", "fail", "Forbidden test/assertion delta detected", {"violations": violations[:20]})
        raise SystemExit(1)

    emit_json("git_delta", "pass", "No forbidden assertion, test-block, or skip-marker deltas detected", {"checked_lines": len(diff.splitlines())})


def detect_project() -> str:
    if Path("Cargo.toml").exists():
        return "rust"
    if Path("package.json").exists():
        return "node"
    if any(Path(name).exists() for name in ("pyproject.toml", "requirements.txt", "poetry.lock", "setup.py")):
        return "python"
    return "unknown"


def command_from_env(name: str) -> list[str] | None:
    value = os.environ.get(name)
    if not value:
        return None
    return value.split()


def verify_command(target: str, command: list[str], timeout: int) -> None:
    code, stdout, stderr = run_command(command, timeout=timeout)
    evidence = {"command": command, "stdout_tail": stdout[-4000:], "stderr_tail": stderr[-4000:], "returncode": code}
    if code != 0:
        emit_json(target, "fail", "Verification command failed", evidence)
        raise SystemExit(1)
    emit_json(target, "pass", "Verification command passed", evidence)


def verify_python(args: argparse.Namespace) -> None:
    command = command_from_env("GOAL_PYTHON_CHECK")
    if command is None:
        if Path("pyproject.toml").exists() or Path("pytest.ini").exists() or Path("tests").exists():
            command = [sys.executable, "-m", "unittest", "discover"] if not Path("tests").exists() else [sys.executable, "-m", "unittest", "discover", "-s", "tests"]
        else:
            emit_json("python", "fail", "No Python verification command discovered; set GOAL_PYTHON_CHECK")
            raise SystemExit(1)
    verify_command("python", command, args.timeout)


def verify_node(args: argparse.Namespace) -> None:
    command = command_from_env("GOAL_NODE_CHECK")
    if command is None:
        package_json = Path("package.json")
        if not package_json.exists():
            emit_json("node", "fail", "package.json not found")
            raise SystemExit(1)
        data = json.loads(package_json.read_text(encoding="utf-8"))
        scripts = data.get("scripts", {})
        if "test" in scripts:
            command = ["npm", "test"]
        elif "build" in scripts:
            command = ["npm", "run", "build"]
        else:
            emit_json("node", "fail", "No test/build script found; set GOAL_NODE_CHECK")
            raise SystemExit(1)
    verify_command("node", command, args.timeout)


def verify_rust(args: argparse.Namespace) -> None:
    command = command_from_env("GOAL_RUST_CHECK") or ["cargo", "check"]
    env = os.environ.copy()
    env.setdefault("RUSTFLAGS", "-D warnings")
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=args.timeout, env=env)
    except FileNotFoundError as exc:
        emit_json("rust", "fail", str(exc), {"command": command})
        raise SystemExit(1)
    except subprocess.TimeoutExpired as exc:
        emit_json("rust", "fail", f"Command timed out after {args.timeout}s", {"stdout_tail": (exc.stdout or "")[-4000:], "stderr_tail": (exc.stderr or "")[-4000:]})
        raise SystemExit(1)
    evidence = {"command": command, "stdout_tail": result.stdout[-4000:], "stderr_tail": result.stderr[-4000:], "returncode": result.returncode}
    if result.returncode != 0:
        emit_json("rust", "fail", "Rust verification failed", evidence)
        raise SystemExit(1)
    emit_json("rust", "pass", "Rust verification passed", evidence)


def verify_auto(args: argparse.Namespace) -> None:
    project = detect_project()
    if project == "python":
        verify_python(args)
    elif project == "node":
        verify_node(args)
    elif project == "rust":
        verify_rust(args)
    else:
        emit_json("auto", "fail", "Could not detect project type; use --command or a project-specific target", {"project": project})
        raise SystemExit(1)


def verify_custom(args: argparse.Namespace) -> None:
    if not args.command:
        emit_json("custom", "fail", "--command is required for custom verification")
        raise SystemExit(1)
    verify_command("custom", args.command, args.timeout)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Runtime goal verification harness")
    parser.add_argument("--target", required=True, choices=["git_delta", "python", "node", "rust", "auto", "custom"], help="Verification target to execute")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Command timeout in seconds")
    parser.add_argument("--command", nargs=argparse.REMAINDER, help="Command for --target custom")
    args = parser.parse_args(argv)

    if args.target == "git_delta":
        verify_git_delta(args)
    elif args.target == "python":
        verify_python(args)
    elif args.target == "node":
        verify_node(args)
    elif args.target == "rust":
        verify_rust(args)
    elif args.target == "auto":
        verify_auto(args)
    elif args.target == "custom":
        verify_custom(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
