/goal

MISSION:
Migrate the cache adapter from Redis to Memcached while preserving the existing cache interface, caller behavior, and integration test expectations.

LONG-HORIZON INTENT:
This is a sustained autonomous execution mission. Optimize for durable, reviewable, evidence-backed completion, not a short investigation. Continue through normal uncertainty and failed attempts unless a hard blocker or explicit budget limit is reached.

TARGET RUNTIME:
Work for up to 6 hours or until DONE. Checkpoint every 60 minutes or at each meaningful phase transition.

PREFLIGHT:
Inspect README, AGENTS, CONTRIBUTING, SECURITY, package manifests, cache modules, existing tests, fixtures, CI workflows, and neighboring adapter patterns. Produce a mission manifest with observed context, risk envelope, candidate strategies, selected strategy, verification plan, expected touched files, rollback plan, hard blockers, and soft blockers.

CONTEXT:
Work only in the local repository. Preserve the public cache interface and all callers. Discover test, lint, typecheck, and build commands from repository manifests.

PERSISTENT STATE:
Create or update .goal/ and .agent/ unless forbidden by repository rules. Maintain .goal/state.md, .goal/evidence.md, .goal/failures.md, .goal/commands.md, .goal/handoff.md, .agent/goal.json, .agent/goal_anchor.md, .agent/goal_telemetry.jsonl, and .agent/interrupted_state.md as needed.

GOAL ANCHOR:
Write .agent/goal_anchor.md and read it at the start of every observe-orient-act-verify cycle.
# GOAL_ANCHOR_START
objective: Migrate the cache adapter from Redis to Memcached while preserving interface parity.
target_refs: src/cache, tests/cache, package/test manifests
core_constraints: no public API drift, no deleted or weakened tests, no production side effects
verification: .agent/verify_step.py --target git_delta plus discovered cache tests
stop_gates: approval-required action, hard blocker, external side effect, budget exhaustion
# GOAL_ANCHOR_END

GROUNDED STRATEGY SEARCH:
Generate up to 3 candidate strategies. Each strategy must cite observed evidence and include files touched, verification path, risk class, rollback plan, likely failure mode, and first evidence-producing action. Select the best strategy for success probability, minimality, reversibility, verification clarity, architectural fit, scope control, and safe continuation.

RISK + ACTION POLICY:
Allowed without approval:
- read-only inspection
- reversible local edits inside cache implementation and directly related tests
- local verification commands

Allowed with rollback plan:
- local fixture or configuration changes directly required for Memcached parity

Approval required:
- production deploys, production migrations, secrets, credentials, external cache infrastructure, billing, auth, security, destructive actions, broad dependency upgrades, or public exposure changes

Forbidden:
- public cache API signature drift
- unrelated caller rewrites
- deleting, muting, or weakening tests to create a false pass
- adding broad mocks that bypass real cache adapter behavior

SUCCESS CRITERIA:
1. The Memcached adapter preserves the existing cache interface and caller behavior.
2. Existing cache tests and relevant integration checks pass or unavailable checks are explicitly bounded with closest evidence.
3. Git delta verification shows no deleted assertions, removed test blocks, skip markers, or unrelated public API drift.

EVIDENCE MATRIX:
For each criterion, maintain required proof, evidence found, pass/fail/unknown, confidence, source, remaining gap, and next action to close the gap.

EXECUTION LOOP:
Repeat observe, orient, decide, act, verify, reflect, compact, and continue or stop. Start each cycle by reading .agent/goal_anchor.md. Choose the next action that most directly closes an evidence gap and is permitted by the risk envelope.

FAILURE RECOVERY:
Do not repeat the same failed command or edit more than twice without changing inputs, assumptions, or strategy. Record each failure in .goal/failures.md and .agent/goal_telemetry.jsonl.

SOFT VS HARD BLOCKERS:
Soft blockers include failing tests, incomplete docs, flaky commands, missing optional local services, and ambiguous low-risk implementation details. Hard blockers include production-impacting actions, irreversible/destructive actions, secrets/security/privacy risk, external side effects without approval, required unavailable dependencies with no safe parallel work, or no safe validation evidence possible.

ADVERSARIAL VERIFICATION:
Use anti-sandbagging gates. Do not delete, comment out, or weaken test assertions. Do not add skip markers. Do not use broad mocks to bypass behavior. Run .agent/verify_step.py --target git_delta before DONE when git is available.

TELEMETRY HOOKS:
Append structured checkpoints to .agent/goal_telemetry.jsonl. On blocked, unsafe, budget exhausted, or needs human decision, write .agent/interrupted_state.md with blocking errors, changed files, evidence, risk notes, and recovery steps.

QUALITY RATCHET:
After first green check, do not immediately stop. Run quality passes for correctness, verification strength, maintainability, minimality, architectural fit, and risk containment. Any score below 4 requires another improvement cycle or explicit explanation.

VERIFY:
Use a verification ladder: .agent/verify_step.py --target git_delta, narrow cache tests, related integration checks, lint/typecheck/build/static validation, and manual or diagnostic evidence if automated checks are unavailable. Map every success criterion to evidence.

STOP:
Stop when all success criteria are verified and quality ratchet is satisfied, the next action does not close an evidence gap, action exceeds authorization, a hard blocker prevents progress with no safe parallel work, repeated diverse strategies show the mission is not achievable, budget is exhausted after resumable handoff, or scope expansion is required.

TERMINAL STATE:
Return exactly one: DONE, PARTIAL DONE, BLOCKED, UNSAFE, BUDGET EXHAUSTED, or NEEDS HUMAN DECISION.

OUTPUT:
Return terminal state, summary, phase reached, selected strategy, evidence matrix, files/artifacts changed, commands/checks run, verification results, quality-ratchet scores, failures and lessons, risk/rollback notes, unresolved uncertainties, next actions, and persistent handoff location.
