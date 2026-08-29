# Baldur's Gate 3 — Game-Specific Modding Rules

Status: **starter ruleset**. Every implementation detail must still be verified against the exact current BG3 build and chosen toolchain before coding.

## BG3-specific rules
1. Record the exact BG3 game build before implementing or debugging version-sensitive behavior.
2. Decide explicitly whether a feature belongs in the official toolkit/data layer, Script Extender Lua/Osiris, or another verified BG3 mechanism. Do not mix layers without a reason.
3. Treat UUIDs, stat names, spell/status/passive identifiers, localization keys, resource references, and internal names as stable project data. Never invent or casually regenerate them.
4. Verify spell/status/passive/stat syntax against actual game data or known-working examples before creating records.
5. For Script Extender work, verify the required extender version and API behavior against Norbyte's current repository/documentation before use.
6. Keep client and server behavior conceptually separate when using Script Extender. Do not assume an event or API exists on both sides.
7. Prefer reusable, isolated systems for statuses, passives, spells, resources, and scripted mechanics rather than one monolithic script.
8. Do not claim a packaged mod works until BG3 loads it and the target feature is tested in-game.
9. Any mechanic that manipulates spells/actions dynamically must define persistence rules: temporary, until rest, until unequipped, per-save, or permanent.
10. Any mechanic that observes/copies enemy abilities must maintain an explicit eligibility filter and deny-list. Boss-only, quest-only, transformation, environmental, cinematic, internal/debug, and structurally incompatible actions must not be assumed safe to copy.
11. Keep a registry of every custom UUID/internal ID and the system that owns it.
12. Preserve a minimal test character/save for repeatable class, spell, status, resource, and Script Extender testing.

## Script Extender facts currently verified from maintainer sources
- Norbyte's BG3 Script Extender adds Lua/Osiris scripting support.
- Its maintainer documentation exposes APIs covering areas including Stats, timers, JSON, mod info, localization, templates, static data, resources, levels, engine events, networking, and UI-related facilities.
- A mod using Script Extender supplies a `Mods/<ModName>/ScriptExtender/Config.json` configuration describing required features/version.

These statements are a starting point, not permission to invent specific functions. Verify exact API names and signatures before coding.

## Required evidence before adding a BG3 technical rule
Use at least one of:
- actual BG3 project/game data,
- Larian-maintained toolkit/documentation,
- Norbyte BG3 Script Extender maintainer docs/repository,
- compiler/validator/log output,
- direct in-game test,
- a known-working open-source BG3 mod using the same mechanism.

## Project-specific extension
Each BG3 mod under `projects/` should maintain its own manifest, stable-ID registry, tested-game-build note, and implementation/verification status.

---

# Verified findings — class mods, Patch 8

Added 2026-08-25 from `projects/bg3-cursed-arts`. Every item below is **VERIFIED —
Primary**: measured in shipped game data, or observed as a reproducible crash or a
confirmed in-game result. Where a claim is weaker it says so explicitly.

Method for all data claims: unpack the shipped `.pak`s with LSLib/Divine and search the
extracted corpus, and diff against class mods that demonstrably run. Counts below are
occurrences in that corpus.

## Structure and loading

1. **Two subclass declaration dialects exist and must not be mixed.** One uses
   `<node id="SubClasses">` child nodes with no `Subclasses` attribute; the other uses
   flat attributes. Each working mod is internally consistent. Mixing them crashed the
   game at an identical fault address (`bg3_dx11.exe +0x4E625DA`, reading `0x70`) nine
   consecutive times. *Evidence: reproducible crash, plus three working mods each
   internally consistent.*
2. **`Tags` is mandatory on a base class ClassDescription** (12/12 vanilla classes carry
   it). Removing it crashes. *Evidence: corpus count plus reproducible crash.*
3. **`CharacterCreationPose` and `SoundClassType` appear on 24/24 vanilla subclasses and
   12/12 base classes.** Without them a subclass chosen at level 1 silently fails to
   present a picker; the game assigns the first entry instead. *Evidence: corpus count
   plus in-game observation before and after.*
4. **Never point `using` at live shipping content.** Inheriting from an in-use parent
   (for example `Target_Shatter` or `Target_UnarmedAttack`) crashed on load twice.
   Working scaffolds use no `using` at all. *Evidence: two reproducible crashes.*
5. **No XML comments in `Localization/English/english.xml`.** They crash the game.
   Neither working reference mod contains any. *Evidence: reproducible crash.*
