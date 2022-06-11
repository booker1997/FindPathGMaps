from hashlib import new

from matplotlib.pyplot import close
from numpy import Infinity
from .graphclasses import Node
from .google_api_and_graph_functions import get_travel_times
from .graphclasses import WeightedEdge
from alive_progress import alive_bar

def add_node_to_path(node, path):
    """
    Parameters:
        path: list composed of [[list of nodes], int]
            Represents the current path of nodes being traversed. Contains
            a list of nodes (Node) and total time traveled
    
        node: Node object 
            Node of t stop being added to the path
            
    Returns:
        [[list of nodes], int] - A safely COPIED version of path with the Node added to the end of 
        a COPY of the first element of path.
        
        This method should not mutate path or path[0]
        
    """
  
    time = path[1] # time of path so far. WE DON'T WANT TO CHANGE THIS
    copy_of_list_of_nodes = path[0].copy() # Copies list of nodes
    copy_of_list_of_nodes.append(node) # Add new node to copy
    
    answer = [copy_of_list_of_nodes,time] # return copy with the unchanged time
    return answer

def get_best_path(digraph, start, end, path, best_time,best_path,paths):
    """
    Finds the shortest path between t stops subject to constraints.

    Parameters:
        digraph: Digraph
            The graph on which to carry out the search
        start: Node
            t stop at which to start
        end: Node
            t stop at which to end
        path: list composed of [[list of Nodes], int]
            Represents the current path of nodes being traversed. Contains
            a list of Nodes and total time traveled.
        restricted_colors: list[strings]
            Colors of lines not allowed on path
        best_time: int
            The shortest time between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of Nodes
            The path with the shortest total time found so far between the original start
            and end node.

    Returns:
        A tuple of the form (best_path, best_time).
        The first item is the shortest-path from start to end, represented by
        a list of t stops (Nodes).
        The second item is an integer, the length (time traveled)
        of the best path.
        

        If there exists no path that satisfies restricted_colors constraints, then return None.
    """
    
    #print(path,len(path), len(digraph.get_nodes()))
    if type(start) != Node and type(end) != Node: # Nodes are valid nodes
        raise ValueError('Nodes given are not valid Nodes')
    elif path[0][-1]==end and len(path[0]) == (len(digraph.get_nodes())+1): # BASE CASE. How we know when we have found a valid path
        #print('MADE IT TO BASE')  
        paths += 1     
        #print(paths) 
        return path
    else:
#        print(digraph.get_edges_for_node(start))
        for edge in digraph.get_edges_for_node(start): # indexes the dictionary at the start node to try all edges from that node
#            print(edge)
            edge_end = edge.get_destination()
            edge_trans_type = edge.get_trans_type()
            edge_time = edge.get_time()
            if path[1]+edge_time > best_time:
                continue
            if edge_end == end and len(path[0])>2:
                if best_path == None or path[1] < best_time : # If the time is greater than the best path, then we want it to stop going down that path

                    updated_path = add_node_to_path(edge_end, path) # adds the current destination node to our path
                    updated_path[1] += edge_time # updates the time traveled with the time of edge
                    
                    
                    ## RECURSIVE CALL ##
                    # In this I create a new path, being our function called with the end of the 
                    # current edge as thew now beggining of the new path, as well as having the 
                    # most updated path as the path being passed in. this allows it to keep track of all
                    # of the paths as it goes through recursively. 
                    new_path = get_best_path(digraph, edge_end, end, updated_path,best_time,best_path,paths)
#                    print(new_path,'lsjdfkldsjfla')
#                    if new_path[0] == None:
#                        print('got here')
#                    print(new_path,'nepath')
                    
                    if new_path != None and new_path[1] < best_time: 
                        # with new path, check to see if it either was no path (None) or if the time is better than the old path. 
                        best_path = new_path[0] # If so, updat
                        best_time = new_path[1]# update
                        #print('best time so far:',best_time)
            elif edge_end not in path[0]: # avoids cycles

                if best_path == None or path[1] < best_time : # If the time is greater than the best path, then we want it to stop going down that path

                    updated_path = add_node_to_path(edge_end, path) # adds the current destination node to our path
                    updated_path[1] += edge_time # updates the time traveled with the time of edge
                    
                    
                    ## RECURSIVE CALL ##
                    # In this I create a new path, being our function called with the end of the 
                    # current edge as thew now beggining of the new path, as well as having the 
                    # most updated path as the path being passed in. this allows it to keep track of all
                    # of the paths as it goes through recursively. 
                    new_path = get_best_path(digraph, edge_end, end, updated_path,best_time,best_path,paths)
#                    print(new_path,'lsjdfkldsjfla')
#                    if new_path[0] == None:
#                        print('got here')
#                    print(new_path,'nepath')
                    
                    if new_path != None and new_path[1] < best_time: 
                        # with new path, check to see if it either was no path (None) or if the time is better than the old path. 
                        best_path = new_path[0] # If so, updat
                        best_time = new_path[1]# update
                        #print('best time so far:',best_time)
                        
        if best_path ==None: # No path possible
            return None
        else:
            return (best_path,best_time)  # Our return tuple


def directed_dfs(digraph, start, end,algorithm = get_best_path):
                    
    """
    Finds the shortest time path from start to end using a directed depth-first
    search. Minimize the total time and do not use the color lines in colors_not_used.

    Parameters:
        digraph: instance of Digraph
            The graph on which to carry out the search
        start: Node
            t-stop at which to start
        end: Node
            t-stop at which to end
        restricted_colors: list[string]
            Colors of lines not allowed in path

    Returns:
        The shortest-path from start to end, represented by
        a list of t stops (Nodes).

        If there exists no path that satisfies restricted_colors constraints, then raises a ValueError.
    """
    print()
    print('CALCULATING THE MOST OPTIMAL PATH FOR YOUR TOUR..............................')
    path = [[start], 0]  # begin at start node with 0 distance
    result = algorithm(digraph, start, end, path, Infinity, None,0)
    if result is None:
        raise ValueError("No path from {} to {}".format(start, end))
    
    return result