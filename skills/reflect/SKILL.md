---
name: reflect
description: Close a work session or a finished task - classify corrections as general or project-specific and propose the smallest rule edit for general ones, applied only after approval.
---

# reflect

Talk to the owner in the language they use. Edit nothing before the owner approves.

## Steps

1. List what went wrong or took long in this session, and every correction made during the work.
2. Classify each item as general (it would recur in other projects: a missing rule, a vague template, a bad default) or specific (only this project). With nothing to propose, say so and stop.
3. Specific items go to `context/known-issues.md` of the project, as a proposed edit shown in full.
4. For each general item, propose the smallest edit to a kit rule or template that would have avoided it. Prefer removing an instruction to adding one. Show the exact edit and the evidence.
5. Wait for approval of each edit. Apply only what is approved. Add a dated line to `CHANGELOG.md` with the model name.
6. After a model swap, rerun the checks, edit only where they fail, and log it the same way.

## Rules

- Never apply an edit to the kit without approval.
- Specific errors never change the kit.
- Propose updates to the progress tracker, decision log and known issues with evidence, and wait for approval.
