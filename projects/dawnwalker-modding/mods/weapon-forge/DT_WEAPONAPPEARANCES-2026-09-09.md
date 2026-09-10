# Reading DT_WeaponAppearances — how far it got

Codex had not read this table. This is the attempt, including where it stops.

## Oodle is solved

The format notes recorded Oodle as a hard blocker ("statically linked, no
`oo2core` DLL in the install"). That was true of the *game* folder — but **Epic
ships a signed Oodle inside Unreal Engine itself**:

```
D:\UE55\UE_5.5\Engine\Binaries\DotNET\AutomationTool\AutomationScripts\BuildGraph\oo2core_9_win64.dll
```

Authenticode: **"Epic Games Inc.", status Valid**. Use this one. FModel also
downloads an `oodle-data-shared.dll` into its `.data` folder, but that copy is
**unsigned with no version metadata** — prefer Epic's.

Combined with the AES key from FModel's config (AES-256-**ECB**), `iostore_read.py`
now reads any package out of the encrypted base container. `DT_WeaponAppearances`
decompresses to **51,047 bytes**.

## What the table gave up

Its name map parses cleanly — 733 names, 32,518 bytes of strings:

- **~210 `ITM_Weapon_*` row keys**, the item side of the mapping. Everything from
  `ITM_Weapon_SwordGreatMaster1a` through the Dawnwalker/unique/quest swords and
  a handful of obvious dev leftovers (`ITM_Weapon_AxeTest`, `...DemoOnly`).
- **712 weapon visual asset paths**, the appearance side — every
  `Characters/Swords/<Name>/<Name>` blade and `_Scabbard`, plus the improvised
  weapons (`SM_Axe_01`, `SM_Mace`, `SM_Pickaxe_01`, `SM_Board_01`…).

So both halves of the mapping are confirmed present in this one table, and every
name in it is a real, verifiable package path.

## Where it stops, and why I did not guess past it

**The row-to-appearance pairing is not decoded.** Row bodies use UE5 unversioned
property serialization, which needs the `.usmap` schema applied to interpret field
order and types. Without it the bytes are not self-describing.

A naive scan does produce something that *looks* like an answer — the export data
has 52 row markers at a clean 212-byte stride — but the "values" it yields are
mostly name index `0`, which resolves to the first string in the map and prints as
a plausible-looking asset path. That is convincing nonsense, and exactly the trap
`DAWNWALKER_RULES.md` warns about. **No mapping is recorded here because none was
actually read.**

Also unresolved: the export holds ~52 rows while the name map carries ~210 item
keys. Whether the table only overrides a subset, or rows continue in another
chunk, is **unknown** — do not assume either.

## To finish it

Either route works; neither is guesswork:

1. **FModel** — already configured and now known to have a valid key. Export
   `DT_WeaponAppearances` to JSON and read the rows directly. Fastest path.
2. **Implement usmap-driven unversioned property decoding** on top of
   `iostore_read.py`. More work, but it makes every cooked asset in the game
   readable from this toolchain rather than one table.

Until one of those happens, "which sword mesh does item X use" remains **UNVERIFIED**.

## Tools

- `iostore_read.py` — AES + Oodle package reader. See its docstring for the
  Epic-vs-FModel Oodle DLL point and the limits of what it decodes.

Nothing was installed and no game file or save was modified.
