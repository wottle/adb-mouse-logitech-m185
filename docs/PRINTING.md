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
As modelled, rim down and top up, with tree supports under the inside of the roof. The outside then
needs no supports and keeps its finish. The mouse is slightly wedge-shaped and only the top few
millimetres of the sides belong to the upper shell, so printing it on its side (as for the Macintosh
mouse) doesn't suit this one.

### Buttons
Cap face down on the bed, with supports under the plate around the cap. The cap top is the visible
surface and gets the first-layer finish. The thin hinge strip (0.8 mm) then prints flat, in four
layers, which is the strong direction for it.

PLA is fine for the hinges: they bend about 0.25 % at a full click, far below what PLA tolerates.
PETG is an alternative if you prefer.

### Battery door and power slider
As for the Lisa mouse (see its [PRINTING.md](https://github.com/wottle/lisa-mouse-logitech-m185/blob/main/docs/PRINTING.md)).

## Fit

- Each cap has 0.35 mm of clearance to the window all round, and the two caps have 0.8 mm between them.
- If a cap rubs in the window, sand its side lightly; don't enlarge the window.
