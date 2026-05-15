# Contributing

Thanks for helping improve Goal Prompt Architect.

## Good contributions

Useful contributions include:

- stronger `/goal` templates
- examples for real coding-agent workflows
- domain adaptations for research, product, data, operations, regulated work, or security-sensitive work
- clearer stop rules and verification patterns
- prompt audits showing before/after improvements
- compatibility notes for Codex, Claude Code, Hermes, or other agent systems

## Design principles

Contributions should preserve the core philosophy:

1. One mission only.
2. Success criteria must be measurable.
3. Every success criterion needs an evidence path.
4. Autonomy must be bounded by a risk envelope.
5. Agents should reduce uncertainty, not just keep acting.
6. Stop rules are as important as action rules.
7. Templates should be useful in real repositories, not just theoretically elegant.

## Pull request checklist

Before opening a PR, check that your change:

- keeps `SKILL.md` concise enough to load efficiently
- moves long reusable material into `references/`
- avoids fake claims about official support in specific tools
- avoids unverifiable hype
- includes examples where helpful
- does not add secrets, private data, or proprietary content
- preserves the skill directory layout

## Style

Use clear, direct language. Prefer concrete prompt blocks over abstract explanations. Avoid bloated prompt sections that make the resulting `/goal` unusable in practice.
