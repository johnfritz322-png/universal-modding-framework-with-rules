# Real Millennium Falcon layout research

## Design target

The target is the classic, modified YT-1300 Millennium Falcon silhouette—not a generic disk-shaped Corvette.

Reliable visual rules:

1. Two shallow, convex saucer hulls form the main body.
2. The front has **two separate cargo mandibles**, leaving a wide central notch. They must not read as a single pointed nose.
3. The cockpit is a narrow, **starboard-side** outrigger connected by a neck. In a top view with the nose facing up, it belongs on the right side.
4. A small top turret sits on the upper centreline and a matching lower turret belongs beneath it.
5. The rear is a full-width, long rectangular blue engine band—not two isolated engine pods.
6. The sensor dish, venting, panel trenches, and asymmetric side details break up the saucer.
7. The interior must retain a clear cockpit tunnel and a central walkable area. Decorative geometry must never overlap the doorway.

Sources:

- Star Wars describes the production concept as a cockpit mounted on the side of a large dish with mandibles forward: https://www.starwars.com/news/ships-of-the-galaxy-the-millennium-falcon
- Star Wars' official databank: https://www.starwars.com/databank/millennium-falcon
- The published technical references consistently show the front mandibles, side cockpit, top/bottom turrets, dish, and rear drive section.

## Requested NoMansApp reference

`https://nomansapp.com/?corvette=2931643163`

- Name shown publicly: `Millennium Falcon 2.0 (full interior`.
- Reference size: `36 x 48 x 8`.
- Public listing reports `All:1495, Basic:11`.
- The public page returns only metadata and a preview image. It does not expose the actual `Objects[]` placement data required for a save import.
- NoMansApp's exact delivery service can inject the build only through an active multiplayer session and a submitted NMS friend code. The user declined that service.

## What this changes

The previous `Falcon Courier` script made an ellipse from repeated wing pieces. It did not follow this layout and is rejected.

An exact-looking result has two viable routes:

1. Obtain an openly exportable, legitimate `Objects[]` build of this exact layout and import it into slot 7, then test boarding in-game.
2. Build a local custom 3D exterior model based on this layout, using NMSDK, and package it as a private replacement for the Falcon's exterior while retaining a stock, walkable Corvette interior.

Route 2 is technically supported: NMSDK is a Blender add-on for bringing models into No Man's Sky (https://github.com/monkeyman192/NMSDK). Older NMS Nexus ship mods also show that custom modeled ships can be packaged for NMS (for example, Ships of Moar: https://www.nexusmods.com/nomanssky/mods/1064). This needs a current-game-version compatibility check before any install.

## Non-negotiable tests before presenting a new build

- Save round-trip succeeds for both `save.hg` and `save2.hg`.
- Darth Fritz remains active in slot 8, byte-for-byte unchanged in its ship/base records.
- Only slot 7 changes; no third Corvette is added.
- The custom visual model or part layout has a clear cockpit door and entry path.
- The game is launched and the Corvette is boarded in-game before it is called fixed.
