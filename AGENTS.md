# AGENTS.md

## Purpose
This repository is a shared operating framework for AI-assisted game modding. Any AI agent that reads, edits, or extends this repository must follow these rules before making changes.

## Non-negotiable rules
1. Verify before coding. Do not invent APIs, hooks, IDs, UUIDs, FormIDs, blueprint names, records, file schemas, loader behavior, commands, dependencies, or engine capabilities.
2. Establish the exact environment first: game, game version/build, platform, mod loader/framework, SDK/toolkit, script extender, dependencies, compiler/runtime, and relevant existing mods.
3. Research before architecture. Map requested features only to verified engine capabilities.
4. Separate design from implementation. Player-facing goals are not proof of technical feasibility.
5. Prefer official and established modding systems before invasive hacks.
6. Make the smallest necessary change. Prefer additive, patch-based, injected, wrapped, or event-driven approaches over broad replacements when the target framework supports them.
7. Preserve working architecture and stable identifiers. Never casually regenerate UUIDs, FormIDs, resource keys, namespaces, localization keys, or persistent references.
8. AI output is untrusted until verified. Generated code is a proposal until compiled, validated, loaded, and tested.
9. Never claim a feature is working, fixed, compatible, or safe without evidence.
10. Label uncertainty as VERIFIED, HIGH CONFIDENCE, ASSUMPTION, UNVERIFIED, or NEEDS TESTING.
11. Debug from actual compiler output, logs, crash reports, stack traces, or reproducible behavior. Do not repeatedly guess.
12. Never rewrite a working project from scratch because context was lost. Inspect first and modify surgically.
13. Keep rollback points. Every meaningful working milestone should be recoverable by branch, commit, tag, or archive.
14. Treat saves and persistent state as sacred. Never assume install/update/uninstall is save-safe.
15. Do not silence tests, warnings, or exceptions just to get a green result.
16. Document dependencies, install steps, compatibility, updates, uninstall risks, known issues, and tested versions.
17. Respect licensing and asset rights.
18. The engine sets the limits. If a design cannot be implemented reliably, explain the limitation and propose the closest faithful alternative instead of fabricating support.

## Required workflow
1. Scope the exact player-facing goal.
2. Inspect the existing project and repository.
3. Research the game/framework/version and verify relevant APIs or data structures.
4. Write a feasibility note for any uncertain mechanic.
5. Choose the smallest compatible architecture.
6. Confirm or create a minimal loading baseline.
7. Implement one independently testable feature.
8. Compile/lint/validate/package.
9. Test in a controlled environment.
10. Freeze a working checkpoint and update the project manifest.
11. Regression-test previously working systems.
12. Only then expand.

## Required pre-change gate
Before modifying a working system, determine:
- What currently works?
- What exact requirement is changing?
- What files/systems/identifiers will change?
- What could this break?
- How will the change be verified?
- What is the rollback point?

If those are not known, inspect or research first.

## Definition of done
Report the highest verified state only:
Designed -> Implemented -> Compiles -> Validates -> Loads -> Tested In-Game -> Regression Tested -> Compatibility Tested -> Release Ready

## Repository structure
- `UNIVERSAL_MODDING_RULES.md` — universal hard rules.
- `games/<game>/` — verified game-specific rules and limitations.
- `templates/` — project, testing, and compatibility templates.
- `projects/` — individual mod projects that consume this framework.

## Change policy
Prefer branches and pull requests for meaningful changes. Keep `main` as the stable source of truth. Update `CHANGELOG.md` when behavior, architecture, dependencies, compatibility, or framework rules materially change.
