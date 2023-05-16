from general_search import general_search
import puzzle
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

test_puzzles = [
    ("test depth 0", [[1, 2, 3], [4, 5, 6], [7, 8, 0]]),
    ("test depth 2", [[1, 2, 3], [4, 5, 6], [0, 7, 8]]),
    ("test depth 4", [[1, 2, 3], [5, 0, 6], [4, 7, 8]]),
    ("test depth 8", [[1, 3, 6], [5, 0, 2], [4, 7, 8]]),
    ("test depth 12", [[1, 3, 6], [5, 0, 7], [4, 8, 2]]),
    ("test depth 16", [[1, 6, 7], [5, 0, 3], [4, 8, 2]]),
    ("test depth 20", [[7, 1, 2], [4, 8, 5], [6, 3, 0]]),
    ("test depth 24", [[0, 7, 2], [4, 6, 1], [3, 5, 8]]),
]

heuristics = {
            "1": "Uniform Cost Search",
            "2": "A* Misplaced Tile Heuristic",
            "3": "A* Manhattan Distance Heuristic", }

def get_position(val, state):
    state_len = len(state)
    for i in range(state_len):
        for j in range(state_len):
            if (state[i][j] == val):
                return i, j      
    return None, None

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

def init_puzzle(puzzles):
    list_len = len(puzzles)
    print("Default puzzle: enter the difficulty (1 to " + str(list_len) + "):")
    print("*1 " + puzzles[0][0])
    for i in range(1, len(puzzles)):
        print(" " + str(i + 1) + "  " + puzzles[i][0])
    while True:
        selected_difficulty = int(input() or 1)
        if ((selected_difficulty < 1) or (selected_difficulty > list_len)):
            print("Error: input " + str(selected_difficulty) + " is not within range.\n")
            selected_difficulty = 1
        break
    print("Selected difficulty: " + puzzles[selected_difficulty - 1][0] + "\n")
    return puzzles[selected_difficulty - 1][1]


def customize_goal(num_rows):
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
    print("We have three options for you:")
    init_state = []
    goal_state = []
    while True:
        mode = input("*1  Default 3x3 puzzle\n" + " 2  Custom puzzle\n" + " 3  test puzzle\n") or "1"
        if mode == "1":
            init_state = init_puzzle(default_puzzles)
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
        if mode == "3":
            init_state = init_puzzle(test_puzzles)
            goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
            break     
        else:
            print("Invalid input.")
    return init_state, goal_state

def driver():
    print("Welcome to Zichao Xiao's 8-puzzle solver.")
    init_state, goal_state = set_puzzle()
    # "y" for Yes, "n" for no
    display_traceback = input("Display traceback? (YES) \n") or "n"
    heuristic = get_heuristic()
    # Compute search Time
    start_time = perf_counter()
    general_search(init_state, goal_state, heuristic, display_traceback)
    end_time = perf_counter()
    timer = (end_time - start_time)
    print("\nElapsed time: %s ms." % timer)
    return

# driver()

# Get data for evaluation
def graph():
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    counters = []
    maxis = []
    for test in range(len(test_puzzles)):
        print("-----" + test_puzzles[test][0] + "-----")
        init_state = test_puzzles[test][1]
        for h in range(1, len(heuristics)+1):
            # h = "Uniform Cost Search"
            heuristic = heuristics[str(h)]
            print("-----" + heuristic + ("-----"))
            start_time = perf_counter()
            counter, maxi = general_search(init_state, goal_state, heuristic)
            end_time = perf_counter()
            timer = (end_time - start_time)
            print("Elapsed time: %s ms." % timer)
            counters.append(counter)
            maxis.append(maxi)

    print("\nheuristic: " + str(heuristics))
    print("expanded: " + str(counters))
    print("max nodes in queue:" + str(maxis))

# graph()   

def print_all_puzzles():
    for i in range(len(default_puzzles)):
        print(puzzle[i][0])
        print_puzzle(puzzle[i][1])

print_all_puzzles()
