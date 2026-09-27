# Stage 4 exterior-face fix

The first successful modern `GAMEDATA/MODS` overlay loaded the Stage 3 Death
Star shell in game, but the screen showed only its far hemisphere behind the
stock Mothership. That is the expected symptom of reversed face winding under
No Man's Sky's back-face culling.

`tools/build_death_star_silhouette_stage3.py -- <output> --reverse-winding`
now exports `DEATH_STAR_SILHOUETTE_STAGE4` with every shell quad reversed.
The parent remains at the measured donor centre, so this correction changes
only which side of the shell is rendered; it does not guess at the freighter
attachment transform.

The modern EXML overlay builder accepts `--shell-name` and produced the four
Stage 4 runtime files. They were copied to:

`D:\Steam\steamapps\common\No Man's Sky\GAMEDATA\MODS\DeathStarFreighterOverlay`

The live root reference resolves to:

`//CUSTOMMODELS\DEATH_STAR_SILHOUETTE_STAGE4\DEATH_STAR_SILHOUETTE_STAGE4.SCENE.MBIN`

All four deployed files were SHA-256 matched to the staged build after copy.
An in-game view is still required to verify the exterior is now opaque over
the donor freighter and to assess the visual aperture.
