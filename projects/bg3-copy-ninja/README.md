# BG3 Copy Ninja

## Design goal
Create a Kakashi-inspired BG3 class/subclass whose identity comes from a strong permanent shinobi technique library plus a Sharingan-driven enemy-technique copy system.

## Core design pillars
- Permanent jutsu library must be fun and complete even if copying is unavailable.
- Sharingan copying is an adaptive bonus layer, not the entire class.
- Temporary copies should use a limited slot system.
- Rare permanent mastery may allow selected copied techniques to become permanent if technically safe and balanced.
- Boss-only, cinematic, quest-only, transformation, internal, or structurally unsafe abilities are denied by default.
- Signature lightning progression should culminate in high-impact Kakashi-style techniques without invalidating normal class gameplay.

## Proposed permanent technique library — DESIGN ONLY
These names describe intended gameplay and are not verified implementation records:
- Fire Style: Fireball Jutsu — ranged area attack
- Water Style: Water Dragon — heavy ranged attack
- Earth Style: Mud Wall — defense/terrain control
- Body Flicker — mobility
- Substitution Jutsu — reactive escape/defense
- Shadow Clone — temporary duplicate/distraction
- Ninja Tool Barrage — multi-hit ranged physical option
- Lightning Clone — defensive lightning counter/decoy
- Lightning Hound — ranged lightning technique
- Chidori — signature melee burst
- Lightning Blade / Raikiri — upgraded signature attack
- Purple Lightning — later-game ranged lightning technique
- Genjutsu: Sharingan — control/debuff
- Kamui — late-game ultimate concept

## Copy system — DESIGN ONLY
Intended loop:
Observe enemy -> analyze technique -> eligibility check -> acquire temporary copy -> equip/use within copy-slot rules -> optionally pursue mastery for selected safe techniques.

Suggested copy-slot progression:
- Early game: 2 temporary copy slots
- Mid game: 3 temporary copy slots
- Late game: 4 temporary copy slots

This progression is provisional until mapped to actual class levels and balance.

## Required implementation research
Before coding:
1. Verify the exact BG3 build and toolchain.
2. Determine the safest real mechanism for adding/removing temporary abilities.
3. Determine how to identify eligible enemy spells/actions reliably.
4. Determine whether copied abilities should map directly to vanilla abilities or to curated player-safe equivalents.
5. Determine persistence behavior across combat, rest, level-up, respec, save/load, multiplayer, and uninstall/update.
6. Build an explicit allow/conditional/deny registry.

## Development order
1. Minimal class/subclass loads.
2. Permanent resource/system baseline works.
3. One permanent jutsu works.
4. Sharingan activation/status works.
5. Analyze one known-safe enemy spell.
6. Add one temporary copied ability.
7. Remove/replace copied ability safely.
8. Expand temporary copy slots.
9. Add curated eligibility registry.
10. Prototype permanent mastery only after temporary copying is stable.
11. Add advanced permanent jutsu.
12. Prototype Mangekyo/Kamui last.

## Status
**DESIGN / RESEARCH** — no technical implementation is considered verified yet.
