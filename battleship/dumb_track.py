import numpy as np
import random
import copy

from ship import *

class dumb_track:
    
    def change_slide(self,arr,x,y,ship,p):
        (X,Y)=arr.shape
        temp_arr=copy.deepcopy(arr)
        
        for i in range(ship.x):
            for j in range(ship.y):
                if (ship.shape[i][j]==1):
                    if (x-i>=0 and x+ship.x-i<X and y-j>=0 and y+ship.y-j<Y):
                        for a in range(x-i,x+ship.x-i):
                            for b in range(y-j,y+ship.y-j):
                                temp_arr[a][b]+=p
                    if (x-j>=0 and x+ship.y-j<X and y-ship.x+i+1>=0 and y+i+1<Y):
                        for a in range(x-j,x+ship.y-j):
                            for b in range(y-ship.x+i+1,y+i+1):
                                temp_arr[a][b]+=p
                    if (x-ship.y+j+1>=0 and x+j+1<X and y-i>=0 and y+ship.x-i<Y):
                        for a in range(x-ship.y+j+1,x+j+1):
                            for b in range(y-i,y+ship.x-i):
                                temp_arr[a][b]+=p
                    if (x-ship.x+i+1>=0 and x+i+1<X and y-ship.y+j+1>=0 and y+j+1<Y):
                        for a in range(x-ship.x+i+1,x+i+1):
                            for b in range(y-ship.y+j+1,y+j+1):
                                temp_arr[a][b]+=p
        return temp_arr
    
    def __init__(self,x,y,ships):
        self.x=x
        self.y=y
        self.ship=ships

        self.last_x=-1
        self.last_y=-1
        self.track_list=[]

        self.prob_list=[]
        self.name_list=[]
        self.cnt_list=[]
        for i in self.ship:
            self.prob_list.append(np.zeros((self.x,self.y)))
            
            self.name_list.append(i)

            temp_cnt=0
            for a in range(self.ship[i].x):
                for b in range(self.ship[i].y):
                    if (self.ship[i].shape[a][b]==1):
                        temp_cnt+=1
            self.cnt_list.append(temp_cnt)
        self.prob_tot=np.zeros((self.x,self.y))

        
        self.target_list=[i for i in range(x*y)]
        random.shuffle(self.target_list)
        self.pt=0
        self.ship_sunk=0
        self.hit_list=np.ones((self.x,self.y))
        
    def coord(self):
        if (self.prob_tot.max()==0):
            cur_x=self.target_list[self.pt]//self.y
            cur_y=self.target_list[self.pt]%self.y
            while (self.hit_list[cur_x][cur_y]==0):
                self.pt+=1
                cur_x=self.target_list[self.pt]//self.y
                cur_y=self.target_list[self.pt]%self.y

            (self.last_x,self.last_y)=(cur_x,cur_y)
            self.hit_list[self.last_x][self.last_y]=0
            return (cur_x,cur_y)

        else:
            coord=np.unravel_index(self.prob_tot.argmax(),self.prob_tot.shape)
            print(coord)
            (self.last_x,self.last_y)=coord
            self.hit_list[self.last_x][self.last_y]=0
            return coord
            

    def read_outcome(self,val):
        for i in range(self.x): print(self.prob_tot[i])
        if (val[0]==0):
            self.prob_tot[self.last_x][self.last_y]=-np.inf
        if (val[0]==1):
            self.prob_tot[self.last_x][self.last_y]=-np.inf
            for i in range(len(self.cnt_list)):
                if (self.cnt_list[i]!=0):
                    self.prob_list[i]=self.change_slide(self.prob_list[i],
                                                       self.last_x,
                                                       self.last_y,
                                                       self.ship[self.name_list[i]],
                                                       1)
                    self.prob_tot=self.change_slide(self.prob_tot,
                                                       self.last_x,
                                                       self.last_y,
                                                       self.ship[self.name_list[i]],
                                                       1)
        if (val[0]==2):
            self.prob_tot[self.last_x][self.last_y]=-np.inf
            for i in range(len(self.cnt_list)):
                if (self.cnt_list[i]!=0):
                    self.prob_list[i]=self.change_slide(self.prob_list[i],
                                                       self.last_x,
                                                       self.last_y,
                                                       self.ship[self.name_list[i]],
                                                       1)
                    self.prob_tot=self.change_slide(self.prob_tot,
                                                       self.last_x,
                                                       self.last_y,
                                                       self.ship[self.name_list[i]],
                                                       1)
            self.prob_tot-=self.prob_list[val[1]]
            self.cnt_list[val[1]]=0
            for coord in val[2]:
                for i in range(len(self.cnt_list)):
                    if (self.cnt_list[i]!=0):
                        self.prob_list[i]=self.change_slide(self.prob_list[i],
                                                           coord[0],
                                                           coord[1],
                                                           self.ship[self.name_list[i]],
                                                           -1)
##                        self.prob_tot=self.change_slide(self.prob_tot,
##                                                           coord[0],
##                                                           coord[1],
##                                                           self.ship[self.name_list[i]],
##                                                           -1)
            self.ship_sunk+=1
         

    def exit(self):
        if (self.ship_sunk==len(self.ship)):
            return True
        else: return False

    def debug(self):
        print(self.coord())
        return

##ships={}
##ships["sloop"]=ship(1,2,np.ones((1,2)))
##ships["men-of-war"]=ship(1,4,np.ones((1,4)))
##temp=np.zeros((2,2))
##temp[0][0]=1
##temp[0][1]=1
##temp[1][0]=1
##ships["weird"]=ship(2,2,temp)
##
##brain=dumb_track(4,8,ships)
##brain.debug()
