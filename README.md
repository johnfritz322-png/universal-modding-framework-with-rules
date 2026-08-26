# Universal Modding Framework With Rules

A reusable framework for AI-assisted game modding. It was originally conceived around Baldur's Gate 3, but the repository is structured so the universal rules can be reused for other games while each game gets its own verified implementation rules.

## Goal
Create one shared source of truth that Claude, Codex, ChatGPT, or another capable coding agent can inspect before designing, coding, debugging, or extending a mod.

The framework is built around five principles:
1. **Verify before coding.**
2. **Do not invent engine capabilities, APIs, IDs, or dependencies.**
3. **Preserve working systems and stable identifiers.**
4. **Make the smallest compatible change and test incrementally.**
5. **Never claim success beyond the evidence available.**

## Start here
AI agents should read these files in this order:
1. [`AGENTS.md`](AGENTS.md)
2. [`UNIVERSAL_MODDING_RULES.md`](UNIVERSAL_MODDING_RULES.md)
3. the relevant file under `games/<game>/`
4. the target mod's `PROJECT_MANIFEST.md`
5. the target mod's design/implementation files

## Repository layout
```text
.
├── AGENTS.md
├── UNIVERSAL_MODDING_RULES.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── games/
│   └── baldurs-gate-3/
│       ├── BG3_RULES.md
│       ├── KNOWN_LIMITATIONS.md
│       └── SOURCES.md
├── templates/
│   ├── PROJECT_MANIFEST.md
│   ├── MOD_DESIGN.md
│   ├── TEST_PLAN.md
│   └── COMPATIBILITY_REPORT.md
└── projects/
    └── bg3-copy-ninja/
        ├── README.md
        └── PROJECT_MANIFEST.md
```

## Verification states
Use these labels consistently:
- **VERIFIED** — supported by primary/maintainer evidence, project/game files, tool output, or direct testing.
- **HIGH CONFIDENCE** — supported by known-working examples in the same relevant environment.
- **ASSUMPTION** — plausible but not yet verified.
- **UNVERIFIED** — not established.
- **NEEDS TESTING** — implementation requires direct validation.

## Current project
The first design tracked here is **BG3 Copy Ninja**, a Kakashi-inspired mod concept combining a permanent shinobi technique library with a Sharingan-driven temporary enemy-technique copy system.

Its current status is **DESIGN / RESEARCH**. The repository intentionally does not pretend the technical implementation is finished before the exact BG3 build, toolchain, APIs, identifiers, persistence behavior, and copy eligibility rules are verified.

## Collaboration
Meaningful changes should be made on branches and reviewed through pull requests where practical. `main` should remain the stable source of truth.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the workflow.
