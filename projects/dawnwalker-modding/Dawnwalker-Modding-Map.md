# Dawnwalker Modding Map

Game install:
D:\steam\steamapps\common\The Blood of Dawnwalker

Active pak folder:
D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks

Active loose mod folder:
D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\~mods

User config folder:
C:\Users\johnf\AppData\Local\Dawnwalker\Saved\Config\Windows

## Rules for installing Nexus Dawnwalker mods

1. Use the logged-in browser and Nexus manual download.
2. Do not use direct command-line Nexus downloads; those fail or hit access checks.
3. Prefer the normal/main file unless the user asks for experimental/optional files.
4. Inspect the ZIP before installing.
5. Install `.pak`, `.ucas`, and `.utoc` into `Dawnwalker\Content\Paks\~mods` unless the mod author explicitly says otherwise.
6. Back up only when replacing an existing same-named file.
7. Restart the game after changing mods.

## Installed Mods

### PlayStation DualSense Button Prompts
Files:
- D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\zzz_DualSenseAtlas_v1_1_P.pak
- D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\zzz_DualSenseAtlas_v1_1_P.ucas
- D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\zzz_DualSenseAtlas_v1_1_P.utoc

What it changes — **VERIFIED 2026-09-04** by fully extracting the container:
- Container: TOC v3, flags `0x09` (Compressed | Indexed), Zlib, **not encrypted**.
  5 chunks = 1 ContainerHeader + 3 ExportBundleData + 1 BulkData.
- Exact paths:
  - `Dawnwalker/Content/_Dawnwalker/UI/_Unified/Settings/Atlas/Frames/T_Image_Controller_Generic.uasset`
  - `Dawnwalker/Content/_Dawnwalker/UI/_Unified/Settings/Atlas/Frames/T_Image_Controller_XBOX.uasset`
  - `Dawnwalker/Content/_Dawnwalker/UI/_Unified/SharedTextures/Controls/Microsoft_Xbox/Textures/Atlas_0.uasset`
  - `…/Atlas_0.ubulk` (2,785,280 bytes)
- It does **not** add PlayStation support — it overwrites the **Xbox** atlas in
  place. That is why the paths say `Microsoft_Xbox`.
- Texture format is `PF_B8G8R8A8` (read from the package name map): uncompressed
  BGRA8, not a block-compressed format. First mip 2,097,152 B = 1024×512×4.
- Proves mod containers may use **Zlib** and **no encryption** even though the base
  game is Oodle + AES.

### Better Story Timer
File:
- C:\Users\johnf\AppData\Local\Dawnwalker\Saved\Config\Windows\Game.ini

Content:
```ini
[/Script/Quest.QuestSettings]
DaysToPass=91
```

What it changes:
- Plain config override. Makes the story timer 91 days.

**VERIFIED 2026-09-04:** `/Script/Quest/QuestSettings` **exists in the shipped
`global.ucas` script-object table** (global index `0x5b782aa1c565ff82`), which is
why the `[/Script/Quest.QuestSettings]` section resolves. The property name
`DaysToPass` is **not** verifiable from shipped data — `global.ucas` stores object
names, not property names — so it rests on the mod working in practice.

The file is marked **read-only** on this install. HIGH CONFIDENCE that is
deliberate, to stop the game rewriting it. NEEDS TESTING whether it is required.

**This is the most important mod on the list**, because its technique needs no
packaging, no key and no tooling — and `games/blood-of-the-dawnwalker/CONFIG_SURFACE.md`
lists **67 shipped settings classes** reachable the same way, including
`DogwoodVampireHungerSettings`, `DogwoodCombatSettings`, `DogwoodBalanceSettings`,
`PoliceSettings`, `HUDVisibilitySettings`, `DrinkBloodSettings` and
`DawnwalkerTraversalSettings`.

There is also a **second, untouched** quest settings class:
`[/Script/DogwoodQuest.DogwoodQuestSettings]`.

