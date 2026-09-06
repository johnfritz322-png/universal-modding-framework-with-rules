# NVIDIA DLSS 5 — what it is, and whether it can be forced into a game

**Researched and cross-checked 2026-09-05.** Dates in this document are local
(UTC-6); the second pass ran the same evening, not the following day. Status on
the AGENTS.md ladder:
**Researched only.** Nothing here was installed, injected, or run. No in-game
evidence of any kind. Findings will move quickly — re-verify before relying on them.

Cross-game hardware/platform reference, not game-specific, hence `platform/`
rather than `games/<game>/`.

---

## 1. What DLSS 5 actually is — VERIFIED except where noted in the table

Not an upscaler. Not a frame generator. **A one-step pixel-space diffusion model
that generates the final displayed appearance of the frame**, adding lighting and
material detail the renderer never computed, from appearance priors learned on
real-world imagery. NVIDIA's name for the technique is **3D-Guided Neural
Rendering**.

| Fact | Value |
|---|---|
| Unveiled | **GTC 2026**, by NVIDIA's CEO — per NVIDIA's own GeForce article of 2026-03-17 |
| Public NVIDIA Research / GeForce pages | **2026-09-01** |
| Available in a shipping game | **2026-09-03**, 21:00 PT, with driver 616.64 |
| First and (as of 2026-09-05) only native title found in NVIDIA public material | **NBA 2K27** |
| Minimum driver | **Game Ready 616.64 WHQL** |
| Supported hardware | **GeForce RTX 50 series** desktop + laptop, and GeForce NOW |
| Runtime DLL | `nvngx_dlssnr.dll` — **HIGH CONFIDENCE, not VERIFIED** (see note below) |
| Integration routes | NVIDIA Streamline, or an Unreal Engine 5 plugin |
| Developer controls | Multiple model variants (A/B/C), Structure Intensity, Tone Intensity, semantic AI masking |

Properties that matter for modding: it is **causal and deterministic**, one frame
in / one frame out, trained for frame-to-frame temporal stability. It **extends**
the pipeline — it does not replace Super Resolution, Multi Frame Generation or Ray
Reconstruction, and runs as an additional stage alongside them.

It is the first DLSS technology to *generate* final appearance rather than
*reconstruct* a more expensive reference. NVIDIA describes it as the first
generative rendering model productised to run in real time.

### Note on the DLL name — HIGH CONFIDENCE, downgraded 2026-09-05

`nvngx_dlssnr.dll` is named consistently across independent secondary sources
(modding coverage describing it being patched for Ada, and SDK reporting), and it
fits NVIDIA's confirmed naming convention — `nvngx_dlss.dll`, `nvngx_dlssd.dll`
and `nvngx_dlssg.dll` were all found in an actual game install. But:

- **No NVIDIA primary source naming the file was found**, by either agent.
- A search of this machine's NVIDIA driver locations, `ProgramData`, NVIDIA
  program folders, and both Steam libraries found **no `nvngx_dlssnr.dll`**. The
  one DLSS feature DLL that *is* present in the driver store is `nvngx_dlssg.dll`,
  under `DriverStore/FileRepository/nv_dispi.inf_amd64_*` — recorded because it
  shows the search was capable of finding such a file had one been there. The only
  native DLSS 5 title, NBA 2K27, is not installed here, so this remains an absence
  of evidence rather than evidence of absence.
- The public `NVIDIA/DLSS` SDK sample (latest public release 310.7.0) contains
  `nvngx_dlss.dll` and not `nvngx_dlssnr.dll`.

**To settle it:** inspect an NBA 2K27 install, or a driver package that ships the
neural-rendering runtime. Until then do not state the filename as fact.

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

### Officially: no — HIGH CONFIDENCE (downgraded 2026-09-05)

**There is no DLSS 5 toggle in the NVIDIA App**, per-game or global. Whether a
game supports DLSS 5 depends on the developer integrating it. The existing DLSS
Override feature modifies an existing DLSS feature; it cannot create one.

This was originally labelled NVIDIA-STATED. That was **overclaiming**, and the
label is corrected here. The basis was a VideoCardz headline reporting an NVIDIA
confirmation — but the article itself returned HTTP 402 and was never actually
read, so no direct NVIDIA wording was ever in hand. What genuinely supports the
conclusion:

- Neural Rendering does not appear among the DLSS Override options in NVIDIA's
  own NVIDIA App documentation, which lists Super Resolution, model presets,
  Frame Generation and Ray Reconstruction.
- NVIDIA's own DLSS 5 instructions direct users to enable it in **NBA 2K27's
  in-game video settings**, not through the NVIDIA App.

That is strong, consistent, and indirect. It is not a direct denial from NVIDIA.

### Unofficially: three tiers, by what the game already provides

**Tier 1 — native integration.** Developer-tuned models, semantic masking, art
direction per scene. The real thing. As of the 2026-09-05 re-check, NBA 2K27 is
the only native title found in NVIDIA public material. Announced support includes
Bethesda, Capcom, Ubisoft, NetEase, NCSOFT, Tencent, WB Games, Hotta and S-GAME,
with no dates given.

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

## 5. Supply-chain risk — HIGH CONFIDENCE, and the reason nothing was installed

A cluster of repositories appeared within days of launch offering one-click DLSS 5
for every game. These were **read, not run**. The recurring pattern:

- **The important binaries are not auditable.** One checked one-click wrapper has
  buildable Rust source, but its own documentation says the DLSS 5 add-on/model is
  leaked, closed-source, and third-party hosted. That is the part that matters.
