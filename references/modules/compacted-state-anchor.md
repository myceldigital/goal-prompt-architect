# Compacted State Anchor Module

Use this module when a `/goal` may run across many tool cycles, compaction events, restarts, or handoffs.

```text
GOAL ANCHOR:
Create `.agent/goal_anchor.md` unless forbidden by repository rules.

The anchor must be short enough to re-read at the start of every execution cycle:

# GOAL_ANCHOR_START
objective: <dense one-sentence outcome>
target_refs: <files/modules/artifacts in scope>
core_constraints: <non-negotiable boundaries>
verification: <primary command or assertion set>
stop_gates: <approval-required, unsafe, hard-blocker, or budget triggers>
# GOAL_ANCHOR_END

At the start of every observe-orient-act-verify cycle:
1. Read `.agent/goal_anchor.md`.
2. Compare the next action against the anchor.
3. Stop or re-orient if the action does not serve the objective, violates constraints, or bypasses verification.

Before compaction, interruption, or handoff, rewrite the anchor verbatim and update only fields whose evidence has changed.
```
