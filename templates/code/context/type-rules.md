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
- After the plan and the unit specs are final, the evaluator (strongest model) writes the code tests and, when there are screens, a hidden checklist of expected behaviours, adds every test the owner named unchanged, and freezes them by hash in `work/tests/` before any build. Each test has a pass and a fail outcome.
- The builder never sees the evaluator tests; it may write its own tests in the code folders, never in `outputs/`.
- For screens, one blind visitor (two or more with different profiles under the best priority) gets only the address and the purpose of the product, clicks everything and tries to break it with the browser tool already available; the evaluator scores its report against the hidden checklist.
- A failing test is rerun; if the test is wrong, the evaluator fixes it and logs the reason and the new hash.
- The reviewer checks build, types, lint and tests with the commands recorded in `architecture.md`.
- Do not install a test tool without the owner approval.

## Specification
- For a larger build, suggest the interview plugin (`/ite:start`) to produce a specification network.
