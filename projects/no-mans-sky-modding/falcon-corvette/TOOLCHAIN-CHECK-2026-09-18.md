# Custom Falcon toolchain check

## Local game target

- Steam app: `275850` (No Man's Sky)
- Installed Steam build: `25351301`
- Game executable timestamp: 2026-09-18 19:01 local time

## Portable-only setup

Nothing in this section changes the game or a save.

- Blender 4.5.14 was downloaded from Blender's official release and extracted only under the Codex working folder.
- Its downloaded archive SHA-256 was checked against Blender's published SHA-256: `B9533D2397AC1984DB4466FB23A7A4649391CCA93F6E84209F9BCC60D071C8B9`.
- NMSDK was cloned from its upstream repository: <https://github.com/monkeyman192/NMSDK>.
- NMSDK supports Blender 4.2 and newer and exports NMS scenes, geometry, materials, and primitive collision nodes.
- MBINCompiler `v7.03.2-pre1` was downloaded only into the Codex working folder. Its executable reports that version and has SHA-256 `C856BEB50C2E248943379BEB6D82A6401FCA380DDC94160AAA5EE19578E8E358`.

## Version conclusion

The local game updated on 2026-09-18. MBINCompiler `v7.03.2-pre1` was published by its upstream project on 2026-09-17, immediately before that update. This makes it the best current candidate, but it is an **inference**, not proof: the tool must successfully compile/decompile a copied game asset before it is used to make a mod.

## Correct build strategy

The prior save-edit build used stock Corvette components and was rejected: it is neither a faithful Falcon exterior nor verified boardable.

For the replacement, preserve the stock slot-7 interior, access door, landing zone, and collision. Make only a new exterior scene/model that follows the layout research:

1. shallow twin-saucer hull;
2. two separated forward mandibles and central notch;
3. starboard cockpit tunnel/capsule;
4. centreline turret mounts and sensor dish;
5. one full-width rear engine band.

The custom exterior must have no collision mesh in the doorway/cockpit tunnel. It should use simple primitive collision only if a new collision is later required. NMSDK warns that mesh collision is expensive and should be kept very low-poly; the preferred plan is no replacement collision at all.

## Gates before installation

1. Prove MBINCompiler compatibility on a copied asset.
2. Build and inspect a locally exported scene (mesh, UVs, normals, materials).
3. Establish the specific Corvette exterior scene/part binding. A generic NMSDK export alone does not attach itself to a save Corvette.
4. Package only the new mod files; do not overwrite base `.pak` files.
5. Back up both save files and the existing `MODS` folder, then install only after the game is closed.
6. Test the slot-7 ship: summon, land, enter, exit, and reload its save. Confirm slot 8 Darth Fritz is unchanged.

No claim of a working custom model or an in-game test is made here.
