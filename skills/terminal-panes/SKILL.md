---
name: terminal-panes
description: Use when a run has two or more units in parallel, or the owner asks to watch the workers, to show each worker in its own terminal pane (Windows Terminal or tmux). Optional; the run works the same without panes.
---

# terminal-panes

Talk to the owner in the language they use. One question per turn, with a recommended answer and a one-line reason.

## Steps

1. Use this skill only when the `run` plan has two or more parallel units or the owner asks to watch. The owner turns it on with the go on the one-page plan; it is never mandatory, and without that go the run proceeds without panes.
2. The coordinator never executes. Brief one worker to open the panes. The worker detects `wt.exe` (Windows) or `tmux` (macOS, Linux). If neither exists it says so in its report and the run continues without panes. Never install anything; an install always asks the owner.
3. Each pane runs one worker and replaces the subagent call for that unit; the unit never runs twice. Only builder-type workers run in panes, never the evaluator or the reviewer (the evaluator writes only `work/tests/`). The pane reads the brief or spec the run already names (`context/specs/<nn>-<unit>.md` for code units, otherwise `work/briefs/<unit>.md`, which the coordinator writes), writes its log to `work/runs/<unit>/log.txt` and its report to `work/reports/<unit>-<role>.md` in the report format of the `run` skill: the first line is `Status: done | done with concerns | blocked | needs context`, then `Model:` (the model you actually ran on), the files read and the commands run.
4. Panes are for watching. The coordinator reads the report files only. A closed pane or a missing report is a missing result: sent back once, then a gap (`run`, section 5).
5. Windows Terminal (source: learn.microsoft.com/windows/terminal/command-line-arguments): `wt new-tab -d <dir> --title <unit> <command>`, then `split-pane -V ...` (or `-H`) per extra unit, joined with `;`. In PowerShell escape each `;` with a backtick, or launch with `Start-Process wt`. The native agent-team split panes of Claude Code do not work in Windows Terminal (code.claude.com/docs/en/agent-teams), so the worker builds the grid itself.
6. tmux: the syntax was not verified for this skill. The worker checks `tmux -V` and the output of `man tmux` or `tmux list-commands` before using `split-window` and `send-keys`, and says in its report that it did.
7. Pane command for a Claude worker (`claude -p --model <model> ...`): read `claude --help` first and use only flags it lists; never assume them. An external-model worker (`external-models`) may run in a pane too, still in its temporary copy. `claude -p` cannot answer permission prompts: allow the tools a pane needs before launch with flags that `claude --help` lists, with the owner's approval; otherwise the tool is refused and the worker reports blocked.

## Rules

- A pane never writes `context/`; the blinding rule and the briefs of `run` apply unchanged.
- The model of each pane is the one the plan names, passed explicitly.
- Never put keys or secrets in a pane command or its log.
