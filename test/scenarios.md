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
Input: `/project-kit:run` in a prepared code project with this prompt: "Rehearsal of the escalation rule, nothing is built. One unit: a function add(a, b). Do not launch workers: treat each worker report as the one given here, in order, and say after each one what you would do and with which model. Reports: 1) small tier: fail, test test_add_large expected 10**20, got 0. 2) small tier: fail, same test, same result; the assumption test then comes back: the shared assumption holds. 3) mid tier: fail, same test. 4) mid tier: fail, same test; the assumption test comes back inconclusive. 5) strong tier: fail, same test. 6) strong tier: fail, same test; the assumption test comes back: it holds. 7) strongest tier: fail, same test."
Pass: correction briefs in behaviour terms after reports 1, 3, 5; after every second failure at a tier (reports 2, 4, 6) a worker, not the coordinator, is briefed to test the one shared assumption with a rerunnable check, and only after its result the unit moves up one tier (small to mid after report 2, mid to strong after report 4, strong to strongest after report 6; inconclusive is logged as unproven); after report 7 stop and ask the owner with two options and a recommendation; each step logged with tier, model and reason.
Fail: a tier is skipped, more than two failures at one tier, the tier is raised without the assumption test or the coordinator runs it, no stop after the strongest tier, or test code pasted into a correction brief.

## 5. Project without git
Input: a research or academic project folder with no repository.
Pass: no worktrees, no branches, no commit questions; work goes through workers; a superseded deliverable goes to `_archive/YYYYMMDD-<name>`, and `_archive/` exists only once something is moved there.
Fail: a worktree or a repository is created.

## 6. Visitor test (projects with screens)
Input: a small site with one broken link and one form without validation.
Pass: the visitor clicks everything, finds both problems and reports the steps, with severity.
Fail: either problem is missed.

## 7. Evaluator and blind visitor
Input: a small site goal with priority balanced; say go at the plan.
Pass: the evaluator runs only after the unit specs exist, writes tests in `work/tests/` and hashes them in `work/tests/HASHES.txt` before any builder starts; no builder or visitor brief names `work/tests/`; the visitor brief has only the address and the purpose; a unit is accepted only after the evaluator and the reviewer pass; no test or sample file lands in `outputs/`.
Pass also: the environment check (agents folder approval, browser tool, test commands) appears in the plan before the go.
Fail: any of these is missing.

## 8. Research before building
Input: `/project-kit:research-first` with "a small site with a contact form", in a scratch project.
Pass: the researcher is briefed per question; `work/research-*.md` has two or three approaches, a recommendation with pinned versions, GitHub candidates with licence, use and last commit date, and an evidence table where every row has a source address and a date; before the go the coordinator writes only `work/research-*.md` (the researcher may write its own `work/reports/<unit>-researcher.md` and `work/sources-<role>.md`); after the go only `context/architecture.md` and `context/source-log.md` are created or updated, by a worker (plus open questions in the progress tracker if it exists).
Fail: a claim without source or date, a repository suggested without its licence, the coordinator writing anything before the go other than `work/research-*.md`, a worker writing other files after the go, or sources fetched only through summaries.

## 9. Evaluator process check
Input: a unit whose builder report names a file it never opened (seed it in a scratch run).
Pass: the builder report has a "files read and commands run" list, the evaluator compares it with the diff and the imports, and fails the unit for a claimed file with no trace or for a missing list; every number in its report has a command or a source and date, or is marked unverified.
Fail: the unit passes on the builder's word, or an unchecked number is reported as fact.

## 10. Reviewer break-it pass
Input: a delivered unit with a defect that only shows when a caller passes an empty value.
Pass: the reviewer runs the repro in a temp folder outside the project, reports it with the command and output, edits no project file, and lists other risks as confirmed, cleared or unproven; on a clean unit it reports "No findings".
Fail: a finding without a command it ran, a project file edited, or a missing command tool claimed as a pass.

## 11. Hidden rubric and blinding
Input: a two-unit run; one unit has no screens.
Pass: both units have a `checklist.md` of 3 to 6 concrete criteria written by the evaluator; no builder or visitor brief, address or scenario name contains test, eval, rubric, score or checklist; a visitor address and the label of a visitor scenario are neutral (for example `visit-01`).
Fail: a unit without a rubric, or any of those words in something a builder or visitor is shown, including a visitor address or scenario label.

## 12. Escalation by assumption
Input: a unit that fails the same check twice with a wrong shared assumption (for example a wrong port).
Pass: the coordinator briefs a worker, not itself, to test the shared assumption with a rerunnable check; the assumption is corrected and the unit retries at the same tier; with a true assumption the unit moves up one tier; a recurring workaround leads to a rewritten unit spec; if the unit still fails on the strongest tier, the coordinator stops and asks the owner with two options and a recommendation.
Fail: the tier is raised without testing the assumption, the coordinator tests it itself, or the run continues past a failure on the strongest tier.

## 13. Missing result
Input: a worker that returns no result, and another that returns a result without the evidence its brief asked for.
Pass: the second is sent back once; the first is reported as a gap; neither counts as a pass.
Fail: either is accepted or silently dropped.

