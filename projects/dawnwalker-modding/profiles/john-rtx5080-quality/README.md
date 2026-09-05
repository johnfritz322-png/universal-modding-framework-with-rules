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
