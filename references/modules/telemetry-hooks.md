# Telemetry Hooks Module

Use this module when long-running execution needs resumability, observability, or human intervention points.

```text
TELEMETRY HOOKS:
Create `.agent/goal_telemetry.jsonl` unless forbidden by repository rules.

Append one JSON object per meaningful checkpoint:
- event_id: monotonically increasing integer or timestamp slug
- phase: reconnaissance, vertical_slice, expansion, hardening, handoff, blocked, done
- action: short description of the last action
- evidence_delta: what evidence changed
- files_touched: paths changed or inspected
- commands_run: commands and exit codes
- uncertainty_delta: uncertainties reduced or introduced
- next_action: next evidence-closing action
- status: continue, done, blocked, unsafe, needs_human_decision, budget_exhausted

Intervention gates:
- If the same command fails 3 consecutive times with no changed hypothesis, write `.agent/interrupted_state.md` and stop.
- If an action crosses the risk policy, write `.agent/interrupted_state.md` and stop before acting.
- If external side effects are required without approval, write `.agent/interrupted_state.md` and stop.

On DONE, BLOCKED, UNSAFE, BUDGET EXHAUSTED, or NEEDS HUMAN DECISION, write a final handoff entry with evidence, changed files, commands, risks, and next actions.
```
