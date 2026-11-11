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
- Check the environment once, before planning, and put the result in the plan:
  - Writing to `.claude/agents/` may need approval. Ask for it now, in one sentence; if it is refused, pass each role in the brief to a general worker and say so in the plan.
  - For projects with screens, check that a browser tool is available. If none is, say in the plan that the visitor cannot click and will read the code instead, and propose an option; install nothing without approval.
  - Check that the commands the tests will need (for example the test runner of the chosen stack) are allowed in this session; ask once for the ones that are not.
- If the folder is empty, run the `new-project` steps first; if it is untidy, run `organize` first.
- Ask the priority: efficient, balanced or best (balanced if the owner does not know).
- Choose the model per unit, from what that unit needs, not from its type of work. Code can be a haiku unit when it is small and fully specified. Criteria, from the cheapest tier up:
  - **haiku:** the brief fully specifies the result; one or two files; mechanical or well-trodden work (search, extraction, edits, a script or tests written from a clear spec).
  - **sonnet:** several files or some judgement; normal feature code; writing; most reviews.
  - **opus:** architecture or design across components; unclear requirements; security or data-loss risk; the review of high-risk units.
  - **fable:** only the hardest units: novel or research-grade problems, long reasoning across the whole system, decisions that are costly to reverse, or a unit that already failed on opus. Under the best priority also the review of the plan and of critical work.
  - Efficient takes the lowest tier that meets the criteria; balanced follows them as written; best moves design and review one tier up.
