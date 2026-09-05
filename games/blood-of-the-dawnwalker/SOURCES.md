# The Blood of Dawnwalker — sources

All findings dated **2026-09-04** were derived by **direct binary analysis of the
shipped game files on the user's machine**, not from documentation or web sources.
No external source was consulted for the format work.

## Primary source: the installed game

```
D:\steam\steamapps\common\The Blood of Dawnwalker\
├─ Dawnwalker\Binaries\Win64\Dawnwalker.exe        176,196,472 B
├─ Dawnwalker\Content\Paks\
│  ├─ Dawnwalker-Windows.utoc                       70,109,154 B
│  ├─ Dawnwalker-Windows.ucas                   43,527,831,216 B
│  ├─ Dawnwalker-Windows.pak                    10,732,400,370 B
│  ├─ global.utoc / global.ucas                   374 / 3,837,488 B
│  ├─ zzz_DualSenseAtlas_v1_1_P.{pak,ucas,utoc}
│  └─ ~mods\
│     ├─ 00000000_SkillsNoTimeCost_P.{ucas,utoc}
│     └─ ~TBODoptimizedTweaksBASE_P.pak
└─ Engine\                                        (at game root, not under Dawnwalker\)
```

## Third-party mods examined (credit to their authors)

| Mod | Author | Source |
|---|---|---|
| TBOD Optimized Tweaks | **VynnGfx** | `https://www.nexusmods.com/thebloodofdawnwalker/mods/42` (URL read from the mod's own bundled readme) |
| DualSense Atlas v1.1 | unknown | present on this install |
| Skills No Time Cost | unknown | present on this install |

The VynnGfx readme bundled inside `~TBODoptimizedTweaksBASE_P.pak` also lists a
Ko-fi, a YouTube channel and an X account. Those are the author's own links,
recorded here for attribution only.

## How each claim was validated

| Claim | Validation method |
|---|---|
| TOC header layout | Parsed all four containers; section sizes sum exactly to file size in every case |
| TOC meta entry size | Derived from leftover bytes: 33 B for TOC v3, 24 B for TOC v8, **zero remainder** in both |
| `global.ucas` layout | Name map + script object table consume exactly the declared 3,837,478 B |
| `FIoContainerHeader` v4 | Imported-package arrays tile the data region contiguously; 528 refs × 8 B ends exactly on the declared end offset `0x1b18` |
| Legacy `.pak` | Index SHA-1 recomputed and matched on both shipped paks |
| Zen package summary | Section offsets in the summary line up with the parsed name map / bulk map / import map / export map boundaries |
| Base container encryption | High entropy + 16-byte-aligned size + nonsense `FString` length, contrasted against `global.utoc` which the same parser reads cleanly |
| Texture format `PF_B8G8R8A8` | Read from the Zen package's local name map |
| Engine version | **Inferred only** from `UE5\Engine\Source\ThirdParty\libcurl\8.4.0\` in the exe; no `++UE5+Release-5.x` string exists |

## Engine knowledge applied

UE5 IoStore / Zen structures (`FIoStoreTocHeader`, `FIoChunkId`, `EIoChunkType`,
`FIoDirectoryIndexResource`, `FIoContainerHeader`, `FFilePackageStoreEntry`,
`FZenPackageSummary`, `FMappedName`, `FPackageObjectIndex`, `FPakInfo`) are public
Unreal Engine source. Field *offsets and semantics used here were re-derived and
confirmed against these shipped files* rather than assumed — §4.1 and §4.3 of
`DAWNWALKER_RULES.md` both record places where the naive assumption was wrong.

## Tooling

`tools/*.py` in this folder — written for this analysis, Python 3.14, standard
library only. `pycryptodome` was installed for the (blocked, unsuccessful) key
search and is not needed by any of the parsers.

## Not consulted

No wiki, forum, or third-party format documentation was used. If any claim here
later conflicts with community documentation, **the bytes on disk win** — but
re-verify before overwriting anything on this page.
