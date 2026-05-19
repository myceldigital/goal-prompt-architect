# Adversarial Verification Module

Use this module when a goal could be falsely completed by weakening tests, deleting assertions, mocking away behavior, changing the public surface, or relying on subjective self-assessment.

```text
ADVERSARIAL VERIFICATION:
Before finalizing DONE, run a red-team pass on the success criteria:
- How could an agent satisfy the letter of the goal while violating the intent?
- Could it delete, mute, or weaken tests?
- Could it mock away real behavior instead of implementing it?
- Could it alter public APIs or callers to make the task easier?
- Could it claim success from console output without durable artifacts?

Anti-sandbagging gates:
- Do not delete, comment out, or weaken existing test cases or assertions unless explicitly scoped and justified.
- Do not add skip markers, focus-only tests, or broad mocks to bypass behavior.
- Do not change public API signatures or external behavior unless the mission explicitly requires it.
- Do not mark DONE from self-assessment alone; map each success criterion to reproducible evidence.
- Run or reference `.agent/verify_step.py --target git_delta` when local git history is available.

If an anti-sandbagging gate conflicts with the mission, stop with NEEDS HUMAN DECISION and explain the conflict.
```
