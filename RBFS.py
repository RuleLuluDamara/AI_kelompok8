import math
import time

class Node:
    def __init__(self, state, cost, depth):
        self.state = state

        self.cost = cost

        self.depth = depth

def create_node(state, cost, depth):
    return Node(state, cost, depth)

def check_cost(now, goal):
    if now == None :
        return None
    miss = 0
    cur = now[:]
    fin = goal[:]
    for i in range(9):
        if cur[i] != 0 and cur[i] != fin[i]:
            miss += 1
    return miss

def display_state(state):
    print("---------------")
    print(f"| {state[0]} | {state[1]} | {state[2]} |")
    print(f"| {state[3]} | {state[4]} | {state[5]} |")
    print(f"| {state[6]} | {state[7]} | {state[8]} |")
    print("---------------")


def move_up(state):
    new = state[:]
    ind = new.index(0)
    
    if ind not in [0, 1, 2] :
        temp = new[ind - 3]
        new[ind - 3] = new[ind]
        new[ind] = temp
        return new
    else:
        return None
    
def move_down(state):
    new = state[:]
    ind = new.index(0)
    
    if ind not in [6, 7, 8] :
        temp = new[ind + 3]
        new[ind + 3] = new[ind]
        new[ind] = temp
        return new
    else:
        return None
    
    
def move_left(state):
    new = state[:]
    ind = new.index(0)
    
    if ind not in [0, 3, 6] :
        temp = new[ind - 1]
        new[ind - 1] = new[ind]
        new[ind] = temp
        return new
    else:
        return None
    

def move_right(state):
    new = state[:]
    ind = new.index(0)
    
    if ind not in [2, 5, 8] :
        temp = new[ind + 1]
        new[ind + 1] = new[ind]
        new[ind] = temp
        return new
    else:
        return None
    

def move_node(node, goal):
    expand_prob =[create_node(move_up(node.state), check_cost(move_up(node.state), goal.state), node.depth + 1),
                create_node(move_down(node.state), check_cost(move_down(node.state), goal.state), node.depth + 1),
                create_node(move_left(node.state), check_cost(move_left(node.state), goal.state), node.depth + 1),
                create_node(move_right(node.state), check_cost(move_right(node.state), goal.state), node.depth + 1)]

    expand_node = [x for x in expand_prob if x.state != None]
    # for item in expand_prob:
    #     if (item.parent.parent != None and item.parent.parent.state == item.state) or item.state == None : 
    #         continue
    #     expand_node.append(item)
            
    return expand_node


def rbfs(start, goal, f_limit):
    rank = []
    if start.cost == 0:
        return [start, None]
    children = move_node(start, goal)

    if len(children) == 0:
        return [None, math.inf]
    
    ind = 0
    for child in children:
        child.total = child.cost + child.depth
        rank.append((child.total, ind, child))
        ind += 1
    
    while len(rank) > 0:
        rank.sort()
        best_node = rank[0][2]
        if best_node.total > f_limit:
            return [None, best_node.total]
        
        second_best_total = rank[1][0]

        x = rbfs(best_node, goal, min(f_limit, second_best_total))
        result = x[0]
        best_node.total = x[1]
        rank[0] = (best_node.total, rank[0][1], best_node)
        if result != None:
            break
    return [result, None]
        

# start_time = time.time()

# lst =    [2, 8, 1,
#         4, 6, 3,
#         0, 7, 5]
# goal = [1, 2, 3, 8, 0, 4, 7, 6, 5]

# start_node = create_node(lst, check_cost(lst, goal), 0)
# goal_node = create_node(goal, 0, 0)
# x = rbfs(start_node, goal_node, 15)

# print(x[0].state)

# print(x[0].depth)

# end_time = time.time()

# print(end_time-start_time)








