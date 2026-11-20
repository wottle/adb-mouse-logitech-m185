# CLAUDE.md

Notes for working on this repo with Claude. Read this before changing any model.

## What this is

A 3D-printed replica of the Apple Desktop Bus Mouse (G5431, the boxy IIGS / Mac SE / Mac II mouse)
that holds the electronics of a Logitech M185 and one AA cell, with two buttons. Third of a set:
- Lisa mouse: <https://github.com/wottle/lisa-mouse-logitech-m185> (local `LisaMouseLogitechM185`)
- Macintosh M0100 mouse: <https://github.com/wottle/mac-mouse-logitech-m185> (local `AppleMouseLogitechM185`)

Both have their own `CLAUDE.md`; lessons there apply here.

## Layout

| Path | What |
|------|------|
| `models/` | Print-ready STLs, generated, in assembled position (frame F). `common/`: buttons (standard and `_short` pairs), battery door, slider. `fdm/`: the shells with parallel sides and the edge bevel. `resin/`: the shells with the original sides and edges (`build_lower(fdm=False)`, `build_top(fdm=False)`). |
| `scripts/geo.py` | Frames, board placement (`BOARD_X`, `BOARD_Y`), roof plane, CSG helpers, `clean_export`; `tm_adb` loads the source shells with `parallel_sides` applied. |
| `scripts/fits.py` | Stand-ins for the M185 parts, defined in the Lisa base frame. |
| `scripts/lisa_solid.py` | Rebuilds the Lisa base as a clean solid in `build/` (run once). |
| `scripts/build_lower.py` | Lower shell. |
| `scripts/build_top.py` | Upper shell and both buttons. |
| `scripts/build_models.py` | Runs everything, exports `models/`, runs the fit checks. |
| `scripts/sections.py` | `images/sections.png` (2D side sections). `render.py` is the splat renderer. |
| `scripts/hide_logo.py` | Render-only copies of the upper shells with the moulded Apple logo filled (`build/upper_shell_nologo_*.stl`). |
| `source/adb/` | StephenLulz's G5431 model (CC BY-NC-SA, tracked). Files are named `G4351` as downloaded. |
| `source/lisa/` | Lisa v1 base + battery door + power slider (`models/common/battery_cover_1.stl` is generated from it, lower). |

## Frames and key numbers

