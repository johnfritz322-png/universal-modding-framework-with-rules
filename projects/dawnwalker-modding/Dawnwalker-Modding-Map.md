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

What it appears to change:
- Controller UI texture assets.
- Visible paths from `.utoc`: `_Dawnwalker/_Unified/Settings/Atlas/Frames`, `SharedTextures/Controls/Microsoft_Xbox/Textures`, `T_Image_Controller_Generic.uasset`, `T_Image_Controller_XBOX.uasset`, `Atlas_0.uasset`, `Atlas_0.ubulk`.
- Likely overrides Xbox/generic controller atlas art with DualSense prompts.

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

### Perks Have No Time Cost
Files:
- D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\~mods\00000000_SkillsNoTimeCost_P.pak
- D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\~mods\00000000_SkillsNoTimeCost_P.ucas
- D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\~mods\00000000_SkillsNoTimeCost_P.utoc

What it appears to change:
- Trait/skill data assets named `DA_Trait_*`.
- The `.pak` only provides the mount shell; payload is in `.ucas/.utoc`.
- Likely edits Data Asset values for skill unlock or time cost.

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
- Uses an 8192 MB texture pool and 2048 MB Nanite streaming pool.
- Enables supported PSO precaching and D3D12 disk caching.
- Sizes asynchronous loading for the 5900X and available system memory.
- Enables safe parallel animation, geometry, effects, and shader work.
- Disables mouse smoothing and acceleration.

What it deliberately leaves alone:
- Resolution, screen percentage, DLSS, frame generation, VSync, frame limit,
  ray tracing, Lumen quality, shadows, foliage, post-processing, and VRS.

Installed package SHA-256:
- C3F13F82200FEF32C35511D4182CDFBEFE6DFADBF217F6BB8BFD3D24C73D8F06

## Local Tooling Found

Old UnrealPak:
D:\Vortex Mods\palworld\UnrealPakTool\UnrealPakTool\UnrealPak.exe

Works for listing/extracting simple `.pak` config mods.
Does not reveal contents of Dawnwalker `.ucas/.utoc` payload mods by itself.

## What We Need For Bigger Mods

For asset/gameplay data mods, we need a UE5 I/O Store-aware workflow such as FModel/UAssetGUI or a current Unreal packaging pipeline compatible with Dawnwalker. The current local tool can handle simple config `.pak` files, but not enough to safely author cooked Data Asset replacements yet.
