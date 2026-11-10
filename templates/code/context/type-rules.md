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
- Before a unit starts, the coordinator writes its tests: code tests for the logic and, when there are screens, the tester acting as a visitor who understands nothing, clicking everything and trying to break the product with the browser tool already available. Every test the owner names is added unchanged. Each test has a pass and a fail outcome and runs before the unit is accepted.
- The reviewer checks build, types, lint and tests with the commands recorded in `architecture.md`.
- Do not install a test tool without the owner approval.

## Specification
- For a larger build, suggest the interview plugin (`/ite:start`) to produce a specification network.
