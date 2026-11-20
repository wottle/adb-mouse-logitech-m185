# Assembly

Part names refer to the files in [`models/`](../models/): the shells from `models/fdm/` or
`models/resin/` (whichever you printed), everything else from `models/common/`. There are no build photos yet: the M185
steps are the same as the Lisa mouse's, and its guide has photos of each.

## What you need

- The printed parts (see [PRINTING.md](PRINTING.md)).
- A **genuine** Logitech M185 (see the warning in the [Lisa mouse guide](https://github.com/wottle/lisa-mouse-logitech-m185/blob/main/docs/ASSEMBLY.md)).
- Screwdriver and **M3 screws**:

  | Use | Screw | Qty |
  |-----|-------|:---:|
  | PCB, rear boss (step 2) | M3×4 flat head | 1 |
  | PCB, front standoff (step 2) | M3×6, plus a washer if the head is small | 1 |
  | Button clamps (step 3) | M3×6 countersunk | 4 |
  | Button stop screws (step 4) | M3×8 pan or cap head | 2 |
  | Case, four corners (step 6) | M3×12 countersunk (M3×10 also works) | 4 |

- Optional: silicone grease, PTFE mouse slides.

## 1. Take the M185 apart

Follow steps 1–8 of the [Lisa mouse guide](https://github.com/wottle/lisa-mouse-logitech-m185/blob/main/docs/ASSEMBLY.md):
remove the battery and the single screw, open the case, lift out the board, and remove the rubber
scroll wheel. Then **desolder the scroll wheel's encoder** (the part the wheel's axle went into, beside
the right switch): it gets in the way of the right button. The middle-click switch can stay.

## 2. Board into the lower shell

Fit the power slider (`on_off_button.stl`) into its slot in the lower shell, then lay the board on
its ledges with the slider engaging the M185's power switch, exactly as on the Lisa mouse (its step 9).
Screw it down with the M3×4 flat head at the rear boss, then drive the M3×6 into the standoff in the
board's scroll-wheel cutout so its head (or a washer) clamps the narrow strip of board in front of the
cutout. That stops the front of the board lifting when the rear screw is tightened.

## 3. Buttons into the upper shell

Turn the upper shell over. Each button goes in from inside: its cap goes up through its half of the
window and its rear end (the clamp, with two countersunk holes) sits flat against the two bosses under
the hump. Screw each clamp to its bosses with two M3×6 countersunk screws, fully.

Each button should now spring back up on its own when pressed and released: the thin strip in front
of the clamp is the hinge.

## 4. Stop screws

Under the front of each button is a small boss. Drive an M3×8 into it from below until its tip is
level with the top of the button plate: no further for now.

These screws set the click point. Screwing one in pushes its tip against the inside of the roof and
lowers that button's resting position, bringing the nub on the button's underside down onto the
switch. With the head seated against the boss the screw is at its limit (about 0.7 mm at the nub).

## 5. Set the click point

Rest the upper shell on the lower shell (or put in two corner screws loosely) and press each button.

If the click comes too late with the stop screws out, print the **short-click buttons**
(`button_left_short.stl`, `button_right_short.stl`; see [PRINTING.md](PRINTING.md)) rather than
screwing the stop screws in: the screws shorten the travel by lowering the button, so its front no
longer sits flush. Use the stop screws for small trims:

- **Free play before the click:** open up and turn that button's stop screw **in** half a turn.
- **No click at all, or the button feels stuck down:** turn it **out** half a turn.

Repeat until each button clicks with no free play and no pre-click. Expect about one turn in from
where you started. Judge it with the case closed, as on the Lisa and Macintosh mice.

The stop screws are optional. Without them each button rests where its hinge holds it, and the nub
clicks the switch after a little free travel. If the buttons click well that way, leave them out.

If the left button rubs or will not return no matter how the stop screw is set, check whether the
middle-click switch is touching the underside of the cap. It isn't needed for a two-button mouse;
desolder it.

## 6. Close the case

Fit the halves together and screw them from underneath with four M3×12 countersunk screws at the
corners. Stick PTFE slides on the underside if you're using them.

## 7. Battery and door

Insert the AA cell, pushing it against the spring at the negative end first so the positive contact
wire isn't pushed out of place (see step 15 of the Lisa guide). Assemble the battery door from
`battery_cover_1.stl` and `battery_cover_2.stl`, fit it and latch it.

Use this repo's `battery_cover_1.stl`, not the Lisa mouse's: this mouse is lower-profile, so its door
has a battery saddle 1.2 mm lower. The Lisa door fits the opening but stands about 1.2 mm proud once a
cell is in.

## Troubleshooting

See the Lisa mouse guide's troubleshooting section: the battery contact wire and counterfeit boards
are the usual causes when nothing works.
