import heapq as hq # Heap used to represent priority queue
import copy
from time import perf_counter

def manhattan(state, goal):
    distances = []
    for i in range(0, len(state)):
        for j in range(0, len(state[i])):
            if (state[i][j] == goal[i][j]):
                continue
            if (state[i][j] == 0):
                continue
            else:
                # find where this tile is in the goal state
                i_of_goal_tile, j_of_goal_tile = find_in_sublists(state[i][j], goal)
                distance = abs(i - i_of_goal_tile) + abs(j - j_of_goal_tile)
                distances.append(distance)
    return sum(distances)

def misplaced(state, goal_state):
    """
    Count the number of misplaced tiles between a state and a goal state.
    
    Returns:
        int: The number of misplaced tiles between the two states.
    """
    misplaced_count = 0
    # Flatten the lists
    state_flat = [item for sublist in state for item in sublist]
    goal_flat = [item for sublist in goal_state for item in sublist]
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

def is_state_equal(state1, state2):
    """
    Check if two states are equal.
    
    Returns:
        bool: True if the two states are equal, False otherwise.
    """
    # Flatten the list of lists for easy comparison
    flat_list1 = [item for sublist in state1 for item in sublist]
    flat_list2 = [item for sublist in state2 for item in sublist]
    return flat_list1 == flat_list2


def find_in_sublists(val, state):
    """
    Helper function used in Node.expand to find the indices of a value.
    
    Returns:
    A tuple containing the indices of the value in the list of lists.
    """
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
    # This is how we compare the states of two nodes in heapq and the visited list
    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return (self.depth + self.cost) < (other.depth + other.cost)

    def add_child(self, node, cost=1):
        node.depth = self.depth + cost
        node.parent = self # set parent
        self.children.append(node)
        
    def get_f_val(self):
        return (self.depth + self.cost)
    
    def traceback(self):
        p = self.parent
        count = 1
        temp = []
        while p:
            count += 1
            # print(p.state)
            temp.append(p)
            p = p.parent
        for i in reversed(temp):
            i.print_state()
        self.print_state()
        print(str(count) + " nodes traced.\n")
        
    def print_state(self):
        for i in self.state:
            print(i)
        print("  ")
        
    def expand(self):
        """Returns a list of valid expanded states."""
        i0, j0 = find_in_sublists(0, self.state)
        state_len = len(self.state)
        states_to_return = []
        dir = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        # Move Up: Swap zero and the element above it such element exists
        for i in range(4):
            new_i0 = i0 + dir[i][0]
            new_j0 = j0 + dir[i][1]
            if (new_i0 >= 0 and new_i0 < state_len and new_j0 >= 0 and new_j0 < state_len):
                temp_state = copy.deepcopy(self.state)
                temp_state[i0][j0] = temp_state[new_i0][new_j0]
                temp_state[new_i0][new_j0] = 0
                # if the parent does not have the same expanded state, add none
                if self.parent and is_state_equal(temp_state, self.parent.state):
                    states_to_return.append(None) 
                else:
                    states_to_return.append(temp_state)
        return states_to_return


def general_search(initial_state, goal_state, heuristic, verbose="y"):
    root = Node(state=initial_state)
    heap = [] # priority queue
    hq.heappush(heap, root)
    visited = [] 
    maxi = 1
    counter = 0
    # While heapq is not empty...
    while heap:
        maxi = max(len(heap), maxi)
        curr = hq.heappop(heap)
        if (verbose == "y"):
            print("\nExpanding: g(n) = " + str(int(curr.depth))
                  + " with h(n) = " + str(int(curr.cost)) + " ...")
            curr.print_state()
        if (is_state_equal(curr.state, goal_state)):
            if (verbose == "y"):
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
                # Skip if new already exists in heap
                if (heap and new in heap):
                    continue
                # Skip if new already exists in visited
                if (visited and new in visited):
                    continue
                if (heuristic == "A* Misplaced Tile Heuristic"):
                    new.cost = misplaced(new.state, goal_state)
                if (heuristic == "A* Manhattan Distance Heuristic"):
                    new.cost = manhattan(new.state, goal_state)
                curr.add_child(node=new)
                hq.heappush(heap, new)
            counter += 1 
    print("FAILURE")            
    return -1


# SELECT DIFFERENT ALGORITHM, THREE AVAILABLE
def get_heuristic():
    heuristics = {
                "1": "Uniform Cost Search",
                "2": "A* Misplaced Tile Heuristic",
                "3": "A* Manhattan Distance Heuristic",
            }
    while True:
        try:
            # Default algorithm is Manhattan Distance Heuristic
            # Press Enter for default
            h = input("Select algorithm:\n" + " 1  Uniform Cost Search\n"
          + " 2  A* Misplaced Tile Heuristic\n" + " 3  A* Manhattan Distance Heuristic\n") or "3"
            if int(h) not in range(1, len(heuristics)+1):
                print("Error: input " + h + " is not within range.\n")
                raise ValueError
            break
        except(ValueError):
            print("Error: number not in the valid range or press enter for default.")
    print("Heuristic: " + heuristics[h])
    return heuristics[h]
    
