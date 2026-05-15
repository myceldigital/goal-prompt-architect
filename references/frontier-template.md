# Frontier /goal Prompt Template

Use this for complex coding, repo, product, research, operations, or multi-hour tasks.

```text
/goal

MISSION:
<one measurable durable objective; one mission only>

PREFLIGHT:
Before execution, produce a mission manifest:
- objective
- observed context
- candidate strategies
- selected strategy
- success criteria
- evidence plan
- risk envelope
- expected touched files/systems
- rollback/containment plan
- stop conditions

Do not begin implementation until the manifest is internally consistent and grounded in observed context.

CONTEXT:
<repo/product/system/workflow state>
<known assumptions>
<relevant files/docs/tests/issues/data/tools>
<prior decisions>
<environment constraints>

GROUNDED STRATEGY SEARCH:
For non-trivial work, generate up to 3 candidate strategies.

Each strategy must cite observed evidence and include:
- files/systems/tools touched
- verification path
- risk class
- rollback/containment plan
- likely failure mode

Select the strategy with the best tradeoff between:
- success probability
- minimality
- reversibility
- verification clarity
- architectural/workflow fit
- scope control

RISK + ACTION POLICY:
Classify meaningful actions:

0. read-only
1. local reversible edit
2. costly-to-reverse local edit
3. external side effect
4. irreversible or production-impacting action

Proceed autonomously only with in-scope Class 0-1.
Proceed with Class 2 only when rollback is explicit and allowed.
Stop for Class 3-4 unless explicitly authorized.

Allowed without approval:
- <safe reversible actions>

Allowed with rollback plan:
- <costly-to-reverse local actions>

Approval required:
- <external systems, production, secrets, migrations, auth, billing, security, destructive actions>

Forbidden:
- <actions never allowed>

SUCCESS CRITERIA:
1. <specific measurable criterion>
2. <specific measurable criterion>
3. <specific measurable criterion>

EVIDENCE MATRIX:
For each criterion, maintain:
- required proof
- evidence found
- pass/fail/unknown
- confidence
- source
- remaining gap

EXECUTION LOOP:
Repeat until a terminal state is reached:

1. OBSERVE
   Read the smallest relevant evidence.

2. ORIENT
   Update memory and uncertainty ranking.

3. DECIDE
   Pick the next action that most directly closes an evidence gap.

4. ACT
   Execute only actions permitted by the risk envelope.

5. VERIFY
   Run the narrowest meaningful check.

6. REFLECT
   Convert failures into lessons:
   - what failed
   - likely cause
   - next adjustment
   - what not to repeat

7. COMPACT
   Update memory layers and discard redundant context.

8. CONTINUE / STOP
   Continue only if the next step closes an evidence gap.

MEMORY:
Maintain:
- working memory: current subgoal, immediate observations, next action
- episodic ledger: chronological checkpoints and failures
- semantic mission memory: stable facts, verified commands, invariants, architecture/workflow findings

Each durable memory must include:
- claim
- source/provenance
- confidence
- scope
- type: observation / hypothesis / decision / failure / invariant

Re-verify stale or high-impact memory before relying on it.

SUBGOAL POLICY:
Create subgoals only when they reduce complexity.
Each subgoal must have:
- local done condition
- verification
- relation to parent goal
- evidence gap it closes

Do not create subgoals that expand scope.

BUDGET GATES:
Track:
- elapsed time
- failed attempts
- touched files/artifacts/tools
- tool calls
- unresolved uncertainties
- scope expansion pressure

Pause if:
- repeated failures exceed threshold
- blast radius exceeds expected scope
- verification path becomes unclear
- new requirements are discovered
- confidence drops below acceptable threshold

VERIFY:
Run the narrowest relevant checks first, then broader validation as practical:
- <unit test / narrow check>
- <lint/typecheck/static validation>
- <build/integration/manual validation>

Map every success criterion to evidence.
If verification cannot be completed, explain exactly why and provide the closest available evidence.

STOP:
Stop when:
- all success criteria are verified
- the next action does not close an evidence gap
- action exceeds authorization
- ambiguity is high-impact
- repeated failure indicates the selected strategy is wrong
- budget gate triggers
- scope expansion is required

TERMINAL STATE:
Return exactly one:
- DONE
- BLOCKED
- UNSAFE
- BUDGET EXHAUSTED
- NEEDS HUMAN DECISION

OUTPUT:
Return:
- terminal state
- concise summary
- selected strategy and why
- evidence matrix
- files/artifacts changed
- commands/checks run
- verification results
- failures and lessons
- risk/rollback notes
- unresolved uncertainties
- recommended follow-ups

SKILL EXTRACTION:
After DONE only:
- list reusable procedures discovered
- suggest future automations/templates
- do not implement generalized tooling unless separately requested
```
