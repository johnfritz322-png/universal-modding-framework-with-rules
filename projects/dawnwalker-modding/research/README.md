# Dawnwalker Reverse Engineering

This folder holds the working map for The Blood of Dawnwalker reverse engineering.

## Current Findings

- The current game build is Steam app `3751260`, build `25129649`.
- The base game container `Dawnwalker-Windows.utoc/.ucas` is encrypted and Oodle-compressed.
- `global.ucas` is readable and exposes script/module names.
- The progression system is `DogwoodCharacterDevelopment`.
- The installed `00000000_SkillsNoTimeCost_P` mod contains 112 `DA_Trait_*` cooked trait assets.
- Cooked trait assets expose names, imports, classes, and linked gameplay effects, but not enough property labels to safely make arbitrary balance edits without mappings.

## Files

- `PROGRESSION_RE.md`: readable summary of ability, level, trait, XP, and mutation findings.
- `trait-asset-catalog.csv`: catalog of the 112 trait assets from the installed no-time-cost mod.
- `character-development-scriptobjects.csv`: script-object rows for `DogwoodCharacterDevelopment` and related debug focus hooks.

## Local-Only Extracts

`research/extracted/` is intentionally ignored by git. It can hold extracted reference assets for local inspection, but those are generated/copy-derived files and should not be treated as source.

