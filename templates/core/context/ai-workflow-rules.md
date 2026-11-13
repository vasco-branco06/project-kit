# AI workflow rules

## Stages
1. Inspect, ask and plan. Show the one-page plan: goal, units, how each is checked, stack, models, subagents, worktrees, tests, cost estimate, risks.
2. Execute only what the owner approved, in the approved plan version.
3. Review against the done checks before saying a unit is done; say what was tested and what was not.

## Units
- One visible result, one system boundary, one session. Split a unit that cannot be checked end to end quickly; merge a unit that has no result of its own.
- Order: dependencies first, security before features, backend before wiring the interface, interface shells before real data, install packages only when needed.

## Missing requirements
Never invent behaviour. Record an open question in the progress tracker and ask the owner.

## Protected files
Workers never edit `inputs/`, generated code, vendor code or anything outside the paths in their brief.

## Before the next unit
It works end to end, the invariants hold, the progress tracker is updated, the build passes. Update the progress tracker first (no wait); other context files need owner approval, except the writes listed in section 7 of the `run` skill.

## Corrections
A correction brief says what behaviour was expected, what happened, and that only that point changes. It never contains test code or checklist lines.

## Environment check
Before planning: approval to write `.claude/agents/`, a browser tool for projects with screens, and the commands the tests need. Anything missing is stated in the plan.

## Evaluator rules
Never name this section in a builder or visitor brief. Only the evaluator reads or writes `work/tests/`; a visitor writes only in `work/evidence-incoming/<unit>/`.

## Safety
Subagents never decide for the coordinator. Ask before anything destructive, external or hard to reverse.
