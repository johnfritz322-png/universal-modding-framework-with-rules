# Death Star freighter — toolchain check

## Status
**Not yet run.** This is a checklist for the user to run on the machine
that has No Man's Sky installed — this session has no game install, no
Blender, and no unpacked game files, so none of it can be executed here.
Report the results back and I'll fold them into `PROJECT_MANIFEST.md` and
`FEASIBILITY.md`.

## Environment (last known, NEEDS TESTING for this project)
| Item | Last known value | Status |
|---|---|---|
| Game | No Man's Sky | — |
| Platform | PC / Steam, app id `275850` | VERIFIED (Steam app id is public/static) |
| Installed Steam build | `25351301` (2026-09-18, from the sibling Falcon Corvette project) | NEEDS TESTING — must be re-checked for this project, see Step 1 |
| Blender | 4.5.14, hash-verified for the Falcon Corvette project | NEEDS TESTING — re-verify still present/working, see Step 2 |
| NMSDK | cloned from `github.com/monkeyman192/NMSDK` | NEEDS TESTING — re-pull and re-check compatibility, see Step 2 |
| MBINCompiler | `v7.03.2-pre1`, hash-verified for the Falcon Corvette project | NEEDS TESTING — re-verify or update, see Step 2 |
| PAK unpack tool | none chosen yet for this project | UNVERIFIED — candidates only, see Step 3 |

Nothing in this table is carried over as verified for this project. It is
the starting point the checklist below re-checks.

## Safety — what this checklist does and does not touch
- Nothing here overwrites a game file or a save. Every step either reads
  an existing file or works on a **copy** in a separate working folder.
- Steps 5 and 6 read your unpacked game files and your save file
  respectively. Neither is written to in this checklist. **Do not make
  any save write until a fresh four-file backup exists**, per this
  framework's Rule 14 (saves are sacred) — that backup step comes before
  any future write step, not in this checklist.
- If anything below conflicts with what you actually see on screen, stop
  and report the discrepancy rather than pushing through — that's exactly
  the kind of thing this gate exists to catch.

## Step 1 — confirm the installed game build
Steam app id is `275850` (already known from the sibling Falcon Corvette
project). Confirm the current build, since the Corvette project's last
build check (`25351301`, 2026-09-18) is a week old and cannot be assumed
current.

In PowerShell, find your Steam library path, then:
```powershell
Get-Content "<SteamLibrary>\steamapps\appmanifest_275850.acf" | Select-String "buildid"
(Get-Item "<SteamLibrary>\steamapps\common\No Man's Sky\Binaries\NMS.exe").LastWriteTime
```
Report: the `buildid` value and the exe's last-write timestamp.

## Step 2 — re-verify (or set up) the portable toolchain
"Portable" means: extracted only into a working folder, never touching the
game install itself.

- **Blender**: if you still have the 4.5.14 extraction from the Falcon
  project, confirm it still launches and that NMSDK still loads as an
  add-on. If not, download fresh from blender.org and verify its SHA-256
  against the hash Blender publishes for that release before using it —
  do not skip the hash check even on a re-download.
- **NMSDK**: if already cloned (`github.com/monkeyman192/NMSDK`), `git pull`
  to pick up any changes since 2026-09-18. Confirm its own compatibility
  notes still list your Blender version as supported.
- **MBINCompiler**: if you still have `v7.03.2-pre1` from the Falcon
  project, confirm its executable still reports that version. If NMSDK's
  current docs recommend a newer release for the build found in Step 1,
  download that instead and verify its published SHA-256 before using it.

Report: confirmed versions (and hashes, if anything was freshly
downloaded) for all three.

