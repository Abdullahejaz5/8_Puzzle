import heapq
import copy
import numpy as np
#13582,25
#A* algo is best because it give us sol to solve our puzzle in less moves
class PriorityQueue:
    def __init__(self):
        self.l=[]
    def enqueue(self, x):
        heapq.heappush(self.l,x)
    def dequeue(self):        
        return(heapq.heappop(self.l))
    def is_empty(self):
        return len(self.l)==0



class Node:
    def __init__(self, state, parent=None,level=0):
        self.state = state 
        self.parent = parent
        self.h = self.heuristic(state)
        self.level=level
    def __lt__ (self, other):
        return self.h+self.level<=other.h+other.level
    def heuristic(self, state):
        goal=[[1,2,3],[4,5,6],[7,8," "]]
        count=0
        for i in range(len(goal)):
            for j in range(len(state[i])):
                if state[i][j]!=goal[i][j]:
                    count +=1
        return count
    def __str__(self):
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
        return Node(save,st,st.level+1)

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
    
    def solve_puzzle(self):
        if not self.is_solvable(self.start.state):
            print("not possible to find way ")
            return
        count=0
        q = PriorityQueue()
        q.enqueue(self.start)
        visited=set()
        visited.add(str(self.start.state))
        while q:
            node = q.dequeue()
            children=self.generate_children(node)
            count+=1
            for neighbor in children:
                s=str(neighbor.state)
                if s==str(self.goal):
                    print(count)
                    self.print_solution(neighbor)
                    return True
                if s not in visited:
                    visited.add(s)
                    q.enqueue(neighbor)
        return
    
    def print_solution(self, final_state):
        s=[]
        s.append(final_state)
        count=1
        while final_state.parent:
            count+=1
            s.append(final_state.parent)
            final_state=final_state.parent
        s.reverse()
        for i in s:
            print (i)
        print(count)


ps = PuzzleSolver(Node([[4, 7, 8], [3, 6, 5], [1, 2, " "]]))
solution = ps.solve_puzzle()
