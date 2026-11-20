"""Upper shell and the two buttons.

Each button is one piece: a cap in its half of the window, flush with the roof, on a plate that runs under the roof skin
and is screwed up into two bosses under the hump. The plate bends at a thin hinge in front of its clamp (a flexure, like
the original ADB button), so there are no pins to sag or bind. Each button presses its M185 switch through an M3
countersunk screw (the striker), threaded up into the cap; turning it sets the click point.

Most geometry is made in the roof frame R: the outer roof plane is z=0 and y runs along the roof (y_R = y / cos(roof angle)).
"""
import math
from fits import *
TH=math.degrees(math.atan(-ROOF_A)); CT=math.cos(math.radians(TH))
def toR(M): return M.translate([0,0,-ROOF_C]).rotate([TH,0,0])
def fromR(M): return M.rotate([-TH,0,0]).translate([0,0,ROOF_C])
def R_of(y,z):                       # F (y,z) -> R (y,z)
    a=math.radians(TH); z=z-ROOF_C; return y*math.cos(a)-z*math.sin(a), y*math.sin(a)+z*math.cos(a)

# --- the window (roof frame), measured from the upper shell
WIN_X=(-17.86,18.19); WIN_Y=(13.42,42.87); WIN_R=1.5
GAP=0.8                              # slot between the two buttons
CAP_CLEAR=0.35                       # cap to window, each side
CAP_PROUD=0.3                        # cap top above the roof
# --- plate (roof frame z is negative inside)
PLATE_T=2.0
GAP_LIP=0.1                          # plate top below the roof skin at the front lip (the up-stop)
LIP=1.5                              # plate reaches this far in front of the window
PLATE_X={-1:-23.15,1:23.5}           # outer edges (inner walls are about +-24.0 at the front)
# --- clamp under the hump, hinge in front of it
CLAMP_Y=-9.0                         # F y of the clamp screws
CLAMP_L=9.0; CLAMP_T=3.0
BOSS_H=2.5                           # clamp bosses hang this far below the roof skin
BOSS_R=3.5
CLAMP_X=(5.0,17.0)                   # |x| of the two clamp screws per button
HINGE_L=4.0; HINGE_T=0.8; STRAP_W=5.0
RIB_W=1.6; RIB_CLEAR=0.35; RIB_X=(8.0,15.0)   # |x| of the stiffening ribs on top of each plate
# --- click point: a fixed printed nub over each switch, and an M3 stop screw at the front of each plate whose tip bears
# on the inside of the roof in front of the window. Screwing it in lowers the button's resting position (the hinge holds
# the plate up against it), which brings the nub down onto the switch. The scroll-wheel parts sit about 3 mm inboard of
# each switch, which is where a striker screw in the cap would have to go, so the adjustment lives at the front instead.
NUB_R=1.5; NUB_GAP=0.25              # nub over the plunger; its gap to the plunger top with the button at rest, screw backed off
STOP_X=9.0; STOP_Y=44.0              # stop screw (F); 2.2 mm in front of the window, 2.5 behind the front wall
STOP_BOSS_R=2.2; STOP_BOSS_L=4.5     # boss under the plate; an M3x8 seated against it stands 1.5 above the plate top
TAB_Y=46.2                           # plate front edge round the stop screw (front wall inside face at 46.5)
WHEEL_CLEAR=0.4; PRESS_DEG=2.5       # clearance kept round the scroll-wheel parts, over this much press

yl=WIN_Y[1]+LIP                      # R y of the plate's front lip
yc=R_of(CLAMP_Y,ceil(CLAMP_Y))[0]    # R y of the clamp centre
zl=-SKIN-GAP_LIP; zc=-SKIN-BOSS_H    # plate top at the lip and at the clamp (R z)
SLOPE=(zl-zc)/(yl-yc)                # plate top: z = zc + SLOPE*(y - yc)  (R)
def plate_top_R(y): return zc+SLOPE*(y-yc)
def half_plane(below=True,dz=0.0):
    """everything below (or above) the plate-top plane shifted by dz, in R"""
    n=np.array([0,-SLOPE,1.0]); L=np.linalg.norm(n); off=(zc-SLOPE*yc+dz)/L     # plane: n.p = off
    big=box(-60,60,-80,80,-60,60)
    return big-big.trim_by_plane(list(n),off) if below else big.trim_by_plane(list(n),off)
