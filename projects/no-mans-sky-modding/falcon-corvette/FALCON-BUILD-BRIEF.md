# Millennium Falcon custom Corvette build brief

## Visual identity: the five non-negotiables

The Millennium Falcon must read correctly from a distance before surface detail is added:

1. **Flattened double-dish body.** It is not a sphere, a clean disk, or a pointed ship. The silhouette is a shallow, battered saucer made from an upper and lower hull.
2. **Forward fork.** Two broad, parallel cargo mandibles create a wide rectangular gap down the front centre. Do not join them into one nose.
3. **Right-side cockpit.** With the nose facing forward, the narrow cockpit neck and cockpit pod sit on the starboard/right side. The official production-history account describes the design as a cockpit on the side of a dish, with mandibles ahead.
4. **One continuous rear drive strip.** The rear has a long, glowing horizontal engine band across almost the full width. Two isolated engine pods are wrong.
5. **Purposeful asymmetry.** A sensor dish and the offset cockpit make the ship visibly asymmetric. The surface must look repaired and mechanical, not smooth or symmetrical.

StarWars.com gives the canonical length as 34.75 m. For a comparable NMS exterior, preserve an approximate 1.36:1 length-to-width silhouette, before counting the cockpit pod.

## Exterior layout

### Dorsal / top

- Shallow upper saucer, slightly narrower toward the nose.
- A central dorsal turret mount; use a small, low profile rather than a tall tower.
- Sensor dish offset from the exact centreline.
- Panels arranged in rings and irregular service trenches; retain broad worn gray plating between details.
- The cockpit neck begins on the right front quarter and leads to a rectangular/rounded capsule with forward windows.
- Mandibles should end forward of the saucer, be thick enough to look structural, and leave the centre gap visibly open.

### Ventral / bottom

- Match the lower saucer's broad, shallow profile.
- A matching lower turret belongs on the centreline.
- Keep landing/entry geometry stock. The replacement exterior must leave a generous empty envelope around the Corvette's door, ramp, and cockpit-tunnel path.

### Front / rear

- **Front:** two mandible faces, recessed centre notch, cockpit clearly on the viewer's right.
- **Rear:** full-width rectangular blue engine band, set into a recessed rear edge. Add darker mechanical blocks below/above it instead of circular exhaust pods.

## Boardability rule

The previous attempt failed the user-facing test: boarding was not confirmed. The model is therefore deliberately an exterior shell around an untouched, stock, boardable Corvette core. There may be **no** custom collision or visible mesh across:

- the stock access door;
- the ramp's deployment and walking volume;
- the interior cockpit-tunnel volume;
- any landing contact points used by the base Corvette.

The first in-game test is not a flyover: summon slot 7, walk to the door, enter, walk through the cockpit tunnel, exit, save, reload, and repeat. Only then may it be called usable.

## Surface treatment

- Base: desaturated warm gray, intentionally uneven.
- Details: darker charcoal seams, vents, and exposed machinery.
- Engines: restrained pale-blue emission only in the rear strip.
- Windows: dark blue-gray, not bright neon.
- Geometry budget: use clean, triangulated low/medium-poly panels and separate normal/detail maps for small greebles. Avoid hundreds of standalone physical parts and avoid high-poly mesh collision.

## Legal and scope guardrail

This is a private fan-made visual replica. Do not upload or distribute another creator's model or texture without a license that allows it and the required attribution. If we build it locally, it will use new, original geometry and textures based on the visual layout above.

## Sources

- Official Falcon databank (name, context, and 34.75 m length): <https://www.starwars.com/databank/millennium-falcon>
- Official design history, including side cockpit, big dish, and forward mandibles: <https://www.starwars.com/news/ships-of-the-galaxy-the-millennium-falcon>
- NMSDK capability and model-export documentation: <https://monkeyman192.github.io/NMSDK/>
