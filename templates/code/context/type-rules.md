# Type rules: code

Applies to apps, sites, scripts, data and machine learning, and system architecture.

## Branches
- Never work on the main branch. Each task gets its own branch (or a worktree in `.worktrees/`) cut from the latest main.
- Only the coordinator merges, after the tests pass. Nobody writes another session checkout.
- The first commit of a new repository is the only exception. Ask the owner before any commit.

## Stack
- Define the stack before any code and record it in `architecture.md`. Versions are pinned and checked against the official documentation of each tool.

## Tests
- Before work on a task starts, the coordinator writes the test plan: code tests for the logic and, when there are screens, a simulated user that opens the app or site and clicks through the main flows with the browser tool already available. Add every test the owner names, unchanged. Each test has a pass and a fail outcome. Run every test before accepting the task.
- Do not install a test tool without the owner approval.

## Specification
- For a larger build, suggest the interview plugin (`/ite:start`) to produce the specification network.
