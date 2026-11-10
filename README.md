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
- `/project-kit:new-project` sets up an empty folder.
- `/project-kit:organize` reorganizes an existing folder with a dry-run manifest; it moves nothing until you approve and never deletes without your yes per item.
- `/project-kit:reflect` closes a session: it separates general errors from project-specific ones and proposes improvements to the kit, applied only with your approval.

## How a run works

1. **Intake.** Goal, context and expected end result.
2. **Priority.** Efficient, balanced or best. If you do not know, the default table applies:

   | Work | Model tier |
   |---|---|
   | Search, extraction, mechanical edits | haiku |
   | Building code, writing | sonnet |
   | Architecture, high-risk review, hard decisions | opus |

3. **One-page plan**, saved in `work/`: units and their checks, stack with pinned versions (for code a researcher compares two or three options in official documentation), models per role, number of subagents and what runs in parallel, worktrees yes or no, the test plan, and a cost estimate (low, medium, high). Reply go, or change anything, including the number of subagents. A changed plan needs a new go. "Decide and go" in your prompt skips the stop.
4. **Execution.** The coordinator only coordinates. Workers live in `.claude/agents/`: a builder and a reviewer in every project, a tester and a researcher when needed. Each brief carries a goal, files to read, a done check and a context package. Units run in parallel only when they share no files and no state. Worktrees are used only when two or more workers write code in parallel in a git repository.
5. **Verification.** The coordinator runs the done check itself, then a reviewer in a fresh context checks that the brief was met and then the quality (build, types, lint, tests). Under "best", two independent reviewers must both pass. For sites and apps the tester acts as a visitor who understands nothing: it clicks everything and tries to break the product.
6. **Escalation.** A failure goes back with a correction brief. After two failures the unit moves up one model tier; if it fails on the strongest tier, the coordinator stops and gives you two options with a recommendation.
7. **Close.** Progress, decisions, models and escalations are logged in `context/`; the reflect skill proposes improvements.

Commits, pushes, publication, spending and scope changes always ask first. There is no token cap; the plan shows an estimate.

## Project types

Every type gets the same core (entry file, second entry file, overview, architecture with invariants, AI workflow rules, progress tracker, decisions, known issues, change log) plus one block:

- Research: a source log and evidence rules.
- Academic: deliverable format, citation style, page limit, the teacher guide, a source log, cuts listed with the pages they save.
- Code: a stack record, branches and worktree rules, unit specs (goal, design, implementation, dependencies, verify) and a build plan, tests including the visitor test, code standards that name their sources.
- General: only the core.

## Folders of a project

`inputs/` (read only for agents), `outputs/` (final deliverables), `studies/` (study material), `work/` (plans, drafts, returns and logs; only the coordinator writes), `_archive/` (nothing is deleted; it moves here), `.claude/agents/` (workers), and a hidden `.worktrees/` for parallel code work.

## Recommended settings

The run skill asks once whether you want these; the plugin never edits your settings.

- `/effort xhigh` for the coordinator session (levels are low, medium, high, xhigh, max; ultracode is a separate setting, not a level).
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=40` (60 for long jobs). It can only make compaction happen earlier.
- `/context` shows how full the context is.
- `CLAUDE_CODE_SUBAGENT_MODEL` sets a default model for subagents without one. The model chosen per call or in an agent file takes precedence (since Claude Code 2.1.251); `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` forces the global value on every subagent and defeats per-task routing, so the kit does not use it.

## Known interaction

Some plugins run a hook after every file write that removes metadata keys from Markdown front matter. One such hook removes the `model` line from agent files. The placeholder test catches this, and the coordinator passes the model on every call anyway. If it happens, add the line back with a shell command.

## Not verified

The orchestration practices draw on third-party pages and plugins listed in `CREDITS.md`. Their price and token figures cite no source and were not verified against Anthropic sources, so this README does not repeat them.

## Tests

- `python -I test/check_kit.py --self-test` builds a sample folder per type and checks that no placeholder is left, every file in the read order exists and every agent has name, description and model; bad fixtures must fail. `python -I test/check_kit.py <folder>` checks a real folder.
- `test/scenarios.md` holds six behaviour scenarios run by hand after each release and each model swap.

## Privacy

The kit holds placeholders only. It never asks for or writes keys, tokens, passwords or real personal data.

## Licence

MIT. See `LICENSE`.
