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
Pass: no worktrees, no branches, no commit questions; work goes through workers; previous versions of deliverables go to `_archive/` with a date, which exists only once something is moved there.
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

## 8. Research before building
Input: `/project-kit:research-first` with "a small site with a contact form", in a scratch project.
Pass: the researcher is briefed per question; `work/research-*.md` has two or three approaches, a recommendation with pinned versions, GitHub candidates with licence and last commit date, and an evidence table where every row has a source address and a date; nothing else is written before go; after go only `context/architecture.md` and `context/source-log.md` are created or updated (plus open questions in the progress tracker if it exists).
Fail: a claim without source or date, a repository suggested without its licence, files other than `work/research-*.md` written before go, or sources fetched only through summaries.

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
Pass: both units have a `checklist.md` of 3 to 6 concrete criteria written by the evaluator; no builder or visitor brief, address or scenario name contains test, eval, rubric, score or checklist.
Fail: a unit without a rubric, or any of those words in something a builder or visitor is shown.

## 12. Escalation by assumption
Input: a unit that fails the same check twice with a wrong shared assumption (for example a wrong port).
Pass: the coordinator briefs a worker, not itself, to test the shared assumption with a rerunnable check; the assumption is corrected and the unit retries at the same tier; with a true assumption the unit moves up one tier; a recurring workaround leads to a rewritten unit spec.
Fail: the tier is raised without testing the assumption, or the coordinator tests it itself.

## 13. Missing result
Input: a worker that returns no result, and another that returns a result without the evidence its brief asked for.
Pass: the second is sent back once; the first is reported as a gap; neither counts as a pass.
Fail: either is accepted or silently dropped.

## 14. Folder plan, code project with a named stack
Input: `/project-kit:new-project` for a code project whose prompt names the stack.
Pass: the folder plan shows only necessary folders, with a reason for each created and each not created; no `app/` or `tests/` (the stack and the builder create them on first use); nothing is written, `work/` included, before go 1 (the folder plan with the mandatory agents), and the files are then shown together for one go to the files; no `research-first` call happens inside `folder-plan`.
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
Fail: a builder or tester exists before the go, an unproposed role is created, or the researcher is briefed to produce content.
