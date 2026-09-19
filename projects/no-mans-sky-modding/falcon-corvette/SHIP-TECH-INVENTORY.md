# Ship technology inventory - VERIFIED 2026-09-18

Read out of the user's own save. This is the ship's tech loadout, which is
separate from the Corvette build (`@ZJ`) documented elsewhere.

## Where it lives

`vLc / 6f= / @Cs[slot]` is the ship record. Its keys:

| Key | Meaning |
|---|---|
| `NKm` | ship name |
| `NTx.93M` | model scene, e.g. `MODELS/COMMON/SPACECRAFT/BIGGS/BIGGS.SCENE.MBIN` for a Corvette |
| `;l5.@bB[]` | derived stats: `^SHIP_DAMAGE`, `^SHIP_SHIELD`, `^SHIP_HYPERDRIVE`, `^SHIP_AGILE` |
| **`PMT`** | **the technology inventory container** |

Inside `PMT`:

| Key | Meaning |
|---|---|
| `:No[]` | the installed items |
| `hl?[]` | the **valid slot coordinates** - only these may hold an item |
| `B@N.1o6` | ship class, e.g. `S` |
| `=Tb` / `N9>` | grid width / height (10 x 6 on this Corvette) |

Note the grid is 10x6 = 60 cells but `hl?` listed only **38** valid slots. Never
place an item at a coordinate absent from `hl?`.

## An inventory item

```json
{ "Vn8": {"elv": "Technology"},
  "b2n": "^UP_HYP4#02698",     // item id
  "1o9": -1,                   // amount (-1 on upgrade modules)
  "F9q": 100,                  // max
  "eVk": 0.0,                  // damage, 0 = undamaged
  "b76": true,                 // fully installed
  "5tH": false,
  "3ZH": {">Qh": 7, "XJ>": 4}  // slot X, slot Y
}
```

## Reading the item ids

| Prefix | Meaning |
|---|---|
| plain, e.g. `^HYPERDRIVE`, `^LAUNCHER`, `^SHIPJUMP1`, `^SHIPSHIELD` | base technology |
| `^HDRIVEBOOST1/2/3` | Cadmium / Emeril / Indium drives - warp to red / green / blue stars |
| `^UT_*` | the named special modules. `UT_LAUNCHCHARGE` is the **Launch System Recharger** (self-recharging launch thrusters), `UT_QUICKWARP` the Emergency Warp Unit, `UT_LAUNCHER` Efficient Thrusters, `UT_PULSESPEED` Photonix Core, `UT_PULSEFUEL` Instability Drive, `UT_SHIPDRIFT` Sublight Amplifier, `UT_SHIPSHIELD` Ablative Armour |
| `^UP_<system><tier>#<seed>` | procedural upgrade modules. **The digit is the class: 1=C, 2=B, 3=A, 4=S**, and `X` is the X-class variant. So `UP_HYP4#02698` is an S-class hyperdrive upgrade |
| `^CV_*` | **Corvette-specific** modules: `CV_LAUN`, `CV_PULSE`, `CV_FIT`, `CV_INV`, `CV_S_SHL`, `CV_SLASR`, `CV_SMINI`, again with a tier digit |
| `^T_*` | cosmetic trinkets, e.g. `T_SHIP_GOLD`, `T_BOBBLE_ATLAS` |

Systems seen in `UP_` ids: `HYP` hyperdrive, `LAUN` launch, `PULSE` pulse engine,
`S_SHL` shield, `SGUN` / `SLASR` / `SMINI` / `SBLOB` / `SSHOT` weapons.

## How to add technology safely

**Copy a real instance from another ship in the same save and change only the slot
index.** The user owns those items, so the id, amount, max and structure are all
genuine. Do not hand-build an item dict and do not invent a `#seed` - a seed that
was never generated is not a real module.

Checks worth asserting before writing:

```
ship class B@N.1o6 unchanged
no two items share a (>Qh, XJ>) pair
every item's slot appears in hl?
the other ship's inventory length is unchanged
```

## What was fitted to this Falcon

17 -> 38 items, filling all 21 free slots. The ship was **already S-class**, so
nothing there needed changing.

Requested: `UT_LAUNCHCHARGE`, and `HDRIVEBOOST1/2/3` for all star colours.
Added alongside: `UT_QUICKWARP`, `UT_LAUNCHER`, `UT_PULSESPEED`, `UT_PULSEFUEL`,
`UT_SHIPDRIFT`, `UT_SHIPSHIELD`, `CARGOSHIELD`, `SHIP_TELEPORT`, `SHIPSCAN_ECON`,
`SHIPSCAN_COMBAT`, plus seven tier-4 modules: 2x `UP_HYP4`, 2x `UP_LAUN4`,
2x `UP_PULSE4`, 1x `UP_S_SHL4`, each with a distinct seed.
