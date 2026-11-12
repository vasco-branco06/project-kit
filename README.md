# project-kit

A professional multi-agent setup for Claude Code that anyone can use. You give the goal, any context you have, and how the end result should look and work. A coordinator proposes the stack, the models, the number of subagents and whether worktrees make sense in a one-page plan, waits for your go, then coordinates worker subagents, checks every result and escalates when something keeps failing. It also creates or reorganizes the project folder with an entry file, context files and working rules for four project types: research, academic, code (apps, sites, scripts, data, machine learning, system architecture) and general.

The kit is Markdown and JSON plus one test script that uses only the Python standard library. It has no runtime dependencies and holds no data from any real project.

## Install

```
claude plugin marketplace add vasco-branco06/project-kit
claude plugin install project-kit@project-kit
```

The same steps work with a local path. Inside a session the equivalents are `/plugin marketplace add ...` and `/plugin install project-kit@project-kit`. Update with `/plugin update`.

## Skills

- `/project-kit:run` starts any piece of work. Give a free prompt, a brief file, or both; it asks only what is missing, one question at a time, and interviews you if you give nothing.
- `/project-kit:research-first` runs before building a site, app, algorithm or code: it researches primary sources and existing GitHub projects, writes a sourced findings file in `work/` and waits for your go. Run also calls it during planning. Its Decision standard governs stack, language and architecture choices, and each big one is recorded as an ADR in `context/decisions.md`.
- `/project-kit:folder-plan` decides which folders a project needs, with a reason for each, before new-project or organize create any.
- `/project-kit:terminal-panes` optionally shows each parallel worker in its own Windows Terminal or tmux pane; the run works the same without it.
- `/project-kit:external-models` sets when a small unit may go to a model outside Anthropic (OpenCode with DeepSeek, MiniMax or GLM, or the freellmapi proxy); it always asks you first.
- `/project-kit:new-project` sets up an empty folder.
- `/project-kit:organize` reorganizes an existing folder with a dry-run manifest; it moves nothing until you approve and never deletes without your yes per item.
- `/project-kit:reflect` closes a session: it separates general errors from project-specific ones and proposes improvements to the kit, applied only with your approval.

## How a run works

1. **Intake.** Goal, context and expected end result.
2. **Models, chosen per unit.** The coordinator picks the model for each unit from what that unit needs, not from its type of work. Small or fully specified work goes to the small tier, code included; mid takes several files or some judgement; strong takes architecture, unclear requirements, security or data-loss risk and high-risk review; strongest is kept for the hardest units (novel problems, long reasoning across the system, decisions costly to reverse) or a unit that already failed on strong. Your priority (efficient, balanced or best) shifts these choices down or up. Every choice and its reason is in the plan and the log.

3. **One-page plan**, saved in `work/`: units and their checks, stack with pinned versions (a researcher briefed at the first run (again only if the stack or method changes) checks the stack and the method in official documentation), the model of each unit, number of subagents and what runs in parallel, worktrees yes or no, the test plan, and a cost estimate (low, medium, high). Reply go, or change anything, including the number of builders; the coordinator never checks its own team's work alone. A changed plan needs a new go. "Decide and go" in your prompt skips the stop.
4. **Execution.** The coordinator only coordinates. Workers live in `.claude/agents/`: the mandatory ones are named in each project's entry file; the coordinator proposes builders, blind visitors and any other roles in the plan and creates them after your go. Each brief carries a goal, files to read, a done check and a context package. Units run in parallel only when they share no files and no state. Worktrees are used only when two or more workers write code in parallel in a git repository.
5. **Verification.** Once every unit has a spec or unit brief, an evaluator on the strongest tier writes the tests and, for every unit, a hidden rubric of 3 to 6 criteria (for sites and apps, what a visitor should be able to do). It freezes them by hash before anything is built. The builder never sees them. For sites and apps a blind visitor gets only the address and one sentence of what the product is for, clicks everything and tries to break it; under "best" two or more visitors with different profiles do this without knowing about each other. The evaluator runs its tests, scores the visitor reports against its checklist, and tells a wrong test from a wrong product. A reviewer in a fresh context checks code quality (build, types, lint). A unit is accepted only when both the evaluator and the reviewer pass.
6. **Escalation.** A failure goes back with a correction brief. After two failures a worker tests the one assumption both attempts shared; if it is false it is corrected and the unit retries at the same tier, if it holds the unit moves up one tier (small, mid, strong, strongest), and a workaround that keeps coming back means the unit spec is rewritten; if it fails on the strongest tier, the coordinator stops and gives you two options with a recommendation.
7. **Close.** Progress, decisions, models and escalations are logged in `context/`; the reflect skill proposes improvements.

Commits, pushes, publication, spending and scope changes always ask first. There is no token cap; the plan shows an estimate.

## Project types

Every type gets the same core (entry file, second entry file, overview, architecture with invariants, AI workflow rules, progress tracker, decisions, known issues, change log) plus one block:

- Research: a source log and evidence rules.
- Academic: deliverable format, citation style, page limit, the teacher guide, a source log, cuts listed with the pages they save.
- Code: a stack record, branches and worktree rules, unit specs (goal, design, implementation, dependencies, verify) and a build plan, tests including the visitor test, code standards that name their sources.
- General: only the core.

## Folders of a project

`context/`, `work/` and `.claude/agents/` always; other folders only when the project has them, as `folder-plan` decides (the rules are in the entry file).

## Recommended settings

The run skill asks once whether you want these; the plugin never edits your settings.

- `/effort xhigh` for the coordinator session (levels are low, medium, high, xhigh, max; ultracode is a separate setting, not a level).
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=40` (60 for long jobs). It can only make compaction happen earlier.
- `/context` shows how full the context is.
- Optional, installed only when you ask: Windows Terminal (`wt`) or tmux for terminal panes; OpenCode and the freellmapi proxy for external models.
- `CLAUDE_CODE_SUBAGENT_MODEL` sets a default model for subagents without one. The model chosen per call or in an agent file takes precedence (since Claude Code 2.1.251); `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` forces the global value on every subagent and defeats per-task routing, so the kit does not use it.

## Known interaction

Some plugins run a hook after every file write that removes metadata keys from Markdown front matter. One such hook removes the `model` line from agent files. The placeholder test catches this, and the coordinator passes the model on every call anyway. If it happens, add the line back with a shell command.

## Not verified

The orchestration practices draw on third-party pages and plugins listed in `CREDITS.md`. Their price and token figures cite no source and were not verified against Anthropic sources, so this README does not repeat them.

## Tests

- `python -I test/check_kit.py --self-test` builds a sample folder per type and checks that no placeholder is left, every file in the read order exists and every agent has name, description and model; bad fixtures must fail. `python -I test/check_kit.py <folder>` checks a real folder.
- `test/scenarios.md` holds the behaviour scenarios, run by hand after each release and each model swap.

## Privacy

The kit holds placeholders only. It never asks for or writes keys, tokens, passwords or real personal data.

## Licence

MIT. See `LICENSE`.