## Step 3 — pick and confirm a PAK unpack tool
Web research surfaced several candidates (PSARCTool, HGPAKTool, NMS Modding
Station, AMUMSS's PCBanks Explorer) — **HIGH CONFIDENCE, not VERIFIED**,
since none of their pages were read directly in this session (Nexus Mods
and the NMS modding wiki are both blocked by this sandbox's network egress
proxy). Also flagged in research: modding changed with the "Worlds Part II"
(v5.50) update, and tooling from before that update may not work against
the current build. Before trusting any of these:
1. Confirm whichever tool you pick states compatibility with the build
   number from Step 1 (or a newer one), not just "No Man's Sky" generally.
2. Use it only to **read/extract into a separate working folder** — never
   to write back into `GAMEDATA\PCBANKS`.

Report: which tool and version you're using, and its stated
compatibility.

## Step 4 — prove the toolchain round-trips before trusting it on anything real
This is the framework's Rule 8 in practice ("AI output/tooling is untrusted
until verified") — the same gate the Falcon project's toolchain check
required and never actually completed. Do this before Step 5:
1. Extract any single small, harmless `.MBIN` from the unpacked PCBANKS
   copy (does not need to be freighter-related — this step is only
   proving the tool works on this build).
2. Decompile it with MBINCompiler to `.MXML` and open it — confirm it's
   readable, well-formed XML, not garbage.
3. Recompile that unchanged `.MXML` back to `.MBIN`.
4. Decompile the rebuilt `.MBIN` again and compare its structure with the
   first `.MXML`. Record any difference and do not treat file size alone as
   proof of validity. Byte identity is useful when it occurs, but is not a
   requirement unless the current MBINCompiler documents it as one.

Report: pass/fail, and which file you tested with.

## Step 5 — locate the real freighter hull table and geometry files
This is gate 2 from `FEASIBILITY.md`: confirm or correct
the "hull selected by save seed, added via a new table entry" hypothesis
against real files, rather than trusting the secondhand mod description it
was built from.

Useful confirmed lead: research found that **Frigates** (the small escort
ships assigned to a freighter, not the freighter itself) live under
`MODELS/COMMON/SPACECRAFT/FRIGATES/`, e.g.
`COMBATFRIGATELOD4.SCENE.MBIN`, and that geometry files generally follow
the pattern `NAME.GEOMETRY.MBIN.PC`. **This is a different object than the
freighter hull `Mothership` itself uses** — do not assume the freighter
path mirrors the frigate one; confirm it directly:
1. List (don't need to fully extract yet) filenames under
   `MODELS/COMMON/SPACECRAFT/` matching things like `*FREIGHT*` or
   `*CAPITAL*` to find the real freighter folder name.
2. Inside it, identify the geometry/scene files for individual hull
   variants, and look for a higher-level table file that maps a
   generation seed (or similar) to a hull variant — this is the file the
   Death Star hull would need a new entry added to.

Report: the real folder path, the naming pattern for hull
geometry/scene files, and the name of the seed→hull lookup table if found
(or what's still unclear, if it isn't found on the first pass — this is
allowed to come back partial).

## Step 6 — locate `Mothership`'s save record
1. Identify which save file (`save.hg` / `save2.hg`, or their higher-index
   `save*.hg` counterparts if you have multiple slots) and which slot
   contains `Mothership` — do this by name, using whatever save
   reader/editor you already have set up, not by assuming it's in the same
   slot or even the same save folder as the Falcon Corvette project's
   Corvette work.
2. Within that freighter's record, identify the field that looks like a
   generation seed (this is the field Step 5's table lookup will key on).
   Do **not** change it yet — this step is only locating and naming it.

Report: save file name, slot number, and the seed field's name and current
value.

## What to send back
Once you've run as much of this as you can:
- Step 1: build id + exe timestamp
- Step 2: Blender / NMSDK / MBINCompiler versions (+ any fresh hashes)
- Step 3: unpack tool + version + stated compatibility
- Step 4: pass/fail on the round-trip test, and which file was used
- Step 5: real freighter model folder path, file naming pattern, and the
  seed→hull table name if located
- Step 6: `Mothership`'s save file, slot, and seed field name/value

Partial results are fine — each gate that comes back confirmed lets the
next document narrow from "HIGH CONFIDENCE hypothesis" to "VERIFIED", and
any gate that comes back different from what research assumed is exactly
the kind of correction this checklist exists to surface before anything is
built on a wrong assumption.
