# Source meshes

Inputs for `scripts/build_models.py`.

- `adb/` — **Apple Desktop Bus Mouse - Model G5431 (Shell)** by StephenLulz,
  <https://www.thingiverse.com/thing:4545460>, licensed CC BY-NC-SA (see `adb/LICENSE.txt` and
  `adb/README.txt`). The upper and lower shells are used; the original button and ball retainer are
  included for reference. (The files are named `G4351`, as in the original download.)
- `lisa/base.stl` — the (v1) base from the
  [Lisa mouse conversion](https://github.com/wottle/lisa-mouse-logitech-m185). The M185 mounting is
  taken from it. `scripts/lisa_solid.py` turns it into a clean solid in `build/`.
- `lisa/battery_cover_1.stl`, `battery_cover_2.stl`, `on_off_button.stl` — from the same project,
  copied unchanged into `models/`.
