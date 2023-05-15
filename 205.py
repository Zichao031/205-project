import heapq as hq # Heap used to represent priority queue
import copy
from time import perf_counter

default_puzzles = [
    ("demo", [[1, 0, 3], [4, 2, 6], [7, 5, 8]]),
    ("trivial", [[1, 2, 3], [4, 5, 6], [7, 8, 0]]),
    ("very easy", [[1, 2, 3], [4, 5, 6], [7, 0, 8]]),
    ("easy", [[1, 2, 0], [4, 5, 3], [7, 8, 6]]),
    ("doable", [[0, 1, 2], [4, 5, 3], [7, 8, 6]]),
    ("oh boy", [[8, 7, 1], [6, 0, 2], [5, 4, 3]]),
    ("impossible", [[1, 2, 3], [4, 5, 6], [8, 7, 0]]),
]
heuristics = {
            "1": "Uniform Cost Search",
            "2": "A* Misplaced Tile Heuristic",
            "3": "A* Manhattan Distance Heuristic",
        }
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

def print_puzzle(puzzle):
    for row in puzzle:
        print("|", end="")
        for col in row:
            if col == 0:
                print("  *", end="")
            else:
                print(" {:2d}".format(col), end="")
        print(" |")
    print(" \n")

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
        print("Total number of nodes: " + str(cnt) + "\n")
        
    def display_puzzle(self):
        for i in self.state:
            print(i)
        print("  ")

    # Get valid expanded states 
    def expand(self):
        i0, j0 = get_position(0, self.state)
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

def general_search(initial_state, goal_state, heuristic, display_traceback="y"):
    root = Node(state=initial_state)
    goal = Node(state=goal_state)
    heap = [] # priority queue
    hq.heappush(heap, root)
    visited = [] 
    maxi = 1
    counter = 0
    while heap:
        maxi = max(len(heap), maxi)
        curr = hq.heappop(heap)
        if (display_traceback == "y"):
            print("\nExpanding: g(n) = " + str(int(curr.depth))  + " with h(n) = " + str(int(curr.cost)) + " ...")
            curr.display_puzzle()
        if (curr == goal):
            print("\nThis puzzle is solvable.\n" + "Traceback of this puzzle:")
            curr.traceback()
            print("The search algorithm " + heuristic + " expanded a total of " + str(counter) + " nodes.") 
            print("The maximum number of nodes in the queue: " + str(maxi))
            return counter, maxi
        else:
            visited.append(curr)
            # Skip None
            expanded = [i for i in curr.expand() if i]
            if expanded == []:
                continue
            for i in expanded:
                new = Node(state=i)
                if (heap and new in heap):
                    continue
                if (visited and new in visited):
                    continue
                if (heuristic == "A* Misplaced Tile Heuristic"):
                    new.mis(goal_state)
                if (heuristic == "A* Manhattan Distance Heuristic"):
                    new.man(goal_state)
                curr.add_child(node=new)
                hq.heappush(heap, new)
            counter += 1 
    print("FAILURE")            
    return -1


# SELECT DIFFERENT ALGORITHM, THREE AVAILABLE
def get_heuristic():
    while True:
        # "*" means defalt
        h = input("Select heuristic:\n" + " 1  Uniform Cost Search\n"
        + "*2  A* Misplaced Tile Heuristic\n" + " 3  A* Manhattan Distance Heuristic\n") or "3"
        if int(h) not in range(1, len(heuristics)+1):
            print("Error: input " + h + " is not within range, Using default\n")
        break
    print("Heuristic: " + heuristics[h])
    return heuristics[h]
    
def init_default_puzzle():
    list_len = len(default_puzzles)
    print("Default puzzle: enter the difficulty (1 to " + str(list_len) + "):")
    print("*1 " + default_puzzles[0][0])
    for i in range(1, len(default_puzzles)):
        print(" " + str(i + 1) + "  " + default_puzzles[i][0])
    while True:
        selected_difficulty = int(input() or 1)
        if ((selected_difficulty < 1) or (selected_difficulty > list_len)):
            print("Error: input " + str(selected_difficulty) + " is not within range.\n")
            selected_difficulty = 1
        break
    print("Selected difficulty " + default_puzzles[selected_difficulty - 1][0] + "\n")
    return default_puzzles[selected_difficulty - 1][1]


def customize_goal(num_rows):
    """
    1. Get user input for how many rows and cols the square matrix should have.
    2. Get user input whether they want to use the default goal state. For example,
    for a 3 by 3 puzzle, you get:
       [[1, 2, 3]
        [4, 5, 6]
        [7, 8, 0]]
    3. If user inputs 'n', get custom initial state.
    """  
    goal_state = [[(j + 1) + (num_rows * i) for j in range(num_rows)] for i in range(num_rows)]
    goal_state[num_rows - 1][num_rows - 1] = 0
    print("Use default goal state? (YES)")
    # Display the default goal state
    for i in goal_state:
        print(i)
    goal_mode = input() or "y"
    if goal_mode != "y":
        print("Enter custom goal state, using 0 to represent the blank."
              + " Delimit the numbers with a space. Press enter when done.\n")
        goal_state = []
        # Get custom goal state
        for i in range(0, num_rows):
            row = input("Enter row number " + str(i + 1) + ": ")
            # List comprehension: cast every item to int
            row = [int(x) for x in row.split()] 
            goal_state.append(row)    
        # Check for existence of 0
        if get_position(0, goal_state)[0] == None:
            print("No 0 found. Exiting...")
            return None      
    return goal_state
    
#Customize initial state
def customize_initial(num_rows):
    print("Enter your initial puzzle:")
    matrix = []
    for i in range(0, num_rows):
        row = input("Enter row number " + str(i + 1) + ": ")
        # List comprehension: cast every item to int
        row = [int(x) for x in row.split()]
        matrix.append(row)
    # Check for existence of 0
    if get_position(0, matrix)[0] == None:
        print("No 0 found. Exiting...")
        return None
    return matrix

def set_puzzle():
    print("We have two options for you:")
    init_state = []
    goal_state = []
    while True:
        mode = input("*1  Default 3x3 puzzle\n" + " 2  Custom puzzle\n") or "1"
        if mode == "1":
            init_state = init_default_puzzle()
            goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
            break     
        if mode == "2":
            while True:
                num_rows = int(input("Enter the number of rows and columns to make a square puzzle: \n")) or 3
                if num_rows not in range(0, 20):
                    num_rows = 3
                break
            init_state = customize_initial(num_rows)
            if init_state == None:
                return
            goal_state = customize_goal(num_rows)
            if goal_state == None:
                return
            break
        else:
            print("Invalid input.")
    return init_state, goal_state

def main():
    print("Welcome to Zichao's 8-puzzle solver.")
    init_state, goal_state = set_puzzle()
    # "y" for Yes, "n" for no
    display_traceback = input("Display traceback? (YES) \n") or "y"
    heuristic = get_heuristic()
    # Compute search Time
    start_time = perf_counter()
    general_search(init_state, goal_state, heuristic, display_traceback)
    end_time = perf_counter()
    timer = (end_time - start_time)
    print("\nElapsed time: %s ms." % timer)
    return

main()
