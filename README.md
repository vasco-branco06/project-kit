# project-kit

A general model for organizing any project. It creates or reorganizes a project folder with a short entry file, a fixed set of context files and working rules for Claude Code, and it shows every file before writing it. It works for four project types: research, academic, code (apps, sites, scripts, data, machine learning, system architecture) and general.

The kit is Markdown and JSON plus one test script that uses only the Python standard library. It has no runtime dependencies and holds no data from any real project.

## Install

From a local clone, in a terminal:

```
claude plugin validate <path-to-this-folder>
claude plugin marketplace add <path-to-this-folder>
claude plugin install project-kit@project-kit
claude plugin list
```

From the public repository, once it is published, replace the path with `<owner>/project-kit`. Inside a session the equivalents are `/plugin marketplace add ...` and `/plugin install project-kit@project-kit`.

## Skills

- `/project-kit:new-project` for an empty folder. It asks the type and the language of the work, asks you to define the objectives and what counts as done, shows each file in full and writes only what you approve.
- `/project-kit:organize` for a folder that already has files. It writes a manifest first (origin, destination, reason), moves nothing until you approve, never deletes, and archives what does not fit. Only zero-byte debris can be proposed for deletion, line by line.
- `/project-kit:reflect` to close a session or a finished task. It classifies the corrections as general or specific to the project and proposes the smallest rule edit for the general ones, applied only after you approve.

## Project types

Every type gets the same core (entry file, second entry file, overview, architecture, AI workflow rules, progress tracker, decisions, known issues, change log) plus one block of rules:

- Research: an evidence and source log.
- Academic: deliverable format, citation style, page limit, the teacher guide, a source log, cuts listed with the pages they save before cutting.
- Code: a stack record with pinned versions and reasons, a branch per task (never the main branch), a test plan with code tests and a simulated user that clicks through the product, and code standards that name their sources. The skill suggests the `ite` plugin for a larger specification.
- General: only the core.

The standards file is `code-standards.md` for code and `writing-and-evidence-standards.md` for the others. A UI context file is added only when there are screens or a visual deliverable.

## Folders of a project

`inputs/` (read only for agents), `outputs/` (final deliverables), `studies/` (study material), `work/` (drafts, returns and logs; only the coordinator writes), `_archive/` (nothing is deleted; it moves here), and a hidden `.worktrees/` for code projects.

## How the rules work

You define the objectives and what counts as done, and may add rules and name tests. The coordinator decides the rest and logs each decision. The main session orchestrates: it writes briefs (goal, files to read, a done check that can be run or seen), runs the check itself before accepting and never passes on a worker report unchecked. Every subagent gets a context package. Work runs in three stages: inspect and plan, approved execution, review. Commits, pushes, publication, spending and scope changes always need your approval. At the end of the work the coordinator separates general errors from project-specific ones and proposes self-improvements of the kit rules for the general ones.

## Manual settings

These are optional and live in Claude Code, not in the plugin. Check the official documentation before relying on them.

- `/effort` sets the reasoning effort. Levels are low, medium, high, xhigh and max; ultracode is a separate setting, not a level.
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` sets the percentage of the context window at which automatic compaction starts. It can only make compaction earlier. A page studied for this kit suggests 40, and 60 for long jobs.
- `/context` shows how full the context is.
- `CLAUDE_CODE_SUBAGENT_MODEL` sets the default model for subagents that have no model of their own. Since Claude Code 2.1.251 the model chosen per call or in an agent definition takes precedence, and `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` forces the global value on all subagents, which defeats per-task routing. The kit forces no global model.

## Not verified

The orchestration practices come from two third-party pages. Their price and token figures cite no source and were not verified against Anthropic sources, so this README does not repeat them. The pattern sources are listed in `CREDITS.md`.

## Test

`python -I test/check_kit.py --self-test` builds a sample folder for each type and checks that no placeholder is left and that every file named in the read order exists. It also checks that a bad fixture fails. `python -I test/check_kit.py <folder>` checks a real generated folder.

## Privacy

The kit holds placeholders only. It never asks for or writes keys, tokens, passwords or real personal data.

## Licence

MIT. See `LICENSE`.
