import numpy as np
from generatev2 import *
from dumb import *
from dumb_trackv2 import *
from smartv2 import *
from ship import *

ships={}
ships["sloop"]=ship(1,2,np.ones((1,2)))
ships["men-of-war"]=ship(1,4,np.ones((1,4)))
ships["cutter"]=ship(1,3,np.ones((1,3)))
ships["alien"]=ship(1,5,np.ones((1,5)))

####ships={}
##ships["sloop"]=ship(1,2,np.ones((1,2)))
##ships["men-of-war"]=ship(1,4,np.ones((1,4)))


board=board(10,10,ships)
brain=smart(10,10,ships)
print(brain.target_list)

cnt=0
while (not brain.exit()):
    c=brain.coord()
    val=board.fire(c)
    brain.read_outcome(val)
    board.visualise()
    if (val[0]==-1): break
    input("Press Enter to continue...")
    cnt+=1
print(cnt)
print(brain.target_list)
