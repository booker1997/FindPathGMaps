def get_best_path_dynamic_programming(digraph, start,nodes_subset):
    #print(nodes_subset,len(nodes_subset))
    visited = []
    for node in nodes_subset:
        node.reset_visited()
    cost = 0
    start.has_been_visited()
    if len(nodes_subset) == 2:
        for node in nodes_subset:
            if node != start:
                k = node
        if k != start:
            cost = digraph.get_edge_between_two_nodes(start,k).get_time()
            print('made it to base case')
            return cost
    else:
        for node_1 in nodes_subset:
            for node_2 in nodes_subset:
                if not node_2.get_visited_status() and node_1 != node_2 and node_1 != start:
                    #print(node_1,node_2)
                    nodes_subset.remove(node_2)
                    cost = min(get_best_path_dynamic_programming(digraph,node_1,nodes_subset)\
                           , digraph.get_edge_between_two_nodes(node_1,node_2).get_time())
                    node_1.has_been_visited()
    return cost