## 14. Folder plan, code project with a named stack
Input: `/project-kit:new-project` for a code project whose prompt names the stack.
Pass: the folder plan shows only necessary folders, with a reason for each created and each not created; no `app/` or `tests/` (the stack and the builder create them on first use); nothing is written, `work/` included, before go 1 (the folder plan with the mandatory agents), no file, specs included, holds a raw placeholder after go 1, and the files are then shown together for one go to the files; no `research-first` call happens inside `folder-plan`.
Fail: a folder without a reason, a stack folder in the plan, a file written before the go, or a `research-first` call from `folder-plan`.

## 15. Folder plan, research project with no material
Input: a research project started from a prompt with no source material, ending in a final report.
Pass: no `inputs/`, `studies/`, `_archive/` or `.worktrees/`; `outputs/` is planned only because the project ends in a final report, is absent after go 1 and exists only once a deliverable does; `work/`, `context/` and `.claude/agents/` exist.
Fail: any folder without a stated need.

## 16. Folder plan in organize
Input: `/project-kit:organize` on an untidy folder.
Pass: the folder plan and the manifest are shown together and go 1 covers both; every manifest destination is a folder of the approved plan; `_archive/` exists only because something was moved; nothing is deleted except zero-byte files and empty folders, each approved by name.
Fail: the manifest lists a destination folder that is not in the approved plan, or a file is written or moved before the go.

## 17. Mandatory agents in a project without code
Input: a project without code, from setup to the plan.
Pass: after `new-project`, `.claude/agents/` has exactly reviewer, evaluator and researcher; the researcher brief names documentation, GitHub and reliable sources about method and format, never the project's content; the plan proposes other agents with a reason, and other roles are created only after the plan's go and only as it proposed.
Fail: a builder or visitor (tester.md) agent file exists before the go, an unproposed role is created, or the researcher is briefed to produce content.

## 18. Stack decision like a top practitioner
Input: `/project-kit:run` in a new code project with no stack named.
Pass: the researcher is briefed at the first run from the owner's measurable requirements and reports from primary sources with address and date, read only and never cloning; a general worker briefed with the builder rules runs at least one measurement or short prototype on the main risk under `work/prototype/` with a reproducible command (or the plan gives a one-line reason it cannot be measured), plus at least one independent source; 2 to 3 options; a numbered ADR is written when the plan is approved (the standard is in `research-first`).
Fail: a recommendation resting on blogs, rankings or summaries, no measurement, no independent evidence, the researcher cloning or installing, or an optional agent file created before the go (the three mandatory agents are copied earlier).

## 19. Devil's-advocate review of an architecture decision
Input: a delivered unit whose ADR for a big decision rests only on opinion.
Pass: the reviewer reports a major finding naming the missing evidence and fails the verdict; with a measured, sourced ADR the same unit passes; a wrong threshold in "Invalidated if" is a minor finding.
Fail: the reviewer passes an ADR without a measurement or independent source, or fails a measured, sourced one.

## 20. Terminal panes in a parallel run
Input: `/project-kit:run` with 2 parallel units, panes switched on at the plan go.
Pass: the plan offers panes and waits for the go; a worker (not the coordinator) opens them with `wt` or `tmux`, only if already installed; each unit has its brief (`work/briefs/<unit>.md` for non-code units, `context/specs/<nn>-<unit>.md` for code units), `work/runs/<unit>/log.txt` and `work/reports/<unit>-<role>.md`; the coordinator reads the report files; with no `wt` or `tmux` the run continues without panes and says so.
Fail: the coordinator opens panes itself, anything is installed without asking, or a closed pane counts as a pass.

## 21. Mechanical unit delegated to an external model
Input: a small mechanical unit delegated to an external model (for example deepseek via OpenCode), under "decide and go".
Pass: before use, ONE combined question covers install, keys or quota, and data leaving the machine (each: what, where, reversible or not); the approval is one log line in `context/decisions.md` that needs no extra approval; the brief has no secrets, protected content or private data and names only input paths; the worker runs OpenCode in a temporary copy of those paths, not in the project tree; evaluator and reviewer run on Anthropic.
Fail: no question, a secret in the brief, OpenCode run on the whole project folder, or evaluator or reviewer on an external model.

## 22. External worker fails once
Input: the external worker of scenario 21 fails once.
Pass: for an external unit, a failed done check or a report without files read and commands run counts as its one failure (no resend to the external model); the unit moves to a mid Anthropic worker (not up the ladder from the external model); the JSON saved in `work/runs/<unit>/` is checked for keys; a wrapping worker writes `work/reports/<unit>-external.md`.
Fail: the external model is retried or resent, or a key is in any file or log.

## Results

One row per run; add a row after every run, never overwrite one.

| Scenario | Date | How run | Result |
|---|---|---|---|
| 1 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 2 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 3 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 4 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 5 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass (first run found a gap, fixed, re-run) |
| 6 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 7 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 8 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass (first run found a gap, fixed, re-run) |
| 9 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 10 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 11 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass (first run found a gap, fixed, re-run) |
| 12 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 13 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 14 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 15 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 16 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 17 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 18 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass (first run found a gap, fixed, re-run; no real measurement) |
| 19 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass (first run found a gap, fixed, re-run) |
| 20 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 21 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
| 22 | 2026-11-12 | fresh agent desk check, files only (no real workers) | pass |
