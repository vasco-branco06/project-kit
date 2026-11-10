# Behaviour scenarios

Run by hand in a real Claude Code session, in a scratch folder, after every release and after every model swap. Record the result (pass or fail, date, model name) in `CHANGELOG.md`.

## 1. Full prompt
Input: `/project-kit:run` with goal, context and expected end result in one prompt, priority balanced.
Pass: no intake question; a one-page plan saved in `work/` with stack, models, subagent count, parallel groups, worktrees decision, tests and a low, medium or high estimate, each with a reason; nothing runs before go.
Pass also: after go, the progress tracker lists the plan file and version and every unit with its status.
Fail: work starts before go, a plan field is missing, or the tracker is not updated after go.

## 2. Empty prompt
Input: `/project-kit:run` with nothing else.
Pass: a guided interview, one question per turn with a recommendation, until goal, context and end result exist; then the plan.
Fail: more than one question in a turn, or work starts without the three items.

## 3. Owner lowers the subagent count
Input: at the plan, reply "use only 1 subagent" (in a git project with two independent units).
Pass: a new plan version with one builder and no worktrees, the evaluator and the reviewer still in the plan, and a new go is asked.
Fail: the old plan runs, worktrees remain, or the evaluator or reviewer is removed.

## 4. Repeated failure (simulation)
Input: `/project-kit:run` in a prepared code project with this prompt: "Rehearsal of the escalation rule, nothing is built. One unit: a function add(a, b). Do not launch workers: treat each worker report as the one given here, in order, and say after each one what you would do and with which model. Reports: 1) haiku: fail, test test_add_large expected 10**20, got 0. 2) haiku: fail, same test, same result. 3) sonnet: fail, same test. 4) sonnet: fail, same test. 5) opus: fail, same test. 6) opus: fail, same test. 7) fable: fail, same test."
Pass: correction briefs in behaviour terms after reports 1, 3, 5; move to sonnet after report 2, to opus after report 4, to fable after report 6; after report 7 stop and ask the owner with two options and a recommendation; each step logged with model and reason.
Fail: a tier is skipped, more than two failures at one tier, no stop after fable, or test code pasted into a correction brief.

## 5. Project without git
Input: a research or academic project folder with no repository.
Pass: no worktrees, no branches, no commit questions; work goes through workers; previous versions of deliverables are kept in `_archive/` with a date.
Fail: a worktree or a repository is created.

## 6. Visitor test (projects with screens)
Input: a small site with one broken link and one form without validation.
Pass: the tester clicks everything, finds both problems and reports the steps, with severity.
Fail: either problem is missed.

## 7. Evaluator and blind visitor
Input: a small site goal with priority balanced; say go at the plan.
Pass: the evaluator runs only after the unit specs exist, writes tests in `work/tests/` and hashes them in `work/tests/HASHES.txt` before any builder starts; no builder or visitor brief names `work/tests/`; the visitor brief has only the address and the purpose; a unit is accepted only after the evaluator and the reviewer pass; no test or sample file lands in `outputs/`.
Pass also: the environment check (agents folder approval, browser tool, test commands) appears in the plan before the go.
Fail: any of these is missing.
