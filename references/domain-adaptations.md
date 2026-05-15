# Domain Adaptations

Use these sections to adapt the frontier template.

## Software Repository / Coding Agent

Add:

```text
WORKTREE PROTOCOL:
- inspect git status before changes
- preserve unrelated dirty files
- make small PR-reviewable diffs
- inspect neighboring files and tests before editing
- follow repository agent instructions such as AGENTS.md, CONTRIBUTING.md, SECURITY.md
- run narrow tests before repo-wide validation
- do not mark DONE with accidental unrelated changes

REPO NAVIGATION:
Start with:
1. README / AGENTS / CONTRIBUTING / SECURITY docs
2. package/build/test manifests
3. route/API entrypoints
4. domain models and migrations
5. existing tests and fixtures
6. neighboring implementation patterns

LOCAL SCHEMA POLICY:
Local/dev migrations are allowed only if:
- migration pattern already exists
- change is additive or reversible
- no production migration is run
- rollback notes are included
- dry-run/local validation is used where available
```

Typical approval-required actions:
- production deploys
- production migrations
- secrets or credential handling
- auth/security/billing/payment changes
- destructive deletes
- broad dependency upgrades
- public exposure changes

## Regulated / Clinical / Legal / Financial Work

Add stricter boundaries:

```text
REGULATED BOUNDARIES:
- use synthetic or approved test data only
- do not use real customer/patient/client data unless explicitly authorized
- do not create diagnosis, legal advice, financial advice, or risk classification beyond the approved scope
- preserve auditability and human-review requirements
- stop before compliance-significant changes
```

## Research / Analysis

Add:

```text
RESEARCH PROTOCOL:
- define research question and decision the research supports
- separate verified facts, interpretations, and hypotheses
- cite sources or files for every non-obvious claim
- rank uncertainty and evidence quality
- stop when evidence is sufficient for the requested decision, not when the topic is exhausted
```

## Data / Spreadsheet / Batch Processing

Add:

```text
DATA PROTOCOL:
- preserve original input data
- create a reversible output artifact
- document transformations
- validate row counts, schema, missing values, duplicates, and outliers as relevant
- never overwrite source files unless explicitly requested
```

## Operations / Business Workflow

Add:

```text
OPERATIONS PROTOCOL:
- define the exact operational outcome
- identify systems touched and permission boundaries
- separate draft recommendations from actions that change live systems
- record decisions, assumptions, and handoff notes
- stop before sending, publishing, deleting, purchasing, or changing external systems unless authorized
```