def init_default_puzzle():
    """
    Gets user input and returns the corresponding puzzle matrix.
    
    Parameters:
    puzzle_list (list of pairs): list containing pairs of ["name", list of lists]
        E.g, puzzle_list = [("trivial", [[1, 2, 3], [4, 5, 6], [7, 8, 0]])]
    
    Returns:
    list of lists: represents a matrix.
    """
    
    puzzle_list = [
        ("demo", [[1, 0, 3], [4, 2, 6], [7, 5, 8]]),
        ("trivial", [[1, 2, 3], [4, 5, 6], [7, 8, 0]]),
        ("very easy", [[1, 2, 3], [4, 5, 6], [7, 0, 8]]),
        ("easy", [[1, 2, 0], [4, 5, 3], [7, 8, 6]]),
        ("doable", [[0, 1, 2], [4, 5, 3], [7, 8, 6]]),
        ("oh boy", [[8, 7, 1], [6, 0, 2], [5, 4, 3]]),
        ("impossible", [[1, 2, 3], [4, 5, 6], [8, 7, 0]]),
        # insert new puzzle here
    ]
    
    list_len = len(puzzle_list)

    print("Default puzzle: enter the difficulty (1 to " + str(list_len) + "):\n")
    
    # Show the user different puzzle difficulties
    print("[1] " + puzzle_list[0][0])
    for i in range(1, len(puzzle_list)):
        print(" " + str(i + 1) + "  " + puzzle_list[i][0])
    
    while True:
        try:
            selected_difficulty = int(input() or 4)

            if ((selected_difficulty < 1) or (selected_difficulty > list_len)):
                print("Error: input " + str(selected_difficulty) + " is not within range.\n")
                raise ValueError

            break
        except(ValueError):
            print("Error: please input a number or press enter for default!")

    # e.g, Selecting trivial returns [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    print("Selected difficulty " + puzzle_list[selected_difficulty - 1][0] + "\n")
    return puzzle_list[selected_difficulty - 1][1]


def get_goal_state(num_rows):
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

    print("Use default goal state? [y]/n")
    
    # Show the user what the default goal looks like
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
            row = [int(x) for x in row.split()] # https://www.geeksforgeeks.org/python-converting-all-strings-in-list-to-integers/
            goal_state.append(row)
        
        # Check for existence of 0
        if find_in_sublists(0, goal_state)[0] == None:
            print("No 0 found. Exiting...")
            return None
        
    return goal_state
    
def get_initial_state(num_rows):
    print("Enter your initial puzzle, using 0 to represent the blank."
              + " Delimit the numbers with a space. Press enter when done.\n")
        
    matrix = []

    # Get custom start state
    for i in range(0, num_rows):
        row = input("Enter row number " + str(i + 1) + ": ")
        # List comprehension: cast every item to int
        row = [int(x) for x in row.split()]
        matrix.append(row)

    # Check for existence of 0
    if find_in_sublists(0, matrix)[0] == None:
        print("No 0 found. Exiting...")
        return None
        
    return matrix



def get_puzzle():
    print("We have two options for you:")
    init_state = []
    goal_state = []

    while True:
        mode = input(" 1  Default 3x3 puzzle\n" + " 2  Custom puzzle\n") or "1"
        if mode == "1":
            init_state = init_default_puzzle()
            goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
            break     
        if mode == "2":
            while True:
                try:
                    num_rows = int(input("Enter the number of rows and columns to make a square puzzle: \n")) or 3
                    if num_rows not in range(0, 20):
                        raise ValueError
                    break
                except ValueError:
                    print("Error: Vaild input must be positive and less than 20")
            init_state = get_initial_state(num_rows)
            if init_state == None:
                return
            goal_state = get_goal_state(num_rows)
            if goal_state == None:
                return
            break
        else:
            print("Invalid input.")

    return init_state, goal_state


def main():
    print("Welcome to Zichao's 8-puzzle solver.")
    init_state, goal_state = get_puzzle()
    # "y" for Yes, "n" for no
    verbose = input("Display traceback? \n") or "y"
    heuristic = get_heuristic()
    # Compute search Time
    t1_start = perf_counter()
    general_search(init_state, goal_state, heuristic, verbose)
    t1_stop = perf_counter()
    timer = (t1_stop - t1_start)
    print("--- %s milliseconds ---" % timer)
        
    return

main()