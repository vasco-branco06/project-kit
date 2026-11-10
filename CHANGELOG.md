# Change log

One line per fix of a rule or template: date, model name, what changed and why.

- 2026-11-10 | claude-sonnet-5-5 | 0.1.0: first build of the plugin from the decided specification.
- 2026-11-10 | claude-opus-5-5 | 0.2.0: run skill (intake, one-page plan, coordination, verification, escalation); builder, reviewer, tester and researcher agent templates; unit specs and build plan for code; invariants, open questions and unit gate; language-independent read order and agent checks in the test; six behaviour scenarios.
- 2026-11-10 | claude-opus-5-5 | 0.2.1: models chosen per unit from what the unit needs (no fixed table by type of work), fable added for the hardest units and as the top of the escalation ladder; agent files use model inherit as a fallback. Requested by the owner.
- 2026-11-10 | claude-opus-5-5 | Scenarios 1 and 2 run on 0.2.1 in fresh non-interactive sessions: 1 pass with a note (asked one missing-requirement question with a recommendation; planned tests and samples in outputs, fixed in 0.2.2), 2 pass. Scenarios 3 to 6 not run.
- 2026-11-10 | claude-opus-5-5 | 0.2.2: evaluator agent on the strongest model writes tests after the spec, freezes them by hash, scores code tests and blind visitor reports against a hidden checklist, separates wrong tests from wrong products; builder never sees the tests; visitor gets only address and purpose; two or more visitors under best; outputs holds final deliverables only; scenario 7. Requested by the owner.
