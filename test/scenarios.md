# Behaviour scenarios

Run after every release and after every model swap, in a scratch folder. Record the result (pass or fail, date, model name) in `CHANGELOG.md` and as a row in Results.

What counts as a run: a **desk check** is a fresh agent that reads the kit files and says what the kit makes the coordinator do; a **real session** is a Claude Code session in a scratch folder where the scenario is carried out and the folder and the transcript are inspected. A desk check can judge the wording of a clause but not what happened, so scenarios 1, 6, 7, 9, 10, 13, 18, 20, 21 and 22 (their Pass names an order of events, files written, commands run or a tool used) count as passed only after a real session; the other scenarios may be passed by a desk check. Results says which kind each row was.

A scenario fails when any Pass clause is not met or any Fail clause applies; the Fail line lists the usual ways, not the only ones.

## 1. Full prompt
Input: `/project-kit:run` with goal, context and expected end result in one prompt, priority balanced.
Pass: no intake question; a one-page plan saved in `work/` with stack, models, subagent count, parallel groups, worktrees decision, tests and a low, medium or high estimate, each with a reason; nothing runs before go.
Pass also: after go, the progress tracker lists the plan file and version and every unit with its status.
Fail: work starts before go, a plan field is missing, or the tracker is not updated after go.

## 2. Empty prompt
Input: `/project-kit:run` with nothing else, in an empty scratch folder.
Pass: a guided interview, one question per turn with a recommendation (the `new-project` questions run first and count), until goal, context and end result exist; then the plan.
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
Input: a research or academic project folder with no repository, holding a deliverable that the run replaces with a new version.
Pass: no worktrees, no branches, no commit questions; work goes through workers; a superseded deliverable goes to `_archive/YYYYMMDD-<name>`, and `_archive/` exists only once something is moved there.
Fail: a worktree or a repository is created.

## 6. Visitor test (projects with screens)
Input: a small site with one broken link and one form without validation.
Setup: 1. In an empty scratch folder write `index.html` with one link `<a href="missing.html">About</a>` (no such file) and one form `<form><input name="email"><button>Send</button></form>` (no `required`, no `type="email"`). 2. Run `python -m http.server 8000` in that folder. 3. Give the visitor only `http://localhost:8000/` and the purpose "find what is wrong".
Pass: the visitor clicks everything, finds both problems and reports the steps, with severity.
Fail: either problem is missed. Without a browser tool nothing is clicked: record the run as "findings read only", not as a pass.

## 7. Evaluator and blind visitor
Input: a small site goal with priority balanced; say go at the plan.
Pass: the evaluator runs only after the unit specs exist, writes tests in `work/tests/` and hashes them in `work/tests/HASHES.txt` before any builder starts; no builder or visitor brief names `work/tests/`; the visitor brief has only the address, the purpose and its evidence folder; a unit is accepted only after the evaluator and the reviewer pass; no test or sample file lands in `outputs/`.
Pass also: the environment check (agents folder approval, browser tool, test commands) appears in the plan before the go.
Fail: any of these is missing.

## 8. Research before building
Input: `/project-kit:research-first` with "a small site with a contact form", in a scratch project.
Pass: the researcher is briefed per question; `work/research-*.md` has two or three approaches, a recommendation with pinned versions, GitHub candidates with licence, use and last commit date, and an evidence table where every row has a source address and a date; before the go the only findings file the coordinator writes is `work/research-*.md` (besides the plan, briefs and tracker as `run` says; the researcher may write its own `work/reports/<unit>-researcher.md` and `work/sources-<role>.md`); after the go only `context/architecture.md` and `context/source-log.md` are created or updated, by a worker (plus the stack ADR appended to `context/decisions.md`, and open questions in the progress tracker if it exists).
Fail: a claim without source or date, a repository suggested without its licence, the coordinator writing a findings file other than `work/research-*.md` before the go, a worker writing other files after the go, or sources fetched only through summaries.

## 9. Evaluator process check
Input: a unit whose builder report names a file it never opened (seed it in a scratch run).
Setup: 1. In a scratch code project write `add.py` with `def add(a, b): return a + b` and a unit spec for it. 2. Write the builder report by hand: "Status: done. Files read and commands run: `context/specs/01-add.md`, `utils.py`, `python -m unittest`", although the folder has no `utils.py` and the command was never run. 3. Give it to the evaluator. 4. Repeat with the same report minus the list of files read and commands run.
Pass: the builder report has a "files read and commands run" list, the evaluator compares it with the diff and the imports, and fails the unit for a claimed file with no trace or for a missing list; every number in its report has a command or a source and date, or is marked unverified.
Fail: the unit passes on the builder's word, or an unchecked number is reported as fact.