6. **`SharedDev` and `GustavDev` are not dead content.** Meenlock, Shambling Mound, Giant
   Eagle and Displacer Beast have their *only* RootTemplate in `SharedDev`, and all four
   are encounterable in the shipped game. **Status: HIGH CONFIDENCE** — the deduction is
   sound, but no mod-authored reference to a `SharedDev` template has been confirmed
   in-game yet. Treat as NEEDS TESTING before relying on it.

## Stats syntax, measured

7. **`StatusType` is mandatory on StatusData** — 4631 of 4631 entries.
8. **`ApplyStatus` target keywords are `SELF` (1030), `SWAP` (37), `OBSERVER_TARGET` (34)
   and `OBSERVER_OBSERVER` (34).** `TARGET` **never appears** and silently orphans the
   status. `SWAP` resolves to the other party in an interaction, which is the supported
   way for a creature to apply something to whoever hit it.
9. **`SpellAnimation` is exactly 9 slots** — 652 of 652 Target spells.
10. **`CriticalHit(AttackRoll|AttackTarget, Success|Failure, Always|Never|ForcedAlways
    [,range])`.** `AlwaysSucceed` appears nowhere and is inert — but see **finding 42**:
    this entry previously concluded from that a guaranteed critical hit is impossible,
    **which is wrong**. `Always` and `ForcedAlways` both exist and both work.
11. **`Force(-n)` pulls, `Force(+n)` pushes.**
12. **`SpellAnimationIntentType` is the real field name** (487 uses).
    `AnimationIntentType` has 0 uses.
13. **There is no `OnDeath` `StatsFunctorContext`.** The vocabulary is `OnDamage`,
    `OnAttack`, `OnCast`, `OnDamaged`, `OnCreate`, `OnStatusApplied`, `OnAttacked`,
    `OnStatusRemoved`, `OnTurn`, `OnLongRest`, `OnHeal`, `OnCombatStarted` and similar.
    To react to a creature dying, use `OnDamaged` with
    `(HasHPPercentageEqualOrLessThan(0) or IsKillingBlow())`, the pattern
    `MAG_MYRKULITES_UNDEAD_PRESENCE` uses.
14. **`GetHPPercentage()` does not exist.** The real names are
    `HasHPPercentageEqualOrLessThan`, `HasHPPercentageLessThan`,
    `HasHPPercentageWithoutTemporaryHPLessThan` and their variants.

## Summons

15. **`Summon(template, duration, aiHelper, , stackId, status, status, ...)`** — arguments
    6 and beyond are **statuses applied to the summoned creature**. Confirmed across
    `Target_MageHand`, Moonbeam, Find Familiar and Ranger's Companion.
16. **RootTemplates are not loose files.** Each module ships one
    `RootTemplates/_merged.lsf`. Convert with Divine and **stream** the result: Shared is
    about 12.6 MB packed and about 41 MB as `.lsx`. Parse `node id="GameObjects"` where
    `Type == "character"`, reading `Name` and `MapKey`. **A line-based scan gives wrong
    answers**, because `</node>` also closes child nodes and resets state mid-record; it
    silently reports "not found" for creatures that are present.
17. **`FactionOverride(<faction-uuid>)` is a boost carried by `StatusData`.** It is how
    `HAG_INSANITYS_KISS`, `FIENDISH_CHARM` and `INCUBUS_CHARM` change a creature's
    allegiance. Pair it with `StatusPropertyFlags "LoseControl"`, or the creature remains
    under player command. Faction `Evil NPC` is `64321d50-d516-b1b2-cfac-2eb773de1ff6`
    (from `Factions/Factions.lsx`). **`SetFaction` exists only in Osiris story scripts,
    not in stats.**
18. **`FactionOverride` DOES override a summon's inherited faction — VERIFIED
    in-game 2026-08-25.** Summons normally take the caster's faction, so this was the
    open question. A creature summoned via `Summon(...)` carrying a status with
    `FactionOverride(<hostile faction>)` and `StatusPropertyFlags "LoseControl"` arrives
    hostile and attacks the summoner. *Evidence: direct in-game observation,
    `projects/bg3-cursed-arts` Worg trial.* This makes summon-a-hostile-creature
    mechanics viable **in pure stats, with no Script Extender.**
19. **`UnlockSpell(<spell>)` is a boost**, so a permanent (`duration -1`) status can grant
    a spell that appears in no spell list.

## Icons — two separate registrations, both mandatory

