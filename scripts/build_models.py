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
CARRIED=('on_off_button',)      # from the Lisa mouse project, unchanged
BATTERY_SUPPORT_DROP=2.42        # battery_cover_1 is the Lisa door's main plate with the saddle that holds the cell lowered this much:
                                 # puts its rims (where a 14.5 cell sits; groove radius 7.10) at CELL_Z. History (Mike): 1.2, the
                                 # door closed but would not latch with a cell in; 2.7, flush but the latch end sat low and
                                 # dragged; 3.4, latched but very tight. All three still had the latch box's 4.8 roof under the cell
LATCH_TAB_SHIFT=0.5              # battery_cover_2 is the Lisa door's latch with its tab moved this much toward the battery (-x in
                                 # the print-orientation profile): with the cell in and the door flush, the Lisa latch's tab only
                                 # reached the surface of the fingernail recess (Mike, final assembly). 1.0 latched, but held the
                                 # door's latch end too low
LATCH_TAB_EXTEND=0.3             # ... and made this much longer along its own sides (64.7 deg), so it sticks out a little further
                                 # into the pocket (Mike: moved 1.0 alone it barely cleared the end of the bar; 1.0 longer was too
                                 # much; moved only 0.5 it needs less: 0.3)
LATCH_ARM_TOP=3.2                # battery_cover_2's arm, inside the latch box's tunnel, thinned from its top to this (was 3.6;
LATCH_ARM_END=19.95              # its underside stays on the tunnel floor at 2.0, so the tab doesn't move) up to this y, just
                                 # past the tunnel's mouth (19.85): room for a roof under the cell (BOX_TUNNEL_TOP)
LATCH_ARCH_THIN=0.3              # the arch spring thinned this much from its outside (1.2 -> 0.9 thick; the top comes down to
                                 # about 6.5): softer, since the cell still presses it down at the latch end (Mike)
def battery_cover_2():
    """the Lisa door's latch (a 6.2 mm extrusion of a zig-zag spring, print orientation as in source/lisa) with its tab moved,
    its arm thinner where it sits in the latch box and its arch spring thinner.
    The tab is the profile above the line along its base, (4.44, 10.16) to (5.87, 10.38) in profile coordinates (from
    the bounding-box corner), right of x 4.44; it is cut out, put back LATCH_TAB_SHIFT to the left, and the thin wedge
    under it is filled down to the bar."""
    from shapely import affinity
    t=trimesh.load(os.path.join(SRC,'lisa','battery_cover_2.stl'),force='mesh'); b=t.bounds; o=b[0][:2]
    g=xs_to_shapely(to_man(t).slice((b[0][2]+b[1][2])/2)); g=max((g.geoms if hasattr(g,'geoms') else [g]),key=lambda q:q.area)
    g=affinity.translate(g,-o[0],-o[1])
    A=(4.44,10.16); B=(5.87,10.38); k=(B[1]-A[1])/(B[0]-A[0]); S=LATCH_TAB_SHIFT
    above=sg.Polygon([A,(9,A[1]+k*(9-A[0])),(9,14),(A[0],14)])
    tab=g.intersection(above); base=g.difference(above); assert tab.geom_type=='Polygon' and 1.6<tab.area<1.8
    u=np.array([0.4274,0.9041])                                    # along the tab's sides, outward
    tab=tab.union(affinity.translate(tab,*(LATCH_TAB_EXTEND*u))).convex_hull      # the tab is convex: this just lengthens it
    def top_y(x): return sg.LineString([(x,0),(x,14)]).intersection(base).bounds[3]
    x0,x1=A[0]-S,B[0]-S
    fill=sg.Polygon([(x0,top_y(x0)-0.05),(x0,A[1]+0.01),(x1,B[1]+0.01),(x1,top_y(x1)-0.05)])
    new=base.union(affinity.translate(tab,-S,0)).union(fill).buffer(0); assert new.geom_type=='Polygon'
    # the rest is easier in the installed section (y along the door toward its latch end, z up), where the arm lies in the
    # latch box's tunnel (y 14.33..19.85, on the floor at z 2.0) and the arch rises from its end
    ang=math.degrees(math.atan2(u[1],u[0])); x0=affinity.rotate(new,-ang,origin=(0,0)).bounds[0]
    def inst(q): return affinity.translate(affinity.rotate(q,-ang,origin=(0,0)),14.33-x0,3.28)
    def prof(q): return affinity.rotate(affinity.translate(q,-(14.33-x0),-3.28),ang,origin=(0,0))
    I=inst(new); assert abs(I.bounds[1]-0.01)<0.02 and abs(I.bounds[3]-6.82)<0.02           # finger grip at the door's face
    I=I.difference(sg.box(13,LATCH_ARM_TOP,LATCH_ARM_END,5))                               # thinner arm in the tunnel
    zone=sg.box(19.9,2.5,25.2,9)
    out=[q for q in zone.difference(I).geoms if q.contains(sg.Point(22.4,7.5))][0]         # the air above the arch
    legs=sg.Polygon([(20.1,3.6),(24.55,4.06),(24.55,9),(20.1,9)])                           # above the arm's and the tab's tops
    I=I.difference(out.buffer(LATCH_ARCH_THIN,quad_segs=32).intersection(legs))
    for c in ((20.1,3.6),(24.55,4.06)):                                                     # round the two steps that leaves
        I=I.union(I.buffer(0.3,quad_segs=16).buffer(-0.3,quad_segs=16).intersection(sg.Point(c).buffer(0.8)))
    I=I.buffer(0); assert I.geom_type=='Polygon'
    new=prof(I)
    return prism(affinity.translate(new.simplify(0.002),o[0],o[1]),b[0][2],b[1][2])