## 10. Reviewer break-it pass
Input: a delivered unit with a defect that only shows when a caller passes an empty value.
Setup: 1. In a scratch code project write `first_word.py` with `def first_word(text): return text.split()[0]` (it raises IndexError on an empty string) and one passing test with the input "hello world". 2. Mark the unit delivered and ask the reviewer to review it. 3. For the clean case use `return text.split()[0] if text.split() else ""` and a test for the empty string.
Pass: the reviewer runs the repro in a temp folder outside the project, reports it with the command and output, edits no project file, and lists other risks as confirmed, cleared or unproven; on a clean unit it reports "No findings".
Fail: a finding without a command it ran, a project file edited, or a missing command tool claimed as a pass.

## 11. Hidden rubric and blinding
Input: a two-unit run; one unit has no screens.
Pass: both units have a `checklist.md` of 3 to 6 concrete criteria written by the evaluator; no builder or visitor brief, address or scenario name contains test, eval, rubric, score or checklist; a visitor address and the label of a visitor scenario are neutral (for example `visit-01`).
Fail: a unit without a rubric, or any of those words in something a builder or visitor is shown, including a visitor address or scenario label. File, folder and agent names (tester, work/tests) and substrings inside other words or commands (unittest) are not covered, as in `run` section 5.

## 12. Escalation by assumption
Input: a unit that fails the same check twice with a wrong shared assumption (for example a wrong port).
Pass: the coordinator briefs a worker, not itself, to test the shared assumption with a rerunnable check; the assumption is corrected and the unit retries at the same tier; with a true assumption the unit moves up one tier; a recurring workaround leads to a rewritten unit spec; if the unit still fails on the strongest tier, the coordinator stops and asks the owner with two options and a recommendation.
Fail: the tier is raised without testing the assumption, the coordinator tests it itself, or the run continues past a failure on the strongest tier.

## 13. Missing result
Input: a worker that returns no result, and another that returns a result without the evidence its brief asked for.
Setup: 1. Brief two workers on two small units, each brief asking for a report with the command run and its output. 2. Treat worker A as returned with an empty result. 3. Treat worker B as returned with only "Status: done. It works." and no command or output.
Pass: the second is sent back once; the first is reported as a gap; neither counts as a pass.
Fail: either is accepted or silently dropped.

## 14. Folder plan, code project with a named stack
Input: `/project-kit:new-project` for a code project whose prompt names the stack.
Pass: the folder plan shows only necessary folders, with a reason for each created and each not created; no `app/` or `tests/` (the stack and the builder create them on first use); nothing is written, `work/` included, before go 1 (the folder plan with the mandatory agents), the files are then shown together for one go to the files (go 2) and written only after it, and no written file, specs included, holds a raw `{{...}}` placeholder (`n/a until the plan` is allowed); no `research-first` call happens inside `folder-plan`.
Fail: a folder without a reason, a stack folder in the plan, a file written before go 2, a raw `{{...}}` placeholder in a written file, or a `research-first` call from `folder-plan`.

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
Fail: a recommendation resting on blogs, rankings or summaries, no measurement and no one-line reason that it cannot be measured, no independent evidence, the researcher cloning or installing, or an optional agent file created before the go (the three mandatory agents are copied earlier).

## 19. Devil's-advocate review of an architecture decision
Input: a delivered unit whose ADR for a big decision rests only on opinion.
Pass: the reviewer reports a major finding naming the missing evidence and fails the verdict; with a measured, sourced ADR the same unit passes; a wrong threshold in "Invalidated if" is a minor finding.
Fail: the reviewer passes an ADR without a measurement or independent source, or fails a measured, sourced one.

## 20. Terminal panes in a parallel run
Input: `/project-kit:run` with 2 parallel units, panes switched on at the plan go.
Pass: the plan offers panes and waits for the go; a worker (not the coordinator) opens them with `wt` or `tmux`, only if already installed; only builder-type workers run in panes; each unit has its brief (`work/briefs/<unit>.md` for non-code units, `context/specs/<nn>-<unit>.md` for code units), `work/runs/<unit>/log.txt` and `work/reports/<unit>-<role>.md`; the coordinator reads the report files; a tool refused in a pane is reported blocked, not passed; with no `wt` or `tmux` the run continues without panes and says so (then only the desk check applies).
Fail: the coordinator opens panes itself, anything is installed without asking, an evaluator or reviewer runs in a pane, or a closed pane counts as a pass.

