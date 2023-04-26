class Node:
    def __init__(self, state, parent, depth,  cost):
        self.state = state
        self.parent = parent
        self.heuristic = cost
        self.depth = depth


def create_node(state, parent, depth, cost):
    return Node(state, parent, depth, cost)


def heuristic(state, goal):
    if state == None :
        return None

    dmatch=0
    for i in range(0,9):
        if state[i] != goal[i]:
            dmatch+=1
    return dmatch
    # distance = 0
    # for i in range(len(state)):
    #     if state[i] == 0:
    #         continue
    #     x1, y1 = divmod(i, 3)
    #     x2, y2 = divmod(goal.index(state[i]), 3)
    #     distance += abs(x1 - x2) + abs(y1 - y2)
    # return distance

def move_up(state):
    new_state = state[:]
    index = new_state.index(0)
    if index not in [0, 1, 2]:
        temp = new_state[index - 3]
        new_state[index-3] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None

def move_down(state):
    new_state = state[:]
    index = new_state.index(0)
    if index not in [6, 7, 8]:
        temp = new_state[index + 3]
        new_state[index + 3] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None
    
def move_right(state):
    new_state = state[:]
    index = new_state.index(0)
    if index not in [2, 5, 8]:
        temp = new_state[index + 1]
        new_state[index + 1] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None
    
def move_left(state):
    new_state = state[:]
    index = new_state.index(0)
    if index not in [0, 3, 6]:
        temp = new_state[index - 1]
        new_state[index - 1] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None


def expand_node(node, goal):
    expanded_nodes = []
    expanded_nodes.append(create_node(move_up(node.state), node,node.depth+1 , heuristic(move_up(node.state), goal)))
    expanded_nodes.append(create_node(move_down(node.state), node,node.depth+1 ,heuristic(move_down(node.state), goal)))
    expanded_nodes.append(create_node(move_left(node.state), node,node.depth+1 ,heuristic(move_left(node.state), goal)))
    expanded_nodes.append(create_node(move_right(node.state), node,node.depth+1,heuristic(move_right(node.state), goal))) 
    expand_res= []
    for item in expanded_nodes:
        if (item.parent.parent != None and item.parent.parent.state == item.state) or item.state == None : 
            continue
        expand_res.append(item)
            
    return expand_res


def greedy(start_node, goal):
    open_list = [start_node]
    
    while open_list:
        #sorting list berdasarkan heuristic (ascending)
        open_list.sort(key=lambda x: x.heuristic)
        
        #ambil node dengan heuristic terkecil
        current_node = open_list.pop(0)
        
        #cek apakah current_node adalah goal state
        if current_node.heuristic == 0:
            return current_node
        
        #expand node dan extend child ke open_list
        open_list = []
        open_list.extend(expand_node(current_node, goal))
        
        display_board(current_node.state)

    return None

def display_board(state):
    print( "-------------")
    print( "| %i | %i | %i |" % (state[0], state[1], state[2]))
    print( "-------------")
    print( "| %i | %i | %i |" % (state[3], state[4], state[5]))
    print( "-------------")
    print( "| %i | %i | %i |" % (state[6], state[7], state[8]))
    print( "-------------")
    print("\n")
    
start_state =  [1, 3, 4, 8, 6, 2, 7, 0, 5]
#start_state = [2, 8, 1, 0, 4, 3, 7, 6, 5] 
#start_state = [2, 8, 1, 4, 6, 3, 0, 7, 5]
goal_state =   [1, 2, 3, 8, 0, 4, 7, 6, 5]
start_node = create_node(start_state, None, 0, heuristic(start_state, goal_state))

result = greedy(start_node, goal_state)
display_board(result.state)
print(result.depth)
    