import matplotlib.pyplot as plt
expanded_nodes = [0, 0, 0, 5, 2, 2, 35, 4, 4, 248, 18, 12, 2020, 119, 36, 11416, 619, 201]
expanded_nodes_Uniform = []
expanded_nodes_mis = []
expanded_nodes_man = []

for i in range(0, len(expanded_nodes), 3):
    expanded_nodes_Uniform.append(expanded_nodes[i+0])
    expanded_nodes_mis.append(expanded_nodes[i+1])
    expanded_nodes_man.append(expanded_nodes[i+2])
# print(expanded_nodes_Uniform)
# print(expanded_nodes_mis)
# print(expanded_nodes_man)
expanded = [expanded_nodes_Uniform, expanded_nodes_mis, expanded_nodes_man]

max_node_in_queue = [1, 1, 1, 6, 3, 3, 32, 6, 6, 152, 16, 12, 1190, 84, 28, 6328, 389, 137]
max_node_Uniform = []
max_node_mis = []
max_node_man = []
for i in range(0, len(max_node_in_queue), 3):
    max_node_Uniform.append(max_node_in_queue[i+0])
    max_node_mis.append(max_node_in_queue[i+1])
    max_node_man.append(max_node_in_queue[i+2])
# print(max_node_Uniform)
# print(max_node_mis)
# print(max_node_man)
maxi = [max_node_Uniform, max_node_mis, max_node_man]

depth = [0, 2, 4, 8, 12, 16]
h = ['Uniform Cost Search', 'A* Misplaced Tile Heuristic', 'A* Manhattan Distance Heuristic']

# generate the plot "Nodes Expanded vs Solution Depth"
for i, alg in enumerate(h):
    plt.plot(depth, expanded[i], label=alg)
plt.xlabel('Solution depth')
plt.ylabel('Expanded Nodes')
plt.title('Nodes Expanded vs Solution Depth')
plt.legend()
plt.show()

# generate the plot "Max Node In Queue vs Solution Depth"
for i, alg in enumerate(h):
    plt.plot(depth, expanded[i], label=alg)
plt.xlabel('Solution depth')
plt.ylabel('Max Node In Queue')
plt.title('Max Node In Queue vs Solution Depth')
plt.legend()
plt.show()