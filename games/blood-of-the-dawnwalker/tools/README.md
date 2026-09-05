# Dawnwalker format tools

Python 3 (tested on 3.14), **standard library only**. No Oodle, no AES, no external
tool needed for anything these scripts do.

Each was validated against the shipped files described in `../SOURCES.md`.

Set `PAKS` to your install:

```
D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks
```

## gameversion.py — RUN THIS FIRST

```bash
python gameversion.py          # add --json for machine-readable output
```

Reads Steam's `appmanifest_3751260.acf` for the build id and update state, then
hashes `global.utoc`, `global.ucas`, `Dawnwalker-Windows.utoc` and the exe, and
prints the base container's structural fingerprint.

Compare the output against `projects/dawnwalker-modding/GAME_VERSION.md`. If it
matches, every format finding in this folder still applies. If it does not, the
game was patched and findings must be re-verified before being trusted.

Takes a few seconds — it deliberately does not hash the 43.5 GB `.ucas`.

## utoc.py — inspect any container

```bash
python utoc.py "<PAKS>/global.utoc"
python utoc.py "<PAKS>/~mods/00000000_SkillsNoTimeCost_P.utoc" --max=20
```

Prints TOC version, chunk count, compression method table, container flags
(so you can see immediately whether a container is encrypted), the directory
index, and every chunk with type / id / offset / uncompressed size.

`--max=N` limits how many chunk rows are printed. Use it on the base game
container — it has 778,643 entries.

## extract.py — unpack a container

```bash
python extract.py "<PAKS>/zzz_DualSenseAtlas_v1_1_P.utoc" out_dualsense
```

Handles `None` and `Zlib` blocks. Writes chunks to their real paths from the
directory index; chunks with no path (e.g. the container header) are written as
`_chunkNNNN_<Type>_<id>.bin`.

Will **not** work on the base game container — it is Oodle-compressed and
AES-encrypted (see `../KNOWN_LIMITATIONS.md` L1, L2).

## zen.py — parse a `.uasset` from inside a container

```bash
python zen.py out_skills/DA_Trait_CombatFocus_Kick.uasset
```

Prints the Zen summary, the local name map, the import map with each
`FPackageObjectIndex` classified (Export / ScriptImport / PackageImport / Null),
the export map, and the bulk data map.

Cross-reference `ScriptImport` values against `scriptobjects.json` from
`globals.py` to get real class names.

## globals.py — dump the engine script-object table

```bash
python globals.py
```

Reads `global.ucas` (unencrypted, no key needed) and writes:

* `scriptobjects.json` — 58,720 entries, `0x<globalIndex>` → full path such as
  `/Script/DogwoodCharacterDevelopment/TraitAsset`
* `global_names.txt` — all 54,880 names, one per line

`global_names.txt` is greppable and is the fastest way to find what a system is
called before hunting for its assets.

## containerheader.py — parse + validate `FIoContainerHeader`

```bash
python containerheader.py out_skills/_chunk0112_ContainerHeader_*.bin
```

Prints the package id list and each store entry, then **validates** that the
imported-package arrays tile the data region contiguously and land exactly on the
declared end. If `TILING VALID: False`, the layout assumption is wrong — do not
trust the parse.

Version 4 headers only (see `../KNOWN_LIMITATIONS.md` L5).

## pak.py — legacy `.pak`

```bash
python pak.py "<PAKS>/~mods/~TBODoptimizedTweaksBASE_P.pak"
python pak.py x "<PAKS>/~mods/~TBODoptimizedTweaksBASE_P.pak" out_tweaks
```

Reads pak v3 and v11 footers, **recomputes and checks the index SHA-1**, lists
entries, and with `x` extracts them.

This is the format to use for config/CVar mods — the one mod type with no blockers.

## Notes

* Encoding: the scripts call `sys.stdout.reconfigure(encoding="utf-8")` because
  game paths contain characters cp1252 cannot encode.
* `utoc.py` is imported by `extract.py`, so keep them in the same folder.
