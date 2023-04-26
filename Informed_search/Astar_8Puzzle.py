import numpy as np
import time

class Node():
    def __init__(self,state,parent,move,depth,step_cost,path_cost,heuristic_cost):
        self.state = state 
        self.parent = parent 
        self.move = move
        self.depth = depth # depth of the node in the tree
        self.step_cost = step_cost # g(n), the cost to take the step
        self.path_cost = path_cost # accumulated g(n), the cost to reach the current node
        self.heuristic_cost = heuristic_cost # h(n), cost to reach goal state from the current node
     
        self.moves = {'up': None, 'left': None, 'down': None, 'right': None}
    
    
    # return user specified heuristic cost
    def h_cost(self,new_state,goal_state,heuristic_function,path_cost,depth):
        if heuristic_function == 'num_misplaced':
            return self.h_misplaced_cost(new_state,goal_state)
        elif heuristic_function == 'manhattan':
            return self.h_manhattan_cost(new_state,goal_state)
    
    # return heuristic cost: number of misplaced tiles
    def h_misplaced_cost(self,new_state,goal_state):
        cost = 0
        for i in range(3):
            for j in range(3):
                if new_state[i][j] != goal_state[i][j]:
                    cost += 1
        return cost 
            
     # return heuristic cost: sum of Manhattan distance to reach the goal state
    def h_manhattan_cost(self,new_state,goal_state):
       
        goal_position_dic = {1:(0,0),2:(0,1),3:(0,2),8:(1,0),0:(1,1),4:(1,2),7:(2,0),6:(2,1),5:(2,2)} 
        distance = 0 
        for i in range(3):
            for j in range(3):
                current = new_state[i][j]
                if current != 0:
                    goal_position = np.argwhere(goal_state == current)[0]
                    distance += abs(i - goal_position[0]) + abs(j - goal_position[1])
        return distance

    # see if moving down is valid
    def move_down(self):
        # index of the empty tile
        zero_index=[i[0] for i in np.where(self.state==0)] 
        if zero_index[0] == 0:
            return False
        else:
            up_value = self.state[zero_index[0]-1,zero_index[1]] # value of the upper tile
            new_state = self.state.copy()
            new_state[zero_index[0],zero_index[1]] = up_value
            new_state[zero_index[0]-1,zero_index[1]] = 0
            return new_state,up_value
        
    # see if moving right is valid
    def move_right(self):
        zero_index=[i[0] for i in np.where(self.state==0)] 
        if zero_index[1] == 0:
            return False
        else:
            left_value = self.state[zero_index[0],zero_index[1]-1] # value of the left tile
            new_state = self.state.copy()
            new_state[zero_index[0],zero_index[1]] = left_value
            new_state[zero_index[0],zero_index[1]-1] = 0
            return new_state,left_value
        
    # see if moving up is valid
    def move_up(self):
        zero_index=[i[0] for i in np.where(self.state==0)] 
        if zero_index[0] == 2:
            return False
        else:
            lower_value = self.state[zero_index[0]+1,zero_index[1]] # value of the lower tile
            new_state = self.state.copy()
            new_state[zero_index[0],zero_index[1]] = lower_value
            new_state[zero_index[0]+1,zero_index[1]] = 0
            return new_state,lower_value
        
    # see if moving left is valid
    def move_left(self):
        zero_index=[i[0] for i in np.where(self.state==0)] 
        if zero_index[1] == 2:
            return False
        else:
            right_value = self.state[zero_index[0],zero_index[1]+1] # value of the right tile
            new_state = self.state.copy()
            new_state[zero_index[0],zero_index[1]] = right_value
            new_state[zero_index[0],zero_index[1]+1] = 0
            return new_state,right_value
        
    # once the goal node is found, trace back to the root node and print out the path
    def print_path(self):
        path = []
        node = self
        while node:
            path.append(node)
            node = node.parent

        state_trace = [self.state] # create FILO stacks to place the trace
        move_trace = [self.move]
        depth_trace = [self.depth]
        step_cost_trace = [self.step_cost]
        path_cost_trace = [self.path_cost]
        heuristic_cost_trace = [self.heuristic_cost]

        while self.parent:
            self = self.parent
            state_trace.append(self.state)
            move_trace.append(self.move)
            depth_trace.append(self.depth)
            step_cost_trace.append(self.step_cost)
            path_cost_trace.append(self.path_cost)
            heuristic_cost_trace.append(self.heuristic_cost)

        path.reverse()
        step_counter = 0
        moves = []

        for node in path:
            print('step', step_counter)
            print(node.state)
            print('g(n) =', node.depth, ', h(n) =', node.step_cost, ', f(n) =', node.path_cost + node.heuristic_cost, 'move =', node.move, '\n')
            moves.append(move_trace.pop())
            step_counter += 1
        
        moves.pop(0)
        print("Moves : ", moves[::1])

    # search based on path cost + heuristic cost
    def AStar_search(self,goal_state,heuristic_function):
        start = time.time()
        
        queue = [(self,0)] # queue of (found but unvisited nodes, path cost+heuristic cost), ordered by the second element
        queue_max_length = 1 # max number of nodes in the queue, measuring space performance
        
        depth_queue = [(0,0)] # queue of node depth, (depth, path_cost+heuristic cost)
        path_cost_queue = [(0,0)] # queue for path cost, (path_cost, path_cost+heuristic cost)
        visited = set([]) # record visited states
        
        while queue:
            # sort queue based on path_cost+heuristic cost, in ascending order
            queue = sorted(queue, key=lambda x: x[1])
            depth_queue = sorted(depth_queue, key=lambda x: x[1])
            path_cost_queue = sorted(path_cost_queue, key=lambda x: x[1])
                
            # update max queue length
            if len(queue) > queue_max_length:
                queue_max_length = len(queue)
                
            current_node = queue.pop(0)[0] 
            current_depth = depth_queue.pop(0)[0] # select and remove the depth for current node
            current_path_cost = path_cost_queue.pop(0)[0] # # select and remove the path cost for reaching current node

            # avoid repeated state
            current_state_tuple = tuple(current_node.state.reshape(1, 9)[0])
            if current_state_tuple in visited:
                continue
            visited.add(current_state_tuple)
            
            # when the goal state is found, trace back to the root node and print out the path
            if np.array_equal(current_node.state,goal_state):
                current_node.print_path()
                print ('Time spent: %0.5fs' % (time.time()-start), ('\n'))
                
                return True
            
            else:     
                # see if moving upper tile down is a valid move
                if current_node.move_down():
                    new_state,up_value = current_node.move_down()
                    # check if the resulting node is already visited
                    if tuple(new_state.reshape(1,9)[0]) not in visited:
                        path_cost=current_path_cost+up_value
                        depth = current_depth+1
                        # get heuristic cost
                        h_cost = self.h_cost(new_state,goal_state,heuristic_function,path_cost,depth)
                        # create a new child node
                        total_cost = path_cost+h_cost
                        current_node.move_down = Node(state=new_state,parent=current_node,move='down',depth=depth,\
                                              step_cost=up_value,path_cost=path_cost,heuristic_cost=h_cost)
                        queue.append((current_node.move_down, total_cost))
                        depth_queue.append((depth, total_cost))
                        path_cost_queue.append((path_cost, total_cost))
               
                if current_node.move_right():
                    new_state,left_value = current_node.move_right()
                  
                    if tuple(new_state.reshape(1,9)[0]) not in visited:
                        path_cost=current_path_cost+left_value
                        depth = current_depth+1
                        # get heuristic cost
                        h_cost = self.h_cost(new_state,goal_state,heuristic_function,path_cost,depth)
                        # create a new child node
                        total_cost = path_cost+h_cost
                        current_node.move_right = Node(state=new_state,parent=current_node,move='right',depth=depth,\
                                              step_cost=left_value,path_cost=path_cost,heuristic_cost=h_cost)
                        queue.append((current_node.move_right, total_cost))
                        depth_queue.append((depth, total_cost))
                        path_cost_queue.append((path_cost, total_cost))
                    
            
                if current_node.move_up():
                    new_state,lower_value = current_node.move_up()
                   
                    if tuple(new_state.reshape(1,9)[0]) not in visited:
                        path_cost=current_path_cost+lower_value
                        depth = current_depth+1
                        # get heuristic cost
                        h_cost = self.h_cost(new_state,goal_state,heuristic_function,path_cost,depth)
                        # create a new child node
                        total_cost = path_cost+h_cost
                        current_node.move_up = Node(state=new_state,parent=current_node,move='up',depth=depth,\
                                              step_cost=lower_value,path_cost=path_cost,heuristic_cost=h_cost)
                        queue.append((current_node.move_up, total_cost))
                        depth_queue.append((depth, total_cost))
                        path_cost_queue.append((path_cost, total_cost))

                
                if current_node.move_left():
                    new_state,right_value = current_node.move_left()
                    
                    if tuple(new_state.reshape(1,9)[0]) not in visited:
                        path_cost=current_path_cost+right_value
                        depth = current_depth+1
                        # get heuristic cost
                        h_cost = self.h_cost(new_state,goal_state,heuristic_function,path_cost,depth)
                        # create a new child node
                        total_cost = path_cost+h_cost
                        current_node.move_left = Node(state=new_state,parent=current_node,move='left',depth=depth,\
                                              step_cost=right_value,path_cost=path_cost,heuristic_cost=h_cost)
                        queue.append((current_node.move_left, total_cost))
                        depth_queue.append((depth, total_cost))
                        path_cost_queue.append((path_cost, total_cost))
                        

# read input array from user
arr = input('Enter 9 space-separated values: ').split()
arr = np.array(arr, dtype=int)
initial_state = arr.reshape(3, 3)

goal_state = np.array([1,2,3,8,0,4,7,6,5]).reshape(3,3)
print ('initial state')
print (initial_state, '\n')
print ('goal state')
print (goal_state, '\n')          

root_node = Node(initial_state,None,None,0,0,0,0)

# A*1 search based on path cost+heuristic cost, using priority queue
# root_node.AStar_search(goal_state,heuristic_function = 'num_misplaced')
root_node.AStar_search(goal_state,heuristic_function = 'manhattan')