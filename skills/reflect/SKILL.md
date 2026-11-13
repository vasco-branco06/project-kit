---
name: reflect
description: Use at the end of a session or a finished run, or after a model swap - classify corrections as general or project-specific, propose the smallest rule edit for general ones and, with approval, apply it to the kit itself. Nothing changes without approval.
---

# reflect

Talk to the owner in the language they use. Edit nothing before the owner approves, except `work/kit-improvements.md` and the progress tracker.

## Steps

1. List what went wrong or took long in this session, every correction made during the work, and every escalation in the progress tracker.
2. Classify each item as general (it would recur in other projects: a missing rule, a vague template, a bad default) or specific (only this project). With nothing to propose, say so, update the tracker (step 7) and stop.
3. Specific items: propose the edit to `context/known-issues.md`, shown in full.
4. General items: write each proposal to `work/kit-improvements.md` with the evidence and the exact edit to a kit rule, template or skill. Fix at the highest level that works: remove an instruction, then add an automated check to `test/check_kit.py` (like its agent model-line check) whose error names the fix, then a test, and a sentence or docs last; a mistake that happened twice is a class and gets the same treatment.
5. Ask approval for each proposal, then, as a separate question, the path of the owner's git clone of the plugin. Without a clone the proposals stay in `work/kit-improvements.md` and nothing is applied. With approval and a clone, apply the edit to that clone, never to the installed cache (a plugin update overwrites it), run `python -I "<clone>/test/check_kit.py" --self-test` (the cache copy `${CLAUDE_PLUGIN_ROOT}/test/check_kit.py` only checks the installed version), and add a dated line to the plugin `CHANGELOG.md` in the clone with the model name.
6. Ask a second, separate approval before any commit or push of the plugin, in one sentence: what, where, reversible or not. Users get the change with `/plugin update`.
7. Update the progress tracker without waiting (see section 7 of the `run` skill); propose the edits to the decision log of the project with evidence, and wait for approval (the known issues are step 3).
8. After a model swap, rerun the checks and the scenarios in `<clone>/test/scenarios.md`, edit only where they fail, and log it the same way.

## Rules

- Never apply or push an edit to the kit without approval.
- Specific errors never change the kit.
