# Type rules: code

Applies to apps, sites, scripts, data and machine learning, and system architecture.

## Branches and worktrees
- Never work on the main branch. Each task gets its own branch cut from the latest main.
- Worktrees only when two or more workers write code in parallel in a git repository: the native worktree tool, in `.worktrees/` (check it is ignored by git), each from the latest main. The coordinator merges after the tests pass and removes the worktrees. Research, review and single-builder work never get worktrees.
- Only the coordinator merges. Nobody writes another session checkout. Ask the owner before any commit; the first commit of a new repository included.

## Stack
- If the owner names a stack, use it. Otherwise a researcher compares two or three candidates in official documentation and current versions, against the goal, the end result, zero extra cost, maintenance and what the owner already uses. Record the choice in `architecture.md` with pinned versions and a reason for each.

## Units and specs
- Each unit has a spec in `specs/` made from `specs/_unit-template.md`; the build plan lives in `specs/00-build-plan.md`.

## Tests
- After the plan and the unit specs are final, the evaluator (strongest tier) writes the code tests and, for every unit, a hidden rubric of 3 to 6 criteria (`checklist.md`), adds every test the owner named unchanged, and freezes them by hash in `work/tests/` before any build. Each test has a pass and a fail outcome.
- The builder never sees the evaluator tests; it may write its own tests in the code folders, never in `outputs/`.
- For screens, one blind visitor (two or more with different profiles under the best priority) gets only the address and the purpose of the product, clicks everything and tries to break it with the browser tool already available; the evaluator scores its report against the hidden checklist.
- A failing test is rerun; if the test is wrong, the evaluator fixes it and logs the reason and the new hash.
- The reviewer checks build, types, lint and tests with the commands recorded in `architecture.md`.
- Do not install a test tool without the owner approval.
- Each visitor saves screenshots and outputs in `work/evidence-incoming/<unit>/` and names them in its report; the evaluator moves them, with its own command outputs and exit codes, to `work/tests/<unit>/evidence/` and checks they still exist after cleanup, which removes instances and scratch files, never evidence.
- Sites and apps only: keep one file per user-facing feature in `context/features/`, with four headings: sub-features, how a user reaches it, how to drive it (action, exact command, observable result), traps. The unit that creates a feature writes its file and a unit that changes it updates the file in the same unit; the brief names the file. The evaluator builds checklists from these files, never from one convenient entry point.

## Specification
- For a larger build, suggest the interview plugin (`/ite:start`) to produce a specification network.
