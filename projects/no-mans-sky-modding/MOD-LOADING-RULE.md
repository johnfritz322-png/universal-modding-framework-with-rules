# No Man's Sky only loads mods that live in a FOLDER — verified

Game: 7.03.1 "Cosmos", Steam build `25351301`.

A `.EXML` or `.MBIN` dropped loose at the root of
`GAMEDATA\MODS\` is **silently ignored**. No warning, no log line, no error.
The game only treats **immediate subfolders** of `MODS\` as mods.

## The proof

`Binaries\SETTINGS\GCMODSETTINGS.MXML` is written by the game at every startup
and lists every mod it registered. Comparing it against the folder contents:

| `MODS\` contains | type | appears in GCMODSETTINGS.MXML |
|---|---|---|
| `Buy All Corvette Parts\` | folder | yes, `_index="0"` |
| `CorvetteExtras\` | folder | yes, `_index="1"` |
| `GLOBALS\` | folder | yes, `_index="2"` |
| `GCSETTLEMENTGLOBALS.EXML` | loose file | **no** |
| `CorvetteOverhaul.lua` | loose file | **no** |
| `AMUMSS_v5.6.2.0w.txt` | loose file | **no** |

Every folder is registered. No loose file is. The settings file had been
rewritten by a launch *after* the loose EXML was placed, so this is not a
staleness artefact.

**`GCMODSETTINGS.MXML` is therefore the cheapest possible check that a mod
loaded at all** — read it after one launch instead of testing in game.

## Paths inside the mod folder mirror the game's own paths

Globals sit at the **root** of `NMSARC.globals.pak`, with no `GLOBALS\`
directory. Verified by extracting them:

```
gcsettlementglobals.mbin        <- note: no ".global" in this one
gccameraglobals.global.mbin
gcspaceshipglobals.global.mbin
gcaispaceshipglobals.global.mbin
```

So the mod file goes at the root of its own folder, named exactly like the
vanilla file with `.MBIN` swapped for `.EXML`:

```
MODS\BetterSettlements\GCSETTLEMENTGLOBALS.EXML
MODS\GLOBALS\GCCAMERAGLOBALS.GLOBAL.EXML
```

Do not invent a `GLOBALS\` subfolder inside the mod, and do not add `.GLOBAL`
to a name that does not have it. `gcsettlementglobals` is the odd one out.

## `.EXML` is a partial patch

A known-working mod (`GCCAMERAGLOBALS.GLOBAL.EXML`, 26 lines) sets a single
property and leaves the other ~40 alone. Root element is
`<Data template="cGcCameraGlobals">` — the `c` prefix is required and matches
the struct name, not the `GcModSettingsInfo`-style name used elsewhere.

## Don't put files in a Vortex-managed folder

A folder containing `__folder_managed_by_vortex` may be purged or reverted on
Vortex's next deploy. Hand-made mods get their own folder.
