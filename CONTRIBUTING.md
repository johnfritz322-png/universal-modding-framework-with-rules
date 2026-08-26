# Contributing

This repository is designed for collaboration between humans and AI coding agents.

## Core rule
All contributors must follow `AGENTS.md` and `UNIVERSAL_MODDING_RULES.md`.

## Workflow
1. Read the relevant game-specific rules and project manifest.
2. Create a branch for meaningful work.
3. Make the smallest necessary change.
4. Record any new stable identifiers or dependencies.
5. Update tests/documentation when behavior changes.
6. State the highest verified status honestly.
7. Open a pull request describing evidence, risks, and rollback path.

## Branch naming
Suggested patterns:
- `feature/<name>`
- `fix/<name>`
- `research/<name>`
- `compat/<name>`
- `docs/<name>`
- `setup/<name>`

AI agents may prefix branches with their own name when helpful, for example `codex/feature-copy-slots` or `claude/research-bg3-events`.

## Pull request expectations
A useful PR should explain:
- what changed,
- why it changed,
- what source/evidence supports the implementation,
- what was actually tested,
- what remains unverified,
- what could break,
- how to roll back.

## Do not
- invent technical facts,
- regenerate stable IDs casually,
- rewrite working architecture without justification,
- hide errors/tests,
- claim in-game success without in-game evidence,
- add third-party assets without checking permission/licensing.
