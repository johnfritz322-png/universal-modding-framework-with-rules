# Dawnwalker — the config-mod surface

**This is the roadmap for making more mods without the AES key.**

Every class below is a `UObject` settings class that exists in the **shipped**
`global.ucas` script-object table. In Unreal, such a class is addressable from an
INI file as `[/Script/<Module>.<ClassName>]`, and its `config`-marked properties can
be overridden.

**The technique is already proven on this game.** The installed *Better Story Timer*
mod is nothing but a two-line file at
`%LOCALAPPDATA%\Dawnwalker\Saved\Config\Windows\Game.ini`:

```ini
[/Script/Quest.QuestSettings]
DaysToPass=91
```

`/Script/Quest/QuestSettings` is **VERIFIED** present in the shipped tables
(global index `0x5b782aa1c565ff82`), which is why that section name resolves.

---

## Important caveat before you use this list

| Claim | State |
|---|---|
| These classes exist in the shipped build | **VERIFIED** — read from `global.ucas` |
| The `[/Script/Module.Class]` section name is therefore valid | **VERIFIED** |
| Which *properties* each class has | **UNVERIFIED — not obtainable from `global.ucas`** |
| Which properties are `config`-writable | **UNVERIFIED** |

`global.ucas` contains **object** names (classes, enums, structs, functions, CDOs).
It does **not** contain property names. So this list tells you *where to aim*, not
what to type. To get actual property names you need one of:

1. a **`.usmap`** dumped from the running game (Dumper-7 / UE4SS), or
2. the game's own log — UE warns about unknown INI keys, so a wrong guess is
   visible, or
3. trial and error against a known-good example (`DaysToPass` above).

**Do not invent property names.** Per `AGENTS.md` rule 1, a guessed property name is
exactly the kind of fabrication this framework exists to prevent.

---

## Gameplay settings classes (56)

Highest modding interest marked ★.

| INI section | Module | Why it's interesting |
|---|---|---|
| `[/Script/Quest.QuestSettings]` | Quest | ★ **PROVEN** — `DaysToPass` drives the story clock |
| `[/Script/Quest.QuestWorldSettings]` | Quest | per-world quest config |
| `[/Script/DogwoodQuest.DogwoodQuestSettings]` | DogwoodQuest | ★ game-specific quest layer, untouched by any known mod |
| `[/Script/DogwoodQuest.CourtSettings]` | DogwoodQuest | the Court system |
| `[/Script/DogwoodVampireHunger.DogwoodVampireHungerSettings]` | DogwoodVampireHunger | ★ hunger mechanics |
| `[/Script/DogwoodVampireHunger.VampireHungerPostProcessSettings]` | DogwoodVampireHunger | hunger visual FX |
| `[/Script/DogwoodVampireHunger.VampireHungerLevelPostProcessSettings]` | DogwoodVampireHunger | per-level hunger FX |
| `[/Script/DogwoodSystem.DogwoodBalanceSettings]` | DogwoodSystem | ★ global balance |
| `[/Script/DogwoodSystem.TimeSystemUserSettings]` | DogwoodSystem | ★ time system — pairs with the story clock |
| `[/Script/DogwoodSystem.DogwoodSystemSettings]` | DogwoodSystem | core system config |
| `[/Script/DogwoodSystem.DogwoodSystemWorldSettings]` | DogwoodSystem | per-world system config |
| `[/Script/DogwoodSystem.CreaturesSettings]` | DogwoodSystem | creature config |
| `[/Script/DogwoodSystem.DogwoodPhotomodeSettings]` | DogwoodSystem | photo mode |
| `[/Script/DogwoodSystem.PhotoCamSettings]` | DogwoodSystem | photo camera |
| `[/Script/DogwoodCharacterDevelopment.DogwoodCharacterDevelopmentSettings]` | DogwoodCharacterDevelopment | ★★ **see hypothesis below** |
| `[/Script/DogwoodCombat.DogwoodCombatSettings]` | DogwoodCombat | ★ combat tuning |
| `[/Script/DogwoodCombat.MetricsScalingSettings]` | DogwoodCombat | combat scaling |
| `[/Script/DogwoodCombat.DWLeftPoseSettings]` | DogwoodCombat | pose config |
| `[/Script/DogwoodStats.DogwoodStatsSettings]` | DogwoodStats | ★ stats |
| `[/Script/DogwoodInventory.DogwoodInventorySettings]` | DogwoodInventory | ★ inventory rules |
| `[/Script/DogwoodInventory.GlobalAppearanceSettings]` | DogwoodInventory | appearance |
| `[/Script/DogwoodWorld.DogwoodWorldSettings]` | DogwoodWorld | world config |
| `[/Script/DogwoodWorld.PoliceSettings]` | DogwoodWorld | ★ guard/police response |
| `[/Script/DogwoodWorld.RegionPoliceSettings]` | DogwoodWorld | per-region response |
| `[/Script/DogwoodWorld.LootPanelSettings]` | DogwoodWorld | loot UI |
| `[/Script/DogwoodUI.HUDVisibilitySettings]` | DogwoodUI | ★ HUD elements — minimal-HUD mods |
| `[/Script/DogwoodUI.DogwoodUISettings]` | DogwoodUI | UI config |
| `[/Script/DogwoodUI.DogwoodHUBSettings]` | DogwoodUI | hub UI |
| `[/Script/DogwoodUI.DogwoodCourtUISettings]` | DogwoodUI | court UI |
| `[/Script/DogwoodUI.DogwoodTextSettings]` | DogwoodUI | text |
| `[/Script/DogwoodUI.DogwoodUIAudioSettings]` | DogwoodUI | UI audio |
| `[/Script/DogwoodMap.DogwoodMapSettings]` | DogwoodMap | map/mappins |
| `[/Script/DogwoodAI.DogwoodAISettings]` | DogwoodAI | ★ AI behaviour |
| `[/Script/DogwoodFocus.DogwoodFocusSettings]` | DogwoodFocus | focus system |
| `[/Script/DogwoodDialogue.DogwoodDialogueSettings]` | DogwoodDialogue | dialogue |
| `[/Script/DogwoodDialogue.VoiceSetChatSettings]` | DogwoodDialogue | voice sets |
| `[/Script/DogwoodGlossary.DogwoodGlossarySettings]` | DogwoodGlossary | glossary |
| `[/Script/DogwoodAudio.DogwoodAudioSettings]` | DogwoodAudio | audio |
| `[/Script/DogwoodAchievements.DogwoodAchievementsSettings]` | DogwoodAchievements | achievements |
| `[/Script/DogwoodUtil.DogwoodPostProcessSettings]` | DogwoodUtil | post-processing |
| `[/Script/DogwoodUtil.DogwoodStringTableSettings]` | DogwoodUtil | string tables |
| `[/Script/DogwoodEditor.AssetListSettings]` | DogwoodEditor | asset lists |

