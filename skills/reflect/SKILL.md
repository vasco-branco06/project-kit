---
name: reflect
description: Close a work session or a finished run - classify corrections as general or project-specific, propose the smallest rule edit for general ones and, with approval, apply it to the kit itself. Nothing changes without approval.
---

# reflect

Talk to the owner in the language they use. Edit nothing before the owner approves.

## Steps

1. List what went wrong or took long in this session, every correction made during the work, and every escalation in the progress tracker.
2. Classify each item as general (it would recur in other projects: a missing rule, a vague template, a bad default) or specific (only this project). With nothing to propose, say so and stop.
3. Specific items: propose the edit to `context/known-issues.md`, shown in full.
4. General items: write each proposal to `work/kit-improvements.md` with the evidence and the exact edit to a kit rule, template or skill. Prefer removing an instruction to adding one.
5. Ask approval for each proposal. With approval, apply it to the local copy of the plugin repository, run `python -I "${CLAUDE_PLUGIN_ROOT}/test/check_kit.py" --self-test`, and add a dated line to the plugin `CHANGELOG.md` with the model name.
6. Ask a second, separate approval before any commit or push of the plugin, in one sentence: what, where, reversible or not. Users get the change with `/plugin update`.
7. Propose the updates to the progress tracker, the decision log and the known issues of the project, with evidence, and wait for approval.
8. After a model swap, rerun the checks and the scenarios in the plugin `test/scenarios.md`, edit only where they fail, and log it the same way.

## Rules

- Never apply or push an edit to the kit without approval.
- Specific errors never change the kit.
