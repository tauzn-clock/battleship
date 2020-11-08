import numpy as np
import random
import copy

from ship import *
    

class smart:
    def check(self,arr1,arr2,a,b,c,d):
        (X,Y)=arr1.shape
        if (a<0): return False
        if (b>=X):return False
        if (c<0): return False
        if (d>=Y):return False
        for i in range(a,b+1):
            for j in range(c,d+1):
                #Ideally should -inf, we need to check
                if (arr1[i][j]<0 and arr2[i-a][j-c]==1):
                    return False
        return True

    def overlay_target_list(self,n,d,x,y,p):
        ship=np.rot90(self.ship[self.name_list[n]].shape,d)
        (x_d,y_d)=ship.shape
        
        for i in range(x_d):
            for j in range(y_d):
                if (ship[i][j]==1):
                    a=x-i
                    b=x-i+x_d-1
                    c=y-j
                    d=y-j+y_d-1
                    if (a>=0 and b<self.x and c>=0 and d<self.y):
                        for i_2 in range(a,b+1):
                            for j_2 in range(c,d+1):
                                if (ship[i_2-a][j_2-c]==1):
                                    self.target_list[i_2][j_2]+=p                                

    
    def populate_target_list(self):
        for ship in range(len(self.ship)):
            for x in range(self.x):
                for y in range(self.y):
                    for direction in range(4):
                        self.overlay_target_list(ship,direction,x,y,1)
                    
        
    def __init__(self,x,y,ships):
        self.x=x
        self.y=y
        self.ship=ships

        self.last_x=-1
        self.last_y=-1
        self.track_list=[]

        self.TRACKING=False
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

        
        self.target_list=np.zeros((self.x,self.y))
        self.populate_target_list()
        self.pt=0
        self.ship_sunk=0
        self.hit_list=np.ones((self.x,self.y))

        self.hit_yes=np.zeros((self.x,self.y))

    def biggest_2d(self,arr):
        (X,Y)=arr.shape
        dtype=[("x",int),("y",int),("w",int)]
        store=[]
        for i in range(X):
            for j in range(Y):
                if (self.hit_list[i][j]==1):
                    store.append((i,j,arr[i][j]))
        store=np.array(store,dtype=dtype)
        store=np.sort(store,order="w")
        return store[-1]
        
    def coord(self):
        coord=self.biggest_2d(self.prob_tot)
        if (coord[2]==0):
            self.TRACKING=False
            coord=self.biggest_2d(self.target_list)
            print(coord)
            (self.last_x,self.last_y)=(coord[0],coord[1])
            self.hit_list[self.last_x][self.last_y]=0
            return coord

        else:
            self.TRACKING=True
            print(coord)
            (self.last_x,self.last_y)=(coord[0],coord[1])
            self.hit_list[self.last_x][self.last_y]=0
            return coord

    

    def overlay(self,n,d,x,y,p):
        ship=np.rot90(self.ship[self.name_list[n]].shape,d)
        (x_d,y_d)=ship.shape
        
        for i in range(x_d):
            for j in range(y_d):
                if (ship[i][j]==1):
                    a=x-i
                    b=x-i+x_d-1
                    c=y-j
                    d=y-j+y_d-1
                    if (self.check(self.prob_tot,ship,a,b,c,d)):
                        for i_2 in range(a,b+1):
                            for j_2 in range(c,d+1):
                                if (ship[i_2-a][j_2-c]==1):
                                    self.prob_tot[i_2][j_2]+=p
                                    self.prob_list[n][i_2][j_2]+=p                        

    def special_check(self,arr1,arr2,a,b,c,d):
        (X,Y)=arr1.shape
        if (a<0): return False
        if (b>=X):return False
        if (c<0): return False
        if (d>=Y):return False
        bo=False
        for i in range(a,b+1):
            for j in range(c,d+1):
                #Ideally should -inf, we need to check
                if (arr1[i][j]<0 and arr2[i-a][j-c]==1):
                    return False
                if (self.hit_yes[i][j]==1 and arr2[i-a][j-c]==1):
                    bo=True
        return bo

    def special_overlay(self,n,d,x,y,p):
        ship=np.rot90(self.ship[self.name_list[n]].shape,d)
        (x_d,y_d)=ship.shape
        
        for i in range(x_d):
            for j in range(y_d):
                if (ship[i][j]==1):
                    a=x-i
                    b=x-i+x_d-1
                    c=y-j
                    d=y-j+y_d-1
                    if (self.special_check(self.prob_tot,ship,a,b,c,d)):
                        for i_2 in range(a,b+1):
                            for j_2 in range(c,d+1):
                                if (ship[i_2-a][j_2-c]==1):
                                    self.prob_tot[i_2][j_2]+=p
                                    self.prob_list[n][i_2][j_2]+=p 
    
    def read_outcome(self,val):
        for i in range(self.x): print(self.target_list[i])
        for i in range(self.x): print(self.prob_tot[i])
        for i in range(len(self.ship)):
            if (self.cnt_list[i]!=0):
                for direction in range(4):
                    self.overlay_target_list(i,direction,self.last_x,self.last_y,-1)
        if (val[0]==0):
            if (self.TRACKING==True):
                for i in range(len(self.ship)):
                    if (self.cnt_list[i]!=0):
                        for direction in range(4):
                            self.special_overlay(i,direction,self.last_x,self.last_y,-1)
            else:
                for i in range(len(self.ship)):
                    if (self.cnt_list[i]!=0):
                        for direction in range(4):
                            self.overlay_target_list(i,direction,self.last_x,self.last_y,-1)
            self.prob_tot[self.last_x][self.last_y]=-np.inf
            self.target_list[self.last_x][self.last_y]=-np.inf
        if (val[0]==1):
            self.hit_yes[self.last_x][self.last_y]=1
            for i in range(len(self.ship)):
                if (self.cnt_list[i]!=0):
                    for direction in range(4):
                        self.overlay(i,direction,self.last_x,self.last_y,1)
            
        if (val[0]==2):
            self.hit_yes[self.last_x][self.last_y]=1
            for i in range(len(self.ship)):
                if (self.cnt_list[i]!=0):
                    for direction in range(4):
                        self.overlay(i,direction,self.last_x,self.last_y,1)
        
            self.prob_tot-=self.prob_list[val[1]]
            self.cnt_list[val[1]]=0

            for i in range(len(self.ship)):
                if (self.cnt_list[i]!=0):
                    for direction in range(4):
                        for coord in val[2]:
                            self.overlay(i,direction,coord[0],coord[1],-1)
            for i in range(self.x):
                for j in range(self.y):
                    if (self.hit_list[i][j]==1):
                        for direction in range(4):
                            self.overlay_target_list(val[1],direction,i,j,-1)


            for coord in val[2]:
                self.prob_tot[coord[0]][coord[1]]=-np.inf
                self.target_list[coord[0]][coord[1]]=-np.inf
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

