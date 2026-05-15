Most people use /goal wrong.

They write: “make no mistakes.”

Goal Prompt Architect turns /goal into an execution contract:

- mission
- risk envelope
- grounded strategy search
- evidence matrix
- memory loop
- stop rules

Agent Skill for Codex, Claude Code, Hermes, and long-running AI agents.



# Goal Prompt Architect

**An agent Skill for creating `/goal` prompts for Codex, Claude Code, Hermes, and long-running autonomous AI agents.**

Goal Prompt Architect turns vague task ideas into mission-grade execution contracts: measurable outcomes, grounded strategy search, risk boundaries, action classification, verification evidence, memory discipline, budget gates, and clean stop conditions.

It is designed for people building with frontier coding agents and agentic workflows who want better long-horizon performance than prompts like:

```text
/goal make this perfect and make no mistakes
```

Instead, it helps produce prompts that tell agents exactly:

- what mission to complete
- what context to inspect first
- what actions are allowed or forbidden
- how to rank uncertainty before acting
- how to verify success with evidence
- how to avoid scope creep
- when to stop, pause, or ask for human approval

## Why this exists

Long-running agents fail when goals are vague, scope is unbounded, verification is delayed, or the agent keeps acting after it should stop. This skill encodes a stricter architecture for `/goal` prompts:

```text
mission -> preflight -> grounded strategy search -> risk policy -> success criteria -> evidence matrix -> execution loop -> memory -> budget gates -> stop state -> output
```

The core principle:

> Do not ask the agent to keep going. Ask it to keep reducing uncertainty with verified evidence inside a bounded risk envelope.

## What it creates

The skill can create:

- repo-specific `/goal` prompts
- Codex CLI mission prompts
- Claude Code long-running task prompts
- Hermes autonomous agent prompts
- software refactor and migration prompts
- product, research, data, and operations goal prompts
- prompt audits and rewrites
- compact, standard, and frontier-grade variants

## Repository contents

```text
goal-prompt-architect/
├── SKILL.md                         # ChatGPT Skill entrypoint
├── agents/
│   └── openai.yaml                  # ChatGPT skill UI metadata
├── references/
│   ├── frontier-template.md         # full advanced /goal architecture
│   ├── compact-template.md          # lightweight /goal template
│   └── domain-adaptations.md        # repo, regulated, research, data, ops variants
├── examples/
│   └── software-repo-goal.md        # example generated prompt
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

## Install as a ChatGPT Skill

1. Download or clone this repository.
2. Zip the skill folder so the archive contains `SKILL.md` at the skill root.
3. Upload the zip in ChatGPT's Skills interface.
4. Ask ChatGPT for a `/goal` prompt, for example:

```text
Create a frontier-grade /goal prompt for migrating our Next.js app from Pages Router to App Router without breaking auth or billing.
```

## Example use

```text
Create a /goal prompt for this repo: implement password reset end-to-end. It should inspect the repo first, avoid auth architecture rewrites, run tests, and stop before production changes.
```

The skill will produce a prompt with:

- a single measurable mission
- context inspection instructions
- grounded strategy search
- action classes and risk envelope
- success criteria
- an evidence matrix
- execution loop
- memory protocol
- verification commands
- terminal states
- final output contract

## Frontier template shape

```text
/goal

MISSION:
<one measurable durable objective>

PREFLIGHT:
<objective, observed context, strategies, evidence plan, risks, stop conditions>

GROUNDED STRATEGY SEARCH:
<up to 3 grounded candidate strategies with verification and rollback>

RISK + ACTION POLICY:
<allowed, rollback-required, approval-required, forbidden actions>

SUCCESS CRITERIA:
<measurable criteria>

EVIDENCE MATRIX:
<proof for each criterion>

EXECUTION LOOP:
observe -> orient -> decide -> act -> verify -> reflect -> compact -> continue/stop

MEMORY:
<working memory, episodic ledger, semantic mission memory>

BUDGET GATES:
<time, failures, touched files, tool calls, unresolved uncertainty, scope pressure>

STOP:
<done, unsafe, blocked, budget exhausted, needs human decision>

OUTPUT:
<summary, evidence, changed files, checks, risks, follow-ups>
```

