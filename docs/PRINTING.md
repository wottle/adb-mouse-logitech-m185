# Printing

## Settings

Untested on this mouse yet. These are the settings used for the Lisa and Macintosh mice:

| Setting | Value |
|---------|-------|
| Nozzle | 0.4 mm |
| Layer height | 0.20 mm |
| Walls | 2 |
| Top / bottom layers | 5 / 3 |
| Infill | 15 %, grid |
| Supports | Tree; paint them on by hand where listed below |
| Material | PLA |

Any FDM printer with roughly a 100 × 100 mm bed can print every part.

**Which shells:** print `models/fdm/lower_shell.stl` and `models/fdm/upper_shell.stl` on an FDM printer,
and everything in `models/common/`. On a resin printer use `models/resin/` instead: those shells keep
the original's sloping sides and rounded edges, which don't need straightening for resin. Orient and
support them as your resin slicer suggests; the notes below are for FDM.

## Orientation

The STLs are in assembled position, not print position: lay them out as below.

### Lower shell
Flat underside on the bed. Supports only where the slicer insists inside the M185 mounting, as for
the Lisa mouse's base.

### Upper shell
**On its side** (either side down) gives the best finish on the top, and the shell is shaped for it:
- the sides are flat and parallel, so the side facing up has no layer banding;
- the side on the bed is a flat strip about 2.3 mm tall, topped by a 45° bevel instead of a curve, so
  the outside needs no supports (apart from a few mm² where the bevel meets the rounded corners);
- inside, the case-screw and button-clamp bosses still need supports;
- the window prints with one jamb as an overhang, which may sag a little; the caps have 0.6 mm of
  clearance to allow for it.

It also prints **as modelled**, rim down and top up, with tree supports under the inside of the roof;
the outside then needs no supports, but the top shows its layer steps.

### Buttons
There are two pairs; print one:

| Pair | Files | Click |
|------|-------|-------|
| Short throw (default) | `button_left.stl`, `button_right.stl` | The nubs start on the switches, so the click comes almost as soon as you press. |
| Longer throw | `button_left_long.stl`, `button_right_long.stl` | The nubs are 0.25 mm shorter: about 0.5 mm more travel at the front edge of the cap before the click, for a more deliberate press. |

They are otherwise identical. Print the default pair unless you want each press to be more deliberate.
If a default button feels held down or won't click back on your board, use the longer-throw one.

Cap face down on the bed, with supports under the plate around the cap. The cap top is the visible
surface and gets the first-layer finish. The thin hinge strip (0.8 mm) then prints flat, in four
layers, which is the strong direction for it.

PLA is fine for the hinges: they bend about 0.25 % at a full click, far below what PLA tolerates.
PETG is an alternative if you prefer.

### Battery door and power slider
As for the Lisa mouse (see its [PRINTING.md](https://github.com/wottle/lisa-mouse-logitech-m185/blob/main/docs/PRINTING.md)).
Print this repo's `battery_cover_1.stl`: its battery saddle is 1.2 mm lower than the Lisa mouse's,
for this mouse's lower profile.

## Fit

- Each cap has 0.6 mm of clearance to the window all round, and the two caps have 0.8 mm between them.
  The plates keep about 1 mm from the side walls and the front case-screw bosses.
- If a cap rubs in the window, sand its side lightly; don't enlarge the window.