### Perks Have No Time Cost
Files:
- D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\~mods\00000000_SkillsNoTimeCost_P.pak
- D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\~mods\00000000_SkillsNoTimeCost_P.ucas
- D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\~mods\00000000_SkillsNoTimeCost_P.utoc

What it changes — **VERIFIED 2026-09-04** by fully extracting the container:
- Container: TOC v8, flags `0x08` (Indexed only) — **uncompressed and unencrypted**.
  113 chunks = 112 `ExportBundleData` + 1 `ContainerHeader`.
- Replaces exactly **112** `DA_Trait_*.uasset` data assets from
  `/Game/_Dawnwalker/Player/CharacterDevelopment/Traits/DataAssets/`.
- The asset class is `/Script/DogwoodCharacterDevelopment/TraitAsset` (resolved
  from `global.ucas`).
- Confirmed: the `.pak` is a 347-byte 0-file stub; payload is in `.ucas`/`.utoc`.
- **What was changed inside each asset is still unknown.** Cooked packages use
  unversioned property serialization, so property names are not stored. Reading
  the actual edited values needs a `.usmap` (KNOWN_LIMITATIONS L3). The author
  almost certainly made byte-level edits to known offsets.
- Related engine symbols: `ETimeCostType`, `GetTimeSegmentCost`, `AddTimeSegments`.
- **Hypothesis worth testing:** the same effect might be reachable through
  `[/Script/DogwoodCharacterDevelopment.DogwoodCharacterDevelopmentSettings]` as a
  few INI lines instead of 112 replaced assets — which would need no AES key.
  See `CONFIG_SURFACE.md`. Unproven.

### Optimized Tweaks BASE (reference, no longer active)
Original backup:
- D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\PerformanceTweaks-backup-20260904-213547\~TBODoptimizedTweaksBASE_P.pak

Readable packed files extracted to:
- C:\Users\johnf\Documents\Codex\2026-07-31\referenced-chatgpt-conversation-this-is-untrusted\dawnwalker_mod_scan\mod42_extracted

What it changes:
- Packed `Engine/Config/Windows/WindowsEngine.ini`.
- Adjusts Unreal console/config values for streaming, shader pipeline cache, D3D12, Lumen, shadows, Niagara, task graph, and input smoothing.
- This is a good template for future config-only mods.

Audit result:
- The generic profile forced a 1280x720 resolution command, four foreground
  workers, a 624 MB Nanite pool, reduced Lumen cache values, and conflicting
  VRS settings.
- Those limits were not appropriate for the installed high-end hardware.

### John RTX 5080 Quality + Smoothness (active custom profile)
Active package:
- D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\~mods\~JohnRTX5080Quality_P.pak

Source:
- profiles/john-rtx5080-quality

Target hardware:
- NVIDIA GeForce RTX 5080, 16 GB VRAM
- AMD Ryzen 9 5900X, 12 cores / 24 threads
- 32 GB RAM
- 3840x2160 display

What it changes:
- Uses an 8192 MB texture pool and a safer 1792 MB Nanite streaming pool.
- Enables supported PSO precaching and D3D12 disk caching.
- Uses a 2048 MB IoDispatcher cache and eight decompression workers sized for
  the 5900X and available system memory.
- Limits large texture and Nanite install bursts to improve frame consistency.
- Enables safe parallel animation, geometry, effects, and shader work.
- Disables mouse smoothing and acceleration.

What it deliberately leaves alone:
- Resolution, screen percentage, DLSS, frame generation, VSync, frame limit,
  ray tracing, Lumen quality, shadows, foliage, post-processing, and VRS.

Installed package SHA-256:
- **Revision 1.1 (current):**
  4C6CD96937480E29C05FD0DE4744AD91D0E1ABA21401F8298530C097CFF1B00B
