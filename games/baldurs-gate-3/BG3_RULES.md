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
10. **`CriticalHit(AttackRoll|AttackTarget, Success|Failure, Always|Never [,threshold])`.**
    `AlwaysSucceed` appears **nowhere** and is inert, so a guaranteed critical hit is
    **not expressible** this way.
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
- **Resolve UUID arguments by kind.** `Summon()` takes a **character** RootTemplate;
  `FactionOverride()` takes a **faction**. Asking "has vanilla passed this exact UUID
  here before" is the wrong question and produces false failures. Build an index instead
  (25,560 templates and 971 factions, from `_merged.lsf` and `Factions.lsx`).
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
