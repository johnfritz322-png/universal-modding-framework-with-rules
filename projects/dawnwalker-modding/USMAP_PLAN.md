# Getting a `.usmap` for Dawnwalker

**Researched 2026-09-04.** Status: **plan verified, not yet executed.** Nothing here
has been installed or run. See `KNOWN_LIMITATIONS.md` L3 for why this matters.

---

## Why we want it

Cooked Unreal packages use **unversioned property serialization**: the values are
there, the property *names* are not. A `.usmap` is the missing dictionary — it maps
every class and struct to its ordered property list and types.

With one we could:

1. Read the property names on all **67 settings classes** in `CONFIG_SURFACE.md`,
   turning "we know where to aim" into "we know what to type". This is the big one —
   it unblocks config mods, which need **no AES key**.
2. Test the standing hypothesis that perk time cost is a `config` property on
   `DogwoodCharacterDevelopmentSettings`, rather than baked into 112 data assets.
3. Actually decode `DA_Trait_*` assets instead of guessing at byte offsets.

**It does not** unblock asset replacement — that still needs the AES key (L1).

---

## What we established first (VERIFIED)

| Finding | Evidence |
|---|---|
| **No anti-cheat.** No EasyAntiCheat or BattlEye anywhere in the install | filesystem search |
| **Property names ARE in the exe** — `DaysToPass` found at `0x8e84c10` | direct binary search |
| …stored in a **length-bucketed name pool** (10-char names padded to 16 bytes, packed together) | byte context around the hit |
| Real game version: **`dw1-pc-257186-shipping-patch2-all-CL-257186`** | PE version resource |
| Engine is **UE 5.4 or 5.5** | `UniversalObjectLocator` + `WorldConditions` modules (5.4+), libcurl 8.4.0, TOC v8, container header v4 |

The name-pool finding is interesting but **not a shortcut**. A flat list of names
does not say which properties belong to which class, and that mapping is precisely
what a `.usmap` provides. Static reconstruction would mean parsing UE's reflection
registration structures out of the binary — far more work than dumping at runtime.

---

## The tool: UE4SS

`RE-UE4SS` has a built-in mappings dumper (Dumpers tab → "Generate .usmap file",
or the default keybind **Ctrl + Numpad 6**). v3.0.1 supports UE 5.4 and 5.5.

### ⚠ Do NOT install stock UE4SS for this game

Per the community package's own notes:

> "UE4SS cannot detect the engine version for this game, and even after manually
> setting the version, two default function hooks cause the game to crash."

So a vanilla UE4SS install is expected to **crash Dawnwalker**. Use the
preconfigured package instead.

### Use the Dawnwalker-specific package

