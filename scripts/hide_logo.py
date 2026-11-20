#!/usr/bin/env python3
"""Copies of the upper shells with the moulded Apple logo filled in, for renders only.

Mike's rule for this repo (as for the source model it is based on): keep the Apple logo out of pictures. The printed
models keep the logo; images/ (preview, animation) are rendered from these copies, from views that don't look straight
down on the top.

    python3 scripts/hide_logo.py      # writes build/upper_shell_nologo_fdm.stl and build/upper_shell_nologo_resin.stl
"""
from geo import *
LOGO_BOX=(-22.5,-13.5,-40.5,-31.0)   # plan box round the logo on the rear slope (logo: x -21.5..-14.5, y -39.5..-32)
LOGO_ROOF=(0.3622,36.265)            # the rear slope there: z = a*y + c (exact plane in the source)
LOGO_FILL=1.2                        # fill this far below the slope (the logo is shallower)
def hide_logo(U):
    x0,x1,y0,y1=LOGO_BOX; a,c=LOGO_ROOF
    n=np.array([0,-a,1.0]); L=np.linalg.norm(n)
    slab=box(x0,x1,y0,y1,0,40).trim_by_plane(list(-n),-c/L).trim_by_plane(list(n),(c-LOGO_FILL)/L)   # between the slope and 1.2 under it
    return U+slab
if __name__=='__main__':
    for v in ('fdm','resin'):
        U=to_man(trimesh.load(os.path.join(ROOT,'models',v,'upper_shell.stl'),force='mesh'))
        p=os.path.join(BUILD,f'upper_shell_nologo_{v}.stl'); to_tm(hide_logo(U)).export(p); print('wrote',p)
