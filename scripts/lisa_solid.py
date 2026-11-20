"""Rebuild the Lisa mouse base (a messy export) as a clean solid, layer by layer, so it can be used in boolean operations.

Heights are snapped to a 0.05 mm grid and consecutive layers with the same outline are merged; the source has layers
0.01 mm apart whose outlines differ by slivers, which otherwise survive into the final STLs as broken faces.
"""
from geo import *
STEP=0.05; SIMPLIFY=0.01; SAME=0.05      # mm, mm, mm2
def make_lisa_solid(verbose=True):
    b=trimesh.load(LISA_BASE,force='mesh')
    zs=np.unique(np.round(b.vertices[:,2]/STEP)*STEP)
    layers=[]                                   # [z0, z1, polygon]
    for z0,z1 in zip(zs[:-1],zs[1:]):
        g=xs_to_shapely(section_xs(b,(z0+z1)/2)).simplify(SIMPLIFY).buffer(0)
        if g.is_empty: continue
        if layers and abs(layers[-1][1]-z0)<1e-6 and layers[-1][2].symmetric_difference(g).area<SAME:
            layers[-1][1]=z1; continue
        layers.append([z0,z1,g])
    L=Manifold.batch_boolean([prism(g,z0,z1) for z0,z1,g in layers],mf.OpType.Add)
    if verbose: print(f'lisa base solid: {len(layers)} layers, volume {L.volume():.1f} mm3 (source mesh {b.volume:.1f})')
    save(L,LISA_SOLID); return L
if __name__=='__main__': make_lisa_solid()
