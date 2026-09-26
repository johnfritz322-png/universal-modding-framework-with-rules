---
description: Review every rule the user has defined across this repository
---

Review all rules currently defined in this repository and report their state back to the user. Do not modify any files — this is a read-only audit.

Read these, skipping any that don't exist:
- `AGENTS.md` — non-negotiable agent rules and required workflow
- `UNIVERSAL_MODDING_RULES.md` — universal hard rules
- `CONTRIBUTING.md` and `README.md` — process/repo rules
- `CHANGELOG.md` — most recent entries, for what rules changed and why
- Every `games/<game>/*.md` file (e.g. `*_RULES.md`, `KNOWN_LIMITATIONS.md`, `CONFIG_SURFACE.md`, `SOURCES.md`) — per-game verified rules and limitations
- Every `templates/*.md` file — process rules baked into project templates
- Any `RULES.md`, `CLAUDE.md`, or `AGENTS.md` found under `projects/` or `platform/` — per-project or per-platform rules

For each file found, report:
1. Its path.
2. A concise summary of the rules/constraints it defines.

Then call out:
- Contradictions or overlaps between files (e.g. a project rule that conflicts with `UNIVERSAL_MODDING_RULES.md`).
- Rules that look stale, unverified, or no longer match the current repo state.
- Gaps — e.g. a `games/<game>/` or `projects/<project>/` directory missing rule/limitation docs that sibling directories have.

Organize the final report by scope: universal (`AGENTS.md`, `UNIVERSAL_MODDING_RULES.md`) → per-game → per-project → templates/process. Keep it a structured list, not prose.