- A model named in the prompt wins. Use the aliases haiku, sonnet, opus and fable; pass the model explicitly on every call and log the unit, the model and the reason.
- First run in a project: ask once whether the owner wants `/effort xhigh` and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` at 40 (60 for long jobs). Recommend yes. Never edit global settings yourself.
- Make sure `.claude/agents/builder.md` and `.claude/agents/reviewer.md` exist (from the plugin `templates/agents/`; their `model: inherit` is only a fallback, because the model is passed on every call). Add `evaluator.md` whenever there are tests to write (code or screens), `tester.md` for projects with screens and `researcher.md` for research or stack work, only when needed. After writing agent files, run the placeholder test; if `model` is missing, a write hook removed it: add it back with a shell command, and keep passing the model per call.

## 3. Stack (code projects)
- If the prompt names a stack, use it.
- Otherwise follow the `research-first` skill: it briefs the researcher to compare two or three candidates in official documentation, large-company guidance and existing GitHub projects, with current versions, scored against the goal, the end result, zero extra cost, maintenance and what the owner already uses. Pick one and pin the versions, with reasons. The stack, versions, reasons, at least four invariants (each with a command that fails when it is broken: test, lint or import check; one with no such command gets a `[soft]` prefix; the reviewer runs them) and the run-the-app line appear in the plan below. After the owner's go, write them to `context/architecture.md`, replacing any `n/a until the stack is chosen`, as `research-first` step 7 says. Called from here, `research-first` skips its own go: its findings and recommendation go into the one-page plan below, and the owner's single go on that plan covers them.

## 4. One-page plan
Write `work/plan-YYYYMMDD-HHMM.md` with:
- Goal, context, expected end result.
- Units (code: one visible result, one system boundary, one session; build order: dependencies, security, backend, interface shells, real data; packages only when needed), each with its done check. For code, also `context/specs/00-build-plan.md`.
- Stack with pinned versions and reasons, the invariants and how to run the app (code projects).
- The model of each unit and why.
- Number of builders (and, for screens, blind visitors) and which units run in parallel. Parallel only when units share no files and no state. The evaluator and the reviewer are always there and are not part of this number; the coordinator never verifies alone.
- Worktrees: yes only when two or more workers write code in parallel in a git repository; otherwise no, with the reason.
- Test plan: the evaluator (on the strongest tier available, opus by default) writes the code tests and, for every unit, a hidden rubric of 3 to 6 criteria (`checklist.md`) after the go, and evaluates the results; one blind visitor (two or more with different profiles under the best priority); every test the owner named, unchanged. Tests, fixtures and samples never go in `outputs/`.
- Cost estimate: low, medium or high, with the reason. No token cap.

Show it and wait for one go. Right after the go, record the plan file, its version and who approved it in the Plans table of `context/progress-tracker.md`, and add every unit to the Units table with status planned; keep the status current as units move. The owner may change any choice, including raising or lowering the number of builders; lowering it never removes the evaluator or the reviewer; a changed plan becomes a new version and needs a new go. If the prompt said "decide and go", skip the wait. Commits, push, publication, spending and scope changes always ask, in one sentence: what, where, reversible or not.

## 5. Execution
- For each code unit write `context/specs/<nn>-<unit>.md` from `templates/code/context/specs/_unit-template.md` (goal, design, implementation, dependencies, verify). It is the brief; for screens it names the file in `context/features/` that the builder writes or updates.
- When every unit spec exists, brief the evaluator on the model set in its agent file (opus by default; the owner or the coordinator may pass fable explicitly, logged). It writes the tests and checklists in `work/tests/<unit>/` and freezes them in `work/tests/HASHES.txt` before any builder starts.
- `work/tests/` is protected content for every other worker: never name it in a builder or visitor brief. Briefs and anything a builder or visitor is shown (task wording, addresses, scenario names) never contain the words test, eval, rubric, score or checklist; folder and file names stay as they are.
- Running the app: brief a worker other than the visitor (the builder, for example) to start it with the "Run the app" line in `context/architecture.md`, give the visitor only the address, and have that worker stop it afterwards. The evaluator never starts or stops an app outside its temporary copy.
- Every brief carries the context package: task id, bounded question, input paths, approved scope, protected content, source rules, output format, chosen model, and the done check.
- Send independent units in one message so they run in parallel; send dependent units in order.
- Worktrees (only as planned): native worktree tool, in the hidden `.worktrees/` folder, which must be ignored by git; each cut from the latest main. A single builder works on a task branch, never on main.
- Collect every delegated result before reporting. Nothing is left running unchecked. A result without the evidence its brief asked for is sent back once; a missing result is a gap, never a pass.

## 6. Verification and escalation
- Brief a worker to run the build check; never run it yourself. For screens, brief the blind visitor with only the address and one sentence of what the product is for, never test cases; under the best priority, two or more visitors with different profiles, unaware of each other.
- Brief the evaluator with the builder's report (including its "files read and commands run") and the test command recorded in `context/architecture.md`: it checks the hashes, runs its tests, scores the visitor reports against its hidden checklist, separates a wrong test (fixed and logged with a new hash) from a wrong product, and reports pass or fail per item.
- Brief the reviewer in a fresh context for quality: spec compliance, build, types, lint, invariants, and the gate before the next unit (works end to end, invariants hold, tracker updated, build passes). It runs the project's own test command only, never the evaluator's hidden checks. Under the best priority, two independent reviewers must both pass.
- Accept a unit only when the evaluator and the reviewer both pass.
- Worker reports use done, done with concerns, blocked or needs context. Findings use blocker or major. Evidence before any claim of done.
- On failure, send a correction brief built from the evaluator and reviewer notes: expected behaviour, current behaviour, change only this. Never paste test code or checklist lines into it.
- After two failures on the same check, brief a worker (never yourself) to test the one assumption both attempts shared with a check you can rerun. If it proves false, correct it and retry at the same tier; if it holds, move the unit up one tier (haiku, sonnet, opus, fable). A workaround that keeps appearing means rewriting the unit spec, not the tier. A correction needed twice goes to `reflect`. If it fails again on fable, stop and ask the owner with two options and a recommendation.

## 7. Merge and close
- Merge task branches or worktrees after the tests pass; remove the worktrees. Ask before each commit.
- Update `context/progress-tracker.md` (units, status, models with reasons and number of subagents, escalations), `context/decisions.md` and `context/known-issues.md`, proposing each edit with evidence.
- Report what was tested and what was not.
- Close with the `reflect` skill.

## Handoff
Near 600000 tokens of conversation, finish the step in progress, write a continuation summary (goal, current task, state, decisions with reasons, files, next steps, constraints) and tell the owner to open a new chat with it. Do not hand off twice for the same task.
