# Contributing

The kit is Markdown, JSON and a few scripts that use only the Python standard library. Keep it that way: no runtime dependencies, and no data from real projects.

## Before you open a pull request

1. Run `python -I test/check_kit.py --self-test`. It must exit 0. CI runs the same command on Linux and Windows.
2. If you changed a rule that a behaviour scenario covers, read the scenario in `test/scenarios.md` and run it by hand. Add a scenario when you add a rule that nothing covers.
3. Add one line to `CHANGELOG.md` that starts with `Unreleased`, after the date and model name: date, model name, `Unreleased`, what changed and why. Never write a new version number there: the version check compares the last versioned line with `plugin.json`, and only `scripts/release.sh` bumps the version. The owner folds the Unreleased lines into the release line.
4. Do not edit `version` in `plugin.json` or `marketplace.json` by hand.

## Rules for the files

- Line endings are LF (`.gitattributes` enforces it).
- Every agent file in `templates/agents/` keeps its `name`, `description` and `model` lines. Some plugins strip front matter keys after a file write; check the diff.
- A skill folder name equals the `name` in its `SKILL.md`. Reference template files as `${CLAUDE_PLUGIN_ROOT}/templates/...` so they resolve in an installed copy.
- Tool limits: the reviewer and the researcher set `tools`; the evaluator, builder and tester inherit all tools and state their limits in prose only, and the self-test does not check them.
- State each rule once, in one place, and point to it from the others.
- Every borrowed idea gets a row in `CREDITS.md` with an address and the date you read it. If you cannot verify an address, write "address not verified".
- No keys, tokens, passwords or personal data in any file or fixture.

## Release

Only the owner releases. Running the script by hand is the owner's approval of the release commit and tag it makes; it asks nothing more.

```
bash scripts/release.sh X.Y.Z "what changed and why" MODEL_NAME
```

On Windows run it from Git Bash, not PowerShell or cmd. Run it on a branch: on a detached HEAD it stops before changing anything.

The release line of `X.Y.Z` in `CHANGELOG.md` must say that scenarios were run: it needs the word `scenario` or `scenarios`, then `run on`, `pass on` or `passed on` and an ISO date (for example `scenarios 1 to 7 run on 2026-11-13`), and no `not run`. The self-test fails and the script restores its files otherwise. Put that wording in the message, or write the release line in `CHANGELOG.md` yourself first (`- DATE | MODEL | X.Y.Z: ...`): the script keeps an existing line for that version and adds no second one.

The script stops with an error if any file other than the ones it edits (`plugin.json`, `CHANGELOG.md`, the agent templates) is changed or untracked, so commit other work first. It bumps `plugin.json`, adds the changelog line, restores missing `model:` lines in the agent templates, runs the self-test, commits and tags `vX.Y.Z`. It never pushes. It prints the push command, and the owner runs it after review. CI then checks that the tag equals the `plugin.json` version.
