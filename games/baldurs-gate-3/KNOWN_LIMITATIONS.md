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
| ~~No guaranteed critical hit~~ | **RETRACTED — this was wrong.** `AlwaysSucceed` does not exist, but `CriticalHit(AttackRoll,Success,Always)` and `ForcedAlways` both do and both work. See BG3_RULES finding 42. The absence of one token was generalised into an engine limitation. | RETRACTED 2026-08-26 |
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
- **A field on the wrong entry type is ignored, not rejected.** `StatsFunctorContext`,
  `Conditions` and `StatsFunctors` are PassiveData-only; on a StatusData they do
  nothing at all and produce no error. Verify fields against the entry **type**.
- **A melee spell with no `TargetRadius` does not error** — the character just never
  walks into position, and the hit lands visibly late. Looks like an animation bug.
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

## Load order written by hand or by script does not survive a launch — cause UNVERIFIED

**Observed twice on 2026-08-28, one variable at a time.** A `modsettings.lsx` written
while BG3 was closed, and verified by reparsing it from disk, was reduced to **GustavX
only** after the game ran — losing every other mod, not just the newly added one.

| time | event | verified result |
|---|---|---|
| 00:41 | script wrote 6 entries, BG3 closed, confirmed on disk | 6 active |
| 00:43 | BG3 launched and exited (closed by user, not a crash) | **GustavX only** |
| 00:56 | script wrote 2 entries, BG3 closed, confirmed on disk | 2 active |
| ~01:06 | BG3 Mod Manager used to uninstall unrelated mods | — |
| 01:08 | — | **GustavX only** |

What this rules out: it is **not** specific to the new mod (a mod that had loaded for
days was also dropped), and **not** a failed write (both writes were confirmed on disk
before the game ran).

**The cause is NOT established.** Recorded here so the observation is not lost, not as
an explanation. Leading candidates, none tested:
- BG3 re-serialises the profile from its in-memory module list and discards entries it
  did not author — which would make manager export the only supported path.
- BG3 rejects a file whose byte shape differs from its own writer's. Measured
  difference between BG3's output and a .NET `XmlWriter` round-trip of the same content:
  `encoding="UTF-8"` vs `encoding="utf-8"`, and `value="x"/>` vs `value="x" />`
  (983 vs 1010 bytes). Neither matters to a conforming XML parser; Larian's LSX loader
  may not be one.
- A second tool (Vortex, BG3 Mod Manager) rewriting the file on its own schedule.

**Practical rule until this is settled: treat the load order as manager-owned.** Write
it with BG3 Mod Manager and export to game, and verify `modsettings.lsx` *after* a
launch rather than after the write. Any tool that edits the file directly must refuse
to run while `bg3`, `bg3_dx11` or `LariLauncher` is running, and must back up first.

### RESOLVED IN PRACTICE 2026-08-28 01:42 — cause still not isolated

A launch finally ended with the added mod **still present** in `modsettings.lsx`. The
tell that BG3 *accepted* rather than regenerated the file: during every earlier wipe
GustavX came back with a blank `MD5` and `Version64` reset to the 1.0.0.0 default
(36028797018963968); afterwards it carried its true version (145241946983300916).

**What changed — four things at once, so attribution is UNVERIFIED:**
1. `FileSize` and `MD5` were added to the mod's `meta.lsx` `ModuleInfo`.
2. The profile writer was changed to match BG3's byte shape (`UTF-8` casing, `/>`).
3. A validator's file-scope was narrowed.
4. BG3 Mod Manager exported the load order.

Either (1) or (4) is the plausible cause and **they were not tested separately**
(Rule 58 was not followed). Do not record a single cause as fact.

**Caveat on (1): the values cannot ever be correct.** `meta.lsx` lives *inside* the
pak, so writing the pak's own size and hash into it changes both — there is no fixed
point. Here `meta.lsx` claimed `FileSize=14743` / `MD5=fa7bef71…` while the packed
result was `14806` / `f8fa94e3…`, wrong from the moment it was packed. **All 9 vanilla
`meta.lsx` files set `FileSize="0"`.** So if this attribute is what mattered, it is the
*presence* of the field and not its value — which also means treating the value as
meaningful is a mistake.

**Practical guidance unchanged:** treat the load order as manager-owned, and verify
`modsettings.lsx` *after* a launch rather than after the write.

## A UI mod can hide every custom class while the mods still report as enabled

**2026-08-28.** Both custom class mods showed green/enabled in BG3's own Installed Mods
screen, both paks validated and deployed clean — and the character-creation class picker
still showed only the 12 vanilla classes.

**ImprovedUI (ImpUI) replaces the character-creation UI wholesale.** Its pak ships
`Mods/ImpUI_<uuid>/GUI/Pages/CharacterCreation.xaml` and `CharacterCreation_c.xaml`,
i.e. the page that *renders* the class list. A UI mod built for an older patch therefore
removes custom classes from the picker without touching class data, without failing any
validator, and without any mod reporting a problem.

**ImpUI is NOT required for custom classes.** VERIFIED from load-order backups: on
2026-08-26, when a custom class was confirmed working in game, the active order was
`GustavX, CursedArts, AnimationUnlocker, Instant Level Up, Combat Log Viewer` —
**no ImpUI**. It was added later, and the class picker broke.

That ImpUI is the *cause* is HIGH CONFIDENCE, not verified — the decisive test is to
remove it, restore the known-good order, and check the picker.

**The general rule: when a custom class is enabled but absent from the picker, suspect a
UI-overriding mod before suspecting the class data.** Diagnose by listing every active
pak for `GUI/Pages/CharacterCreation*.xaml` — anything that overrides it is a candidate,
and only one of them can win.

### RETRACTION 2026-08-28 — ImpUI was NOT the cause

The entry above named ImprovedUI as HIGH CONFIDENCE for hiding custom classes.
**That is now contradicted by direct evidence and is withdrawn.** Both custom
classes were confirmed visible in the character-creation list by the user while
**ImpUI was still active in the load order** (position 1, ahead of both class mods).

What stands, and what does not:

- **STILL TRUE (verified by pak listing):** ImprovedUI does ship
  `GUI/Pages/CharacterCreation.xaml` and `CharacterCreation_c.xaml`, so it *does*
  override the page that draws the class list. That was measured, not inferred.
- **STILL TRUE (verified from load-order backups):** ImpUI is not a required
  dependency — a custom class worked on 2026-08-26 with no ImpUI present.
- **WITHDRAWN:** that overriding the page was *breaking* class registration here.
  It demonstrably does not, at least at this ImpUI version and load position.

The real fix was the load order itself — BG3 Mod Manager's stale one-mod `Current`
order was overwriting the profile and dropping the class mods entirely.

**The lesson is about the reasoning, not the mod.** A mod that overrides the
relevant UI page is a *plausible* suspect, and "it was absent when things worked"
is real correlational evidence — but neither is proof of causation, and both
pointed the wrong way here. The diagnostic below is still worth running; just do
not stop at it.

**General diagnostic (unchanged, still useful):** when a class is enabled but
missing from the picker, list every active pak for
`GUI/Pages/CharacterCreation*.xaml` — but confirm by removing the candidate and
retesting before recording a cause.
