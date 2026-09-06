# NVIDIA DLSS 5 — what it is, and whether it can be forced into a game

**Researched 2026-09-05**, two days after launch. Status on the AGENTS.md ladder:
**Researched only.** Nothing here was installed, injected, or run. No in-game
evidence of any kind. Findings will move quickly — re-verify before relying on them.

Cross-game hardware/platform reference, not game-specific, hence `platform/`
rather than `games/<game>/`.

---

## 1. What DLSS 5 actually is — VERIFIED

Not an upscaler. Not a frame generator. **A one-step pixel-space diffusion model
that generates the final displayed appearance of the frame**, adding lighting and
material detail the renderer never computed, from appearance priors learned on
real-world imagery. NVIDIA's name for the technique is **3D-Guided Neural
Rendering**.

| Fact | Value |
|---|---|
| Launched | **2026-09-03**, 21:00 PT |
| First and (as of 2026-09-05) **only** native title | **NBA 2K27** |
| Minimum driver | **Game Ready 616.64 WHQL** |
| Supported hardware | **GeForce RTX 50 series** desktop + laptop, and GeForce NOW |
| Runtime DLL | `nvngx_dlssnr.dll` |
| Integration routes | NVIDIA Streamline, or an Unreal Engine 5 plugin |
| Developer controls | Multiple model variants (A/B/C), Structure Intensity, Tone Intensity, semantic AI masking |

Properties that matter for modding: it is **causal and deterministic**, one frame
in / one frame out, trained for frame-to-frame temporal stability. It **extends**
the pipeline — it does not replace Super Resolution, Multi Frame Generation or Ray
Reconstruction, and runs as an additional stage alongside them.

It is the first DLSS technology to *generate* final appearance rather than
*reconstruct* a more expensive reference. NVIDIA describes it as the first
generative rendering model productised to run in real time.

---

## 2. The decisive finding — VERIFIED

This is the single most important fact in this document, and most public coverage
gets it wrong.

Nearly every article lists DLSS 5's inputs as albedo, surface normals, lighting
buffers, object semantics and light-source positions. **If that were the runtime
requirement, injecting DLSS 5 into an arbitrary game would be flatly impossible** —
no post-process hook can recover per-object semantics or light positions.

NVIDIA Research's own technical page separates them:

| Consumed **at inference** | Used **during training** |
|---|---|
| The current rendered frame | Renderer-derived scene attributes, as consistency supervision to keep generation faithful to the authored scene |
| **Engine motion vectors** | |
| Carried temporal state (internal to DLSS) | |
| Artistic-direction values (parameters, not buffers) | |

Semantic masking is exposed as an **optional developer control**; ray/path-traced
lighting is an **optional** input that improves output where present.

**Consequence:** the hard runtime dependency is *colour plus genuine engine motion
vectors* — the same requirement DLSS has always had. That is what makes the
community injection tools possible at all.

Source: NVIDIA ADLR Research, *DLSS 5: Generative Neural Rendering*, published
2026-09-01. <https://research.nvidia.com/labs/adlr/DLSS5/>

---

## 3. Can DLSS 5 be forced into a game that lacks it?

### Officially: no — NVIDIA-STATED

**NVIDIA has confirmed there is no DLSS 5 toggle in the NVIDIA App**, neither
per-game nor global. Whether a game supports DLSS 5 depends entirely on the
developer integrating it. The existing DLSS Override feature modifies an existing
DLSS feature; it cannot create one.

### Unofficially: three tiers, by what the game already provides

**Tier 1 — native integration.** Developer-tuned models, semantic masking, art
direction per scene. The real thing. Today: NBA 2K27 only. Announced support
includes Bethesda, Capcom, Ubisoft, NetEase, NCSOFT, Tencent, WB Games, Hotta and
S-GAME, with no dates given.

**Tier 2 — driven over an existing upscaler.** COMMUNITY-CLAIMED, not tested here.
A game already running DLSS, FSR2 or XeSS is producing genuine engine motion
vectors and exposing an interception point. `OptiScaler_DLSSNR` (a fork of the
established OptiScaler project) hooks that and runs the neural model as an extra
pass over the upscaler's output. Requirements per its release notes: driver
616.56+, RTX 50 (older needs modded DLLs), and the user supplies
`nvngx_dlssnr.dll` themselves, one copy per game folder. Native Vulkan and DX12;
DX11 only through a bridged upscaler. **This is the realistic answer to "more
games".**

**Tier 3 — ReShade optical-flow feeder.** UNVERIFIED and treated here as
unreliable. For games with no upscaler, feeder tools substitute ReShade's depth
buffer and an optical-flow motion estimate. Optical flow is *inferred from pixels*;
engine motion vectors are *ground truth*. Feeding a model trained on the latter
with the former is precisely the input mismatch its temporal stability was designed
around. **No independent image-quality comparison against a native DLSS 5 reference
was found.** It runs; whether it produces genuine neural rendering rather than a
plausible-looking approximation is unestablished.

### What injection cannot supply — HIGH CONFIDENCE

At tiers 2 and 3 there is **no per-game art direction and no semantic masking**,
because those are authored by the developer. OptiScaler_DLSSNR's own release notes
admit the consequences: flashing lights, or lights missing entirely, in certain
titles; broken output on DLAA in at least one game; and a VRAM leak (roughly 1 GB
per re-enable) fixed only in a recent build.

