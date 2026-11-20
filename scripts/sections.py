import sys; sys.path.insert(0,'.')
from build_top import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP
M=os.path.join(ROOT,'models')+os.sep
parts={n:to_man(trimesh.load(M+n+'.stl',force='mesh')) for n in ('upper_shell','lower_shell','button_left','button_right')}
col={'upper_shell':'#c9c9d0','lower_shell':'#a3abbd','button_left':'#e8b860','button_right':'#6f9be0','pcb':'#3c9650','swL':'#d84a3c','swR':'#d84a3c','encoder':'#e6aa28','tact':'#e6aa28','AA':'#4670dc'}
def yz(Mn,x): return xs_to_shapely(Mn.rotate([0,90,0]).slice(-x))
def draw(ax,x,title,xlim=(-50,50),ylim=(0,31),pressed=0.0):
    hy,hz=hinge_axis_F(); fwd=box(-60,60,hy,80,-60,80)
    for n,Mn in list(parts.items())+list(prox.items()):
        if pressed and n.startswith('button'): Mn=press(Mn^fwd,pressed)+(Mn-fwd)
        g=yz(Mn,x)
        for p in (g.geoms if hasattr(g,'geoms') else [g]):
            if p.is_empty: continue
            xy=np.asarray(p.exterior.coords)[:,::-1]
            ax.add_patch(MP(xy,closed=True,fc=col[n],ec='k',lw=0.4,alpha=0.9 if n in parts else 0.55))
            for h in p.interiors: ax.add_patch(MP(np.asarray(h.coords)[:,::-1],closed=True,fc='white',ec='k',lw=0.4))
    ax.set_title(title,fontsize=10); ax.set_aspect('equal'); ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.grid(alpha=0.25)
    ax.set_xlabel('y (mm, front to the right)'); ax.set_ylabel('z (mm)')
if __name__=='__main__':
    fig,axes=plt.subplots(4,1,figsize=(13,15))
    draw(axes[0],SW_L[0],f'left switch plunger (x = {SW_L[0]:.1f}): red switch, green board, blue cell; yellow = left button')
    draw(axes[1],11.5,'scroll-wheel encoder (x = 11.5, yellow box) under the right button (blue)')
    draw(axes[2],9.0,'right stop screw (x = 9.0): boss under the plate front, tip bears on the roof just ahead of the window',xlim=(25,50),ylim=(5,25))
    draw(axes[3],SW_L[0],'left switch, close up: nub 0.25 above the plunger at rest',xlim=(10,32),ylim=(12,24))
    plt.tight_layout(); plt.savefig(sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,'images','sections.png'),dpi=105)
