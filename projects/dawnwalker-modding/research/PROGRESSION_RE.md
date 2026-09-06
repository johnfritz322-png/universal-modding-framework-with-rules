# Progression Reverse Engineering

Analysis date: 2026-09-05.

## Short Version

DW's ability/skill progression lives in the `DogwoodCharacterDevelopment` module.
The game exposes real script objects for level, XP, mutation, trait points, trait unlocks, and equipped abilities. This is the right target area for skill-point, ability-level, XP, and perk-tree mods.

The save files are binary and did not expose a readable `AbilityLevel=0` style field. Direct save byte-editing is therefore not the safe first route.

## Current Game Fingerprint

- Game install: `D:\steam\steamapps\common\The Blood of Dawnwalker`
- Steam app: `3751260`
- Steam build: `25129649`
- Game exe hash: `7ad7d09645b0589dc0ff78b53aa1a7b18eca79b1b7f888b403ab41d88ac7e853`
- Main TOC hash: `7cf811c2a52e0f56ed9dc385168d1d871519ba99664eb18ced895c9ce14bc614`
- `global.ucas` hash: `0ecfc5f66e6f52733787c85c9bba237b626b730623dd64b361e42515e0ad1cd5`

## Verified Progression Surface

From the readable global script-object table:

- `/Script/DogwoodCharacterDevelopment/CharacterDevelopmentSubsystem`
- `/Script/DogwoodCharacterDevelopment/DogwoodCharacterDevelopmentSettings`
- `/Script/DogwoodCharacterDevelopment/TraitAsset`
- `/Script/DogwoodCharacterDevelopment/TraitLevel`
- `/Script/DogwoodCharacterDevelopment/TraitLevelRequirements`
- `/Script/DogwoodCharacterDevelopment/LevelUpXPRequirementRow`
- `/Script/DogwoodCharacterDevelopment/VampireMutationLevelRow`

High-value functions present in the shipped build:

- `ForceLevelUp`
- `ForceLevelUpTo`
- `AddQuestXP`
- `GetCurrentLevel`
- `GetCurrentXP`
- `GetCurrentLevelXPRequirement`
- `GetCurrentMutationLevel`
- `AddMutationCharges`
- `ReceiveTraitPoints`
- `SetTraitPointsAmount`
- `SpendTraitPoints`
- `UnlockTrait`
- `UnlockAllTraits`
- `UnlockRandomTrait`
- `UnblockTraitNextLevel`
- `UnblockTraitToLevel`
- `SetTraitEquipped`
- `GetEquippableAbilities`
- `GetEquippedAbilities`
- `SetAbilityInSlot`

Related focus debug hooks:

- `/Script/DogwoodFocus/FocusAbilitiesSubsystem/UnlockAllFocusAbilities_Debug`
- `/Script/DogwoodFocus/FocusAbilitiesSubsystem/ToggleDisablingAllCooldowns_Debug`

## Trait Asset Map

The installed `00000000_SkillsNoTimeCost_P` mod is an IoStore asset mod:

- `D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\~mods\00000000_SkillsNoTimeCost_P.pak`
- `D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\~mods\00000000_SkillsNoTimeCost_P.ucas`
- `D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\~mods\00000000_SkillsNoTimeCost_P.utoc`

Its `.utoc` lists 113 chunks:

- 112 `ExportBundleData` chunks, each one a `DA_Trait_*` cooked asset.
- 1 `ContainerHeader` chunk.

Trait group counts:

- CombatFocus: 45
- Human: 21
- Shared: 24
- Vampire: 20
- Edict: 2

The asset class is `/Script/DogwoodCharacterDevelopment/TraitAsset`.

See `trait-asset-catalog.csv` for the full list.

## What The Cooked Assets Reveal

Representative parsed assets show:

- package path
- local name map
- imported script classes
- linked gameplay effect class names such as `GE_Trait_*_Level_1_C`
- localization keys such as `CombatFocus_Kick_LocalizedName`
- one exported `TraitAsset`

Example: `DA_Trait_CombatFocus_Kick.uasset`

- Package path: `/Game/_Dawnwalker/Player/CharacterDevelopment/Traits/DataAssets/DA_Trait_CombatFocus_Kick`
- Class: `/Script/DogwoodCharacterDevelopment/TraitAsset`
- Export serial size: 525 bytes
- Names: 6

Example: `DA_Trait_Human_HexDuration.uasset`

- Package path: `/Game/_Dawnwalker/Player/CharacterDevelopment/Traits/DataAssets/DA_Trait_Human_HexDuration`
- Class: `/Script/DogwoodCharacterDevelopment/TraitAsset`
- Linked effects: `GE_Trait_Human_HexDuration_Level_1_C` through `_Level_4_C`
- Names: 32

## Current Blockers

Base game asset extraction is blocked by two separate issues:

- AES key: the base container is encrypted.
- Oodle: the base container uses Oodle compression.

Arbitrary cooked asset editing is blocked by a third issue:

- `.usmap` mappings are needed to map binary unversioned properties back to names.

Without a `.usmap`, we can identify assets and byte-level patterns, but we should not pretend we know every property.

## Safest Modding Routes Right Now

Ready now:

- Engine/config performance paks.
- Loose `Game.ini` gameplay config overrides where property names are known.
- Mods modeled on existing working paks, if we can isolate exact byte changes.

Next unlock:

- Install a DW-compatible UE4SS/mapping dumper and produce a `.usmap`.
- Use that mapping to inspect `DogwoodCharacterDevelopmentSettings`, `TraitAsset`, `TraitLevel`, and XP/mutation structs.

Once mappings exist, the best first real gameplay mods are:

- John skill-point/progression mod.
- XP multiplier or faster leveling.
- trait unlock freedom mod.
- vampire mutation tuning.
- ability cooldown/cost tuning.

