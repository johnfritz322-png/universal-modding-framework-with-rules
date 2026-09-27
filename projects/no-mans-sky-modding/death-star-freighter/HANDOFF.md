# Death Star freighter — current handoff

Updated 2026-09-25 UTC. **Start with [WHATS-NEXT.md](WHATS-NEXT.md).**
This checkpoint is on codex/death-star-nmsdk-fix, based on canonical
claude/death-star-freighter-mod-iteration at 2a57866.

## Completed

- Design remains the original spherical exterior for the already-owned
  S-class Mothership, with offset concave dish, equatorial trench and clear
  hangar access. See DEATH-STAR-BUILD-BRIEF.md and concept-reference.html.
- The missing hgpaktool import is repaired in portable Blender 4.5.14.
  NMSDK registration, operators, preferences and archive payload checks pass.
- The SDK extension manifest requires Blender >=5.0.0. A dedicated profile
  using the existing Blender 5.0.1 now starts with NMSDK enabled in a fresh
  process. No source patches or reduced version requirements were needed.
- HGPAKtool 1.1.3 and MBINCompiler 7.03.2.1 have passed specific archive and
  no-edit conversion checks. The latter version string is from the same
  executable previously labelled v7.03.2-pre1, not evidence of an upgrade.
- Current game data identifies the actual capital hull under INDUSTRIAL.
  Its descriptor and AI model mapping are in NMSARC.Precache.pak; both
  passed no-edit round trips. BIGGS is explicitly a Corvette.
- Local HANGARROOTA/B locators were found. Their gameplay role and world
  positions still require verification.

## Evidence and saved work

- NMSDK-REPAIR-2026-09-25.md: precise fix, versions, hashes, restart tests,
  dedicated-profile launch commands and rollback.
- FREIGHTER-SELECTION-FINDINGS.md: archive paths, literal IDs, descriptor
  structure, locator ancestry, hashes, commands and bounded conclusions.
- tools/verify_nmsdk_load.py: repeatable add-on and archive validation.
- TOOLCHAIN-RESULTS-2026-09-25.md: historical pre-repair report; its missing
  dependency blocker is superseded by this checkpoint.
- WHATS-NEXT.md: ordered resume steps and all important local paths.

## Remaining work

1. Review/incorporate this branch into the canonical branch while preserving
   any newer work; fetch explicitly because the original clone fetched main only.
2. Identify Mothership's actual resource and seed fields read-only. Verify
   how they relate to the capital scene and descriptor.
3. Prove a minimal current-build scene and geometry import/export using the
   working Blender 5.0.1 profile. NMSDK loading does not prove model export.
4. Choose the smallest architecture supported by those findings. The
   earlier proposed table-row plus seed mechanism is UNVERIFIED; a
   personal-only additive hull is not established by the observed AI mapping.
5. Measure donor bounds, accumulated transforms and the docking route.
   Preserve all functional components while producing the desired silhouette.
6. Before any installation or save write: verify backups, rollback and
   target identity, then test docking/walking/exit/reload/summon/warp and
   freighter base behavior, checking that existing stats/class/crew persist.

## Active limitations

NMSDK's dependency blocker is resolved. The open gates are owned-freighter
selection, geometry import/export, and gameplay validation. No target save
has been read or edited in this checkpoint. The broad claim that one globals
round trip proves the entire toolchain safe was too strong; checks establish
only the tested operations and files.

Highest state for the Death Star mod: **Designed / scratch geometry verified**.
An original sphere/dish/trench/aperture mesh exports and re-imports through
NMSDK, but no mod package, installation, or in-game test has been completed.
The user's game files and saves were unchanged.
