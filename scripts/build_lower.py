"""Lower shell: the ADB mouse's outside, a flat bottom, and the M185 mounting from the Lisa mouse base inside."""
from fits import *
SEAM=5.9                         # where the upper shell's corner bosses (and front wall) start
ZT=5.5                           # height of the outline used for the flat bottom
BEVEL=1.0                        # 45 degree bevel round the bottom edge (3 mm on the Mac mouse; the battery door
                                 # opening reaches 26.2 mm out on the right, so only 1 mm fits here)
FLOOR=2.15                       # top of the Lisa base floor (F)
FLOOR_CUT=1.83                   # our floor is cut here and the Lisa floor fills up from it (overlapping joins; the
                                 # Lisa layers sit on a 0.05 mm grid, so this is kept off it)
# case screws: from underneath into the upper shell's four corner bosses (centres measured on the upper shell)
SCREW=[(-20.5,42.155),(20.8,42.155),(-22.3,-43.145),(22.7,-43.145)]
POST_R=3.6
LISA_TOP=17.6                    # Lisa features are cut to this height (the battery bay walls stood 18.15, 0.12 under
                                 # the right button's plate; the cell's top is 16.5)
CABLE_TOP=12.4                   # top of the lower shell's front wall at the cable slot
# PCB front hold-down in the scroll-wheel cutout (same place on the board as on the Lisa v2 and Macintosh mice)
ST_B=(-3.0,45.18); PCB_SEAT=8.05+DZ
def outline(m,z):
    g=xs_to_shapely(section_xs(m,z)); polys=list(g.geoms) if g.geom_type!='Polygon' else [g]
    return max(polys,key=lambda p:p.area)
def build_lower(verbose=True):
    t=tm_adb('lower'); lo=to_man(t)
    ring=outline(t,5.6)
    O=sg.Polygon(ring.exterior).convex_hull                        # outside, near the bottom
    interior=max([sg.Polygon(r) for r in ring.interiors],key=lambda q:q.area).buffer(0.3)    # 0.3 into the walls (2.5 -> 2.2 mm): a cutter that only grazes
                                                                    # the drafted inner faces leaves zero-width slivers in the mesh
    # --- flat bottom with a small 45 degree bevel; fill everything up to ZT first
    Oi=O.buffer(-0.05)                                             # fills stay just inside the original skin (no coincident faces)
    bev=(prism(O.buffer(-BEVEL),0,0.01)+prism(O,BEVEL,BEVEL+0.01)).hull()
    lo=lo+(bev^prism(Oi.buffer(BEVEL),-1,ZT))+prism(Oi,BEVEL,ZT)
    lo=lo-(box(-60,60,-60,60,-5,BEVEL)-bev)
    # --- strip the ball-mouse internals, keep the walls
    lo=lo-prism(interior,FLOOR_CUT,45)
    # front wall: close the cable slot (5 mm wide, z 6..12, centre of the front wall) to the wall's outside contour
    lo=lo+(prism(Oi,ZT-0.2,SEAM-0.05)-prism(interior,-1,50))
    front=(to_man(t)^box(-12,12,40,50,4.0,CABLE_TOP)).hull()
    lo=lo+((front^box(-4,4,40,50,4.0,CABLE_TOP))-prism(interior,-1,50))
    # --- M185 mounting from the Lisa base
    L=to_man(trimesh.load(LISA_SOLID,force='mesh')).translate([DX,DY,DZ])
    lisa_fp=outline(to_tm(L),0.3)
    R_int=sg.Polygon(lisa_fp.exterior).buffer(-1.0).intersection(O.buffer(-BEVEL-0.3))     # where the Lisa floor replaces ours
    R_all=sg.box(*B2F(-27.35,-32.7),*B2F(27.2,48.4)).intersection(interior.buffer(-0.15))   # Lisa features kept above the floor
    Lmod=L^(prism(R_all,FLOOR_CUT,45)+prism(R_int,-5,FLOOR_CUT))
    lo=lo-prism(R_int,-5,FLOOR_CUT)
    lo=lo+Lmod
    lo=lo-prism(interior.buffer(-0.31),LISA_TOP,45)                  # battery bay walls: keep them clear of the button plates
    for x,y in ((-23.89,-29.8),(23.89,-29.8)):                    # the Lisa base's own case-screw holes
        lo=lo+(cyl(*B2F(x,y),0,FLOOR,3.4)^prism(R_int,-5,FLOOR_CUT+0.2))
    # --- corner posts for the case screws, tied to the walls
    H=prism(Oi,0,SEAM)^(bev+prism(O,BEVEL,SEAM))
    for x,y in SCREW:
        s=np.sign(x); f=np.sign(y)
        web=box(min(x,s*30),max(x,s*30),y-2.5,y+2.5,0,SEAM)+box(x-2.5,x+2.5,min(y,f*52),max(y,f*52),0,SEAM)
        lo=lo+((cyl(x,y,0,SEAM,POST_R)+web)^H)
    # --- PCB front hold-down post
    sx,sy=B2F(*ST_B)
    lo=lo+box(sx-3.5,sx+3.5,sy-3.0,sy+2.5,FLOOR-0.5,PCB_SEAT)-cyl(sx,sy,0.8,PCB_SEAT+1,1.35)
    # --- screw holes: 3.3 clearance, recess for a countersunk head flush with the bottom (90 degree cone)
    for x,y in SCREW:
        lo=lo-cyl(x,y,-1,SEAM+1,1.65)-cyl(x,y,-1,0.3,3.15)-cyl(x,y,0.299,1.8,3.15,1.65)
    # print tolerance against the upper shell where they meet
    up=to_man(tm_adb('upper'))
    for dx,dy in ((0.15,0),(-0.15,0),(0,0.15),(0,-0.15)): lo=lo-up.translate([dx,dy,0])
    lo=max(lo.decompose(),key=lambda d:d.volume())
    if verbose: print(f'lower shell: volume {lo.volume():.0f} mm3, bounds {np.round(lo.bounding_box(),2)}')
    return lo,dict(O=O,interior=interior,R_int=R_int,R_all=R_all,Lmod=Lmod)
if __name__=='__main__':
    lo,info=build_lower()
    clean_export(lo,os.path.join(BUILD,'lower_shell.stl'))