Icons are the most common place a class mod stalls, and the failure mode is silent: every
file present, correctly named, byte-perfect, and invisible in game.

20. **`Mods/<Mod>/GUI/metadata.lsf` must register every loose image under `Assets/`**, or
    BG3 raises a blocking **Missing MetaData** dialog during character creation, once per
    icon per click. `MapKey` is the **`.png`** path even though a `.DDS` ships beside it;
    **nothing under `AssetsLowRes/` is ever registered**; each entry carries `w`, `h` and
    `mipcount=1`. *Unanimous across three working mods; fix confirmed in-game.*
21. **A spell-icon atlas needs a `TextureBank` resource, or it is never loaded.**
    `GUI/Icons_<Mod>.lsx` describes UV rectangles only. The atlas is discovered through
    `Public/<Mod>/Content/[PAK]_<Name>/<uuid>.lsf`, region `TextureBank`, node `Resource`,
    where **`ID` equals the `TextureAtlasPath` UUID in the lsx** and **`SourceFile` is a
    path from the PAK ROOT**, plus `Name` and `Template` (atlas name), `Streaming` True,
    `Type` 1, `SRGB` False, and `Width`/`Height`/`Depth`. *Confirmed in-game.*
22. **The Icons lsx filename does not matter** — the game scans the mod's `GUI/` folder.
    The atlas file itself is lowercase **`.dds`**.
23. **UV maths**, verified exactly against vanilla: `U1 = (x + 0.5) / atlasWidth` and
    `U2 = (x + iconSize - 0.5) / atlasWidth`; the same for V.
24. **Do not write DDS with Pillow.** It emits `mipcount=0` and a bogus
    `dwPitchOrLinearSize` (1036 where DXT5 256x256 requires 65536) — a file that
    misreports its own payload and renders blank. Use **texconv** (DirectXTex). Class
    icons are **BC7_UNORM in a DX10 header, 1 mip**; the spell atlas is **BC3/DXT5 with a
    full mip chain**. Read the header back afterwards and refuse to ship one that lies.
25. **An `Icon` naming a vanilla icon that does not exist renders blank silently.**
    `PassiveFeature_Generic_Buff`, `Action_Sorcerer_MetamagicOptions` and
    `Skill_Monastic_Tradition` all look plausible and exist in **no atlas anywhere**.
    Resolve every `Icon` against the vanilla `Icons_*.lsx` atlases plus your own keys.

## Build-gate checks worth having

Each below caught a real failure that every path, name and existence check passed. Per
universal rule 40, **prove each one fails on the broken input before trusting it**.

- **Atlas registration** — every `TextureAtlasInfo` lsx must have a matching `TextureBank`
  `Resource` whose `SourceFile` exists and whose dimensions agree, and every `Icon` in
  stats must resolve.
- **GUI metadata registration** — every `.png` under `GUI/Assets/` registered, nothing
  under `AssetsLowRes/`, and no registered key without a file behind it.
- **DDS header sanity** — recompute the base surface from width, height and block size,
  and reject any file whose declared pitch, mip count or payload disagrees.
- **Resolve UUID arguments by kind.** `Summon()` takes a **character OR item**
  RootTemplate — see finding 36, this was published here as "character only" and was
  wrong. `FactionOverride()` takes a **faction**. Asking "has vanilla passed this exact
  UUID here before" is the wrong question and produces false failures. Build an index
  instead (25,560 templates and 971 factions, from `_merged.lsf` and `Factions.lsx`).
  **Watch the token filter:** a check that skips arguments beginning with a digit never
  validates about 62% of UUIDs, since 10 of the 16 possible hex first-characters are
  numerals.

## Fields are type-scoped, and BG3 ignores the ones it does not recognise

Added 2026-08-25. **VERIFIED — Primary** (corpus counts plus in-game observation).

26. **`StatsFunctorContext`, `Conditions` and `StatsFunctors` work on `PassiveData`
    only** — 272 occurrences on PassiveData, **0 on StatusData**. Put them on a status
    and BG3 does not complain; it **silently ignores them**. The status applies, its
    boosts work, and the logic it was supposed to carry never exists.
27. **A status attaches logic by granting a passive:** `data "Passives" "<PassiveName>"`
    on the StatusData (147 StatusData entries do this), with the functor context on the
    passive. Working template: the `UND_AdamantineGolem` taunt — `OnDamaged` plus
    `ApplyStatus(SWAP, ...)`.
