# BG3 CursedArts

A Jujutsu Kaisen class for Baldur's Gate 3. **Loads and is playable**; several systems
are confirmed in-game. See `PROJECT_MANIFEST.md` for per-feature verification state.

Unlike a design-only project, most of this one exists and runs. Statements below are
labelled accordingly.

## Design goal
A base class whose identity is **cursed energy as a spendable resource**, with three
subclasses that play very differently: a ranged technique caster, a hand-to-hand bruiser,
and a summoner who must beat his own shikigami before they will serve him.

## Structure — IMPLEMENTED

Base class **Limitless** (displayed "Jujutsu Sorcerer"), subclass chosen at level 1. All
abilities cost the custom **Cursed Energy** action resource, which recharges on short rest.

| Subclass | Ability | Identity | State |
|---|---|---|---|
| Limitless Adept | CHA | Infinity, Blue, Red, Purple | Playable; Blue and Infinity confirmed in-game |
| Blackfist Vessel | DEX | Divergent Fist, Melting Strike, Black Flash, King's Cleave | Playable; abilities validated, mostly uncast |
| Ten Shadows | WIS | Defeat-to-tame shikigami | 12 of 12 implemented; only the Worg has been played |

## Ten Shadows: the Ritual of Subjugation

The design pillar is that **a shikigami is not given, it is beaten**. Casting the trial
summons a real BG3 creature that arrives **hostile and uncontrollable**. Defeat it and it
is bound permanently; the ally version of that summon unlocks and stays unlocked.

One shikigami per level, 1 through 12, ending on Ansur.

| Lvl | Shikigami | Template | Module |
|----|----|----|----|
| 1  | Worg | `Worg_A` | Shared |
| 2  | Meenlock | `Meenlock_A` | SharedDev |
| 3  | Giant Eagle | `Bird_Eagle` | SharedDev |
| 4  | Owlbear | `Owlbear` | Shared |
| 5  | Hook Horror | `HookHorror_A` | Shared |
| 6  | Displacer Beast | `Displacer_Beast` | SharedDev |
| 7  | Minotaur | `Minotaur` | Shared |
| 8  | Shambling Mound | `ShamblingMound_Dark_A` | SharedDev |
| 9  | Phase Spider Queen | `Phase_Spider_Queen` | Shared |
| 10 | Spectator | `Beholder_Spectator` | Shared |
| 11 | Bulette | `Bulette` | Shared |
| 12 | **Ansur** | `Dragon_Skeletal` | Shared |

Every UUID above is **VERIFIED to exist** — mined from `RootTemplates/_merged.lsf`. Only
the Worg has been summoned in game; the other eleven are implemented and unplayed. Full
UUIDs are in `PROJECT_MANIFEST.md`.

### Implementation — VERIFIED primitives, UNVERIFIED assembly

Each mechanism was measured in shipped data before use (details in
`games/baldurs-gate-3/BG3_RULES.md`):

- `Summon(template, duration, ai, , stack, status...)` — args 6+ are statuses applied to
  the summon, so the trial status rides along with the creature
- `FactionOverride(<faction>)` + `StatusPropertyFlags "LoseControl"` — how
  `HAG_INSANITYS_KISS` turns a creature against the party
- `(HasHPPercentageEqualOrLessThan(0) or IsKillingBlow())` under `OnDamaged` — how a
  creature notices its own death, since **there is no `OnDeath` functor context**
- `ApplyStatus(SWAP, ...)` — marks whoever landed the killing blow
- `UnlockSpell(...)` on a permanent status — grants the real summon

**The load-bearing question is answered.** Summons normally inherit the caster's faction,
so whether `FactionOverride` could override that was the whole risk. **Confirmed in-game
2026-08-25: the worg arrives hostile and attacks the summoner.** Hostile-summon mechanics
work in pure stats with no Script Extender.

The *tame* half was tested and **failed**, which turned out to be the most useful result
of the project. The functor fields sat on a **StatusData**, where BG3 ignores them
entirely — 272 uses on PassiveData, 0 on StatusData. The status applied, the worg turned
hostile, and the tame trigger simply did not exist. Rewired onto a passive granted by the
status; retest pending. See `games/baldurs-gate-3/BG3_RULES.md` findings 26-28.

## Known limitations

- **Black Flash's guaranteed critical is not implementable as designed.** `AlwaysSucceed`
  exists nowhere in the corpus; the vocabulary is `Success`/`Failure` and `Always`/`Never`.
  Needs a different mechanic. VERIFIED limitation.
- **Art is copyrighted anime/fan art and blocks public release** (universal rule 31). It
  is placeholder for private play only.
- Save-safety of installing, updating or removing the mod mid-save is UNVERIFIED.

## Toolchain

Local repo at `C:\Users\johnf\Documents\BG3Mods\CursedArts`, not yet on GitHub. Build gate
is 24 checks, each proven to fail on its broken input; `build.ps1` refuses to pack when
the gate fails.

Notable tools: `validate.py` (gate), `build_icons.py` (atlas + TextureBank + metadata),
`index_templates.py` (25,560 RootTemplates and 971 factions, so the gate can resolve UUID
arguments by kind), `map_mod.py`, `parse_dump.py`.

## What this project contributed back

The icon findings in `games/baldurs-gate-3/BG3_RULES.md` (both registrations, the DDS
formats, the silent blank-icon modes) and universal rules 37 through 42 all came out of
failures on this mod.