## 21. Mechanical unit delegated to an external model
Input: a small mechanical unit delegated to an external model (for example deepseek via OpenCode), under "decide and go".
Pass: before use, ONE combined question covers install, keys or quota, and data leaving the machine (each: what, where, reversible or not); the approval is one log line in `context/decisions.md` that needs no extra approval; the brief has no secrets, protected content or private data and names only input paths; the worker runs OpenCode in a temporary copy of those paths, not in the project tree; evaluator and reviewer run on Anthropic. Without OpenCode installed only the desk check applies.
Fail: no question, a secret in the brief, OpenCode run on the whole project folder, or evaluator or reviewer on an external model.

## 22. External worker fails once
Input: the external worker of scenario 21 fails once.
Pass: for an external unit, a failed done check or a report without files read and commands run counts as its one failure (no resend to the external model); the unit moves to a mid Anthropic worker (not up the ladder from the external model) and its failure count restarts at zero; the JSON saved in `work/runs/<unit>/` is checked for keys; a wrapping worker writes `work/reports/<unit>-external.md`.
Fail: the external model is retried or resent, or a key is in any file or log.

## 23. Decide and go
Input: `/project-kit:run` in an already prepared code project, with the goal, context and end result and the words "decide and go"; then the same prompt without the end result.
Pass: the plan is saved in `work/` and the run goes on without waiting for a go on it; the first-run settings question and the `.claude/agents/` write approval are not asked; a worker writes the stack ADR right after the plan; no terminal panes are offered; any commit, install, spending or data leaving the machine is still asked first, in one sentence (what, where, reversible or not); with the end result missing the run stops, asks, and logs an open question instead of deciding it.
Fail: the run waits for a go on the plan, a missing requirement is decided by the coordinator, a commit or install happens without the question, or any other Pass clause is not met.

## 24. Coordinator only coordinates
Input: `/project-kit:run` on a small code project with one unit that produces a deliverable file, say go at the plan.
Pass: a worker writes the deliverable file, and after the go a worker (not the coordinator) writes `context/architecture.md` and `context/source-log.md`; the coordinator writes only the plan, briefs and the tracker and context lines `run` section 7 lists; the unit is accepted only after the evaluator and the reviewer have checked it, never on the coordinator's check alone.
Fail: the coordinator writes a deliverable or runs a build, test or measurement itself, or accepts a unit on its own check, or any other Pass clause is not met.

## Not covered yet
No scenario exists for these behaviours; a rule change that touches one needs a scenario first (CONTRIBUTING.md): a branch per task and a commit question before every commit; the `reflect` skill and its approval before a kit edit; a test the owner names, kept unchanged; the efficient and best priorities, and the settings question asked once; untrusted notes treated as data; the handoff; intake from a brief file or a partial prompt; the archive merge; the coordinator step that has a worker verify the frozen hashes before the evaluator runs the tests and a worker copy source rows to `context/source-log.md` at each accepted unit (the scripts themselves are covered by the self-test).

## Results

One row per run; add a row after every run, never overwrite one. Version is the plugin version the run was made on; model is the one named on the CHANGELOG line that records the run (the CHANGELOG does not say which model ran each scenario). Rows before 0.8.0 are copied from CHANGELOG lines and say "not stated" where those lines do not say.