CELL_R=7.25                      # AA cell radius (14.5 mm, the largest alkaline cells)
CELL_Z=4.0                       # the cell lies level with its underside this high (door frame, z up from the door's outside):
                                 # on the saddle's rims and on the latch box's roof. Saddle 3.4 lower put the rims at 3.02 but
                                 # the box roof (top 4.8) still held the latch end up, so it latched only very tight (Mike);
                                 # the door also flexes in under the saddle, so the saddle comes back up (BATTERY_SUPPORT_DROP)
BOX_TUNNEL_TOP=3.4               # underside of the latch box's roof, lowered from 3.8 to suit the thinner arm (LATCH_ARM_TOP)
                                 # with the same 0.2 play; the roof's top is grooved to the cell at CELL_Z, so it bridges
                                 # CELL_Z - BOX_TUNNEL_TOP = 0.6 thick in the middle and thicker toward its sides
def door_frame(t):
    """plan centroid and axis angle (deg) of battery_cover_1, with +y pointing to the latch box (the block that is 4.8 tall)"""
    V=t.vertices; c=V[:,:2].mean(0); P=V[:,:2]-c; ax=np.linalg.eigh(P.T@P)[1][:,1]
    box=np.abs(V[:,2]-4.8)<0.01
    if (P[box]@ax).mean()<0: ax=-ax
    return c,math.degrees(math.atan2(ax[1],ax[0]))
def battery_cover_1():
    """the Lisa door's main plate (print orientation, as in source/lisa) with its battery saddle lowered. Everything above
    z 5.5 is the saddle block's top (the rest of the door is 5.0 or lower; the block's walls run straight from 2.0), so its
    vertices move down and the walls just get shorter. Then the latch box's tunnel roof comes down to BOX_TUNNEL_TOP and
    its top gets a groove for the cell at CELL_Z."""
    t=trimesh.load(os.path.join(SRC,'lisa','battery_cover_1.stl'),force='mesh'); V=t.vertices.copy()
    top=V[:,2]>5.5; assert V[top,2].min()-BATTERY_SUPPORT_DROP>2.5     # keep the saddle above the door plate (top at 2.0)
    V[top,2]-=BATTERY_SUPPORT_DROP; t.vertices=V
    c,a=door_frame(t)
    fill=Manifold.cube([6.6,5.6,0.5]).translate([-3.3,14.2,BOX_TUNNEL_TOP])           # lower the tunnel roof (tunnel x +-3.15,
                                                                                    # y 14.33 to the mouth at 19.85, top 3.8)
    g=Manifold.cylinder(21.0,CELL_R,CELL_R,256).rotate([-90,0,0]).translate([0.094,9.0,CELL_Z+CELL_R])  # only over the box
    def place(M): return M.rotate([0,0,a-90]).translate([c[0],c[1],0])
    return to_man(t)+place(fill)-place(g)
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
    Ll=button(-1,U,NUB_GAP_LONG); Rl=button(1,U,NUB_GAP_LONG)                   # long-throw variants (the buttons don't
    for n,M in (('button_left',L),('button_right',R),('button_left_long',Ll),('button_right_long',Rl)):   # depend on the shells' outsides)
        export(M,'common',n)
    t=clean_export(battery_cover_2(),os.path.join(MODELS,'common','battery_cover_2.stl'))
    print(f'  common/battery_cover_2  latch tab moved {LATCH_TAB_SHIFT} mm, {LATCH_TAB_EXTEND} mm longer  size {np.round(t.extents,2)}  watertight {t.is_watertight}')
    t=clean_export(battery_cover_1(),os.path.join(MODELS,'common','battery_cover_1.stl'))
    print(f'  common/battery_cover_1  saddle lowered {BATTERY_SUPPORT_DROP} mm, box roof {BOX_TUNNEL_TOP}-{CELL_Z} grooved  size {np.round(t.extents,2)}  watertight {t.is_watertight}')
    for n in CARRIED:
        src=os.path.join(SRC,'lisa',n+'.stl')
        if os.path.exists(src): shutil.copy(src,os.path.join(MODELS,'common',n+'.stl'))
    for sub,(lo,U) in shells.items():
        print(f'===== {sub} shells, default (short-throw) buttons'); bad+=check(lo,U,L,R)
        print(f'===== {sub} shells, long-throw buttons (nub gap %.2f)'%NUB_GAP_LONG); bad+=check(lo,U,Ll,Rl,nub_gap=NUB_GAP_LONG)
    print('problems:',bad)
