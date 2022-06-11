from numpy import Infinity
from .graphclasses import Node
from .google_api_and_graph_functions import get_travel_times
from .graphclasses import WeightedEdge
from alive_progress import alive_bar


def make_edges_for_node(empty_graph, node,address_list,formatted_addresses_dict,restricted_trans_methods):
    new_list_without_add_1 = address_list.copy()
    new_list_without_add_1.remove(node.get_address())
    edges = []
    if not empty_graph.has_node(node):
        empty_graph.add_node(node)
    for add_2 in new_list_without_add_1:
        travel_times_dict = get_travel_times(node.get_address(),add_2,restricted_trans_methods)
        second_node = Node(add_2,formatted_addresses_dict[add_2])
        if not empty_graph.has_node(second_node):
            empty_graph.add_node(second_node)
        for key in travel_times_dict:
            time = travel_times_dict[key][0] # change from str to int
            edge1 = WeightedEdge(node,second_node,time,key)
            edges.append(edge1)
            empty_graph.add_edge(edge1)
    return edges


def nearest_neighbor(digraph, start, end,address_list,formatted_addresses_dict,restricted_trans_methods):
    """
   
    """
    path = [start]
    print(start)
    total_time = 0
    current_node = start
    with alive_bar(len(address_list)) as bar:
        while len(path) < (len(address_list)+1):
            edges = make_edges_for_node(digraph,current_node,address_list,formatted_addresses_dict,restricted_trans_methods)
            best_edge_time = Infinity
            debugger = []
            for edge in edges:
                
                edge_time = edge.get_time()
                edge_dest = edge.get_destination()
                
                #print(current_node.get_name(),edge_dest,'edge time',edge_time,best_edge_time)

                if len(path) == len(address_list):
                    if edge_dest == end:
                        best_edge_dest = edge_dest
                        best_edge_time = edge_time
                elif edge_time < best_edge_time and edge_dest not in path:
                    best_edge_dest = edge_dest
                    best_edge_time = edge_time
            path.append(best_edge_dest)
            total_time += best_edge_time
            print(total_time,best_edge_time)
            current_node = best_edge_dest
            bar()
        
        #print(current_node,best_edge_dest)
    return path,total_time