28. **This generalises: an unrecognised field for an entry type is inert, not an error.**
    A build gate should verify that every field is attested **for the entry type it sits
    on**, not merely that the field exists somewhere. Flag a field vanilla clearly uses
    on *other* types — that is the signature of a shape copied from the wrong entry type,
    and it is invisible at runtime.

*How this was found: a summon-and-tame mechanic where the hostile summon worked
perfectly and the reward never fired. Every other check passed, because every field was
real and every value was attested — just on the wrong type of entry.*

## Summon patterns — confirmed and not-yet-confirmed

Added 2026-08-25. **The header on this section previously read "verified in-game" and
covered five findings. That was an overstatement: two of them were deployed but untested
and one was an inference never observed.** Corrected below; the untested material is held
out of this repo until a test result exists.

### Confirmed

29. **The defeat-to-tame summon loop works end to end in pure stats, no Script Extender.**
    *Evidence: direct in-game observation of the complete cycle — hostile summon, defeat,
    permanent mark, and the same button then summoning the creature as an ally.* A summon carrying a status with
    `FactionOverride(<hostile faction>)` and `StatusPropertyFlags "LoseControl"` arrives
    hostile and attacks its summoner. That status grants a passive via `Passives`, and the
    passive's `OnDamaged` context with
    `(HasHPPercentageEqualOrLessThan(0) or IsKillingBlow())` fires
    `ApplyStatus(SWAP, <status>, 100, -1)`, permanently marking whoever landed the killing
    blow. A later cast reads that status through a `GROUND:IF(...)` branch and summons the
    same creature as an ally instead, from the **same hotbar button**. Every step observed
    working; no part of this loop needs Script Extender.
30. **A single `SpellProperties` may hold several `GROUND:IF(<condition>):Summon(...)`
    branches.** *Evidence: shipped game data.* `Target_MageHand` summons a different
    creature depending on `HasPassive(...)`, in one spell. This is vanilla's own shape for
    one button doing different things.
31. **Negative `DamageBonus` appears nowhere in the corpus.** *Evidence: shipped game
    data.* `IncreaseMaxHP(-n)` and `AC(-n)` are attested negatives; `DamageBonus` is only
    ever positive. Weaken a creature through HP and AC. An invented form is ignored
    silently — the same failure as findings 26-28.
32. **`UnlockSpell` on a status boost did not surface a new hotbar button.** *Evidence:
    in-game observation.* The status applied and no castable spell appeared. Recorded as
    an observation of one attempt rather than a general rule; the branch approach in
    finding 30 was used instead and is the better shape regardless.
33. **`CharacterLevelGreaterThan(n)` works inside a `GROUND:IF(...):Summon(...)` branch**,
    so a fixed-strength creature can be tiered to the summoner. *Evidence: in-game
    observation.* A summoned worg carrying a tier status of `IncreaseMaxHP(-13);AC(-2)`
    at levels 1-2 is a winnable fight for a level 1 character; the same creature
    unmodified is not. Combine one state condition with two level bounds
    (`not CharacterLevelGreaterThan(2)` / `CharacterLevelGreaterThan(2) and not
    CharacterLevelGreaterThan(5)` / `CharacterLevelGreaterThan(5)`) for clean tiers.

    **This is what makes summoning real game creatures viable as a player mechanic.**
    Shipped creatures are balanced for the encounter they appear in, so without tiering
    a summon is lethal early and irrelevant late.

### Not yet confirmed — deliberately not recorded as fact

- Whether a summon's tier is fixed at summon time rather than updating continuously.
  This is an inference from how statuses are applied, **not an observation.**

These will be written up once a test result exists.

## Reading creature stats — two things that will mislead you

Added 2026-08-25. **VERIFIED — Primary** (shipped game data).

34. **The `Level` field on creature stats is not the encounter level and is usually
    meaningless.** Across the twelve creatures checked, eleven read `Level 1` — including
    Ansur at 400 HP and a Bulette. Only Giant Eagle carried a real value. Encounter
    difficulty lives in the level/area files, not in `Character.txt`. **Do not use it to
    judge how strong a creature is or when a player meets it.** `Vitality` is the usable
    signal.
35. **`Vitality` is frequently inherited and must be resolved through `using`.** A direct
    read of a creature's stats entry often returns nothing — Meenlock has no `Vitality`
    line of its own, but resolves to 49 by walking its `using` chain. A lookup that does
    not follow `using` will report "no HP" for real creatures and quietly skip them.

## Corrections and further findings

