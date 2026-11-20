#!/usr/bin/env python3
"""Build every part into models/ and run the fit checks.

    python3 scripts/lisa_solid.py      # once: clean solid of the Lisa base (build/lisa_base_solid.stl)
    python3 scripts/build_models.py

The checks print overlaps and gaps between every pair of parts and the M185 stand-ins, at rest and through the press,
and end with 'problems: N'.
"""
import shutil, itertools
from build_lower import build_lower, BEVEL
from build_top import *
MODELS=os.path.join(ROOT,'models')
CARRIED=('battery_cover_1','battery_cover_2','on_off_button')   # from the Lisa mouse project, unchanged
def gap(a,b,cap=3.0):
    return 0.0 if (a^b).volume()>1e-4 else a.min_gap(b,cap)
def check(lo,U,L,R,verbose=True):
    bad=0; P=dict(upper=U,lower=lo,left=L,right=R)
    E={k:v for k,v in prox.items()}
    print('--- at rest: overlap (mm3) / gap (mm)')
    for a,b in itertools.combinations(P,2):
        v=(P[a]^P[b]).volume(); g=gap(P[a],P[b])
        ok=v<0.05
        print(f'  {a:6s} x {b:6s} overlap {v:7.3f}  gap {g:5.2f}'+('' if ok else '   <-- PROBLEM')); bad+=not ok
    Ls=to_man(trimesh.load(LISA_SOLID,force='mesh')).translate([DX,DY,DZ])
    for a in P:
        for k,e in E.items():
            v=(P[a]^e).volume(); g=gap(P[a],e)
            if a=='lower': v=((P[a]^e)-(Ls^e)).volume()       # the board and cell boxes are coarse: count only overlap the Lisa base doesn't have
            if g<1.0 or v>0:
                ok=v<0.01
                print(f'  {a:6s} x {k:7s} overlap {v:7.3f}  gap {g:5.2f}'+('' if ok else '   <-- PROBLEM')); bad+=not ok
    print('--- pressing (degrees about the hinge); the nub reaches its plunger at about',
          f'{math.degrees(NUB_GAP/(SW_L[1]-hinge_axis_F()[0])):.2f} deg with the stop screw backed off')
    hy,hz=hinge_axis_F(); fwd=box(-60,60,hy,80,-60,80)
    for side,B,sw in (('left',L,'swL'),('right',R,'swR')):
        row=[]
        for deg in (0.5,1.0,1.5,2.0,2.5,3.0):
            Bm=press(B^fwd,deg)+(B-fwd)                       # only the part ahead of the hinge swings; the clamp stays put
            hits=[]
            for nm,O in list(P.items())+list(E.items()):
                if nm in (side,sw): continue
                v=(Bm^O).volume()-((B-fwd)^O).volume()
                if v>0.01: hits.append(f'{nm} {v:.2f}')
            row.append(f'{deg}: '+(', '.join(hits) if hits else 'clear'))
        print(f'  {side:5s} '+' | '.join(row)); bad+=sum('clear' not in r for r in row[:4])
    return bad
if __name__=='__main__':
    os.makedirs(MODELS,exist_ok=True)
    lo,_=build_lower(); U,L,R=build_top()
    for n,M in (('lower_shell',lo),('upper_shell',U),('button_left',L),('button_right',R)):
        t=clean_export(M,os.path.join(MODELS,n+'.stl')); print(f'  {n:13s} {len(t.faces):7d} tris  size {np.round(t.extents,1)}')
    for n in CARRIED:
        src=os.path.join(SRC,'lisa',n+'.stl')
        if os.path.exists(src): shutil.copy(src,os.path.join(MODELS,n+'.stl'))
    bad=check(lo,U,L,R)
    print('problems:',bad)