[UE4SS for The Blood of Dawnwalker](https://www.nexusmods.com/thebloodofdawnwalker/mods/55)
— UE4SS experimental build **v3.0.1-1111** (2026-09-02), loader binaries unmodified,
with a settings file that pins the engine version and disables the two crashing
hooks.

Details read from the mod page 2026-09-04 (VERIFIED — page inspected directly):

| | |
|---|---|
| Author | **Grimpil** |
| File | **"UE4SS For Dawnwalker 1111 0.2"**, file version 2 |
| Size | **8.5 MB** |
| Uploaded | 2026-09-03, 02:38 |
| Downloads | 5.2k unique / 5.8k total, 35 endorsements |
| Virus scan | Nexus reports "Safe to use" |
| Licence | UE4SS is MIT, by the RE-UE4SS team; included unmodified |

The author's own description, quoted:

> "Out of the box UE4SS cannot find the engine version on this game and, once that
> is overridden, two of its default function hooks crash the game seconds after the
> main menu."

Note the crash is **seconds after reaching the main menu**, not at launch — so a
successful launch alone does not prove the configuration is working. Get to the
menu and wait before concluding anything.

> "Built against the current Steam build, September 2026."

The mod was uploaded **2026-09-03**; this install patched **2026-09-04**. So it
predates the installed build by a day. That is the mismatch risk below.

There is also an earlier [UE4SS for Dawnwalker](https://www.nexusmods.com/thebloodofdawnwalker/mods/18)
and a [Console Enabler and Mod Loader](https://www.nexusmods.com/thebloodofdawnwalker/mods/16).

### ⚠ Build mismatch — the main risk

| | Steam build | Date |
|---|---|---|
| Package built against | reportedly **25107392** | uploaded 2026-09-03 |
| **This install** (`GAME_VERSION.md`) | **25129649** — patch 2 | patched 2026-09-04 |

The package predates the installed build by one day and may carry build-specific
signatures. **UNVERIFIED** whether it still works. It may well be fine — the
documented fixes are configuration (engine version + two disabled hooks) rather
than AOB scanning. Treat the first launch as a test, not a routine step, and
remember the failure mode is **seconds after the main menu**, not at startup.

If it does not work, the fallback is
[UnrealMappingsDumper](https://github.com/TheNaeem/UnrealMappingsDumper), or
waiting for Grimpil to refresh the package against patch 2.

---

## Procedure

Follow the project's own Nexus rules (`Dawnwalker-Modding-Map.md`): use the
logged-in browser and a manual download; do not use command-line Nexus downloads.

**Before starting — this modifies the game folder. It is fully reversible.**

1. **Back up nothing** — this adds files, it does not overwrite any game file.
   Note the two things you will delete to undo it: `dwmapi.dll` and the `ue4ss`
   folder, both in `Dawnwalker\Binaries\Win64\`.
2. In your logged-in browser, open the
   [UE4SS for The Blood of Dawnwalker](https://www.nexusmods.com/thebloodofdawnwalker/mods/55)
   page and download the main file manually.
3. Open the ZIP and look inside **before** extracting. You expect to see
   `dwmapi.dll` and a `ue4ss` folder. If it contains anything else that touches
   game files, stop.
4. Extract so the files land here:
   ```
   D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Binaries\Win64\
   ├─ dwmapi.dll
   └─ ue4ss\
      ├─ UE4SS.dll
      ├─ UE4SS-settings.ini
      └─ Mods\
   ```
5. Open `ue4ss\UE4SS-settings.ini` and confirm these, which the mappings dump needs:
   ```ini
   bUseUObjectArrayCache = false
   ConsoleEnabled = 1
   GuiConsoleEnabled = 1
   GuiConsoleVisible = 1
   ```
   Leave the package's engine-version and hook settings **exactly as shipped** —
   those are the fixes that stop the crash.
6. Launch the game. A separate UE4SS console window should appear.
   **If the game crashes, stop and delete the two items from step 1.**
   That is the build-mismatch risk, not something you broke.
7. Let the game reach the **main menu** and **wait there a good minute**. The known
   failure mode is a crash a few seconds after the menu, not at startup, so a
   successful launch alone proves nothing.
8. Switch to the UE4SS window → **Dumpers** tab → **Generate .usmap file**.
   (Or press **Ctrl + Numpad 6** with the game focused.)
9. `Mappings.usmap` appears next to the game executable, in
   `Dawnwalker\Binaries\Win64\`.
10. Quit the game. Copy `Mappings.usmap` somewhere safe — **it is tied to this
    build**, so record that it came from `CL-257186 / patch 2 / Steam 25129649`.
11. Optional but recommended: uninstall UE4SS again (delete `dwmapi.dll` and the
    `ue4ss` folder). The `.usmap` is what we wanted; the loader does not need to
    stay resident.

### Alternative if UE4SS will not run

[UnrealMappingsDumper](https://github.com/TheNaeem/UnrealMappingsDumper) is a
standalone injector aimed specifically at UE5 games. Same output, different
loader, so it is a genuine fallback if the UE4SS signatures are stale.

---

## What happens once we have it

The `.usmap` is a compact binary format (names table, enums, structs, properties,
with optional Oodle/Brotli/zstd compression of the body). Parsing it is
straightforward and the existing in-repo parsers already handle the same
name-table idiom.

Planned follow-up, in order:

1. Write `tools/usmap.py` to parse it — no external dependencies unless the file
   turns out to be Oodle-compressed, in which case zstd/brotli fallbacks apply.
2. Regenerate `CONFIG_SURFACE.md` with **real property names and types** per class,
   replacing "section verified, properties unknown".
3. Answer the `DogwoodCharacterDevelopmentSettings` hypothesis one way or the other.
4. Only then consider the AES key (L1), which is a separate and larger question.

---

## Related lead, recorded not pursued

While researching this, community discussion indicated a **working AES key for this
game exists publicly** (referred to as "KZekai's key") and has been used
successfully in FModel, with users then needing a mappings file to view assets —
i.e. exactly the two blockers recorded in `KNOWN_LIMITATIONS.md` L1 and L3.

**UNVERIFIED — not obtained, not tested.** Recorded only so the option is visible.
Whether to pursue it is the user's call; see L1 for the options.
