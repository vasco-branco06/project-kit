# Code standards

Each standard names its source. A standard that does not suit the stack is replaced by the stack equivalent and the change is logged in `decisions.md`.

- Write tests first for new logic; keep changes small and reviewable. Source: owner rule.
- One commit per task, after the owner approves. Commit message format: Conventional Commits 1.0.0 (https://www.conventionalcommits.org/en/v1.0.0/, CC BY 3.0).
- No secrets in the repository. Keep shared configuration apart from local secret configuration, and keep the local one out of version control.
- Keep raw data apart from derived data, and keep raw data untouched (layout idea from Cookiecutter Data Science, MIT: https://github.com/drivendataorg/cookiecutter-data-science).
- Notebooks hold experiments; reusable logic lives in code with tests.
- Record decisions one per entry with context, options, decision and consequences (MADR 4.0.0, MIT or CC0: https://adr.github.io/madr/).
- Typed or linted code, using the linter and formatter recorded in `architecture.md`.
- At every API or system boundary: validate input, check permissions before any change, return consistent responses and errors. Source: owner rule.
- Storage: one owner per piece of data, migrations versioned, no personal data without a stated reason and retention. Source: owner rule.
- Language-specific style follows the official style guide of the language; name it here: {{STYLE_GUIDE}}.
