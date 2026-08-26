# Baldur's Gate 3 — Known Limitations and Unknowns

This file is intentionally conservative. It prevents AI agents from treating attractive ideas as verified engine capabilities.

## Current unknowns that must be resolved per mod
- Whether a requested mechanic can be implemented entirely in data/toolkit records or requires Script Extender scripting.
- Whether a target enemy action/spell is safe to expose to players.
- Whether a copied/temporary ability can be added and removed cleanly at runtime without save or UI side effects.
- Whether a specific action depends on hidden templates, equipment, transformations, quest state, animation sets, AI-only flags, or internal resources.
- Whether multiplayer/client-server synchronization affects the mechanic.
- Whether a mod update or uninstall is safe for an existing save.

## Hard prohibition
Do not tell the user that a BG3 mechanic is technically possible merely because it sounds plausible. Mark it NEEDS TESTING until the exact implementation path is verified.

## Copy-mechanic safety categories
For mods that copy or expose enemy abilities, classify targets before implementation:
- **Allowed:** verified ordinary spells/actions that function safely for player characters.
- **Conditional:** abilities requiring adaptation, custom resources, range/target changes, animations, or scripted cleanup.
- **Denied:** cinematic, quest-state, debug/internal, environment-only, transformation-only, boss-phase, death-trigger, map-transition, or otherwise structurally unsafe actions.

The eligibility registry belongs in the individual project's files, not in this universal game folder.

---

## Confirmed engine limits — Patch 8

Added 2026-08-25 from `projects/bg3-cursed-arts`. These are **resolved unknowns**: each
was checked against shipped data rather than assumed, and each is a hard limit rather
than a caution. Full detail and evidence in `BG3_RULES.md`.

| Limit | Consequence | Status |
|---|---|---|
| No `AlwaysSucceed` in `CriticalHit()` | A **guaranteed critical hit is not expressible** in stats. The vocabulary is `Success`/`Failure` and `Always`/`Never`. Any design promising one needs a different mechanic. | VERIFIED |
| No `OnDeath` `StatsFunctorContext` | Nothing can react directly to a creature dying. Use `OnDamaged` with `(HasHPPercentageEqualOrLessThan(0) or IsKillingBlow())`. | VERIFIED |
| `ApplyStatus(TARGET, ...)` is not valid | `TARGET` appears 0 times; using it silently orphans the status with no error. Valid keywords are `SELF`, `SWAP`, `OBSERVER_TARGET`, `OBSERVER_OBSERVER`. | VERIFIED |
| `SetFaction` is Osiris-only | Faction changes from stats must go through the `FactionOverride` **boost** on a status. | VERIFIED |
| Subclass dialects cannot be mixed | Mixing the two valid conventions crashes on load, at a consistent fault address, with no diagnostic. | VERIFIED |
| XML comments in `english.xml` crash the game | Localisation files must contain no comments. | VERIFIED |
| `using` pointing at live shipping content crashes | Do not inherit from records the game actively uses. | VERIFIED |

## Silent-failure modes worth knowing

These do not crash and produce no error. They simply do nothing, which makes them
expensive to diagnose.

- **An icon atlas with no `TextureBank` resource never loads.** Every file is present and
  correct; every spell renders a blank hotbar slot.
- **An `Icon` naming a nonexistent vanilla icon renders blank.** Several plausible-looking
  names (`PassiveFeature_Generic_Buff`, `Action_Sorcerer_MetamagicOptions`,
  `Skill_Monastic_Tradition`) exist in no atlas anywhere.
- **A DDS whose header disagrees with its payload renders blank.** Pillow produces these.
- **Missing `CharacterCreationPose`/`SoundClassType` removes the subclass picker** at
  level 1 without any error; the first subclass is assigned silently.
- **A mis-staged pak makes BG3 delete the mod from `modsettings.lsx`** rather than report
  a problem. Verify internal archive paths after packing, not just that a file exists.

## Still unverified for summon-based mechanics

- ~~Can `FactionOverride` make a *summon* hostile?~~ **RESOLVED — YES, verified in-game
  2026-08-25.** A summon carrying a status with `FactionOverride(<hostile faction>)` plus
  `LoseControl` arrives hostile and attacks the summoner, overriding the caster's faction
  that summons normally inherit. Hostile-summon mechanics need no Script Extender.
- Whether a hostile summon participates in combat initiative normally.
- Whether a permanent status applied by `ApplyStatus(SWAP, ...)` survives save/reload and
  long rest as expected.