- **Claims that contradict the vendor.** "All PC games, RTX 20 through 50" is
  asserted while NVIDIA's own engineers are still tuning RTX 40.
- **Silence on the only hard part.** None explain how they supply motion vectors in
  a game that has none.
- **Known ecosystem risk.** DLSS Swapper's developer has publicly warned about
  malware-bearing DLLs and lookalike sites. Treat downloaded DLSS DLLs as unsafe
  unless they come from NVIDIA or an installed game.

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

Confirmed independently by inspecting the installed game files, which contain
`nvngx_dlss.dll`, `nvngx_dlssd.dll`, `nvngx_dlssg.dll` and Streamline DLLs, and
**no `nvngx_dlssnr.dll`**. That is consistent with the article and is also the
evidence that NVIDIA's `nvngx_dlss*` naming convention is real.

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
   is being treated as unreliable rather than cited. Independently checked
   2026-09-05: the **latest public `NVIDIA/DLSS` release is 310.7.0**, and its
   sample package contains `nvngx_dlss.dll` but **not** `nvngx_dlssnr.dll` — so the
   neural-rendering runtime is not in the public SDK, and ships by some other route.
3. **Whether the RTX 50 gate is in the DLL or the driver** (see section 4).
4. **Whether tier-3 output is genuine neural rendering** or a degraded
   approximation. No side-by-side analysis found.
5. **Whether injected DLSS 5 trips anti-cheat.** Warned about everywhere, tested
   nowhere.

---

## 8. Cross-check record

**2026-09-05.** This document was independently reviewed by Codex against NVIDIA and
official sources, with an explicit brief to falsify it. Recorded here because the
corrections matter more than the agreements.

**Agreed, unchanged:**

- Section 2, the inference-versus-training input split — reached independently from
  the same NVIDIA Research page. This is the load-bearing claim and it holds.
- DLSS 5 as a one-step pixel-space diffusion model generating final appearance;
  RTX 50 official support; driver 616.64; Streamline and Unreal Engine 5 plugin as
  the integration routes; and NBA 2K27 as the only native title found in NVIDIA
  public material.
- The Blood of Dawnwalker conclusion (section 6).
- The refusal to endorse or install any one-click DLSS 5 installer (section 5).

**Corrected as a result — the original was overclaiming in both cases:**

| Item | Was | Now | Why |
|---|---|---|---|
| `nvngx_dlssnr.dll` as runtime DLL | VERIFIED | HIGH CONFIDENCE | No NVIDIA primary source names the file; not present anywhere on the research machine; not in the public SDK |
| No DLSS 5 override in the NVIDIA App | NVIDIA-STATED | HIGH CONFIDENCE | The reporting behind that label was never actually read — the article returned HTTP 402. Supported indirectly, not by a direct NVIDIA denial |

**Also refined:** the timeline now separates three events rather than collapsing
them into one date — the GTC 2026 unveiling, the 2026-09-01 NVIDIA Research and
GeForce publications, and 2026-09-03 availability in a shipping game.

**One correction rejected, with evidence.** The second pass removed the GTC 2026
line as unsourced. It was not — NVIDIA's own GeForce article of 2026-03-17 states
that DLSS 5 was unveiled at GTC by the company's CEO. The line is restored *with*
the citation it should have carried originally. The underlying criticism was fair:
a claim whose source is not cited is indistinguishable from one that has none.

**Unchanged after review:** all five open questions in section 7 remain open. Both
agents were blocked by the same HTTP 403 on NVIDIA Research's paper PDF.

## Sources

- NVIDIA ADLR Research — *DLSS 5: Generative Neural Rendering* (2026-09-01) —
  <https://research.nvidia.com/labs/adlr/DLSS5/> — the inference-vs-training
  distinction in section 2 comes from here. Linked paper PDF is 403-blocked.
- NVIDIA GeForce — *DLSS 5: Neural Rendering Brings Lifelike Lighting to NBA 2K27* —
  <https://www.nvidia.com/en-us/geforce/news/dlss-5-3d-guided-neural-rendering/>
- NVIDIA GeForce — Game Ready 616.64 driver article —
  <https://www.nvidia.com/en-us/geforce/news/nba-2k27-dlss-5-3d-guided-neural-rendering-geforce-game-ready-driver/>
- NVIDIA GeForce — launch article confirming The Blood of Dawnwalker gets DLSS
  Super Resolution —
  <https://www.nvidia.com/en-us/geforce/news/star-wars-zero-company-aliens-fireteam-elite-blood-of-dawnwalker-dlss/>
- NVIDIA GeForce — DLSS 5 unveiled at GTC 2026, article dated 2026-03-17 —
  <https://www.nvidia.com/en-us/geforce/news/death-stranding-2-crimson-desert-dlss-4-multi-frame-gen/>
- NVIDIA Developer — public DLSS SDK and integration page —
  <https://developer.nvidia.com/rtx/dlss>
- GitHub — public `NVIDIA/DLSS` releases —
  <https://github.com/NVIDIA/DLSS/releases>
- GitHub — public `NVIDIA-RTX/Streamline` releases —
  <https://github.com/NVIDIA-RTX/Streamline/releases>
- Secondary/community-only sources for downgraded claims: VideoCardz headline
  about NVIDIA App override status (article not read; HTTP 402), Igor's Lab /
  TweakTown / Guru3D reporting on Ada-patched `nvngx_dlssnr.dll`, Tom's Hardware
  reporting the DLSS Swapper malware warning, and GitHub community tool release
  notes for `Dagherbou/OptiScaler_DLSSNR`.
