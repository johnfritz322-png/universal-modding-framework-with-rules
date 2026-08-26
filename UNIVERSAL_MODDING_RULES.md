# Universal AI Game Modding Rules

These rules apply across games unless a game-specific file explicitly narrows or replaces an implementation detail.

## Core directive
Do not guess your way through game modding. Verify the target environment, preserve working systems, make the smallest compatible change, and never claim success beyond the evidence available.

## Hard rules

### 1. Verify before coding
Never invent APIs, hooks, functions, IDs, UUIDs, FormIDs, blueprint names, records, events, commands, folder structures, file schemas, dependency versions, engine behavior, or loader behavior.

### 2. Establish the exact environment first
Identify game, game build/version, platform, engine where relevant, loader/framework, toolkit/SDK, extender, dependencies, runtime/compiler, and materially overlapping mods.

### 3. Research before architecture
Determine what the current game and modding ecosystem expose, then map requested features to verified capabilities.

### 4. Separate design from implementation
Keep the player-facing fantasy separate from the technical implementation. A design can remain stable while the implementation changes.

### 5. Prefer native and established systems
Use official SDKs, supported APIs, established loaders, scripting systems, data tables, hooks, events, and patch systems before invasive methods.

### 6. Make the smallest necessary change
Touch the fewest files, records, methods, assets, hooks, or systems required.

### 7. Compatibility is a design requirement
Minimize collision surfaces, avoid unnecessary ownership of vanilla resources, use unique namespaces/identifiers, and isolate compatibility logic.

### 8. Prefer additive/chainable changes over destructive replacement
When the framework supports it, prefer adding, extending, patching, injecting, wrapping, or subscribing over replacing whole systems.

### 9. Avoid modifying original assets unless required
Prefer new assets/files and non-destructive patches. If replacement is necessary, document it and expected conflicts.

### 10. Dependencies must be real and explicit
Verify that every dependency exists, is actually required, and supports the target version.

### 11. Understand conflict and load behavior
Do not assume every game uses the same load-order or file-conflict model.

### 12. Automatic sorting is not compatibility proof
Sorters and managers can help order mods but cannot prove runtime compatibility.

### 13. Use compatibility patches when appropriate
Keep integrations or patches separate from the core mod where practical.

### 14. Build one system at a time
Establish a minimal loading baseline, add one system, verify it, create a rollback point, then continue.

### 15. Never stack unresolved failures
Do not move to the next major feature while unexplained compiler errors, crashes, validation errors, missing references, or reproducible abnormal behavior remain.

### 16. AI output is untrusted until verified
Generated code and instructions are proposals until they compile, validate, load, and behave correctly.

### 17. Never hallucinate success
Do not claim working/fixed/compatible/tested/safe without evidence.

### 18. Label uncertainty
Use VERIFIED, HIGH CONFIDENCE, ASSUMPTION, UNVERIFIED, or NEEDS TESTING.

### 19. Debug from evidence
Use compiler output, logs, crash reports, stack traces, validator results, and reproducible steps.

### 20. Preserve working systems
Do not rewrite functioning architecture to solve unrelated problems without evidence.

### 21. Never rebuild from scratch because context was lost
Inspect the existing project, repository history, identifiers, and working implementation first.

### 22. Keep rollback points
Use version control or archives for meaningful milestones and before risky changes.

### 23. Maintain stable unique identifiers
Do not casually regenerate persistent identifiers, internal names, localization keys, or resource IDs.

### 24. Treat saves and persistent state as sacred
Never assume mod install/update/removal is save-safe. Test according to the target engine's persistence behavior.

### 25. Test incrementally in a controlled environment
At minimum test install/load, activation, expected behavior, failure behavior, reload/restart where relevant, and update/removal behavior where applicable.

### 26. Fail gracefully where possible
Missing optional dependencies or unsupported states should disable only affected functionality when the framework allows.

### 27. Log what matters
Development builds should expose useful information for initialization, dependencies, registration, hook installation, scripting, and runtime failures.

### 28. No mystery code
Every significant code/config block must have a traceable purpose.

### 29. Do not silence errors to make a build pass
Do not disable tests, validation, warnings, or exceptions merely to produce a green result.

### 30. Review destructive and privileged actions
Inspect shell commands, deletion, registry/config edits, downloads, package installs, executable patches, and privileged operations before execution.

### 31. Respect licensing and asset rights
Verify permissions before redistributing code, models, textures, audio, animations, or proprietary game content.

### 32. Use clear versioning and changelogs
Record the tested game/framework versions and material changes.

### 33. Document installation and compatibility
Releases require setup instructions, dependencies, supported versions, conflict notes, update/uninstall warnings, and known limitations.

### 34. Maintain a project manifest
Every serious mod should track environment, dependencies, owned files, stable IDs, systems touched, compatibility, verified features, experimental features, bugs, tests, and rollback state.

### 35. Preserve reproducibility
Record exact build/package steps and avoid undocumented manual edits.

### 36. The engine sets the limits
If a requested design cannot be implemented reliably, propose the closest faithful implementation and explain the limitation instead of fabricating support.

## Evidence ladder
1. **VERIFIED — Primary:** official game/SDK documentation; actual game/project files; compiler/validator output; direct in-game test.
2. **VERIFIED — Framework:** maintainer documentation for the exact loader/extender/toolkit/API version.
3. **HIGH CONFIDENCE:** known-working open-source mod using the same relevant system/version.
4. **MODERATE:** well-maintained community documentation corroborated by working examples or multiple sources.
5. **LOW:** isolated forum/Discord/Reddit/video claim without direct verification.
6. **UNVERIFIED:** AI inference, memory, guess, or extrapolation.

## Required development loop
Scope -> Inspect -> Research -> Feasibility -> Architecture -> Baseline -> Implement -> Validate -> Test -> Freeze -> Expand -> Regression -> Compatibility -> Release
