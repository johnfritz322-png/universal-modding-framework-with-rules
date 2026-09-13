# Riftforged Slabblade V2

The first weapon is now being rebuilt from its original concept rather than the
retired 40-vertex blockout.

- **Role:** heavy two-handed greatsword.
- **Silhouette:** thick stone-like slab, broken asymmetric tip, compact split-arch
  guard, long leather grip, octagonal pommel.
- **Material direction:** forged charcoal steel and black leather, with a narrow
  cyan rift channel—not an all-over glow.
- **Source:** `build_riftforged_slabblade_v2.py` generates a V2 `.obj` with
  separate materials, UVs, face normals, and 526 authored vertices / 255 faces.
- **Unreal asset:** imported separately as
  `/Game/Weapons/Meshes/SM_RiftforgedSlabblade_V2` with
  `M_Riftforged_V2`. Unreal validation passed: bounds `39 × 5.425 × 130.5 cm`
  and all five material slots point to the V2 material.
- **Shared snapshot:** `artifacts/riftforged-slabblade-v2/` contains the OBJ,
  MTL, and the two Unreal assets used in that successful isolated import.
- **Safety:** this is only a source-art asset.  It is not cooked, packaged,
  installed, or connected to the game inventory.

The concept art is `concept-art/riftforged-slabblade-concept-v1.png`.
