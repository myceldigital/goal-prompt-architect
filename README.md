Most people use /goal wrong.

They write: `make no mistakes`.

Goal Prompt Architect turns `/goal` into an execution contract:

- mission
- risk envelope
- grounded strategy search
- evidence matrix
- memory loop
- stop rules
- verification oracle
- persistent state for marathon work

Agent Skill for Codex, Claude Code, Hermes, and long-running AI agents.

# Goal Prompt Architect

**An agent Skill and toolkit for creating, linting, and improving `/goal` prompts for Codex, Claude Code, Hermes, and long-running autonomous AI agents.**

Goal Prompt Architect turns vague task ideas into mission-grade execution contracts: measurable outcomes, grounded strategy search, risk boundaries, action classification, verification evidence, memory discipline, budget gates, and clean stop conditions.

The core principle:

> Do not ask the agent to keep going. Ask it to keep reducing uncertainty with verified evidence inside a bounded risk envelope.

## What this repository now contains

```text
goal-prompt-architect/
├── SKILL.md                         # ChatGPT Skill entrypoint
├── agents/
│   └── openai.yaml                  # ChatGPT skill UI metadata
├── references/
│   ├── frontier-template.md         # advanced /goal architecture
│   ├── compact-template.md          # lightweight /goal template
│   ├── marathon-template.md         # long-horizon autonomous mission template
│   ├── domain-adaptations.md        # repo, regulated, research, data, ops variants
│   ├── modules/                     # reusable high-leverage prompt modules
│   └── playbooks/                   # recurring mission playbooks
├── tools/
│   └── lint_goal.py                 # dependency-free /goal prompt linter
├── schemas/
│   ├── goal-contract.schema.json
│   ├── evidence-matrix.schema.json
│   └── risk-policy.schema.json
├── examples/
│   ├── good/                        # passing lint fixtures
│   └── bad/                         # failing anti-pattern fixtures
├── tests/
│   └── test_lint_goal.py            # linter regression tests
├── pyproject.toml
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

## What it creates

The skill can create:

- repo-specific `/goal` prompts
- Codex CLI mission prompts
- Claude Code long-running task prompts
- Hermes autonomous agent prompts
- software refactor and migration prompts
- marathon prompts for multi-hour or multi-day work
- product, research, data, and operations goal prompts
- prompt audits and rewrites
- compact, frontier, and marathon variants

## Toolkit quick start

Run the linter against strong examples:

```bash
python tools/lint_goal.py examples/good/frontier-repo-goal.md
python tools/lint_goal.py --mode marathon examples/good/marathon-repo-goal.md
```

Run the regression tests:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

Emit machine-readable linter output:

```bash
python tools/lint_goal.py --json examples/good/frontier-repo-goal.md
```

The linter exits with status `0` when every prompt passes and `1` when any prompt fails.

## Lint dimensions

The linter scores prompts across:

1. `/goal` prefix
2. mission singularity
3. measurable success criteria
4. contract completeness
5. evidence matrix
6. risk policy
7. verification oracle
8. stop conditions
9. anti-pattern detection
10. marathon protocol and durable memory, when applicable

## Prompt modes

- **Compact**: low-risk, narrow, short-lived tasks where a concise execution contract is enough.
- **Frontier**: complex or high-risk single-session tasks that need strategy search, evidence mapping, risk controls, and strong stopping conditions.
- **Marathon**: long-horizon tasks intended to run for many cycles, hours, or days with persistent state, soft/hard blocker handling, failure recovery, phase gates, and quality ratchets.

## Design standard

A goal should be rejected if it relies on motivational language instead of operational evidence. Examples of anti-patterns include:

- `make no mistakes`
- `make it perfect`
- `do whatever it takes`
- `use every tool`
- `keep going until everything is fixed`
- `skip tests`

## Install as a ChatGPT Skill

1. Download or clone this repository.
2. Zip the skill folder so the archive contains `SKILL.md` at the skill root.
3. Upload the zip in ChatGPT's Skills interface.
4. Ask ChatGPT for a `/goal` prompt, for example:

```text
Create a marathon-grade /goal prompt for migrating our Next.js app from Pages Router to App Router without breaking auth or billing.
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

## Future extensions

The current linter is intentionally heuristic and dependency-free. The next frontier is a compiler that converts structured goal contracts into compact, frontier, and marathon prompts, validates them against the JSON schemas, and benchmarks generated goals against known weak/strong fixtures.