def window_plan_F():
    """plan outline of the window in F. Its walls are vertical (not square to the roof), so the plan is the same at any depth."""
    a=math.radians(TH); ring=np.asarray(rrect(WIN_X[0],WIN_X[1],WIN_Y[0],WIN_Y[1],WIN_R).exterior.coords)
    zr=-0.5                                                       # WIN_Y was measured 0.5 below the outer surface
    yF=ring[:,1]*math.cos(a)+zr*math.sin(a)
    return sg.Polygon(np.c_[ring[:,0],yF])
def cap_prism_F(s):
    w=window_plan_F().buffer(-CAP_CLEAR,join_style=1)
    half=sg.box(min(s*GAP/2,s*40),-60,max(s*GAP/2,s*40),80)
    return prism(w.intersection(half),0,40)
def window_R():
    return xs_from_shapely(rrect(WIN_X[0],WIN_X[1],WIN_Y[0],WIN_Y[1],WIN_R))
y_h0=yc+CLAMP_L/2                    # hinge from here...
y_h1=y_h0+HINGE_L                    # ...to here (R y); the plate proper starts at y_h1
HINGE_AXIS_R=((y_h0+y_h1)/2, plate_top_R((y_h0+y_h1)/2)-HINGE_T/2)
def hinge_axis_F():
    a=math.radians(TH); y,z=HINGE_AXIS_R
    return y*math.cos(a)+z*math.sin(a), -y*math.sin(a)+z*math.cos(a)+ROOF_C
def press(M,deg):
    """rotate a button about its hinge; positive = pressed (front moves down). In F a positive rotation about x lifts
    anything ahead of the axis, hence the minus."""
    hy,hz=hinge_axis_F(); return M.translate([0,-hy,-hz]).rotate([-deg,0,0]).translate([0,hy,hz])

def button(side,U):
    s=side; xin=s*GAP/2; xout=PLATE_X[s]; x0,x1=sorted((xin,xout))
    # plate slab: from the clamp's rear end to the lip
    slab=half_plane(True)-half_plane(True,-PLATE_T)
    plate=slab^box(x0,x1,yc-CLAMP_L/2,yl,-40,10)
    clamp=(half_plane(True)-half_plane(True,-CLAMP_T))^box(x0,x1,yc-CLAMP_L/2,y_h0,-40,10)
    # hinge: thin strip, two straps (inner and outer edge of the plate)
    hinge_cut=(half_plane(True,-HINGE_T)^box(x0-1,x1+1,y_h0,y_h1,-40,10))
    straps=box(*sorted((xin,xin+s*STRAP_W)),y_h0-0.01,y_h1+0.01,-40,10)+box(*sorted((xout,xout-s*STRAP_W)),y_h0-0.01,y_h1+0.01,-40,10)
    slot=box(x0,x1,y_h0,y_h1,-40,10)-straps
    # cap: the window less clearance, this side of the slot, from inside the plate up to just proud of the roof
    cap=fromR(box(-40,40,-40,80,-40,CAP_PROUD)-half_plane(True,-PLATE_T))^cap_prism_F(s)
    # ribs on top of the plate, from the hinge to the window's rear edge, stopping RIB_CLEAR under the skin
    ribs=Manifold.batch_boolean([box(s*rx-RIB_W/2,s*rx+RIB_W/2,y_h1,WIN_Y[0]+0.5,-30,-SKIN-RIB_CLEAR) for rx in RIB_X],mf.OpType.Add)-half_plane(True,-0.5)
    B=fromR(plate+clamp+ribs-(hinge_cut-straps)-slot)+cap
    # --- F-frame details
    for x,y in ((s*cx,CLAMP_Y) for cx in CLAMP_X):              # clamp screws: 3.3 clearance, countersink from below
        zt=plate_top_F(x,y); zb=zt-CLAMP_T/math.cos(math.radians(TH+math.degrees(math.atan(SLOPE))))
        B=B-cyl(x,y,zb-5,zt+1,1.65)-cyl(x,y,zb-5,zb+0.3,3.15)-cyl(x,y,zb+0.299,zb+1.8,3.15,1.65)
    for bx,by in SCREW_TOP:                                      # keep clear of the case-screw bosses at the front corners
        B=B-cyl(bx,by,-5,40,2.55+0.6)
    # pockets for the scroll-wheel encoder and the middle-click switch: their swept volume over the press, plus clearance
    for k in WHEEL:
        P=prox[k]; c=WHEEL_CLEAR; d=c/np.sqrt(2)
        grown=Manifold.batch_boolean([P.translate([dx,dy,dz]) for dx,dy,dz in
              ((c,0,0),(-c,0,0),(0,c,0),(0,-c,0),(0,0,c),(d,d,0),(d,-d,0),(-d,d,0),(-d,-d,0))]+[P],mf.OpType.Add).hull()
        swept=Manifold.batch_boolean([press(grown,-a) for a in np.linspace(0,PRESS_DEG,6)],mf.OpType.Add)
        B=B-swept
    # nub over the switch
    sw=SW_R if s>0 else SW_L; zb=plate_bottom_F(*sw)
    B=B+cyl(sw[0],sw[1],SW_TOP+NUB_GAP,zb+0.5,NUB_R)
    # stop screw: plate tab out to TAB_Y, boss below, M3 pilot through boss and plate
    x=s*STOP_X; zt=plate_top_F(x,STOP_Y); zb=plate_bottom_F(x,STOP_Y)
    tab=fromR((half_plane(True)-half_plane(True,-PLATE_T))^box(x-3.5,x+3.5,yl-1,TAB_Y/CT+1,-40,10))^box(x-3.5,x+3.5,30,TAB_Y,-10,40)
    B=B+tab+cyl(x,STOP_Y,zb-STOP_BOSS_L,zb+0.5,STOP_BOSS_R)
    B=B-cyl(x,STOP_Y,zb-STOP_BOSS_L-1,zt+1,1.35)
    return max(B.decompose(),key=lambda d:d.volume())
