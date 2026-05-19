# Runtime Hardening Layer

This directory contains optional scaffolding for agents that can write local files during `/goal` execution.

The files here are templates and utilities, not a requirement for every prompt. Use them when the goal benefits from deterministic verification, compaction resistance, structured telemetry, or adversarial anti-sandbagging checks.

## Files

- `verify_step.py`: dependency-free verification harness for common integrity checks.
- `goal.schema.json`: versioned schema for `.agent/goal.json` runtime contracts.

## Expected generated runtime files

A compiled marathon or runtime-hardened goal may instruct the target agent to create:

```text
.agent/
├── goal.json                 # objective, target refs, assertions, gates, risk policy
├── goal_anchor.md            # compact state anchor read before every cycle
├── goal_telemetry.jsonl      # append-only checkpoint/event log
└── interrupted_state.md      # human handoff if blocked, unsafe, or interrupted
```

## Safety model

Runtime hardening should never expand authority. It only makes already-authorized local checks more reproducible. External side effects, production operations, secrets, destructive actions, or compliance-significant operations still require explicit approval in the `/goal` risk policy.
