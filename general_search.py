from puzzle import Node
import heapq as hq

def general_search(initial_state, goal_state, heuristic, display_traceback="n"):
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
            print("Number of nodes expanded: " + str(counter)) 
            print("Max queue size: " + str(maxi))
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
 