Added 2026-08-26. **VERIFIED — Primary** unless stated.

36. **`Summon()` takes character templates AND item templates.** Measured: vanilla passes
    a **character** template 99 times and an **item** template 46 times. **This corrects
    an earlier statement in this file** that Summon takes a character RootTemplate. Items
    are how every persistent aura or zone is built — `Helper_Spell_Silence` and
    `Helper_Spell_HungerOfHadar` are both items. A build gate demanding a character
    rejects 46 legitimate vanilla patterns; ours did, and blocked a working domain until
    corrected.

    *General lesson: when a validator blocks something vanilla demonstrably does, suspect
    the validator. This was the second time on one project.*

37. **Persistent zones and domains are an item + an aura status.** The shape, from
    `Target_Silence` and `SILENCED_AURA`:
    `GROUND:Summon(<item template>, <turns>, Projectile_AiHelper_<X>,,,<aura status>)`
    where the aura status carries `AuraRadius` and
    `AuraStatuses "IF(...):ApplyStatus(<status>)"`. The aura reapplies to whoever is
    standing inside, each turn.
38. **Auras can tell friend from foe.** 213 of 237 vanilla `AuraStatuses` use an `IF(...)`
    condition — `IF(Character() and Enemy() and not Dead())`, `IF(Ally() and ...)` and so
    on. A zone can therefore affect only enemies while allies stand in it safely.
    `AuraFlags "IgnoreItems"` is the common companion setting.
39. **Melee weapon spells must declare `TargetRadius "MeleeMainWeaponRange"`** (15 vanilla
    spells do). Omitting it does not error. **Observed symptom in game:** the character
    does not path into position before swinging, so there is a visible gap between moving
    and the hit registering. If a melee attack feels laggy, check this first.
40. **`RegainHitPoints` is not attested in `SpellFail`** (0 uses; it appears in
    `SpellProperties`, `DescriptionParams` and `TooltipDamageList`). Healing that should
    land regardless of a target's saving throw belongs in `SpellProperties` — which is
    also better design, since allies are not the ones rolling that save.
41. **`StatusType "INCAPACITATED"` is what actually stops a creature acting.** `STUNNED`
    and `PARALYZED` are both built on it. `STUNNED` pairs it with
    `AbilityFailedSavingThrow(Strength)`, `AbilityFailedSavingThrow(Dexterity)`,
    `Advantage(AttackTarget)` — which is what makes a target vulnerable to follow-up
    attacks — `DetectDisturbancesBlock(true)`, and `BreakConcentration()` on apply.

42. **A guaranteed critical hit IS expressible.** `CriticalHit(AttackRoll,Success,Always)`
    is used by `WILD_MAGIC_ENCHANT`; `CriticalHit(AttackRoll,Success,ForcedAlways)` by an
    adamantine-weapon passive; and `CriticalHit(AttackTarget,Success,Always,3)` is how
    `UNCONSCIOUS` makes attacks within 3m automatic crits — so the fourth parameter is a
    **distance**, not a multiplier.

    **This corrects an earlier statement in this file and in `KNOWN_LIMITATIONS.md`** that
    a guaranteed crit was not expressible. That was concluded from the absence of one
    token, `AlwaysSucceed`, and generalised into an engine limitation. It is exactly the
    failure universal rule 38 names: *a null search result is evidence about the search,
    not the world.* The rule was already written down here, and still got broken.

43. **To tune crit chance rather than force it, use `ReduceCriticalAttackThreshold(N)`** —
    it lowers the number needed by N. Champion Fighter's Improved Critical is `(1)`, i.e.
    crit on 19+. `(5)` gives crit on 15+, six faces of twenty, about one in three.

44. **A crit needs an attack roll.** There is no free-floating die inside a spell, so
    "cannot miss" and "can crit" are in tension. To have both, keep the attack roll and
    make missing nearly impossible: `RollBonus(Attack,10)` is vanilla's largest flat
    attack bonus.

45. **Boosts can be scoped to a single spell** with `IF(SpellId('<SpellName>')):<boost>` —
    26 vanilla Boosts do this. That is how to give one ability its own to-hit or crit
    behaviour without altering everything else the character does.

46. **Pinning a creature in place: `ActionResourceBlock(Movement)`** — 72 vanilla uses,
    and it is what `WEB` uses. Combined with an aura (finding 37) it makes a zone
    genuinely inescapable rather than merely damaging.
