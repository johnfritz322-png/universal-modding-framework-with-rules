# Visual loadout set — three weapons, built and installed

Existing game meshes only. **Visual replacement of existing weapons — this does
not create new inventory items.**

## The mapping

| Weapon | Item row | Stock blade | Now shows |
| --- | --- | --- | --- |
| The Vrakhir | `ITM_Weapon_SwordVampiric1a` | `L_Sword_Vampiric_01` | `M_Sword_Ancient_Hero_01` |
| Imbued Sword of St Mihai | `ITM_Weapon_SwordDawnwalker5a` | `S_Sword_Dawnwalker_01` | `M_Sword_Matron_01` |
| Sword Great Master 1a | `ITM_Weapon_SwordGreatMaster1a` | `L_Sword_NPC_07` | `M_Sword_Skender_01` |

Scabbards repointed to match in every case.

## The bug the checks caught — do not patch by pattern

Patching The Vrakhir originally worked by searching for its blade's FName byte
pattern, because that pattern happened to be unique. **It is not generally.**

```text
Imbued Sword blade pattern (210,657)  -> occurs 3x
Imbued Sword scabbard      (211,658)  -> occurs 5x
```

The whole `SwordDawnwalker1a–5a` family shares those meshes. A pattern replace
would have silently repointed four other weapons.

**Patch by offset from the row marker instead.** The row name FName is unique,
and the layout is fixed:

```text
row name at R   ->   blade at R+10   ->   scabbard at R+30
```

Verify the bytes at each offset match the expected old value before writing, and
check the siblings afterwards. Confirmed intact here: `Dawnwalker1a` → (213,660),
`2a` → (212,659), `3a` → (210,657).

## Verification, all seven checks

| Check | Result |
| --- | --- |
| Item rows exist | 3/3 — indices 523, 360, 388 |
| Blade + scabbard packages exist | 6/6 |
| Names already in the table's name map | yes — patch is size-neutral |
| Row markers unique | 3/3 |
| Size unchanged | 10,943 bytes before and after |
| Container collisions | 2 chunks, **1 collision** on `0x2b6fc8ead9260336` |
| In game | The Vrakhir: **OVERRIDE_ON_PLAYER** (via address). Other two pending. |

## Rollback — the whole set

```text
Content\Paks\~mods\zzz_VisualLoadout_P.pak
Content\Paks\~mods\zzz_VisualLoadout_P.ucas
Content\Paks\~mods\zzz_VisualLoadout_P.utoc
```

Proven reversible and save-safe — see `PERSISTENCE-TEST.md`.
