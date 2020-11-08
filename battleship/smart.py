import numpy as np
from ship import ship

class smart:
    def __init__(self,x,y,ships):
        self.x=x
        self.y=y
        self.ship=ships
        self.tot=[]
        self.board=[]
        self.ship=[]

    def new_ship(self,ship):
        temp_board=np.zeros((self.x,self.y))
        temp_tot=0
        
        for i in range(self.x):
            for j in range(self.y):
                for s_i in range(ship.x):
                    for s_j in range(ship.y):
                        if (i+ship.x<=self.x and j+ship.y<=self.y):
                            temp_board[i+s_i][j+s_j]+=1
                            temp_tot+=1
                        if (i+ship.y<=self.x and j-ship.x>=-1):
                            temp_board[i+s_j][j-s_i]+=1
                            temp_tot+=1
                        if (i-ship.y>=-1 and j+ship.x<=self.y):
                            temp_board[i-s_j][j+s_i]+=1
                            temp_tot+=1
                        if (i-ship.x>=-1 and j-ship.y>=-1):
                            temp_board[i-s_i][j-s_j]+=1
                            temp_tot+=1
  
        
        self.board.append(temp_board)
        self.tot.append(temp_tot)
        self.ship.append(ship)

    def board_state(self):
        print(sum(self.tot))
        print(sum(self.board))

    #def miss
        
    #def hit

    #def sink
    
