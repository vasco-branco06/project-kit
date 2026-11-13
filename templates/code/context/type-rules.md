# Type rules: code

Applies to apps, sites, scripts, data and machine learning, and system architecture.

## Branches and worktrees
- Never work on the main branch. Each task gets its own branch cut from the latest main.
- Worktrees only when two or more workers write code in parallel in a git repository: the native worktree tool, in `.worktrees/` (check it is ignored by git), each from the latest main. The coordinator merges after the tests pass and removes the worktrees. Research, review and single-builder work never get worktrees.
- Only the coordinator merges. Nobody writes another session checkout. Ask the owner before any commit; the first commit of a new repository included.

## Stack
- If the owner names a stack, use it. Otherwise the choice follows the Decision standard of the plugin skill `research-first`: researched from primary sources, measured, recorded as an ADR in `decisions.md`, with pinned versions and a reason for each in `architecture.md`.

## Units and specs
- Each unit has a spec in `context/specs/` made from `context/specs/_unit-template.md` (the one file that keeps its placeholders); the build plan lives in `context/specs/00-build-plan.md`.

## Tests (evaluator and coordinator; never named in a builder brief)
- The evaluator, hash freeze and blind visitor rules are stated once in `CLAUDE.md` (worker reports line), and the evidence rules in `.claude/agents/evaluator.md` and section 6 of the `run` skill; they are not repeated here.
- Each evaluator test has a pass and a fail outcome. The builder may write its own tests in the code folders, never in `outputs/`.
- A failing test is rerun; if the test is wrong, the evaluator fixes it and logs the reason and the new hash.
- The reviewer checks build, types, lint and tests with the commands recorded in `architecture.md`.
- Do not install a test tool without the owner approval.
- Sites and apps only: keep one file per user-facing feature in `context/features/`, with four headings: sub-features, how a user reaches it, how to drive it (action, exact command, observable result), traps. The unit that creates a feature writes its file and a unit that changes it updates the file in the same unit; the brief names the file (a write covered by the plan go, as listed in section 7 of the `run` skill). The evaluator builds checklists from these files, never from one convenient entry point.

## Specification
- For a larger build, suggest the interview plugin (`/ite:start`) to produce a specification network.
