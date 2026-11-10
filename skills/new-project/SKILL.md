---
name: new-project
description: Create the folder structure, entry file and context files for a new project of any type (research, academic, code, general). Use when starting a project in an empty folder.
---

# new-project

Talk to the owner in the language they use. Ask one question per turn, with your recommended answer and a one-line reason. Never write a file the owner has not seen.

## Steps

1. Check the target folder. If it is not empty, stop and offer the `organize` skill instead. Write nothing.
2. Ask the project type: research, academic, code or general. Recommend the one closest to the final deliverable. An invalid answer gets one clarifying question; with no type, write nothing.
3. Ask the language of the work output. The filled files are written in it; file names stay in English.
4. Ask the owner to define the objectives and what counts as done, plus any rules or tests they want. If they are missing, do not go on. The coordinator decides everything else and logs it.
5. For code projects, define the stack with the owner: language and runtime, framework or libraries, test tool and command, linter and formatter, package manager, hosting or run target. Pin the versions, check each against the official documentation of the tool and give a reason for each. Mention `/ite:start` for a larger specification. Add `ui-context.md` only when there are screens or a visual deliverable.
6. For academic projects, also collect deliverable format, citation style, page limit and the teacher guide.
7. Build each file from `templates/core` plus `templates/<type>` (and `templates/optional/ui-context.md` when it applies). Replace every placeholder in double braces with real content. Use `writing-and-evidence-standards.md` for research, academic and general, and `code-standards.md` for code. The standards placeholder in the entry file names whichever applies.
8. Show each file in full. Write it only after the owner approves that file. If a placeholder is still unfilled, say so and do not write the file.
9. Create the folders `inputs/`, `outputs/`, `studies/`, `work/` and `_archive/`. For code projects also `.worktrees/` (hidden, created and removed by the coordinator) and offer `git init` without a remote; ask before any commit.
10. Run the placeholder test from the plugin `test/check_kit.py` on the new folder when Python is available and report the result. If it is not available, say that the check was skipped.

## Rules

- Never delete anything. Never write secrets, keys or real personal data; use placeholders.
- On a write error, stop, list the files written and the ones pending, and ask how to go on.
- Ask before any commit, push, publication, spending or scope change.
