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
| `models/` | Print-ready STLs, generated. The four new parts are in assembled position (frame F). |
| `scripts/geo.py` | Frames, board placement (`BOARD_X`, `BOARD_Y`), roof plane, CSG helpers, `clean_export`. |
| `scripts/fits.py` | Stand-ins for the M185 parts, defined in the Lisa base frame. |
| `scripts/lisa_solid.py` | Rebuilds the Lisa base as a clean solid in `build/` (run once). |
| `scripts/build_lower.py` | Lower shell. |
| `scripts/build_top.py` | Upper shell and both buttons. |
| `scripts/build_models.py` | Runs everything, exports `models/`, runs the fit checks. |
| `scripts/sections.py` | `images/sections.png` (2D side sections). `render.py` is the splat renderer. |
| `source/adb/` | StephenLulz's G5431 model (CC BY-NC-SA, tracked). Files are named `G4351` as downloaded. |
| `source/lisa/` | Lisa v1 base + battery door + power slider. |

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

**Lower shell** (`build_lower.py`): ADB outline, flat bottom with a 1 mm 45° bevel (not 3 mm as on the
Mac: the Lisa battery door opening reaches x = 26.2 on the right), interior stripped above
`FLOOR_CUT`, Lisa base floor and features inside, corner posts with conical countersinks, PCB front
standoff (same board position as the Lisa v2 and Mac), cable slot closed, Lisa features trimmed to
`LISA_TOP` 17.6 (bay walls stood 18.15, 0.12 under the right plate). Battery door, sensor and on/off
openings are identical to the Lisa base, so the Lisa door and slider fit.

**Buttons** (`build_top.py`): flexure, not pins.
- Cap in its half of the window (0.35 clearance, 0.8 slot, 0.3 proud), on a 2 mm plate under the skin.
- The plate is 2.6° steeper than the roof: 0.1 under the skin at the front lip (the up-stop), 2.5 below
  it at the clamp. Clamp pad 3 mm thick, two M3×6 countersunk screws up into bosses under the hump
  (`CLAMP_Y` −9). Hinge in front of the clamp: 0.8 thick, 4 long, two 5 mm straps per button (about
  0.4 N of spring on top of the switch, by estimate). Ribs on top keep the plate itself stiff.
- **Click point**: a fixed nub over each plunger (0.25 gap at rest) plus an M3×8 **stop screw** under
  the plate front (y 44, x ±9) whose tip bears on the roof just ahead of the window; screwing in lowers
  the rest position. Range 0.71 mm at the nub with the head seated. This replaced cap-mounted striker
  screws: their heads would have landed on the encoder and middle-switch stand-ins, which sit about
  3 mm inboard of each switch.
- Caps are pocketed for the encoder and middle switch, swept over 2.5° of press plus 0.4 clearance;
  0.83–0.85 mm of cap left above them.
- The upper shell's original button mount (pins at x ±21 and on the centreline at the hinge line, two
  ribs) and the cable ribs at the front are removed.

## Checks

`build_models.py` must end with `problems: 0`. Expected:
- buttons × upper 0.000 with gap 0 (clamp pads sit on their bosses);
- lower × pcb / AA counted only beyond what the plain Lisa base has (the boxes ignore the board's cutouts);
- right button at 3.0° press touches the trimmed bay wall (0.07 mm³): beyond the switch's travel
  (the nub meets the plunger at 0.6°, bottoming about 0.5° later).

`press(M, deg)`: positive = pressed (front down). In F a positive rotation about x lifts the front;
the first draft had the sign wrong and swept the wheel pockets the wrong way.

## Status

Built 2026-11-19, **not printed**. Open items:
- Print and test: hinge feel, stop-screw range, cap fit in the window, door fit, case screw lengths.
- Real heights and positions of the M185 encoder and middle-click switch (only photo estimates).
- Print orientation is a recommendation only (lower flat, upper as modelled with roof supports,
  buttons cap down).
- No slicer project or photos yet.

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
- Print-friendliness rules Mike has asked for: flat bottoms with 45° bevels, 45° ramps under bosses,
  conical countersinks, supports only where unavoidable, solid blocks where they save supports.
- One named constant per tunable dimension, with a comment saying what it does.
- Mike's calipers have drifted off zero before; confirm a surprising measurement.
