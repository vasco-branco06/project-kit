# Security

The kit has no server and no runtime dependencies. What can go wrong is narrow: a template or skill that makes a run write or send a secret, a script (`test/check_kit.py`, `scripts/`) that does something unsafe on a user's machine, or a rule that weakens a permission prompt.

## Reporting

Do not post details in a public issue. Open an issue titled "Security contact request" with no details, and the owner will arrange a private channel. Do not include keys, tokens or personal data in any report.

## Supported versions

Only the latest version gets fixes. The version is the `version` field of `.claude-plugin/plugin.json`.
