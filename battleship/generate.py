import numpy as np
import random
from ship import *

class board:
    def add_ship(board,x,y,ship,val):
        
        rand_order=[i for i in range(4)]
        random.shuffle(rand_order)

        for pt in rand_order:
            temp_bo=True
            if (pt==0):
                if (x+ship.x-1<board.x and y+ship.y-1<board.y):
                    for i in range(ship.x):
                        for j in range(ship.y):
                            if (ship.shape[i][j]==np.int32(1) and board.available[x+i][y+j]!=np.int32(-1)):
                                temp_bo=False
                else: temp_bo=False
            if (pt==1):
                if (x+ship.y-1<board.x and y-ship.x+1>=0):
                    for i in range(ship.x):
                        for j in range(ship.y):
                            if (ship.shape[i][j]==np.int32(1) and board.available[x+j][y-i]!=np.int32(-1)):
                                temp_bo=False
                else: temp_bo=False
            if (pt==2):
                if (x-ship.y+1>=0 and y+ship.x-1<board.y):
                    for i in range(ship.x):
                        for j in range(ship.y):
                            if (ship.shape[i][j]==np.int32(1) and board.available[x-j][y+i]!=np.int32(-1)):
                                temp_bo=False
                else: temp_bo=False
            if (pt==3):
                if (x-ship.x+1>=0 and y-ship.y+1>=0):
                    for i in range(ship.x):
                        for j in range(ship.y):
                            if (ship.shape[i][j]==np.int32(1) and board.available[x-i][y-j]!=np.int32(-1)):
                                temp_bo=False
                else: temp_bo=False

            if (temp_bo):
                #print(x,y,pt)
                store=[]
                if (pt==0):
                    for i in range(ship.x):
                        for j in range(ship.y):
                            if (ship.shape[i][j]==np.int32(1)):
                                board.available[x+i][y+j]=val
                                store.append((x+i,y+j))

                if (pt==1):
                    for i in range(ship.x):
                        for j in range(ship.y):
                            if (ship.shape[i][j]==np.int32(1)):
                                board.available[x+j][y-i]=val
                                store.append((x+j,y-i))

                if (pt==2):
                    for i in range(ship.x):
                        for j in range(ship.y):
                            if (ship.shape[i][j]==np.int32(1)):
                                board.available[x-j][y+i]=val
                                store.append((x-j,y+i))

                if (pt==3):
                    for i in range(ship.x):
                        for j in range(ship.y):
                            if (ship.shape[i][j]==np.int32(1)):
                                board.available[x-i][y-j]=val
                                store.append((x-i,y-j))
                                
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
            return (2,temp,board.pos_list[board.available[eff_x][eff_y]])
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
##temp=np.zeros((2,2))
##temp[0][0]=1
##temp[0][1]=1
##temp[1][0]=1
##ships["weird"]=ship(2,2,temp)
##
##board=board(4,8,ships)

