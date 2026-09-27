# Stage 4 overlay clean rebuild and redeploy — 2026-09-27

## Result

**DEPLOYED — awaiting in-game visual test. Not yet confirmed working.**

## What was reviewed

Read every death-star-freighter doc and tool script, plus the Codex commit
history on `codex/death-star-freighter-progress-20260925`, alongside
`CLAUDE-CONTINUATION-HANDOFF-2026-09-26.md`. Findings:

1. The additive stock-scene-plus-REFERENCE overlay (one new `SCENEGRAPH`
   child node, original scene graph otherwise untouched) is the correct,
   minimal approach. A later **direct full-scene replacement**
   (`CAPITALFREIGHTER_PROC.SCENE.MBIN` fully rebuilt, not referenced)
   discarded the stock hangar/locator graph and broke Mothership summoning
   in the live game. That direct-replacement approach is abandoned; it is
   unsafe by construction, not just unfinished.
2. **Root cause of "every screenshot showed stock only":** work alternated
   between two different loose-mod locations without confirming which one
   this installation's loader actually reads —
   `GAMEDATA/PCBANKS/MODS` (older per-bank-archive convention, used for the
   `.pak` builds in `OVERLAY-MOD-BUILD-2026-09-26.md`) versus
   `GAMEDATA/MODS` (used for the later loose-EXML/MXML attempts). Checked
   directly on-disk: `GAMEDATA/PCBANKS/MODS` contains nothing but a Vortex
   pictures folder, while `GAMEDATA/MODS` is Vortex's actual
   `hardlink_activator` deployment target (see its
   `vortex.deployment.json`) and is where the already-working
   `CorvetteOverhaul` mod's loose files live. **`GAMEDATA/MODS` is the real,
   active loose-mod folder for this install.** Any `.pak` built for
   `PCBANKS/MODS` would never have loaded, independent of any geometry or
   reference-prefix fix.
3. The project accumulated a very large number of ad-hoc scratch build
   directories outside the repo (`death-star-overlay-mod-staging`,
   `-v2`, `-v5`, `-verify*`, `DeathStarFreighterOverlay-EXML-stage4/5/6`,
   etc.) with no single source of truth, which made it hard to tell which
   build was actually last deployed. This doc records the exact one clean
   build now live.

## What was rebuilt

- Re-exported the shell geometry with `tools/build_death_star_silhouette_stage3.py --reverse-winding`
  (Stage 4: corrected face winding so the exterior renders instead of only
  the far interior hemisphere) through the dedicated Blender 5.0.1 + NMSDK
  profile. 4703 verts, 4604 faces.
- Generalized `tools/build_overlay_mod.py` and `tools/pack_overlay_mod.py`
  to take `--shell-name` instead of hard-coding `STAGE3`, so the verified
  additive-overlay pipeline could be reused for Stage 4 without duplicating
  scripts.
- Built the overlay staging tree from a **confirmed pristine stock**
  `CAPITALFREIGHTER_PROC.SCENE.MXML` (verified `grep`-clean of any prior
  `DeathStar` reference; matches two independently decompiled copies from
  2026-09-24/25) plus the Stage 4 shell. Added exactly one `REFERENCE`
  child node, `DeathStarExteriorOverlay`, pointing at
  `//CUSTOMMODELS\DEATH_STAR_SILHOUETTE_STAGE4\DEATH_STAR_SILHOUETTE_STAGE4.SCENE.MBIN`.
  Root child count went from 4 to 5 — nothing existing was removed or
  altered.
- Compiled the modified MXML with MBINCompiler v7.04.0-pre1, then
  decompiled the result back to EXML to confirm: the injected reference is
  present and correctly formed, and the entire original scene graph
  (all pre-existing `SCENEGRAPH` nodes/locators) is byte-for-byte still
  there.
- Packed the four required files with `pack_overlay_mod.py`; HGPAKtool
  round-trip byte-verified (`OVERLAY_ARCHIVE=passed ... byte_identical=true`).
  The `.pak` itself was not used for deployment (see root-cause note above)
  but stands as a verified reference build at
  `2026-09-27/DeathStar-Overlay-Stage4.pak`.

## Deployment

The same four compiled files (MXML/EXML source excluded, matching prior
practice) were copied as loose files into
`GAMEDATA/MODS/DeathStarFreighterOverlay/` and byte-compared against the
verified staging tree — all four matched exactly:

- `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN`
- `CUSTOMMODELS/DEATH_STAR_SILHOUETTE_STAGE4/DEATH_STAR_SILHOUETTE_STAGE4.SCENE.MBIN`
- `CUSTOMMODELS/DEATH_STAR_SILHOUETTE_STAGE4/DEATH_STAR_SILHOUETTE_STAGE4.GEOMETRY.MBIN.PC`
- `CUSTOMMODELS/DEATH_STAR_SILHOUETTE_STAGE4/DEATH_STAR_SILHOUETTE_STAGE4.GEOMETRY.DATA.MBIN.PC`

Prior stray mod folders (the broken direct-replacement build and an
unrelated `NoCoordsPrompt` mod) were moved out to
`2026-09-26/who-x20/work/backups/restored-20260926-213947/` before this
redeploy, so the live `GAMEDATA/MODS` now contains only known-good mods
plus this one new overlay.

## Scope and limits — unchanged from prior findings

- No save, ship stat, crew, name, inventory, or collision data was
  changed. The stock hangar/locator graph is fully intact underneath the
  added reference.
- This is a **visual-only** shell. Docking, collision, and clearance
  remain unverified per `RUNTIME-ATTACHMENT-EVIDENCE-PLAN.md`; that gate is
  still open. Do not treat a successful visual load as proof this is safe
  to dock or fly through.
- **NEEDS TESTING**: whether this renders as an opaque exterior shell over
  Mothership at all. Launch the game, summon Mothership, and look — do not
  attempt to dock into the shell opening until collision is separately
  verified.

## Rollback

Close the game, delete `GAMEDATA/MODS/DeathStarFreighterOverlay/`. Nothing
else in `GAMEDATA/MODS` was touched by this change.
