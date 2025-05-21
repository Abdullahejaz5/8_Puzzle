import numpy as np
import copy
from collections import deque
class Node:
    def __init__(self, state, parent=None):
       self.state=state
       self.parent=parent
    
    def __str__(self):
        # Implement a method to print the state of the node
        l=""
        for i in self.state:
            l+=str(i)
            l+=" "
        return l

class PuzzleSolver:
    def __init__(self, start):
        self.start=start
        self.goal=[[1,2,3],[4,5,6],[7,8," "]]
    
    def is_solvable (self, state):
       count=0
       n=np.array(state)
       n1=n.reshape(-1)
       for i in range (9):
           for j in range(i,9):
               if n1[i]!=" " and n1[j]!=" " and n1[i]>n1[j]:
                   count+=1
       if count%2==0:
           return True
       else:
           return False
       
    def find_space(self, s):
        state=s.state
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j]==" ":
                    return(i,j)

    def find_moves(self, pos):
        # Implement the method to generate valid moves for the empty space
        x, y = pos
        b=[(x, y+1), (x, y-1),(x+1, y),(x-1, y)]
        return b

    def is_valid(self, move):
        x,y=move
        if(x>=0 and x<=2) and (y>=0 and y<=2):
            return True
        else:
            return False

    def play_move(self, st, move, space):
        save=copy.deepcopy(st.state)
        space_x,space_y=space
        move_x,move_y=move
        save[space_x][space_y]=save[move_x][move_y]
        save[move_x][move_y]=" "
        return Node(save,st)

    def generate_children(self, state):
        # Implement the method to generate all valid children from a state
        children = []
        space=self.find_space(state)
        moves=self.find_moves(space)

        for move in moves:
            if self.is_valid(move):
                child = self.play_move(state,move,space)
                children.append(child)
        return children
    
    def solve_puzzle_bfs(self):
        if not self.is_solvable(self.start.state):
            print("not possible to find way ")
            return
        else:
            self.solve_puzzle_bfs_mine()

    def solve_puzzle_bfs_mine(self):
        visited = set()
        q = deque()
        visited.add(str(self.start.state))
        q.append(self.start)
        count=0
        while q:
            count+=1
            node = q.popleft()
            children=self.generate_children(node)
            for neighbor in children:
                s=str(neighbor.state)
                if s==str(self.goal):
                    print(count)
                    self.disp_solution(neighbor)
                    return True
                if s not in visited:
                    visited.add(s)
                    q.append(neighbor)
    
    
    
    def solve_puzzle_dfs(self):
        if not self.is_solvable(self.start.state):
            print("not possible to find way ")
            return
        else:
            l=[]
            bol=False
            self.solve_puzzle_dfs_mine()
    def solve_puzzle_dfs_mine(self):
        visited = set()
        q = []
        s=str(self.start.state)
        visited.add(s)
        q.append(self.start)
        while len(q)>0:
            node = q[len(q)-1]
            q.pop(len(q)-1)
            if node.state==self.goal:
                self.disp_solution(node)
                return True
            children=self.generate_children(node)
            for neighbor in children:
                s1=str(neighbor.state)
                if s1 not in visited:
                    visited.add(s1)
                    q.append(neighbor)
                    
    def solve_puzzle_dfid(self):
        if not self.is_solvable(self.start.state):
            print("not possible to find way ")
            return
        for i in range(1,200000000004):
            if (self.solve_mine(i)):
                return    
    def solve_mine(self,depth):
        visited = set()
        q = []
        s=str(self.start.state)
        visited.add(s)
        q.append((self.start,1))
        while len(q)>0:
            node,d = q[len(q)-1]
            q.pop(len(q)-1)
            if node.state==self.goal:
                self.disp_solution(node)
                return True
            children=self.generate_children(node)
            if d<depth:
                for neighbor in children:
                    s1=str(neighbor.state)
                    if  s1 not in visited:
                        visited.add(s1)
                        q.append((neighbor,d+1))
        return False
    def solve_puzzle_backtracking(self):
        if not self.is_solvable(self.start.state):
            print("not possible to find way ")
            return
        start=self.start.state 
        goal=self.goal  
        SL = [start] 
        NSL = [start] 
        DE = [] 
        CS = start
        while NSL:
            if CS == goal:
                for i in SL:
                    print(i)
                return SL
            children = []
            for node in self.generate_children(Node(CS)):
                if node.state not in DE and node.state not in SL and node.state not in NSL:
                    children.append(node.state)
            if not children:
                while SL and CS == SL[len(SL)-1]:
                    DE.append(CS)
                    SL.pop(len(SL)-1)
                    NSL.pop(0)
                    if NSL:
                        CS = NSL[0]
                    else:
                        return "FAIL"
                SL.append(CS)
            else:
                children.extend(NSL)
                NSL=children
                CS = NSL[0]
                SL.append(CS)
        return "FAIL"
    def disp_solution(self, final_state):
        s=[]
        s.append(final_state)
        count=1
        while final_state.parent:
            s.append(final_state.parent)
            final_state=final_state.parent
            count+=1
        s.reverse()
        for i in s:
            print (i)
        print(count)
#Run this Test-Case
def main ():
    #b=[[1,2,' '], [4,5,3], [7,8,6]]
    #b=[[1,2,3], [4,8,5], [7,' ',6]]
    b=[[4, 7, 8], [3, 6, 5], [1, 2, ' ']] 
    start = Node(b)
    
    #print(start)
    solver = PuzzleSolver(start=start)
    solver.solve_puzzle_backtracking()
    solver.solve_puzzle_dfs()
    solver.solve_puzzle_bfs()
    solver.solve_puzzle_dfid()
main()
