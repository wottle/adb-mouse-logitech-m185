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

## Orientation

The STLs are in assembled position, not print position: lay them out as below.

### Lower shell
Flat underside on the bed. Supports only where the slicer insists inside the M185 mounting, as for
the Lisa mouse's base.

### Upper shell
Either way works:
- **On its side** (as for the Macintosh mouse) gives the best finish on the top. The window then
  prints with one jamb as an overhang, which may sag a little; the caps have 0.6 mm of clearance to
  allow for it.
- **As modelled**, rim down and top up, with tree supports under the inside of the roof. The outside
  needs no supports, but the top shows its layer steps.

### Buttons
There are two pairs; print one:

| Pair | Files | Click |
|------|-------|-------|
| Longer click | `button_left.stl`, `button_right.stl` | Some free travel before the click (about 0.5 mm at the front edge of the cap, plus the switch's own travel). |
| Shorter click | `button_left_short.stl`, `button_right_short.stl` | The nubs are 0.25 mm taller and start on the switches, so the click comes about 0.5 mm sooner. |

They are otherwise identical. If you're unsure, start with the shorter click; if a button feels held
down or won't click back, use the longer one (or that one button from the other pair).

Cap face down on the bed, with supports under the plate around the cap. The cap top is the visible
surface and gets the first-layer finish. The thin hinge strip (0.8 mm) then prints flat, in four
layers, which is the strong direction for it.

PLA is fine for the hinges: they bend about 0.25 % at a full click, far below what PLA tolerates.
PETG is an alternative if you prefer.

### Battery door and power slider
As for the Lisa mouse (see its [PRINTING.md](https://github.com/wottle/lisa-mouse-logitech-m185/blob/main/docs/PRINTING.md)).

## Fit

- Each cap has 0.6 mm of clearance to the window all round, and the two caps have 0.8 mm between them.
  The plates keep about 1 mm from the side walls and the front case-screw bosses.
- If a cap rubs in the window, sand its side lightly; don't enlarge the window.