47. **Gating a spell behind a state: `RequirementConditions "HasStatus('<X>',
    context.Source)"`** — 237 vanilla spells do this. The ability appears on the hotbar
    but is uncastable until the condition holds, which is how to make abilities that only
    work inside a zone, stance or transformation.

48. **A melee spell with no `TargetRadius` has no reach.** VERIFIED in game
    2026-08-26: a melee spell missing this field can be cast from any distance, and the
    caster never walks into range. `SpellFlags "IsMelee"` and
    `SpellRoll "Attack(AttackType.MeleeUnarmedAttack)"` do **not** imply a range —
    they describe the attack, not the reach. Set
    `data "TargetRadius" "MeleeMainWeaponRange"`.

    This was found three times on one project before being understood: first as "the hit
    lands late", then as "a punch animation plays while holding a sword", and finally as
    "this fires from across the room". One missing field, three different-looking
    symptoms, none of which named it. Worth an automated check: any entry whose
    `SpellFlags` contain `IsMelee`, or whose `SpellRoll` names a melee attack, and which
    has neither `TargetRadius` nor `Shape`.

49. **Multiple hits from one spell: `Cast2[...]`, `Cast3[...]`.** 67 and 20 vanilla uses
    respectively; vanilla goes as far as `Cast7`. The wrapped functors run as an extra
    attack, and the form appears in both `SpellRoll` and `SpellSuccess`:

    ```
    SpellRoll     "Attack(...);Cast2[Attack(...)];Cast3[Attack(...)]"
    SpellSuccess  "DealDamage(...);Cast2[DealDamage(...)];Cast3[DealDamage(...)]"
    ```

    `Target_FlurryOfBlows` is the cleanest two-hit reference; every
    `Target_Multiattack_*` creature (Owlbear, Werewolf, Hook Horror, Drider) is a
    three-hit one.

50. **`AlternativeCastTextEvents` is mandatory for multi-hit spells, and its absence is
    silent.** Without `data "AlternativeCastTextEvents" "Cast2"` — or `"Cast2;Cast3"` —
    the extra hits still land and still deal damage, but **no animation plays for them**.
    Vanilla writes exactly as many events as there are extra casts.

    This is a nasty one because the ability is not broken, only invisible: damage is
    correct in the log, and the player reports that the ability "does not feel right"
    rather than that it is bugged.

51. **A ground-targeted teleport needs `TargetConditions` or it does nothing at all.**
    VERIFIED in game 2026-08-26: a `SpellType "Target"` spell with
    `SpellProperties "GROUND:TeleportSource();"` and no `TargetConditions` produced no
    effect whatsoever when cast — no error, no movement, no failure message. There is no
    valid ground for it to resolve against. `Target_MistyStep` supplies the working line:

    ```
    TargetConditions  "CanStand('') and not Character() and not Self()"
    ```

52. **Surviving a killing blow: `DownedStatus(<status>, N)`** — 15 vanilla uses, all in
    `Boosts`, and it is how `RELENTLESS_ENDURANCE` works. The named status is
    `StatusType "DOWNED"` and does the actual work on apply:
    `OnApplyFunctors "RemoveStatus(<the guard>);RegainHitPoints(1,Guaranteed)"` — the
    guard is consumed so it cannot fire twice.

53. **BG3 does not appear to validate `MD5` or `Version64` in `modsettings.lsx`.**
    HIGH CONFIDENCE, not proven. On one machine the load order carried a checksum from an
    old build and a recorded version of `1.2.0.0` across roughly fifteen rebuilds up to
    `1.17.0.0`, and the mod loaded correctly every time. Useful because it means a
    deploy script does not have to rewrite those fields — but keeping them in sync costs
    nothing and removes a variable when something else breaks.

54. **Scope a boost to melee only with `IF(IsMeleeAttack()):<boost>`.** `IsMeleeAttack`
    has 85 uses across four fields, and critically **16 of them are in `Boosts`** --
    `AURA_OF_HATE` is the cleanest reference:
    `Boosts "IF(IsMeleeAttack()):CharacterWeaponDamage(max(1, Cause.CharismaModifier))"`.

    Worth stating because the field matters as much as the functor: the same token also
    appears in `Conditions` (60), `Properties` (7) and `RemoveConditions` (2), and a
    functor being attested somewhere is not evidence it is legal where you want to put
    it. Check the field, not just the name.