- Revision 1.0 (superseded, kept in
  `Content\Paks\PerformanceTweaks-backup-20260904-215212\`):
  C3F13F82200FEF32C35511D4182CDFBEFE6DFADBF217F6BB8BFD3D24C73D8F06

Recommended 4K Ultra high-refresh settings:
- Full Screen, NVIDIA DLSS Balanced, DLSS 2x Frame Generation, Unlocked frame
  mode, NVIDIA Reflex On + Boost if available, and in-game VSync Off.

Independent verification (2026-09-04, `profiles/john-rtx5080-quality/verify.py`,
which shares no code with repak or UnrealPak):
- pak version 3, mount point `../../../`, 2 files, nothing encrypted or compressed
- index SHA-1 `aaa4dc78…d964` recomputed from the data and **matched**
- SHA-256 recomputed independently and **matched** the value recorded above, so the
  hash in this file is confirmed by two unrelated toolchains.

Repo/install sync: a desync was flagged earlier on 2026-09-04 (installed 1.1 vs.
repo source 1.0). **Resolved** — Codex pushed the revision 1.1 source to `main`
in "Tune RTX 5080 profile for high refresh stability" / "Document high refresh
Dawnwalker profile". Re-run `verify.py` after any rebuild to confirm they stay in
sync.

## Local Tooling Found

Old UnrealPak:
D:\Vortex Mods\palworld\UnrealPakTool\UnrealPakTool\UnrealPak.exe

Works for listing/extracting simple `.pak` config mods.
Does not reveal contents of Dawnwalker `.ucas/.utoc` payload mods by itself.

repak v0.2.3:
C:\Users\johnf\Documents\Codex\Tools\repak-v0.2.3\repak.exe

Builds and inspects legacy `.pak` archives. Used by `build.ps1`.

In-repo Python readers (no dependencies, no Oodle, no AES):
`games/blood-of-the-dawnwalker/tools/` — `utoc.py`, `extract.py`, `zen.py`,
`globals.py`, `containerheader.py`, `pak.py`. These **do** read Dawnwalker
`.ucas/.utoc` mod containers, which UnrealPak cannot.

## What We Need For Bigger Mods

**Updated 2026-09-04 — this section is now largely answered.** Full detail in
`games/blood-of-the-dawnwalker/`.

What we thought we needed (FModel / UAssetGUI / an Unreal pipeline) turned out to
be needed for only *part* of the problem:

**Already solved — no extra tooling required:**
- Reading and extracting any *mod* `.utoc`/`.ucas` — done, in-repo, pure Python.
  Mod containers use `None`/`Zlib` compression and are unencrypted.
- Reading `global.ucas` — unencrypted (container flags `0x00`). Gave us 54,880
  names and 58,720 script objects, including the game's whole class list.
- **Building config mods** — both the packed `WindowsEngine.ini` shape and the
  loose `Game.ini` shape. See `CONFIG_SURFACE.md`: **67 shipped settings classes**
  are addressable this way, covering hunger, combat, balance, AI, police response,
  HUD visibility, traversal, blood drinking, quests and the time system.

**Still genuinely blocked:**
1. **The AES-256 key.** `Dawnwalker-Windows.utoc` has container flags `0x0b`
   (`Compressed | Encrypted | Indexed`). Base assets cannot be read without it,
   so every asset-replacement mod is blocked. Options in KNOWN_LIMITATIONS L1.
2. **An Oodle decompressor.** The base container uses Oodle and no `oo2core*.dll`
   ships with the game (it is statically linked). Needed only for *reading* the
   base container — never for writing mods.
3. **A `.usmap` mappings file.** Cooked data assets use unversioned property
   serialization: property names are not stored anywhere in the shipped data.
   Needed to interpret `DA_Trait_*` style assets, and to learn the property names
   on the 67 settings classes above.

Practical order of work: config mods now → `.usmap` next (unblocks a lot cheaply)
→ AES key last (only if asset replacement is actually wanted).

(Superseded note, kept for history: this section previously said we needed FModel /
UAssetGUI or a full Unreal pipeline. That is now true only for cooked Data Asset
replacement, not for reading containers or building config mods.)
