import copy

def manhattan(state, goal):
    distances = []
    for i in range(0, len(state)):
        for j in range(0, len(state[i])):
            if (state[i][j] == goal[i][j] or state[i][j] == 0):
                continue
            else:
                # find where this tile is in the goal state
                i_goal, j_goal = get_position(state[i][j], goal)
                distance = abs(i - i_goal) + abs(j - j_goal)
                distances.append(distance)
    return sum(distances)

# get the number of misplaced tiles between the two states.
def misplaced(state, goal_state):
    misplaced_count = 0
    # Flatten the lists
    state_flat = [j for i in state for j in i]
    goal_flat = [j for i in goal_state for j in i]
    for i in range(len(goal_flat)):
        # Skip the blank tile
        if state_flat[i] == 0:
            continue
        if state_flat[i] != goal_flat[i]:
            misplaced_count += 1      
    return misplaced_count

def get_position(val, state):
    state_len = len(state)
    for i in range(state_len):
        for j in range(state_len):
            if (state[i][j] == val):
                return i, j      
    return None, None


   
class Node:
    def __init__(self, parent=None, state=0, depth=0, cost=0):
        self.parent = parent
        self.state = state
        self.depth = depth
        self.cost = cost
        self.children = []
    def __eq__(self, other):
        x = [j for i in self.state for j in i]
        y = [j for i in other.state for j in i]
        return x == y

    def __lt__(self, other):
        return (self.depth + self.cost) < (other.depth + other.cost)

    def add_child(self, node, cost=1):
        node.depth = self.depth + cost
        node.parent = self # set parent
        self.children.append(node)
    
    def traceback(self):
        p = self.parent
        cnt = 1
        temp = []
        while p:
            cnt += 1
            temp.append(p)
            p = p.parent
        for i in reversed(temp):
            i.display_puzzle()
        self.display_puzzle()
        print("Number of traced nodes: " + str(cnt))
        
    def display_puzzle(self):
        for i in self.state:
            print(i)
        print("  ")

    # Get valid expanded states 
    def expand(self):
        i0, j0 = get_position(0, self.state)
        # if (i0 == None or j0 == None):
        state_len = len(self.state)
        states_to_return = []
        dir = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for i in range(4):
            new_i0 = i0 + dir[i][0]
            new_j0 = j0 + dir[i][1]
            if (new_i0 >= 0 and new_i0 < state_len and new_j0 >= 0 and new_j0 < state_len):
                temp_state = copy.deepcopy(self.state)
                temp_state[i0][j0] = temp_state[new_i0][new_j0]
                temp_state[new_i0][new_j0] = 0
                if self.parent and self ==  self.parent:
                    states_to_return.append(None) 
                else:
                    states_to_return.append(temp_state)
        return states_to_return

    def man(self, goal_state):
        self.cost = manhattan(self.state, goal_state)
    
    def mis(self, goal_state):
        self.cost = misplaced(self.state, goal_state)