55. **Status visibility is controlled by `StatusPropertyFlags`, and the default is not
    "visible".** `DisableOverhead` (211 uses) and `DisableCombatlog` (216) suppress a
    status; `OverheadOnTurn` (25) surfaces it on the character each turn.

    This is a correctness issue, not a cosmetic one, whenever a mechanic asks the player
    to line up more than one piece of state. On this project a spell required a target
    to be carrying **two** different marks, and one of the two was flagged
    `DisableOverhead;DisableCombatlog` while the other was `OverheadOnTurn` -- so the
    combo could only be set up by memory. The mechanic was correct and unreadable at the
    same time, and it read to the player as the design being confusing.

56. **A mod's picture in the in-game Mod Manager comes only from mod.io — never from the
    pak.** Larian's own publishing guide states that media uploaded to a mod's mod.io
    **General Settings > Media** section is what appears "on the mod.io website, the
    BaldursGate3.game/mods website, and in the in-game Mod Manager". The Toolkit's
    Project Settings has **Thumbnail as a mandatory field**, and that is the only place
    a BG3 mod's own logo is ever set. **Publish Local** — the Toolkit button that just
    writes a `.pak` — attaches no thumbnail, which is functionally what a Divine-based
    pipeline does.

    **Therefore a blank tile is NOT evidence that a local pak failed to load.** Any
    hand-built, locally-installed mod shows a blank tile no matter how healthy it is.
    Do not use the tile as a load diagnostic.

    Two measurements pin this down:
    - `meta.lsx` **`PhotoBooth` is not an image field.** Across the vanilla corpus it
      only ever holds `""` or `SYS_PortraitGeneration_A` — a **level name**, the same
      class of value as `MenuLevelName`/`LobbyLevelName`. Confirmed against a published
      third-party mod (CombatLogLog), which ships a 1234x727 `mod_publish_logo.png`
      inside its pak **while its `PhotoBooth` is empty**. The PNG in the pak is a
      leftover of the publish flow; the picture users see is the mod.io copy.
    - **Logo spec, measured off `thumb.modcdn.io` 2026-08-28:** mod.io serves a BG3 mod
      logo through exactly three transforms — `crop_320x180`, `crop_640x360`,
      `crop_1280x720`, all 16:9. Browse-grid tiles use **640x360**. Other sizes and the
      un-transformed original 307-redirect and fail. **Author at 1280x720 PNG**: the
      smallest source that never upscales.

57. **When reading a mod's own identity out of `meta.lsx`, select `ModuleInfo` — never
    `ModuleShortDesc`.** `meta.lsx` carries a `ModuleShortDesc` node **per dependency**,
    each with its own `Folder`, `Name`, `UUID` and `Version64`. A tool that grabs the
    first `ModuleShortDesc` gets the *dependency's* identity — typically GustavX's
    `Version64` 145241946983300916 — and will happily write it into `modsettings.lsx`
    under the mod's own UUID.

    The mod's real identity is `//node[@id='ModuleInfo']`. Verified both ways by parsing
    the same file with each XPath, 2026-08-28.

    General form of the same mistake: **never hardcode `Version64` into a load-order
    writer.** It drifts silently the first time `meta.lsx` is bumped, and an existence
    check on the entry cannot see the drift — only comparing the written values against
    `meta.lsx` catches it.

58. **Melee reach must come from something the character actually has.**
    `MeleeMainWeaponRange` resolves the range of the **equipped main-hand weapon**.
    Vanilla draws the line explicitly:

    | spell | TargetRadius |
    |---|---|
    | `Target_MainHandAttack` (weapon) | `MeleeMainWeaponRange` |
    | `Target_UnarmedAttack` (no weapon) | `1.5` |

    Give `MeleeMainWeaponRange` to a class that fights **empty-handed** and there is
    nothing to resolve, so the spell has no valid reach and simply cannot be used.
    No error, no log line — the button is clickable and does nothing.

    This matters because it is a **direct reversal of an earlier finding on the same
    project**: "a melee spell with no `TargetRadius` has no reach, use
    `MeleeMainWeaponRange`" was correct for a weapon class and is exactly wrong for
    an unarmed one. VERIFIED from shipped data 2026-08-28. The general rule is the
    reusable part: reach must derive from something the character actually carries,
    so an unarmed class needs a literal.

