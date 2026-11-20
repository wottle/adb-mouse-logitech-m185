"""Upper shell and the two buttons.

Each button is one piece: a cap in its half of the window, flush with the roof, on a plate that runs under the roof skin
and is screwed up into two bosses under the hump. The plate bends at a thin hinge in front of its clamp (a flexure, like
the original ADB button), so there are no pins to sag or bind. A printed nub under each plate presses its M185 switch;
an M3 stop screw under the front of the plate sets the resting position, and with it the click point.

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
CAP_CLEAR=0.6                        # cap to window, each side (0.35 rubbed on the second print, upper printed on its side)
CAP_PROUD=0.3                        # cap top above the roof at the window's rear edge
CAP_FRONT_RAISE=0.5                  # extra cap height at the window's front edge, tapering to 0 at its rear. The first print
                                     # rested about 1 mm low at the front (rear flush); 1.0 left the fronts standing proud.
# --- plate (roof frame z is negative inside)
PLATE_T=2.0
GAP_LIP=0.1                          # plate top below the roof skin at the front lip (the up-stop)
LIP=1.5                              # plate reaches this far in front of the window
PLATE_X={-1:-22.65,1:23.0}           # outer edges: about 1 mm in from the side walls at the front (0.55 scraped)
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
NUB_R=3.0; NUB_GAP=0.25              # nub over the plunger; its gap to the plunger top with the button at rest, screw backed off
NUB_GAP_SHORT=0.0                    # the 'short click' buttons: nub 0.25 taller, touching the modelled plunger at rest. Mike
                                     # found the standard click late with the fronts flush; the real plungers sit lower than modelled.
STOP_X=9.0; STOP_Y=44.0              # stop screw (F); 2.2 mm in front of the window, 2.5 behind the front wall
STOP_BOSS_R=2.0; STOP_BOSS_L=4.5     # boss under the plate; an M3x8 seated against it stands 1.5 above the plate top
TAB_Y=45.0                           # plate front edge round the stop screw: clear of the roof rounding into the front wall
                                     # (46.2 touched it); the screw boss below the plate still reaches y 46.0
CASE_BOSS_CLEAR=1.0                  # buttons to the front case-screw bosses (0.6 left 0.3 near the roof, where the boss flares)
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

def button(side,U,nub_gap=NUB_GAP):
    s=side; xin=s*GAP/2; xout=PLATE_X[s]; x0,x1=sorted((xin,xout))
    # plate slab: from the clamp's rear end to the lip
    slab=half_plane(True)-half_plane(True,-PLATE_T)
    plate=slab^box(x0,x1,yc-CLAMP_L/2,yl,-40,10)
    clamp=(half_plane(True)-half_plane(True,-CLAMP_T))^box(x0,x1,yc-CLAMP_L/2,y_h0,-40,10)
    # hinge: thin strip, two straps (inner and outer edge of the plate)
    hinge_cut=(half_plane(True,-HINGE_T)^box(x0-1,x1+1,y_h0,y_h1,-40,10))
    straps=box(*sorted((xin,xin+s*STRAP_W)),y_h0-0.01,y_h1+0.01,-40,10)+box(*sorted((xout,xout-s*STRAP_W)),y_h0-0.01,y_h1+0.01,-40,10)
    slot=box(x0,x1,y_h0,y_h1,-40,10)-straps
    # cap: the window less clearance, this side of the slot, from inside the plate up to its top: CAP_PROUD over the roof
    # at the window's rear edge, rising CAP_FRONT_RAISE more by its front edge (R)
    k=CAP_FRONT_RAISE/(WIN_Y[1]-WIN_Y[0]); n=np.array([0,k,-1.0]); Ln=np.linalg.norm(n)
    top=box(-40,40,-40,80,-40,CAP_PROUD+CAP_FRONT_RAISE+5).trim_by_plane(list(n),(k*WIN_Y[0]-CAP_PROUD)/Ln)
    cap=fromR(top-half_plane(True,-PLATE_T))^cap_prism_F(s)
    # ribs on top of the plate, from the hinge to the window's rear edge, stopping RIB_CLEAR under the skin
    ribs=Manifold.batch_boolean([box(s*rx-RIB_W/2,s*rx+RIB_W/2,y_h1,WIN_Y[0]+0.5,-30,-SKIN-RIB_CLEAR) for rx in RIB_X],mf.OpType.Add)-half_plane(True,-0.5)
    B=fromR(plate+clamp+ribs-(hinge_cut-straps)-slot)+cap
    # --- F-frame details
    for x,y in ((s*cx,CLAMP_Y) for cx in CLAMP_X):              # clamp screws: 3.3 clearance, countersink from below
        zt=plate_top_F(x,y); zb=zt-CLAMP_T/math.cos(math.radians(TH+math.degrees(math.atan(SLOPE))))
        B=B-cyl(x,y,zb-5,zt+1,1.65)-cyl(x,y,zb-5,zb+0.3,3.15)-cyl(x,y,zb+0.299,zb+1.8,3.15,1.65)
    for bx,by in SCREW_TOP:                                      # keep clear of the case-screw bosses at the front corners
        B=B-cyl(bx,by,-5,40,2.55+CASE_BOSS_CLEAR)
    # pockets for any scroll-wheel parts left on the board (WHEEL, now none): their swept volume over the press, plus clearance
    for k in WHEEL:
        P=prox[k]; c=WHEEL_CLEAR; d=c/np.sqrt(2)
        grown=Manifold.batch_boolean([P.translate([dx,dy,dz]) for dx,dy,dz in
              ((c,0,0),(-c,0,0),(0,c,0),(0,-c,0),(0,0,c),(d,d,0),(d,-d,0),(-d,d,0),(-d,-d,0))]+[P],mf.OpType.Add).hull()
        swept=Manifold.batch_boolean([press(grown,-a) for a in np.linspace(0,PRESS_DEG,6)],mf.OpType.Add)
        B=B-swept
    # nub over the switch
    sw=SW_R if s>0 else SW_L; zb=plate_bottom_F(*sw)
    B=B+cyl(sw[0],sw[1],SW_TOP+nub_gap,zb+0.5,NUB_R)
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
EDGE_BEVEL=2.0                       # 45 degree bevel (legs, mm) in place of the rounding along the roof's side edges, so the upper
                                     # prints on its side without supports there. The flat side below it (what rests on the bed)
                                     # is then about 2.3 mm tall (1.85 with the rounding). Must not exceed the side's wall thickness.
def roof_edge_z(t,x=22.5,ys=np.arange(-45,45.01,0.5)):
    """top of the roof just inside the side edges (flat across x there), sampled along y; straight beyond |y| 45,
    where the front and rear top edges round off"""
    G=np.array([(s*x,y,80.0) for s in (-1,1) for y in ys]); loc,ri,_=t.ray.intersects_location(G,np.tile([0,0,-1.0],(len(G),1)),multiple_hits=False)
    z=np.full(len(G),np.nan); z[ri]=loc[:,2]; z=np.nanmax(z.reshape(2,-1),axis=0)
    yy=np.r_[-70,ys,70]; k0=(z[1]-z[0])/(ys[1]-ys[0]); k1=(z[-1]-z[-2])/(ys[-1]-ys[-2])
    return yy,np.r_[z[0]+k0*(-70-ys[0]),z,z[-1]+k1*(70-ys[-1])]
def edge_bevel_cutter(t):
    """everything beyond the plane |x| + z = SIDE_W - EDGE_BEVEL + roof(y), on both sides"""
    yy,zz=roof_edge_z(t); r2=math.sqrt(2)
    K=(SIDE_W-EDGE_BEVEL+zz)/r2                                     # in (p, y), p = (x + z)/sqrt2 for the right side
    poly=([(k,y) for k,y in zip(K,yy)]+[(80,yy[-1]),(80,yy[0])])[::-1]     # counter-clockwise
    C=Manifold.extrude(CrossSection([poly]),120).translate([0,0,-60])  # X = p, Y = y, Z = q = (z - x)/sqrt2
    C=C.transform(np.array([[1/r2,0,-1/r2,0],[0,1,0,0],[1/r2,0,1/r2,0]]))
    return C+C.mirror([1,0,0])
EDGE_X=22.5                          # the side edges are rebuilt outboard of this |x| (roof flat across x from the window to 25)
EDGE_DEPTH=2.6                       # ...down to this far below the roof surface (the rounding starts 2.4 down; skin 2.79)
EDGE_INSET=0.03                      # the fill stays this far under the roof and inside the plan's corners (no coincident faces)
EDGE_STRAIGHT_Y=44.0                 # the plan's sides are straight to |y| 45.2 (corner radius about 4)
def yz_extrude(poly_yz,x0,x1):
    """a (y, z) polygon extruded along x from x0 to x1"""
    p=np.asarray(poly_yz); a=0.5*np.sum(p[:,0]*np.roll(p[:,1],-1)-np.roll(p[:,0],-1)*p[:,1])
    if a<0: p=p[::-1]
    M=Manifold.extrude(CrossSection([[(z,y) for y,z in p][::-1]]),x1-x0)   # X' = z, Y' = y, extruded along Z'
    return M.transform(np.array([[0,0,1.0,x0],[0,1.0,0,0],[1.0,0,0,0]]))
def edge_fill(t,H):
    """material that squares off the side edges: the roof's front-to-back profile (the hull at |x| = EDGE_X) carried out
    past the sides, inside the plan's rounded corners, within EDGE_DEPTH of the roof. The side plane and the bevel are cut
    afterwards."""
    g=xs_to_shapely(H.rotate([0,90,0]).slice(-EDGE_X)); g=max((g.geoms if hasattr(g,'geoms') else [g]),key=lambda q:q.area)
    g=sg.Polygon([(y,z) for z,y in np.asarray(g.exterior.coords)]).buffer(-EDGE_INSET,join_style=1)   # slice coords are (z, y)
    prof=list(np.asarray(g.exterior.coords)[:-1])
    E=yz_extrude(prof,-SIDE_W-1,SIDE_W+1)
    plan=xs_to_shapely(H.project()).buffer(-EDGE_INSET,join_style=1).union(sg.box(-SIDE_W-1,-EDGE_STRAIGHT_Y,SIDE_W+1,EDGE_STRAIGHT_Y))
    E=E^prism(plan.simplify(0.005),-5,55)                                    # simplified: no near-duplicate vertices
    yy,zz=roof_edge_z(t); zone=yz_extrude([(y,z-EDGE_DEPTH) for y,z in zip(yy,zz)]+[(yy[-1],80),(yy[0],80)],EDGE_X,40)
    return E^(zone+zone.mirror([1,0,0]))
def upper_shell():
    t=tm_adb('upper'); U=to_man(t); H=to_man(t.convex_hull)
    U=((U+edge_fill(t,H))-edge_bevel_cutter(t))^box(-SIDE_W,SIDE_W,-60,60,-5,60)   # flat sides up to a 45 deg bevel: no supports
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
