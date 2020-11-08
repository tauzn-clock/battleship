import numpy as np
import random

class dumb:
    def __init__(self,x,y,ships):
        self.x=x
        self.y=y
        self.ship=ships
        self.target_list=[i for i in range(x*y)]
        random.shuffle(self.target_list)
        self.pt=0
        self.ship_sunk=0
        
    def coord(dumb):
        val=dumb.target_list[dumb.pt]
        dumb.pt+=1
        return (val//dumb.y,val%dumb.y)

    def read_outcome(dumb,val):
        if (val[0]==2):dumb.ship_sunk+=1

    def exit(dumb):
        if (dumb.ship_sunk==len(dumb.ship)):
            return True
        else: return False