59. **A custom class enabled but absent from the character-creation picker is a
    LOAD-ORDER problem far more often than a data problem.** Confirmed 2026-08-28
    after a long chase: two class mods both showed enabled in BG3's Installed Mods
    screen while neither appeared in the class list. Cause was BG3 Mod Manager
    holding a stale one-mod saved order and re-exporting it, dropping the class mods
    from the active profile.

    Diagnostics in cost order:
    1. Read `modsettings.lsx` **after** a launch, not after writing it.
    2. Check the manager's own saved order — it can silently overwrite the profile.
    3. Only then look at the class data.

    **A blank mod-manager tile proves nothing here** (see finding 56), and a
    UI-overriding mod is a *plausible but unproven* suspect — one was wrongly
    accused on this project; see the retraction in KNOWN_LIMITATIONS.

60. **A custom melee technique should inherit `Target_UnarmedAttack` when the class
    fights empty-handed.** CONFIRMED IN GAME 2026-08-29 — first working attack on
    the Eight Gates class after every hand-rolled version did nothing.

    The working shape, copied from vanilla `Target_UnarmedStrike_Monk`:

    ```
    using "Target_UnarmedAttack"
    data "SpellSuccess" "DealDamage(UnarmedDamage,Bludgeoning);DealDamage(<technique dice>,...)"
    data "TooltipAttackSave" "MeleeUnarmedAttack"
    data "TooltipDamageList" "DealDamage(MartialArtsUnarmedDamage,Bludgeoning);..."
    ```

    Leading with `DealDamage(UnarmedDamage,Bludgeoning)` and adding the technique's
    own dice after it is what makes the strike behave like a real unarmed attack.
    `UnarmedDamage` (35 uses) and `MartialArtsUnarmedDamage` (10) both resolve for a
    **non-Monk** class — previously an open question.

    **This RETRACTS an earlier project note.** `docs/three-way-comparison.md` on the
    sister project recorded "repointed `using` to `Target_UnarmedAttack` -> crash",
    and the accompanying rule was "leave `using` alone until it is understood."
    Pointing `using` at that exact live, shipping parent did **not** crash here — it
    is what finally made the attacks work. The original crash came from a period with
    nine crashes and several variables moving at once, and the single-cause
    attribution did not hold up. Treat that old note as unproven, not as a rule.

61. **A hand-rolled spell with no `using` parent can silently do nothing — and this
    is the single highest-value thing to check when a mod spell is inert.**
    CONFIRMED IN GAME 2026-08-29 by a clean split across eight spells in one mod:

    | | result |
    |---|---|
    | 6 spells with `using "Target_UnarmedAttack"` | **all worked** |
    | 2 spells with **no** `using` parent | **both did nothing** |

    The two failures were the only non-inheriting entries — one `Target` (an area
    save spell) and one `Shout` (a self-buff). Giving each the vanilla parent it was
    modelled on fixed both: `using "Target_Shatter"` and `using "Shout_ActionSurge"`.
    Nothing else about them changed.

    **The symptom is the dangerous part: the button is enabled, clickable, consumes
    nothing and produces no error.** It is indistinguishable from an unaffordable
    cost or a failed condition, and it survives every static check — syntax,
    field-scoped attestation, status existence, icon validity and resource wiring all
    came back clean while the spell was completely inert.

    **Check `using` FIRST.** Before auditing conditions, costs or functors, ask
    whether the entry inherits a real shipping parent. `Shout_ActionSurge` is the
    most-inherited self-buff shout in the game (64 uses) and is a good default parent
    for a self-applied status; override `Requirements ""` because it is combat-only.

    This also finally explains the sister project's old "`using` causes crashes"
    note (retracted in finding 60): `using` is not dangerous, it is **required**.

    **Closed end to end 2026-08-29.** Both no-parent spells were fixed by adding the
    parent they were modelled on, and **both are now confirmed working in game** — the
    self-buff Shout and the area save spell. Seven of seven techniques in the mod
    function. The prediction ("give it a parent and it will work") was made before the
    test and held for both, which is what moves this from correlation to cause.

62. **`StatusEffect` on a status is how you get a visible aura, and the GUID cannot
    be recoloured — pick one that is already the colour you want.** VERIFIED in game
    2026-08-29: `SANCTUARY`'s glow is `2e0fa509-6711-45e2-bda2-debe1046b577` and is
    gold. For a red flame wreath, `FIRE_SHIELD_WARM`'s
    `a25f92a9-7078-4a5f-8648-c0bb9f4fee39` works on an unrelated custom status.

    Worth doing early, not as polish: an ability with no visible effect is
    **unfalsifiable**. "Nothing happens" cost this project several sessions precisely
    because there was no way to tell a broken spell from a working invisible buff.
    Give any toggled state a visible marker before debugging it.
