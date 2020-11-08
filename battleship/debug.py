import numpy as np
from generate import *
from ship import *

ships={}
ships["sloop"]=ship(1,2,np.ones((1,2)))
ships["men-of-war"]=ship(1,4,np.ones((1,4)))

board=board(8,8,ships)
