# BG3 Eight Gates

## Design Goal
Create a standalone Baldur's Gate 3 class mod inspired by Might Guy from Naruto, centered on taijutsu, escalating Eight Gates power, physical burst damage, movement, and self-risk.

This is a separate mod from CursedArts. It must use its own folder, UUIDs, resources, localization, icons, and build/deploy path.

## Core Design Pillars
- Might Guy canon comes first, translated through BG3-supported systems.
- The Eight Gates should evolve through one main class mechanic, not eight unrelated hotbar buttons.
- Levels 1-12 must each be functional and intentionally paced.
- Taijutsu should be the backbone: movement, melee strikes, reactions, durability, and high-risk finishers.
- Every ability must use verified BG3 stats, statuses, passives, resources, spell lists, progression records, and localization patterns.
- Animations must use valid existing animation/cast/impact patterns or proven local references. Do not invent animation names.
- Gate of Death / Night Guy should be powerful, level 12, and leave the player downed at 0 HP rather than permanently dead, so an ally can revive them.

## Proposed Class Identity
- Resource: Chakra
- Combat style: martial striker / mobile bruiser
- Primary damage: bludgeoning, force, thunder, and limited fire/radiant-style impact only if justified by verified BG3 mechanics
- Defensive identity: evasion, grit, physical conditioning, and temporary gate states
- Risk identity: higher gates increase power and cost, ending in a severe self-sacrifice drawback

## Suggested 1-12 Progression
This is design guidance only until verified in the actual EightGates mod files.

| Level | Theme | Expected Feature |
|---|---|---|
| 1 | Taijutsu foundation | Chakra resource, basic taijutsu strike, mobility baseline |
| 2 | Training discipline | defensive stance or reaction |
| 3 | First Gate | Eight Gates activation begins, modest melee/movement boost |
| 4 | Lotus setup | stronger movement strike or combo tool |
| 5 | Primary Power Spike | Extra Attack-equivalent only if BG3 class rules support it cleanly |
| 6 | Hidden Lotus | higher-risk burst strike |
| 7 | Mid-gate escalation | stronger gate state, exhaustion/drawback begins to matter |
| 8 | Dynamic Entry / pressure | mobility attack or prone/knockback control |
| 9 | Morning Peacock-inspired | multi-hit or cone/flurry burst using supported spell patterns |
| 10 | Daytime Tiger-inspired | major single-target or line impact attack |
| 11 | Gate mastery | improved sustain, resistance, or gate control |
| 12 | Night Guy / Gate of Death | ultimate strike; leaves user downed at 0 HP, not killed |

## Animation Rules
Before accepting any animation-related implementation:
1. Confirm the referenced animation, spell style, cast text event, projectile, weapon action, or impact pattern exists in vanilla files or a working reference mod.
2. Prefer reusing proven monk/fighter/barbarian melee spell animation patterns over custom guesses.
3. If an animation cannot be verified, mark it as suspected and replace it with a safe proven pattern before release.
4. Do not approve invisible, missing, cinematic-only, or NPC-only animation assumptions as working player features.

## Safety Rules
- Do not modify CursedArts for this mod.
- Do not modify base game files.
- Do not reuse CursedArts UUIDs.
- Do not regenerate stable IDs once assigned.
- Do not claim in-game functionality until tested in BG3.
- Do not push unverified claims as verified framework findings.

## Required Workflow for This Mod
This project follows the shared GitHub modding workspace rules from
`AGENTS.md`, `UNIVERSAL_MODDING_RULES.md`, and `games/baldurs-gate-3/BG3_RULES.md`.

Before making changes:
1. Read `AGENTS.md`.
2. Read the universal modding rules.
3. Read the Baldur's Gate 3 rules and limitations.
4. Read this Eight Gates project manifest.
5. Inspect the existing repository structure and actual EightGates files before proposing changes.
6. Do not invent APIs, IDs, UUIDs, hooks, files, engine functions, or modding behavior.
7. Mark anything not verified as UNVERIFIED or NEEDS TESTING.
8. Preserve stable identifiers and working systems.
9. Make the smallest necessary change.
10. Do not rewrite working architecture just because you are uncertain.
11. Use a branch for meaningful changes whenever possible.
12. Commit changes clearly and prefer a pull request instead of directly overwriting `main`.
13. Update the manifest, changelog, sources, limitations, or test files whenever the work changes those areas.
14. Never claim something is working unless it reached the relevant verified state: compiled, loaded, tested in-game, or regression tested.
15. Treat the repository's current `main` branch as the stable baseline unless the user explicitly says otherwise.

## Current Status
**ACTIVE BUILD / UNPLAYED** as of 2026-08-26.

Codex monitor is using `C:\Users\johnf\.claude\scheduled-tasks\eightgates-1am-wrapup` as the Claude coordination mailbox when direct Claude messaging is unavailable.
