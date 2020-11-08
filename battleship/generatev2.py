import numpy as np
import random
from ship import *
def check(arr1,arr2,x,y):
    (x1,y1)=arr1.shape
    (x2,y2)=arr2.shape

    if (x>=0 and y>=0 and x+x2<x1 and y+y2<y1):
        for i in range(x2):
            for j in range(y2):
                if (arr1[x+i][y+j]!=-1 and arr2[i][j]==1):
                    return False
        return True
    return False
    

class board:
    def add_ship(board,x,y,ship,val):        
        rand_order=[i for i in range(4)]
        random.shuffle(rand_order)

        for pt in rand_order:
            temp_bo=True
            if (pt==0):
                temp_bo=check(board.available,ship.shape,x,y)
            if (pt==1):
                temp_bo=check(board.available,np.rot90(ship.shape,1),x-ship.y+1,y)
            if (pt==2):
                temp_bo=check(board.available,np.rot90(ship.shape,2),x-ship.x+1,y-ship.y+1)
            if (pt==3):
                temp_bo=check(board.available,np.rot90(ship.shape,3),x,y-ship.x+1)

            if (temp_bo):
                #print(x,y,pt)
                store=[]
                cur=np.rot90(ship.shape,pt)
                (x_d,y_d)=cur.shape
                print(cur)
                if (pt==0):
                    start_x=x
                    start_y=y
                if (pt==1):
                    start_x=x-x_d+1
                    start_y=y
                if (pt==2):
                    start_x=x-x_d+1
                    start_y=y-y_d+1
                if (pt==3):
                    start_x=x
                    start_y=y-y_d+1
                for i in range(x_d):
                    for j in range(y_d):
                        if (cur[i][j]==1):
                            board.available[start_x+i][start_y+j]=val
                            store.append((start_x+i,start_y+j))
                board.pos_list.append(store)
                return True
            
        return False
    
    def __init__(self,x,y,ships):
        self.x=x
        self.y=y
        self.available=np.full((x,y),-1)
        self.ship=ships
        self.cnt_list=[]
        self.pos_list=[]
        self.name_list=[]
        self.ship_sunk=0
        self.vis=["."*self.y for i in range(self.x)]

        rand_order=[i for i in range(self.x*self.y)]
        random.shuffle(rand_order)
        rand_order_pt=0

        for i in self.ship:
            while (self.add_ship(rand_order[rand_order_pt]//self.y,
                            rand_order[rand_order_pt]%self.y,
                            self.ship[i],len(self.name_list))==False):
                rand_order_pt+=1
                if (rand_order_pt==self.x*self.y): break
            
            self.name_list.append(i)
            
            cnt=0
            for a in range(self.ship[i].x):
                for b in range(self.ship[i].y):
                    if (self.ship[i].shape[a][b]==1): cnt+=1
            self.cnt_list.append(cnt)

        print(self.available)
    def fire(board,coord):
        #print(board.available)
        #print(board.cnt_list)
        eff_x=coord[0]
        eff_y=coord[1]
        
        if (board.available[eff_x][eff_y]==-2):
            print("Grid already hit")
            return (-1,None)
        if (board.available[eff_x][eff_y]==-1):
            print("Bloop...")
            board.vis[eff_x]=board.vis[eff_x][:eff_y]+'O'+board.vis[eff_x][eff_y+1:]
            board.available[coord[0]][coord[1]]=-2
            return (0,None)
        board.cnt_list[board.available[eff_x][eff_y]]-=1
        board.vis[eff_x]=board.vis[eff_x][:eff_y]+'X'+board.vis[eff_x][eff_y+1:]
        if (board.cnt_list[board.available[eff_x][eff_y]]==0):
            temp=board.available[eff_x][eff_y]
            print(board.name_list[board.available[eff_x][eff_y]]+" has sunk!!!")
            board.available[eff_x][eff_y]=-2
            print(board.pos_list[temp])
            return (2,temp,board.pos_list[temp])
        else:
            print("Hit!")
            board.available[eff_x][eff_y]=-2
            return (1,None)

    def visualise(board):
        print("-"*board.y)
        for i in range(board.x):
            print(board.vis[i])
        print("-"*board.y)

##ships={}
##ships["sloop"]=ship(1,2,np.ones((1,2)))
##ships["men-of-war"]=ship(1,4,np.ones((1,4)))
##temp=np.zeros((2,3))
##temp[0][0]=1
##temp[0][1]=1
##temp[1][0]=1
##temp[0][2]=1
##print(temp)
##ships["weird"]=ship(2,3,temp)
##
##board=board(4,8,ships)