---

## 4. Hardware gating and the RTX 40 bypass — COMMUNITY-CLAIMED

NVIDIA says RTX 40 support is coming "later this fall", after tuning on RTX 50
completes. Ahead of that, an RTX Remix modder patched the CUDA binaries inside
`nvngx_dlssnr.dll` to target Ada Lovelace, reportedly running on RTX 4090/4080.

Reported results were mixed and are worth recording precisely because they show
what "it works" actually means here: Red Dead Redemption ran; Red Dead Redemption 2
did not; Hogwarts Legacy hung; GTA V crashed after roughly ten seconds. RTX 30
(Ampere) and RTX 20 (Turing) are harder still — no native FP8.

**UNVERIFIED: whether the RTX 50 gate lives in the DLL or in the driver.** That
modders patched CUDA binaries *inside the DLL* suggests architecture targeting
rather than a licence check, but that is inference from how the patch was
described, not a confirmed mechanism.

---

## 5. Supply-chain risk — VERIFIED, and the reason nothing was installed

A cluster of repositories appeared within days of launch offering one-click DLSS 5
for every game. These were **read, not run**. The recurring pattern:

- **Precompiled executables with no buildable source.** The most-starred ships an
  `.exe` plus DLLs; its README states it was engineered with an AI model.
- **Claims that contradict the vendor.** "All PC games, RTX 20 through 50" is
  asserted while NVIDIA's own engineers are still tuning RTX 40.
- **Silence on the only hard part.** None explain how they supply motion vectors in
  a game that has none.
- **An active, named threat.** DLSS Swapper's developer has publicly warned that
  users upload malware-bearing DLLs into the community pool, and that lookalike
  sites distribute viruses under the tool's name.

**Rule for this repository:** model DLLs come from an official NVIDIA driver
package or a game's own installation. Never from a mod bundle. Any tool requiring a
pre-patched `nvngx_dlssnr.dll` is asking you to run an unauditable binary.

Anti-cheat: universally warned against, **never actually tested** in anything found.
Treat as assume-detected. Do not use on EAC / BattlEye / Vanguard titles.

---

## 6. Relevance to this repository's projects

**The Blood of Dawnwalker** ships **DLSS Super Resolution**, upgradeable to DLSS 4.5
via the NVIDIA App — **not DLSS 5** (VERIFIED, NVIDIA launch article). Because it
does have an upscaler, it is a legitimate **tier-2 candidate**. See
`games/blood-of-the-dawnwalker/` and `projects/dawnwalker-modding/`.

Recorded environment of the machine this was researched on (VERIFIED via
`nvidia-smi`): **GeForce RTX 5080, driver 616.64, 16,303 MiB**. That meets the DLSS 5
requirement exactly, so **no patched DLL or hardware bypass is needed here** — every
tool in section 4 solves a problem this machine does not have.

---

## 7. Open questions — UNVERIFIED, do not fill in by guessing

1. **Model size, parameter count, per-frame inference cost in ms.** NVIDIA
   Research's paper PDF returns HTTP 403 to both plain fetch and browser. The
   abstract gives architecture but no numbers; all downstream coverage quotes the
   abstract.
2. **Which DLSS SDK version first shipped `nvngx_dlssnr.dll`.** Secondary reporting
   points at 310.8 with eleven DLLs. A direct read of NVIDIA's DLSS releases page
   returned version dates inconsistent with the known DLSS 4 timeline, so that read
   is being treated as unreliable rather than cited.
3. **Whether the RTX 50 gate is in the DLL or the driver** (see section 4).
4. **Whether tier-3 output is genuine neural rendering** or a degraded
   approximation. No side-by-side analysis found.
5. **Whether injected DLSS 5 trips anti-cheat.** Warned about everywhere, tested
   nowhere.

---

## Sources

- NVIDIA ADLR Research — *DLSS 5: Generative Neural Rendering* (2026-09-01) —
  <https://research.nvidia.com/labs/adlr/DLSS5/> — the inference-vs-training
  distinction in section 2 comes from here. Linked paper PDF is 403-blocked.
- NVIDIA GeForce — *DLSS 5: Neural Rendering Brings Lifelike Lighting to NBA 2K27* —
  <https://www.nvidia.com/en-us/geforce/news/dlss-5-3d-guided-neural-rendering/>
- NVIDIA GeForce — Game Ready 616.64 driver article (driver requirement).
- NVIDIA GeForce — launch article confirming The Blood of Dawnwalker gets DLSS
  Super Resolution —
  <https://www.nvidia.com/en-us/geforce/news/star-wars-zero-company-aliens-fireteam-elite-blood-of-dawnwalker-dlss/>
- VideoCardz — NVIDIA confirms no DLSS 5 override in the NVIDIA App.
- Igor's Lab / TweakTown / Guru3D — `nvngx_dlssnr.dll` patched onto Ada; per-game
  results.
- Tom's Hardware — DLSS Swapper developer's malware warning.
- GitHub — `Dagherbou/OptiScaler_DLSSNR` release notes; `NVIDIA-RTX/Streamline`
  plugin list (no neural-rendering plugin present as of v2.12.0).