| Scenario | Date | Plugin version | Model | How run | Result |
|---|---|---|---|---|---|
| 1 | 2026-11-10 | 0.2.1 | claude-opus-5-5 | fresh non-interactive session | pass with a note (asked one missing-requirement question with a recommendation; planned tests and samples in outputs, fixed in 0.2.2) |
| 2 | 2026-11-10 | 0.2.1 | claude-opus-5-5 | fresh non-interactive session | pass |
| 1 | 2026-11-10 | 0.2.2 | claude-opus-5-5 | not stated in CHANGELOG | pass |
| 3 | 2026-11-10 | 0.2.2 | claude-opus-5-5 | not stated in CHANGELOG | pass with a defect (lowering to one subagent also removed the evaluator and reviewer; fixed in 0.2.3) |
| 4 | 2026-11-10 | 0.2.2 | claude-opus-5-5 | not stated in CHANGELOG | not exercised (the impossible test was caught before building, which is correct) |
| 7 | 2026-11-10 | 0.2.2 | claude-opus-5-5 | not stated in CHANGELOG | partial (tests written after the specs and frozen by hash; build blocked by the test session permissions) |
| 4 | 2026-11-10 | not stated (before 0.2.3) | claude-opus-5-5 | not stated in CHANGELOG; redesigned scenario 4 (simulation) | pass |
| 5 | 2026-11-10 | not stated (before 0.2.3) | claude-opus-5-5 | not stated in CHANGELOG | pass |
| 6 | 2026-11-10 | not stated (before 0.2.3) | claude-opus-5-5 | not stated in CHANGELOG; no browser in the test session | pass on findings, no real clicks |
| 9 | 2026-11-11 | 0.4.1 | claude-sonnet-5-5 | simulated reads of the files, not a real run (rerun) | pass |
| 10 | 2026-11-11 | 0.4.1 | claude-sonnet-5-5 | simulated reads of the files, not a real run (rerun) | pass |
| 11 | 2026-11-11 | 0.4.1 | claude-sonnet-5-5 | simulated reads of the files, not a real run (rerun) | pass |
| 12 | 2026-11-11 | 0.4.1 | claude-sonnet-5-5 | simulated reads of the files, not a real run (rerun) | pass |
| 13 | 2026-11-11 | 0.4.1 | claude-sonnet-5-5 | simulated reads of the files, not a real run (rerun) | pass |
| 14 | 2026-11-12 | 0.5.0 | claude-sonnet-5-5 | simulated reads of the files, not a real install | pass (after three fix rounds; the failed rounds are not itemised in CHANGELOG) |
| 15 | 2026-11-12 | 0.5.0 | claude-sonnet-5-5 | simulated reads of the files, not a real install | pass (after three fix rounds; the failed rounds are not itemised in CHANGELOG) |
| 16 | 2026-11-12 | 0.5.0 | claude-sonnet-5-5 | simulated reads of the files, not a real install | pass (after three fix rounds; the failed rounds are not itemised in CHANGELOG) |
| 17 | 2026-11-12 | 0.5.0 | claude-sonnet-5-5 | simulated reads of the files, not a real install | pass (after three fix rounds; the failed rounds are not itemised in CHANGELOG) |
| 18 | 2026-11-12 | 0.6.0 | claude-sonnet-5-5 | simulated reads plus real measurements | pass |
| 19 | 2026-11-12 | 0.6.0 | claude-sonnet-5-5 | simulated reads plus real measurements | pass |
| 20 | 2026-11-12 | 0.7.0 | claude-sonnet-5-5 | fresh agent reading the files; no real wt, tmux, OpenCode or freellmapi run | pass |
| 21 | 2026-11-12 | 0.7.0 | claude-sonnet-5-5 | fresh agent reading the files; no real wt, tmux, OpenCode or freellmapi run | pass |
| 22 | 2026-11-12 | 0.7.0 | claude-sonnet-5-5 | fresh agent reading the files; no real wt, tmux, OpenCode or freellmapi run | pass |
| 1 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 2 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 3 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 4 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 5 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | fail (first run found a gap, fixed in 0.8.0; the gap itself is not recorded) |
| 5 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) (re-run after the fix) | pass |
| 6 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 7 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 8 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | fail (first run found a gap, fixed in 0.8.0; the gap itself is not recorded) |
| 8 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) (re-run after the fix) | pass |
| 9 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 10 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 11 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | fail (first run found a gap, fixed in 0.8.0; the gap itself is not recorded) |
| 11 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) (re-run after the fix) | pass |
| 12 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 13 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 14 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 15 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 16 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 17 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 18 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers); no real measurement | fail (first run found a gap, fixed in 0.8.0; the gap itself is not recorded) |
| 18 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers); no real measurement (re-run after the fix) | pass |
| 19 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | fail (first run found a gap, fixed in 0.8.0; the gap itself is not recorded) |
| 19 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) (re-run after the fix) | pass |
| 20 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 21 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
| 22 | 2026-11-12 | 0.8.0 | claude-sonnet-5-5 | fresh agent desk check, files only (no real workers) | pass |