### The `/Script/Dawnwalker` module

A module distinct from the `Dogwood*` ones — the game-title layer.

| INI section | Why it's interesting |
|---|---|
| `[/Script/Dawnwalker.DawnwalkerSettings]` | ★ top-level game settings |
| `[/Script/Dawnwalker.DawnwalkerUserSettings]` | ★ user-facing settings |
| `[/Script/Dawnwalker.DrinkBloodSettings]` | ★ the blood-drinking mechanic |
| `[/Script/Dawnwalker.DawnwalkerTraversalSettings]` | ★ movement / traversal |
| `[/Script/Dawnwalker.ShadowstepCameraBlendSettings]` | shadowstep camera |
| `[/Script/Dawnwalker.PlayerConfigSettings]` | ★ player config |
| `[/Script/Dawnwalker.DawnwalkerPetSettings]` | pet system |
| `[/Script/Dawnwalker.DawnwalkerWorldSettings]` | world |
| `[/Script/Dawnwalker.DawnwalkerSignificanceSettings]` | significance / LOD budgeting |
| `[/Script/Dawnwalker.DawnwalkerAudioSettings]` | audio |
| `[/Script/Dawnwalker.DogwoodAudioLocalSettings]` | local audio |
| `[/Script/Dawnwalker.TrailDecalSettings]` | trail decals |
| `[/Script/Dawnwalker.CachedDialogueTransitionSettings]` | dialogue transitions |
| `[/Script/Dawnwalker.CachedDialogueEndTransitionSettings]` | dialogue end transitions |

## Editor / debug settings classes (11)

These shipped in the retail build. Whether any of them do anything in a cooked,
non-editor build is **UNVERIFIED** — but `DogwoodDebugSettings` and
`DogwoodAutomationDeveloperSettings` are worth probing for debug/free-camera style
functionality.

| INI section | Module |
|---|---|
| `[/Script/DogwoodDebug.DogwoodDebugSettings]` | DogwoodDebug |
| `[/Script/DogwoodAutomatedTesting.DogwoodAutomationDeveloperSettings]` | DogwoodAutomatedTesting |
| `[/Script/DogwoodEditor.DogwoodEditorDeveloperSettings]` | DogwoodEditor |
| `[/Script/DogwoodEditor.DogwoodEditorProjectSettings]` | DogwoodEditor |
| `[/Script/DogwoodEditor.DogwoodEditorToolSettings]` | DogwoodEditor |
| `[/Script/DogwoodEditor.PropertiesValidatorDeveloperSettings]` | DogwoodEditor |
| `[/Script/DogwoodMap.DogwoodMapsEditorSettings]` | DogwoodMap |
| `[/Script/DogwoodStats.DogwoodStatsEditorSettings]` | DogwoodStats |
| `[/Script/DogwoodWorld.WorldEditorUserSettings]` | DogwoodWorld |
| `[/Script/Quest.QuestEditorUserSettings]` | Quest |
| `[/Script/Dawnwalker.DogwoodAudioEditorSettings]` | Dawnwalker |

---

## ★★ Hypothesis worth testing first

**HYPOTHESIS, NOT A FINDING.** The installed *Perks Have No Time Cost* mod achieves
its effect by shipping **112 replaced `DA_Trait_*` data assets** in an IoStore
container — the expensive path, which needs the base assets and therefore the AES
key.

`/Script/DogwoodCharacterDevelopment/DogwoodCharacterDevelopmentSettings` exists in
the shipped build. The engine also exposes `ETimeCostType` and `GetTimeSegmentCost`.
**If** the per-trait time cost is driven by a `config` property on that settings
class, the same result could be achieved by a handful of INI lines instead of 112
replaced assets — no key, no IoStore, no Oodle.

This is unproven and may be false: the cost may live purely on each data asset, in
which case no config override reaches it. But it is cheap to test and would remove
the AES-key blocker for one of the most popular mods on this game.

**Next verification step:** dump a `.usmap` and inspect the property list of
`DogwoodCharacterDevelopmentSettings`.

---

## How to regenerate this list

```bash
python tools/globals.py          # writes scriptobjects.json
```

Then filter `scriptobjects.json` for paths matching
`/Script/<Module>/<Name>Settings` with exactly two segments after `/Script/`
(three segments means it is a function on the class, not a class), restricted to
modules starting with `Dogwood` or named `Quest` / `Dawnwalker`.

Counts as of 2026-09-04: **67** game settings classes (56 gameplay, 11 editor) out
of 1,183 across all 705 modules in the build.
