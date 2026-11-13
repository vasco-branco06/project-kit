# Architecture

## Stack record
| Item | Choice | Pinned version | Reason |
|---|---|---|---|
| Language and runtime | {{LANGUAGE}} | {{LANGUAGE_VERSION}} | {{LANGUAGE_REASON}} |
| Framework or libraries | {{FRAMEWORK}} | {{FRAMEWORK_VERSION}} | {{FRAMEWORK_REASON}} |
| Test tool and command | {{TEST_TOOL}} | {{TEST_VERSION}} | {{TEST_REASON}} |
| Linter and formatter | {{LINTER}} | {{LINTER_VERSION}} | {{LINTER_REASON}} |
| Package or environment manager | {{PACKAGE_MANAGER}} | {{PACKAGE_VERSION}} | {{PACKAGE_REASON}} |
| Hosting or run target | {{HOSTING}} | {{HOSTING_VERSION}} | {{HOSTING_REASON}} |

## Components and folders
{{COMPONENTS}}

## Data flow
{{DATA_FLOW}}

## Invariants
Rules that must always hold; the reviewer checks every unit against them. At least four, each with a command that fails when it is broken (test, lint or import check); one with no such command gets a `[soft]` prefix on its line.
{{INVARIANTS}}

## Commands
Build: {{BUILD_COMMAND}}. Types: {{TYPES_COMMAND}}. Lint: {{LINT_COMMAND}}. Tests: {{TEST_COMMAND}}.
Run the app: start {{START_COMMAND}}; ready when {{READY_SIGNAL}}; instance check {{CHECK_COMMAND}}; stop {{STOP_COMMAND}}; two copies can run side by side: {{ISOLATION}}. Ready means usable from an empty data folder, not just a process answering. Instance check is a command that shows whether a copy of the app is already running. Write n/a when an item does not apply (script, data, library). In a new project with no stack yet, the placeholder value (the one `new-project` writes) is accepted until the plan, not an unfilled placeholder; `run` replaces it.

## Constraints
{{CONSTRAINTS}}
