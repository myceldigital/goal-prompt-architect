# Security Policy

Goal Prompt Architect is a prompt/template skill and should not contain secrets, credentials, production data, customer data, or private proprietary material.

## Reporting a vulnerability

If you find a security issue in this repository, open a GitHub issue or contact the maintainers privately if the issue involves sensitive material.

## Boundaries for examples

Examples should not include:

- real API keys or tokens
- production hostnames that imply access instructions
- private customer, patient, client, or employee data
- exploit instructions
- instructions to bypass approvals, sandboxes, or security controls

## Prompt safety principles

The templates in this repo should encourage:

- least-privilege agent behavior
- explicit approval gates for production and external side effects
- synthetic or approved test data
- clear rollback plans
- human review for high-impact ambiguity
- stopping before destructive, irreversible, or unauthorized actions
