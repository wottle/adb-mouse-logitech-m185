#!/usr/bin/env python3
"""Build every part into models/ and run the fit checks.

models/common  parts that are the same however you print: buttons, battery door, power slider
models/fdm     the shells for FDM: parallel sides, and a bevel on the top's side edges, to print on their sides
models/resin   the shells for resin: the original's sloping sides and rounded edges

    python3 scripts/lisa_solid.py      # once: clean solid of the Lisa base (build/lisa_base_solid.stl)
    python3 scripts/build_models.py

The checks print overlaps and gaps between every pair of parts and the M185 stand-ins, at rest and through the press,
and end with 'problems: N'.
"""
import shutil, itertools
from build_lower import build_lower, BEVEL
from build_top import *
MODELS=os.path.join(ROOT,'models')
VARIANTS=(('fdm',True),('resin',False))
CARRIED=('battery_cover_2','on_off_button')   # from the Lisa mouse project, unchanged
BATTERY_SUPPORT_DROP=1.2         # battery_cover_1 is the Lisa door's main plate with the saddle that holds the cell lowered this much:
                                 # with a cell in, the Lisa door stood about 1.2 mm proud of the underside (Mike, first print)
def battery_cover_1():
    """the Lisa door's main plate (print orientation, as in source/lisa) with its battery saddle lowered. Everything above
    z 5.0 is the saddle block's top (the rest of the door is 5.0 or lower; the block's walls run straight from 2.0), so its
    vertices move down and the walls just get shorter."""
    t=trimesh.load(os.path.join(SRC,'lisa','battery_cover_1.stl'),force='mesh'); V=t.vertices.copy()
    top=V[:,2]>5.5; assert V[top,2].min()-BATTERY_SUPPORT_DROP>5.0
    V[top,2]-=BATTERY_SUPPORT_DROP; t.vertices=V; return t
def gap(a,b,cap=3.0):
    return 0.0 if (a^b).volume()>1e-4 else a.min_gap(b,cap)
def check(lo,U,L,R,verbose=True,nub_gap=NUB_GAP):
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
          f'{math.degrees(nub_gap/(SW_L[1]-hinge_axis_F()[0])):.2f} deg with the stop screw backed off')
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
def export(M,sub,n):
    d=os.path.join(MODELS,sub); os.makedirs(d,exist_ok=True)
    t=clean_export(M,os.path.join(d,n+'.stl')); print(f'  {sub}/{n:18s} {len(t.faces):7d} tris  size {np.round(t.extents,1)}')
if __name__=='__main__':
    bad=0; shells={}
    for sub,fdm in VARIANTS:
        lo,_=build_lower(fdm=fdm); U,L,R=build_top(fdm=fdm); shells[sub]=(lo,U)
        export(lo,sub,'lower_shell'); export(U,sub,'upper_shell')
    Ls=button(-1,U,NUB_GAP_SHORT); Rs=button(1,U,NUB_GAP_SHORT)                 # short-click variants (the buttons don't
    for n,M in (('button_left',L),('button_right',R),('button_left_short',Ls),('button_right_short',Rs)):   # depend on the shells' outsides)
        export(M,'common',n)
    t=battery_cover_1(); t.export(os.path.join(MODELS,'common','battery_cover_1.stl'))
    print(f'  common/battery_cover_1  saddle lowered {BATTERY_SUPPORT_DROP} mm  size {np.round(t.extents,2)}  watertight {t.is_watertight}')
    for n in CARRIED:
        src=os.path.join(SRC,'lisa',n+'.stl')
        if os.path.exists(src): shutil.copy(src,os.path.join(MODELS,'common',n+'.stl'))
    for sub,(lo,U) in shells.items():
        print(f'===== {sub} shells, standard buttons'); bad+=check(lo,U,L,R)
        print(f'===== {sub} shells, short-click buttons (nub gap %.2f)'%NUB_GAP_SHORT); bad+=check(lo,U,Ls,Rs,nub_gap=NUB_GAP_SHORT)
    print('problems:',bad)
