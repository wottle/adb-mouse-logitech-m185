"""Shared geometry helpers and frames.

Final frame F: X right (the user's right), Y forward (toward the buttons), Z up, flat underside at z = 0.
The ADB model (Thingiverse 4545460) is Y-up with the front at its +Z end; T_ADB maps it into F.
The M185 mounting comes from the Lisa mouse base (Lisa base frame); BOARD_X / BOARD_Y place it in F.
"""
import numpy as np, trimesh, manifold3d as mf
from manifold3d import Manifold, CrossSection, Mesh
import shapely.geometry as sg
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=os.path.join(ROOT,'source'); BUILD=os.path.join(ROOT,'build'); os.makedirs(BUILD,exist_ok=True)
ADBF={k:os.path.join(SRC,'adb',f'Apple_G4351_ADB_Mouse_-_{n}.STL') for k,n in
      (('upper','upperrshell'),('lower','lowershell'),('button','button'),('ball','ball_retainer'))}
LISA_BASE=os.path.join(SRC,'lisa','base.stl')            # base.stl (v1) from lisa-mouse-logitech-m185/models
LISA_SOLID=os.path.join(BUILD,'lisa_base_solid.stl')     # cleaned copy, made by lisa_solid.py
# model -> F: x = 96.995 - mx, y = mz - 49.565, z = my - 0.63 (a proper rotation, like the Mac mouse's T_MAC)
T_ADB=np.array([[-1,0,0,96.995],[0,0,1,-49.565],[0,1,0,-0.63],[0,0,0,1.0]])
FRONT_Y=49.255                  # outside of the front wall
REAR_Y=-49.255

# --- where the M185 goes ---------------------------------------------------------------------------
# Lisa base frame -> F. BOARD_X centres the two switches on the window (they sit 36.6 mm apart, the window
# is about 37 wide). BOARD_Y = how far the board's front edge sits behind the outside of the front wall:
# further back = more height for the switches and the scroll-wheel parts (the roof rises 0.176 mm per mm),
# but the battery bay moves toward the sloping rear.
BOARD_X=2.6-1.0+0.165           # Mac mouse DX + 2.6, + 0.165 to centre the switches on the window (the model is off-centre by that)
BOARD_Y=13.5
PCB_FRONT_B=49.3                # board front edge, Lisa base frame
DX,DY,DZ=BOARD_X,(FRONT_Y-BOARD_Y)-PCB_FRONT_B,-1.4
def B2F(x,y): return x+DX,y+DY            # Lisa base frame -> F (plan)

# roof: the front part of the top is a plane (fit residual 0.000 mm over y 8..60 from the front)
ROOF_A,ROOF_C=-0.1760,26.711    # outer roof z = ROOF_A*y + ROOF_C
SKIN=2.79                       # roof thickness
def roof(y): return ROOF_A*y+ROOF_C
def ceil(y): return roof(y)-SKIN

def tm_adb(name):
    m=trimesh.load(ADBF[name],force='mesh'); m.apply_transform(T_ADB); m.merge_vertices(digits_vertex=5); return m
def to_man(m):
    M=Manifold(Mesh(vert_properties=np.asarray(m.vertices,dtype=np.float32),tri_verts=np.asarray(m.faces,dtype=np.uint32)))
    assert M.status()==mf.Error.NoError, M.status(); return M
def to_tm(M):
    me=M.to_mesh(); return trimesh.Trimesh(np.asarray(me.vert_properties)[:,:3],np.asarray(me.tri_verts),process=False)
def box(x0,x1,y0,y1,z0,z1): return Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def cyl(x,y,z0,z1,r,r2=None,n=64): return Manifold.cylinder(z1-z0,r,r if r2 is None else r2,n).translate([x,y,z0])
def xs_from_shapely(g):
    polys=[g] if g.geom_type=='Polygon' else list(g.geoms)
    cs=[]
    for p in polys:
        if p.is_empty or p.area<1e-4: continue
        rings=[np.asarray(p.exterior.coords)[:-1]]+[np.asarray(i.coords)[:-1] for i in p.interiors]
        cs.append(CrossSection(rings, mf.FillRule.EvenOdd))
    return CrossSection.batch_boolean(cs,mf.OpType.Add) if len(cs)>1 else (cs[0] if cs else CrossSection())
def prism(g,z0,z1):
    c=g if isinstance(g,CrossSection) else xs_from_shapely(g)
    return c.extrude(z1-z0).translate([0,0,z0])
def rrect(x0,x1,y0,y1,r): return sg.box(x0+r,y0+r,x1-r,y1-r).buffer(r,resolution=24) if r>0 else sg.box(x0,y0,x1,y1)
def section_xs(tm,z,min_area=1e-3):
    s=tm.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
    if s is None: return CrossSection()
    rings=[]
    for e in s.discrete:
        p=np.asarray(e)[:,:2]
        if len(p)<4 or np.linalg.norm(p[0]-p[-1])>1e-4: continue
        p=p[:-1]
        a=0.5*abs(np.dot(p[:,0],np.roll(p[:,1],-1))-np.dot(p[:,1],np.roll(p[:,0],-1)))
        if a>min_area: rings.append(p)
    return CrossSection(rings, mf.FillRule.EvenOdd) if rings else CrossSection()
def xs_to_shapely(c):
    polys=c.to_polygons(); g=sg.Polygon()
    for p in sorted([sg.Polygon(p) for p in polys],key=lambda q:-q.area): g=g.symmetric_difference(p.buffer(0))
    return g
def save(M,path):
    t=to_tm(M); t.export(path); return t
def clean_export(M,path,tol=0.0005):
    """export so the STL reloads as one watertight body (welds and drops zero-area flakes boolean cuts can leave)"""
    rt=lambda N: trimesh.load(trimesh.util.wrap_as_stream(to_tm(N).export(file_type='stl')),file_type='stl')
    t=rt(M)
    if not t.is_watertight: t=rt(M.simplify(tol))
    if not t.is_watertight:
        t.merge_vertices(digits_vertex=5); t.update_faces(t.nondegenerate_faces(height=1e-6)); t.update_faces(t.unique_faces())
        t.remove_unreferenced_vertices(); t=max(t.split(only_watertight=False),key=lambda c:len(c.faces))
    assert t.is_watertight, path
    t.export(path); return t
