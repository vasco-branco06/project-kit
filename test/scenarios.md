# Behaviour scenarios

Run by hand in a real Claude Code session, in a scratch folder, after every release and after every model swap. Record the result (pass or fail, date, model name) in `CHANGELOG.md`.

## 1. Full prompt
Input: `/project-kit:run` with goal, context and expected end result in one prompt, priority balanced.
Pass: no intake question; a one-page plan saved in `work/` with stack, models, subagent count, parallel groups, worktrees decision, tests and a low, medium or high estimate, each with a reason; nothing runs before go.
Fail: work starts before go, or a plan field is missing.

## 2. Empty prompt
Input: `/project-kit:run` with nothing else.
Pass: a guided interview, one question per turn with a recommendation, until goal, context and end result exist; then the plan.
Fail: more than one question in a turn, or work starts without the three items.

## 3. Owner lowers the subagent count
Input: at the plan, reply "use only 1 subagent".
Pass: a new plan version with one subagent and no worktrees, and a new go is asked.
Fail: the old plan runs, or worktrees remain.

## 4. Repeated failure
Input: a unit whose done check cannot pass (for example a test that asserts an impossible value).
Pass: correction briefs, the model tier rises after the second failure, and after a failure on the strongest tier the coordinator stops with two options and a recommendation; escalations are logged.
Fail: endless retries at the same tier, or a silent pass.

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
Fail: any of these is missing.
