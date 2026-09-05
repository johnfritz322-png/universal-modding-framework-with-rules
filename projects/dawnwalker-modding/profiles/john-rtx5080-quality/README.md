# John RTX 5080 Quality + Smoothness Profile

Hardware-specific Unreal Engine configuration for The Blood of Dawnwalker.

## Target

- NVIDIA GeForce RTX 5080 with 16 GB VRAM
- AMD Ryzen 9 5900X with 12 cores / 24 threads
- 32 GB system RAM
- 3840x2160 display

## Goals

- Reduce shader-compilation and traversal stutter.
- Improve texture and Nanite streaming at 4K.
- Use the available CPU threads without forcing a low worker cap.
- Preserve the game's graphics controls and image quality.
- Leave several GB of VRAM available for Lumen, frame generation, render
  targets, and transient allocations.

## Revision 1.1

- Reduced the Nanite pool from 2048 MB to 1792 MB. A newer Dawnwalker
  optimization profile documented a `NaniteStreamingManager.cpp:1361` startup
  failure at the 2048 MB allocation ceiling.
- Increased the IoDispatcher cache from 512 MB to 2048 MB and its buffer from
  64 MB to 128 MB. The machine has enough system RAM to trade 1.5 GB for fewer
  storage reads while traversing the world.
- Increased decompression workers from 6 to 8. This uses the Ryzen 9 5900X
  without assigning all 12 physical cores to streaming work.
- Limited large texture and Nanite install bursts so they are less likely to
  produce individual slow frames.

## High-Refresh Setup

Use these game settings with this profile:

- Display mode: Full Screen
- Resolution: 3840x2160
- Graphics preset: Ultra
- Upscaler: NVIDIA DLSS
- DLSS mode: Balanced
- Frame generation: DLSS 2x
- Frame-rate mode: Unlocked
- NVIDIA Reflex: On + Boost, if the game exposes the option
- In-game VSync: Off

This is the best honest route to a displayed 120-150 FPS target while retaining
Ultra settings. The game currently targets 4K Ultra at roughly 60 FPS in its
published requirements, and independent testing shows severe scene-dependent
drops. Engine configuration can improve frame delivery and 1% lows, but it
cannot guarantee a locked 120 FPS native render rate. DLSS Balanced and 2x frame
generation provide the extra displayed frames. If Balanced does not hold a
base render rate near 60 FPS in dense forests or large fights, switch DLSS to
Performance; do not install additional Engine.ini performance packs on top of
this profile.

## Intentionally Unchanged

The profile does not force resolution, DLSS, frame generation, VSync, frame
limits, ray tracing, Lumen quality, shadows, foliage, post-processing, or VRS.
Those remain controlled by the game and NVIDIA settings.

## Build

Run `build.ps1`. It creates `dist/~JohnRTX5080Quality_P.pak` in the same V3
format used by the reference mod, then verifies it with repak and UnrealPak.

## Install

Use only one performance-tweaks package at a time. Move the generic
`~TBODoptimizedTweaksBASE_P.pak` out of `Content/Paks/~mods`, then place the
custom package there.

## Attribution

The approach was inspired by VynnGfx's Optimized Tweaks TBOD. This profile is
an independently selected and tuned configuration rather than a renamed copy.

https://www.nexusmods.com/thebloodofdawnwalker/mods/42

## Research References

- Epic texture streaming documentation:
  https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-configuration-in-unreal-engine
- Epic Nanite streaming documentation:
  https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-technical-details
- Dawnwalker Hotfix 1.0.2 full-screen stutter workaround:
  https://dawnwalkergame.com/us/en/news/hotfix-102
- PC Gamer Dawnwalker settings and frame-generation testing:
  https://www.pcgamer.com/hardware/the-blood-of-dawnwalker-best-settings-to-tweak/
- Aiorro RTX 50-series performance profile and 2048 MB Nanite crash note:
  https://www.nexusmods.com/thebloodofdawnwalker/mods/59

