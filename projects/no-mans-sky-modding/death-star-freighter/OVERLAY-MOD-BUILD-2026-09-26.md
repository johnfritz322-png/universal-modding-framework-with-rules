# Death Star overlay mod build — 2026-09-26

## Result

**VALIDATED PACKAGE — not yet installed or tested in game.**

`DeathStar-Freighter-Overlay-Cosmos-7.04.pak` was built for the locally
observed Cosmos 7.04 Steam build (`25441199`). It is a reversible overlay of
the stock industrial capital-freighter root scene, not a save edit and not a
base-game archive replacement.

## Contents

The archive contains exactly four files:

1. An overridden
   `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN`.
   It retains the stock scene graph and adds one `REFERENCE` child named
   `DeathStarExteriorOverlay` that points at the custom shell.
2. The custom shell scene.
3. Its geometry stream.
4. Its geometry-data stream.

The stock capital scene was compiled from MXML and decompiled again. The
result retains the injected `SCENEGRAPH` value exactly. The finished archive
was reopened and each of its four extracted files matched its staged source
byte-for-byte by SHA-256.

## Behavior and limits

- The overlay affects the Industrial Capital Freighter scene family, rather
  than proving a personal-only seed selection. Mothership uses this family.
- The stock functional hierarchy stays present below the added shell.
- No save, ship stat, crew, name, inventory, interior, collision, or base
  data was changed.
- The stage-3 aperture is visual-only. Docking, collision, performance, and
  in-game loading are **NEEDS TESTING**.

## Installation and rollback

Install only while No Man's Sky is closed. First copy the entire existing
`GAMEDATA/PCBANKS/MODS` folder to a dated backup. Then copy the package into
that `MODS` folder. If `GAMEDATA/PCBANKS/DISABLEMODS.TXT` is present, move it
to the same backup rather than deleting it. Launch the game and test only
Mothership: summon, approach, dock, enter, exit, save, reload, and warp.

To roll back, close the game, remove this package from `MODS`, and restore the
backed-up `MODS` folder and `DISABLEMODS.TXT` if it existed. No save restore
should be necessary because this package does not edit saves.

## Build tooling

- `tools/build_overlay_mod.py` creates the stock-scene MXML overlay staging
  tree and copies the verified original shell assets.
- `tools/pack_overlay_mod.py` accepts only the intended four non-MXML files,
  packs them with HGPAKtool, and byte-verifies the archive extraction.