- **F**: X right (the user's right), Y forward (toward the buttons), Z up, underside z = 0. Front outside
  y = 49.255, rear −49.255. `T_ADB` maps the source model (Y up, front at its +Z) into F.
- **Lisa base frame → F**: x + `DX`, y + `DY`, z − 1.4. `BOARD_X` = Mac DX + 2.6 + 0.165 centres the
  two switches on the window (the source model is 0.165 off-centre). `BOARD_Y` = 13.5: board front edge
  that far behind the outside of the front wall. Further back gives more height (the roof rises 0.176 per
  mm) but moves the battery bay toward the sloping rear.
- **Roof frame R** (`build_top.toR`): the front part of the roof is a plane, z = −0.1760·y + 26.711 in F,
  exact to 0.002 mm from the front to y ≈ −15. Skin 2.79 thick. R makes it z = 0.
- Window: x −17.86..18.19; plan y 13.13..42.13 (F). Its walls are **vertical in F**, not square to the
  roof, so caps are vertical prisms in F (an earlier square-to-roof cap hit the rear jamb).
- Switch plungers (F): (−18.16, 20.96), (18.50, 20.96), top 16.1; each 0.3 mm outside the window edge.
- Case screws: the original four corners, F (−20.5, 42.155), (20.8, 42.155), (−22.3, −43.145),
  (22.7, −43.145). Upper bosses start at the seam, z 5.9, pilots re-drilled to 2.7 up to z 17. M3×12
  countersunk from below (about 6 mm of thread).
- Shells: the lower is a tub with tall sides at the rear; the upper is a cap whose sides are only the top
  few mm. The front of the lower is about 12.4 tall at the centre (old cable slot, now closed).

## Design and why

**Parallel sides** (FDM shells only; `geo.parallel_sides`, applied when `tm_adb(parallel=True)` loads the source shells, so everything downstream
follows): the source sides lean in (0.033 per mm of height) and taper (narrower at the front); printed on its side the
upward side banded. The outer skin (vertices within 0.3 of the convex hull, open face excluded) moves sideways by
`SIDE_W` − (that side's own fitted plane), ramped in across `RAMP_X` 22.0–24.2 where the roof and the front/rear faces are
flat across x (so they only stretch); beyond it the corners and roof edge move as a block. Side-face vertices snap to
exactly ±`SIDE_W` 28.5. Inner faces, bosses, the window and the logo (to x 21.5) don't move; the inside within 21.9 of
the centreline is unchanged. This also removed the source upper's 0.165 offset step at the seam. `SIDE_W` is set by the
battery door opening (x 26.9): 0.6 floor outside it under the bevel (now 1.6); rear walls lose at most 0.4.

**Lower shell** (`build_lower.py`): ADB outline, flat bottom with a 1 mm 45° bevel (not 3 mm as on the
Mac: the Lisa battery door opening reaches x = 26.2 on the right), interior stripped above
`FLOOR_CUT`, Lisa base floor and features inside, corner posts with conical countersinks, PCB front
standoff (same board position as the Lisa v2 and Mac), cable slot closed, Lisa features trimmed to
`LISA_TOP` 17.6 (bay walls stood 18.15, 0.12 under the right plate). Battery door, sensor and on/off
openings are identical to the Lisa base, so the Lisa door and slider fit the openings.

**Battery door: lower profile.** This shell is lower than the Lisa's, so the cell has less room above it: with a cell
in, the Lisa door stood about 1.2 mm proud (first print). `build_models.battery_cover_1()` makes the door's main plate
from `source/lisa/battery_cover_1.stl` with its battery saddle lowered `BATTERY_SUPPORT_DROP` 1.2: everything above
z 5.0 (print orientation) is the saddle block's top, so those vertices move down and its straight walls shorten. The
latch piece and the power slider are still copied unchanged (`CARRIED`). Seated in the Lisa base's opening the door
overlaps nothing (checked by matching its plate to the opening's 52.5 × 14.9 step at z 1.5–2).

**Battery bay = Lisa base** (`BAY_MARGIN`, `DOOR_MARGIN`, `WALL_MIN` in `build_lower.py`): within 3 mm of the cell and
1 mm of the door opening (and at least 2.2 in from the outside) everything above the floor is the Lisa base. A block of
the original ADB internals on the right wall had survived there (the interior ring wraps round wall-attached features),
leaving a tab in the bay at x 21.6–24.1, y −3.5 to −2.1, and clipping about 8 mm³ of the Lisa bay walls at the cell's +
end. Mike found the door seats without a cell either way; removed anyway as a stray. The cable-slot closing fill (z 5.3–5.85,
all of `Oi` outside the interior) must skip the bay too, or it puts a sliver of the tab back. Check: lower minus the Lisa base
in the bay zone above the floor is under 0.03 mm³.

**Upper edge bevel** (FDM only; `build_top.upper_shell(fdm=True)`, `edge_fill`, `edge_bevel_cutter`): the roof-to-side rounding (2.4 tall) is
replaced by a flat side up to `EDGE_BEVEL` 2.0 below the roof, then 45° to the roof, so the upper prints on its side with
no supports outside (flat strip 1.9 → 2.3). Built as fill + cuts, no coincident faces: the hull's yz profile at
|x| = `EDGE_X` 22.5, shrunk `EDGE_INSET` 0.03, extruded across x, kept inside the plan outline (hull projection −0.03, in
shapely, simplified: the raw CrossSection offset left near-duplicate vertices that broke the STL) and within
`EDGE_DEPTH` 2.6 of the roof; then the bevel is cut and the whole shell trimmed to |x| ≤ `SIDE_W`. Remaining outside
overhang > 45° with a side on the bed: about 25 mm² (corner ends, window radii, logo). Wall behind the bevel ≥ 2.9.

**Buttons** (`build_top.py`): flexure, not pins.
- Cap in its half of the window (`CAP_CLEAR` 0.6, 0.8 slot), on a 2 mm plate under the skin. Its top is a
  wedge in R: `CAP_PROUD` 0.3 above the roof at the window's rear edge, plus `CAP_FRONT_RAISE` 0.5 at its
  front edge. The first print rested about 1 mm low at the front with the rear flush and the click right,
  so the cap was raised rather than the plate re-angled (that would move the nub and the click). 1.0 stood
  proud; 0.5 is Mike's call. 0.35 clearance rubbed with the upper printed on its side (the window's jamb
  is then an overhang).
- Side clearances (second print scraped): plate outer edges `PLATE_X` ±22.65/23.0, at least 0.94 from the
  side walls; `CASE_BOSS_CLEAR` 1.0 round the front case-screw bosses; front tab `TAB_Y` 45.0 (46.2 touched
  the roof's rounding into the front wall). The only gaps under 0.5 left are vertical, under the roof
  (0.1 at the lip up-stop, 0.05 at the tab), and they open as the button is pressed.
- The plate is 2.6° steeper than the roof: 0.1 under the skin at the front lip (the up-stop), 2.5 below
  it at the clamp. Clamp pad 3 mm thick, two M3×6 countersunk screws up into bosses under the hump
  (`CLAMP_Y` −9). Hinge in front of the clamp: 0.8 thick, 4 long, two 5 mm straps per button (about
  0.4 N of spring on top of the switch, by estimate). Ribs on top keep the plate itself stiff.
- **Click point**: a fixed nub over each plunger (`NUB_R` 3.0, doubled so it can't miss; `NUB_GAP` 0.25 at rest,
  `NUB_GAP_SHORT` 0.0 for the `_short` pair, which `build_models.py` builds and checks as well: lever ratio
  cap front / nub is 1.89, so the short pair clicks 0.47 mm sooner at the front) plus an M3×8 **stop screw** under
  the plate front (y 44, x ±9) whose tip bears on the roof just ahead of the window; screwing in lowers
  the rest position. Range 0.71 mm at the nub with the head seated. This replaced cap-mounted striker
  screws: their heads would have landed on the encoder and middle-switch stand-ins, which sit about
  3 mm inboard of each switch.
- No pockets (`WHEEL` in `fits.py` is empty; the code still sweeps a pocket for any part listed there).
  The encoder is **desoldered**: on the first print it got in the way of the right button, and its
  pocket showed through the cap. The middle switch stays and clears the left button unpocketed (the
  photo-estimate box was too tall). Both boxes are kept as `fits.removed` and are not checked.
- The upper shell's original button mount (pins at x ±21 and on the centreline at the hinge line, two
  ribs) and the cable ribs at the front are removed.
  The cable ribs (x ±7.8, 1.5 wide) go via `geo.cable_ribs_cut()`, used by both shells: the first cut stopped at the
  front wall's inside face (y 46.45) and left two 0.11 mm fins hanging below the front rim (z 6.4–11.5), and the lower's
  print-tolerance cut (made from the source upper) had notched its front wall for them. Cut below `FRONT_RIM_Z` 11.5,
  under the front lip (11.53).

## Checks

`build_models.py` builds both shell variants and checks each with both button pairs; it must end with
`problems: 0`. Expected:
- both button pairs checked (the `_short` pair reports gap 0.00 to its switches, by design);
- buttons × upper 0.000 with gap 0 (clamp pads sit on their bosses);
- lower × pcb / AA counted only beyond what the plain Lisa base has (the boxes ignore the board's cutouts);
- right button at 3.0° press touches the trimmed bay wall (0.07 mm³): beyond the switch's travel
  (the nub meets the plunger at 0.6°, bottoming about 0.5° later).

`press(M, deg)`: positive = pressed (front down). In F a positive rotation about x lifts the front;
the first draft had the sign wrong and swept the wheel pockets the wrong way.

## Status

Built 2026-11-19. **Printed 2026-11-20**: prints well, clicks work well (stop screws apparently not fitted).
- First print: the encoder had to be desoldered, its pocket showed through the right cap, and the
  buttons rested about 1 mm low at the front.
- Second print (`CAP_FRONT_RAISE` 1.0): fronts stood proud; with the upper printed on its side (Mike's
  preference, for the top's finish) the right button rubbed on the window's right edge and perhaps the
  inside wall; the left pocket was unneeded.
- Since then: raise 0.5, `CAP_CLEAR` 0.6, plates and tab pulled in, no pockets, `NUB_R` 3.0. Printed: the
  fronts sat flush but the click came late, hence the `_short` pair (not printed yet). The real plungers
  evidently sit lower than `SW_TOP` (the button rests a little nose-down and still has free play).

Open items:
- Print the `_short` buttons: click point right? Free in the window? (Tune `NUB_GAP_SHORT`, `CAP_CLEAR`.)
- Print the parallel-sided, bevelled shells (2026-11-20, not printed): upper on its side, check the bed strip holds and
  the bevel needs no support; check the battery door still fits (its opening is unchanged).
- Whether the stop screws earn their place, or can go (the click was good without them).
- Print orientation: lower flat, upper on its side (or as modelled with roof supports), buttons cap down.
- Slicer project: `print/adb_mouse_m185_creality_k2_plus.3mf` (Mike's, Creality K2 Plus); made before the parallel
  sides and bevel, so re-slice the shells. No photos yet.

## Animation and pictures

**Keep the Apple logo out of pictures** (Mike, 2026-11-20, as on the source model this is based on). The printed
upper shells keep their moulded logo; every render of the top uses `build/upper_shell_nologo_fdm.stl` from
`scripts/hide_logo.py` (the logo recess on the rear slope filled flush), and views stay low and from the front or
sides, not straight down on the top.

`images/animation.gif` (README, 640×360, 15 fps) and `images/animation.mp4` (1280×720, 30 fps, 10 s loop)
are VTK renders of the FDM shells and common buttons: exploded, together, one full turn at 14° elevation, apart
again. `images/preview.png` is two VTK stills from the front right at 18° (assembled; exploded with the M185
stand-ins). Both were rendered outside the repo (offscreen VTK through EGL, piped to ffmpeg); re-render them when
the models change. `images/buttons.png` (splat render, buttons only) and `images/sections.png` don't show the top.

## Working conventions

- **Mike runs git himself.** Leave changes uncommitted; give him the commands. Claude cannot push.
- Never report something as done without checking the output: look at a render or a 2D section
  (`scripts/sections.py` is far clearer than the splat renders for clearances), and after writing to the
  Mac compare checksums there against the build.
- Mesh hygiene, learned here: cutters that only graze a drafted face (or sit exactly on one) leave
  zero-width slivers that break STL round trips. Overlap generously instead (the interior cutter is the
  wall's inner outline + 0.3; fills sit 0.05 inside the original skin; floor joins overlap at
  `FLOOR_CUT`, kept off the Lisa solid's 0.05 grid). `clean_export` tries the plain mesh first; simplify
  can itself break a clean mesh.
- Two outputs: FDM shells (print-friendly changes) and resin shells (the original's outside). Keep anything that
  changes the outside only for printing on FDM behind the `fdm` switch.
- Print-friendliness rules Mike has asked for (FDM): flat bottoms with 45° bevels, 45° ramps under bosses,
  conical countersinks, supports only where unavoidable, solid blocks where they save supports.
- One named constant per tunable dimension, with a comment saying what it does.
- Mike's calipers have drifted off zero before; confirm a surprising measurement.
