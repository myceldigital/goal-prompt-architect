---
name: goal-prompt-architect
description: create, audit, and improve high-performance /goal prompts for autonomous coding agents and long-running agent workflows. use when the user asks for a /goal prompt, goal prompt template, codex/claude code/hermes mission prompt, long-running agent prompt, repo-specific autonomous task prompt, or wants to transform a vague task into a measurable, risk-bounded, verification-driven execution contract.
---

# Goal Prompt Architect

## Core Rule

Generate `/goal` prompts as autonomous execution contracts, not motivational instructions. Always optimize for: one measurable mission, bounded authority, grounded strategy, uncertainty reduction, verification evidence, memory/progress discipline, and clean stopping conditions.

## Workflow

1. **Classify the request**
   - **Repo/software task**: inspect any provided repo/files/docs first when available. Include concrete commands, paths, worktree rules, migrations, and validation.
   - **Business/ops/research task**: adapt the same architecture to documents, tools, datasets, or workflows.
   - **Prompt-only request**: produce a reusable `/goal` prompt without executing the underlying mission.
   - **Audit/improvement request**: critique the provided prompt, then provide a revised version.

2. **Gather missing essentials only when needed**
   Ask concise follow-up questions only if the mission, expected output, or verification standard is impossible to infer. Prefer making safe assumptions and marking them in the prompt over asking open-ended questions.

3. **Create a mission-grade prompt**
   Use the template in `references/frontier-template.md` for complex or high-risk work. Use `references/compact-template.md` for simple tasks or when the user asks for brevity.

4. **Adapt to context**
   Pull in domain-specific sections from `references/domain-adaptations.md` when relevant.

5. **Quality-check before final output**
   Run the checklist in this file before answering. If the prompt fails any mandatory item, revise it.

## Mandatory Design Principles

Every serious `/goal` prompt must include:

- **Single mission**: one durable objective, not a bundle of unrelated tasks.
- **Measurable success criteria**: observable, testable, and scoped.
- **Grounded preflight**: inspect context before acting; do not invent architecture.
- **Risk envelope**: allowed, forbidden, and approval-required actions.
- **Action classification**: read-only, reversible local edit, costly-to-reverse edit, external side effect, irreversible/production-impacting action.
- **Evidence matrix**: each success criterion maps to required proof and current evidence.
- **Execution loop**: observe → orient → decide → act → verify → reflect → compact → continue/stop.
- **Memory protocol**: working memory, episodic ledger, semantic mission memory for long runs.
- **Stop rules**: halt on done, unsafe action, high-impact ambiguity, budget exhaustion, or scope expansion.
- **Terminal state**: DONE, BLOCKED, UNSAFE, BUDGET EXHAUSTED, or NEEDS HUMAN DECISION.
- **Output contract**: summary, evidence, changed files/artifacts, checks run, risks, and follow-ups.

## Construction Procedure

### Step 1: Define the mission

Convert vague user intent into one measurable mission:

- Bad: `make the app better`
- Better: `implement password reset so users can request a reset email, set a new password through a valid token, and pass auth tests without changing the existing login flow`

If there are multiple missions, split them or make the prompt explicitly choose one.

### Step 2: Add context and inspection instructions

Include known repo/product/workflow facts. For software repos, include:

- app/service/package layout
- languages/frameworks
- files/docs to inspect first
- setup, test, build, lint commands
- existing rules such as AGENTS.md, CONTRIBUTING.md, SECURITY.md
- migration or deployment docs

For unknown repos, instruct the agent to inspect these before implementation.

### Step 3: Define risk and authority

Always separate:

- **Allowed without approval**: safe, reversible, local, in-scope actions.
- **Allowed with rollback plan**: costly-to-reverse local changes.
- **Approval required**: production, secrets, external side effects, destructive ops, broad dependency upgrades, migrations, auth/security/billing/payment changes.
- **Forbidden**: anything the user/org explicitly disallows.

Use stricter defaults for regulated, clinical, legal, financial, production, or privacy-sensitive tasks.

### Step 4: Require grounded strategy search

For non-trivial work, require up to 3 candidate strategies. Each must cite observed evidence, expected files/systems touched, verification path, risk class, rollback plan, and failure mode. The agent selects the strategy with best success probability, minimality, reversibility, verification clarity, architectural fit, and scope control.

Skip strategy search only for trivial tasks.

### Step 5: Build the evidence matrix

For every success criterion, specify:

- required proof
- evidence found
- pass/fail/unknown
- confidence
- source
- remaining gap

The agent must continue only when the next action closes an evidence gap.

### Step 6: Add execution loop and memory

Use the loop to control long runs. For multi-hour or multi-day goals, include memory compaction every few meaningful steps and stale-memory re-verification for high-impact actions.

### Step 7: Add verification commands

Use actual known commands when available. If unknown, tell the agent to discover and run narrow checks first, then broader checks. Do not include fake commands as if certain.

### Step 8: Add stop and output contracts

Make stopping explicit. A `/goal` prompt should prevent endless polishing and prevent scope creep after the mission is satisfied.

## Response Style

When returning a `/goal` prompt:

- Put the final prompt in a single copyable fenced code block.
- Precede it with a short note only if needed to explain assumptions.
- Avoid long essays unless the user asks for rationale or debate.
- If the user asked for multiple versions, label them clearly: compact, standard, frontier, repo-specific.
- Do not claim you inspected a repo, file, or docs unless you actually did.

## Quality Checklist

Before finalizing, verify the prompt answers:

1. What exact outcome must be achieved?
2. What context must be inspected first?
3. What must not be changed?
4. What actions require approval?
5. What are the measurable success criteria?
6. What evidence proves each criterion?
7. What loop governs execution?
8. How are failures and memory handled?
9. When must the agent stop?
10. What must the final report contain?

If any answer is missing, revise the prompt.

## Common Anti-Patterns to Remove

- `make no mistakes`
- `make it perfect`
- `use every tool`
- `do whatever it takes`
- `keep going until everything is fixed`
- broad rewrites when minimal edits suffice
- verification postponed until the very end
- open-ended clarification questions inside the running goal
- unbounded production/deployment/secrets access
- success criteria with no proof path

## References

- Use `references/frontier-template.md` for the full architecture.
- Use `references/compact-template.md` for lightweight prompts.
- Use `references/domain-adaptations.md` for repo, product, data, research, and operations variants.
