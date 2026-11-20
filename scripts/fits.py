"""Stand-ins for the M185 electronics, defined in the Lisa base frame (as in the Mac mouse project) and placed in F.

Switch plunger positions are Mike's caliper measurements. The board outline, the switch bodies, the AA cell and
especially the scroll-wheel encoder and the middle-click switch are estimates: boxes that are meant to be a
little larger than the real parts.
"""
import math
from geo import *
SW_L_B=(-19.92,34.5); SW_R_B=(16.73,34.5)     # left/right switch plungers, Lisa base frame (9 / 12 mm in from the base edges)
SW_TOP_B=17.5                                 # plunger free top, Lisa base frame
SW_L=B2F(*SW_L_B); SW_R=B2F(*SW_R_B); SW_TOP=SW_TOP_B+DZ
def bbox(x0,x1,y0,y1,z0,z1): return box(x0+DX,x1+DX,y0+DY,y1+DY,z0+DZ,z1+DZ)
def switch(x,y): return bbox(x-2.9,x+2.9,y-9,y+3.8,9.6,16.7)+bbox(x-1.45,x+1.45,y-.75,y+.75,16.7,SW_TOP_B)
prox={'pcb':bbox(-23.3,15.3,-21,48.3,8.05,9.65),
      'swL':switch(*SW_L_B),'swR':switch(*SW_R_B),
      'encoder':bbox(SW_R_B[0]-10.5,SW_R_B[0]-3.1,SW_R_B[1]-6,SW_R_B[1]+8,9.6,20.4),
      'tact':bbox(SW_L_B[0]+3.2,SW_L_B[0]+10,SW_L_B[1]-7,SW_L_B[1]+2,9.6,20.4)}
a0=np.array([-5.6,-24.0]); a1=np.array([16.2,21.5])          # AA bay axis ends, Lisa base frame
d=a1-a0; L_=np.linalg.norm(d); ang=math.degrees(math.atan2(d[1],d[0]))
c=a0+d/L_*((L_-50.5)/2)
prox['AA']=Manifold.cylinder(50.5,7.25,7.25,48).rotate([0,90,0]).rotate([0,0,ang]).translate([c[0]+DX,c[1]+DY,3.4+7.25+DZ])
WHEEL=('encoder','tact')                      # the parts a builder may choose to desolder
