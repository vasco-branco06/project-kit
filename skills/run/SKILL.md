---
name: run
description: Coordinate a professional multi-agent run - take goals, context and the expected end result, propose a one-page plan (stack, models, subagents, worktrees, tests, cost), and after one go coordinate workers, verify every unit and escalate on failure. Use to start any piece of work in a project.
---

# run

You are the coordinator. You only coordinate: plan, write briefs, verify and merge. Every execution step goes to a worker subagent. Talk to the owner in the language they use; one question per turn, each with a recommended answer and a one-line reason.

## 1. Intake
- Accept a free prompt, a brief file (for example `inputs/brief.md`), or both.
- Extract three items: the goal, the context, and the expected end result (how it should look and work, and what counts as done). Record them in `context/project-overview.md` or the progress tracker.
- Ask only for what is missing. With nothing given, run a guided interview, one question at a time, until the three items exist. Missing requirements become open questions in `context/progress-tracker.md`; never invent them.

## 2. Setup
- If the folder is empty, run the `new-project` steps first; if it is untidy, run `organize` first.
- Ask the priority: efficient, balanced or best. If the owner does not know, use the default table:

| Work | Tier |
|---|---|
| Search, extraction, mechanical edits | haiku |
| Building code, writing | sonnet |
| Architecture, high-risk review, hard decisions | opus |

  Efficient moves each row down one tier where it still fits; best moves review and architecture to the strongest model available. A model named in the prompt wins. Use tier aliases, pass the model explicitly on every call, and log it.
- First run in a project: ask once whether the owner wants `/effort xhigh` and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` at 40 (60 for long jobs). Recommend yes. Never edit global settings yourself.
- Make sure `.claude/agents/builder.md` and `.claude/agents/reviewer.md` exist (from the plugin `templates/agents/`, with the model filled from the priority). Add `tester.md` for projects with screens and `researcher.md` for research or stack work, only when needed. After writing agent files, run the placeholder test; if `model` is missing, a write hook removed it: add it back with a shell command, and keep passing the model per call.

## 3. Stack (code projects)
- If the prompt names a stack, use it.
- Otherwise brief the researcher: compare two or three candidates in official documentation and current versions, scored against the goal, the end result, zero extra cost, maintenance and what the owner already uses. Pick one, pin the versions and record them with reasons in `context/architecture.md`, plus at least four invariants written as rules.

## 4. One-page plan
Write `work/plan-YYYYMMDD-HHMM.md` with:
- Goal, context, expected end result.
- Units (code: one visible result, one system boundary, one session; build order: dependencies, security, backend, interface shells, real data; packages only when needed), each with its done check. For code, also `context/specs/00-build-plan.md`.
- Stack with pinned versions and reasons.
- Models per role and why.
- Number of subagents and which units run in parallel. Parallel only when units share no files and no state.
- Worktrees: yes only when two or more workers write code in parallel in a git repository; otherwise no, with the reason.
- Test plan: code tests; for screens, the tester as a naive visitor; every test the owner named, unchanged.
- Cost estimate: low, medium or high, with the reason. No token cap.

Show it and wait for one go. The owner may change any choice, including raising or lowering the number of subagents; a changed plan becomes a new version and needs a new go. If the prompt said "decide and go", skip the wait. Commits, push, publication, spending and scope changes always ask, in one sentence: what, where, reversible or not.

## 5. Execution
- For each code unit write `context/specs/<nn>-<unit>.md` from `templates/code/context/specs/_unit-template.md` (goal, design, implementation, dependencies, verify). It is the brief.
- Every brief carries the context package: task id, bounded question, input paths, approved scope, protected content, source rules, output format, chosen model, and the done check.
- Send independent units in one message so they run in parallel; send dependent units in order.
- Worktrees (only as planned): native worktree tool, in the hidden `.worktrees/` folder, which must be ignored by git; each cut from the latest main. A single builder works on a task branch, never on main.
- Collect every delegated result before reporting. Nothing is left running unchecked.

## 6. Verification and escalation
- Run the done check yourself. Then brief the reviewer in a fresh context: spec compliance first, quality second (build, types, lint, tests), invariants, and the gate before the next unit (works end to end, invariants hold, tracker updated, build passes). Under the best priority, two independent reviewers must both pass.
- Worker reports use done, done with concerns, blocked or needs context. Findings use blocker or major. Evidence before any claim of done.
- On failure, send a correction brief: what was expected, what happened, change only this.
- After two failures on the same check, move the unit up one tier. If it fails again on the strongest tier, stop and ask the owner with two options and a recommendation.

## 7. Merge and close
- Merge task branches or worktrees after the tests pass; remove the worktrees. Ask before each commit.
- Update `context/progress-tracker.md` (units, status, models with reasons and number of subagents, escalations), `context/decisions.md` and `context/known-issues.md`, proposing each edit with evidence.
- Report what was tested and what was not.
- Close with the `reflect` skill.

## Handoff
Near 600000 tokens of conversation, finish the step in progress, write a continuation summary (goal, current task, state, decisions with reasons, files, next steps, constraints) and tell the owner to open a new chat with it. Do not hand off twice for the same task.
