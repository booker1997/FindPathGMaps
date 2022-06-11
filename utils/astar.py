


from hashlib import new

from matplotlib.pyplot import close
from numpy import Infinity
from .graphclasses import Node
from .google_api_and_graph_functions import get_travel_times
from .graphclasses import WeightedEdge
from alive_progress import alive_bar

def add_hueristics_to_graph(T_graph,start,end):
    for node in T_graph.nodes:
        if node == start:
            continue
        edges = T_graph.get_edges_for_node(node)
        for edge in edges:
            if edge.get_destination() == end:
                node_to_end_edge = edge
                node.add_h_value(node_to_end_edge.get_time())
            
            
    return T_graph

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        #print(current, 'in returnpath function')
        path.append(current)
        current = current.get_parent_node()
    return path[::-1]

def get_f_value(node):
        return node.get_f_value()

def get_best_path_a_star(digraph, start, end, path, best_time,best_path,paths):
    """
   
    """
    open_list = []
    closed_list = []
    open_list.append(start)
    i = 0
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.get_f_value() < current_node.get_f_value():
                current_node = item
                current_index = index
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        print(current_node, i)

        #current_node = sorted(open_list,key=get_f_value)[0]
        # open_list.remove(current_node)
        # closed_list.append(current_node)
        print('openlist', open_list)
        print('current',current_node)
        
        if current_node == end and i == len(digraph.get_nodes()): # and len(return_path(current_node)) == (len(digraph.get_nodes())) :
            print('at end',current_node,end)
            return return_path(current_node),0
        
        children = {}
        for edge in digraph.get_edges_for_node(current_node):
            new_node = edge.get_destination()
            new_node.set_parent_node(current_node)
            children[new_node] = edge.get_time()
        #print(current_node, children)
        for child in children:

            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            child.add_g_value(current_node.g_value + children[child])
            
            if len([open_node for open_node in open_list if child.get_name() == open_node.get_name() and child.g_value > open_node.g_value]) > 0:
                continue
            print('child loop',child,child.h_value)
            open_list.append(child)
        i +=1