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
Rules that must always hold; the reviewer checks every unit against them. At least four.
{{INVARIANTS}}

## Commands
Build: {{BUILD_COMMAND}}. Types: {{TYPES_COMMAND}}. Lint: {{LINT_COMMAND}}. Tests: {{TEST_COMMAND}}.

## Constraints
{{CONSTRAINTS}}