def plate_top_F(x,y):
    """z of the plate's top face above plan point (x,y) in F (solve along the vertical)"""
    lo,hi=0.0,40.0
    for _ in range(60):
        z=(lo+hi)/2; yr,zr=R_of(y,z)
        if zr>plate_top_R(yr): hi=z
        else: lo=z
    return z
def plate_bottom_F(x,y):
    lo,hi=0.0,40.0
    for _ in range(60):
        z=(lo+hi)/2; yr,zr=R_of(y,z)
        if zr>plate_top_R(yr)-PLATE_T: hi=z
        else: lo=z
    return z
SCREW_TOP=[(-20.5,42.155),(20.8,42.155),(-22.3,-43.145),(22.7,-43.145)]   # the upper shell's case-screw bosses
def upper_shell():
    U=to_man(tm_adb('upper'))
    for x,y in SCREW_TOP: U=U-cyl(x,y,5.0,17.0,1.35)                       # M3 pilot (was 2.5)
    # old cable ribs hanging below the front of the roof (anything below the ceiling between the window and the front wall)
    n=np.array([0,-ROOF_A,1.0]); Ln=np.linalg.norm(n)
    U=U-box(-12,12,38.5,46.45,0,40).trim_by_plane(list(-n),-(ROOF_C-SKIN-0.01)/Ln)
    # the original button's mount (pins and ribs under the roof), anywhere over the new plates
    U=U-fromR(box(-23.5,23.5,-14.0/CT,38.0/CT,-30,-SKIN-0.01))
    above=fromR(half_plane(False))                                          # everything above the plates' top plane
    for s in (1,-1):
        for cx in CLAMP_X:
            x=s*cx; y=CLAMP_Y; zb=plate_top_F(x,y)
            U=U+(cyl(x,y,zb-1,ceil(y)+0.6,BOSS_R)^above)                   # boss ends on the plate's (tilted) top face
            U=U-cyl(x,y,zb-1,roof(y)-0.8,1.35)
    return U
def build_top(verbose=True):
    U=upper_shell()
    R=button(1,U); L=button(-1,U)
    if verbose:
        print(f'plate top: R slope {SLOPE:+.4f} (plate {math.degrees(math.atan(SLOPE)):+.2f} deg to the roof)')
        hy,hz=hinge_axis_F()
        zt=plate_top_F(STOP_X,STOP_Y); zb=plate_bottom_F(STOP_X,STOP_Y)
        tip=zb-STOP_BOSS_L+8.0-zt; ratio=(SW_L[1]-hy)/(STOP_Y-hy)
        print(f'  stop screw: plate top {zt:.2f} under a ceiling at {ceil(STOP_Y):.2f}; an M3x8 seated stands {tip:.2f} above the plate,'
              f' i.e. up to {tip-GAP_LIP:.2f} mm push at the front = {(tip-GAP_LIP)*ratio:.2f} mm at the nub (nub gap {NUB_GAP})')
        print(f'  nubs: plate underside at the switches {plate_bottom_F(*SW_L):.2f}, nub {plate_bottom_F(*SW_L)-SW_TOP-NUB_GAP:.2f} tall')
        print('  hinge axis (F y,z):',np.round(hinge_axis_F(),2))
    return U,L,R
if __name__=='__main__':
    U,L,R=build_top()
    for n,M in (('upper_shell',U),('button_left',L),('button_right',R)): clean_export(M,os.path.join(BUILD,n+'.stl'))
