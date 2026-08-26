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
