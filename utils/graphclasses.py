class Node(object):
    def __init__(self,address,name,rating=None,open = True):
        self.visits = 0
        self.address = address
        self.parent = None
        self.rating = rating
        self.visited = False
        self.open = open
        self.name = name
        self.f_value = None
        self.g_value = 0
        self.h_value = 0
    
    def get_visited_status(self):
        return self.visited

    def has_been_visited(self):
        self.visited = True
    def reset_visited(self):
        if not self.visited:
            print('This place has already been marked as not visited.')
        else:
            self.visited = False
    def get_address(self):
        ''' return: the name of the node '''
        return self.address
    def get_name(self):
        return self.name
    def add_g_value(self,g_value):
        self.g_value = g_value
    def set_parent_node(self,parent_node):
        self.parent = parent_node
    def get_parent_node(self):
        return self.parent
    def add_h_value(self,h_value):
        self.h_value = h_value
    def get_f_value(self):
        return self.g_value + self.h_value

    def __str__(self):
        ''' return: The name of the node.
                This is the function that is called when print(node) is called.
        '''
        return self.name

    def __repr__(self):
        ''' return: The name of the node.
                Formal string representation of the node
        '''
        return self.address

    def __eq__(self, other):
        ''' returns: True is self == other, false otherwise
                 This is function called when you used the "==" operator on nodes
        '''
        return self.address == other.address

    def __ne__(self, other):
        ''' returns: True is self != other, false otherwise
                This is function called when you used the "!=" operator on nodes
        '''
        return not self.__eq__(other)

    def __hash__(self):
        ''' This function is necessary so that Nodes can be used as
        keys in a dictionary, Nodes are immutable
        '''
        return self.address.__hash__()

class WeightedEdge(object):
    def __init__(self,src,dest,time,transportation_type = 'walking'):
        self.dest = dest
        self.time = time
        self.visits = 0
        self.src = src
        self.transportation_type = transportation_type
        #
    
    def get_source(self):
        """ Getter method for WeightedEdge
            returns: Node representing the source node """
        return self.src

    def get_destination(self):
        """ Getter method for WeightedEdge
            returns: Node representing the destination node """
        return self.dest
    
    def get_time(self):
        """ Getter method for WeightedEdge
            returns: int representing the time travelled between the source and dest nodes"""
        return self.time
    
    def get_trans_type(self):
        """ Getter method for WeightedEdge
            returns: int representing the time travelled between the source and dest nodes"""
        return self.transportation_type
    def __str__(self):
        """ to string method
            returns: string with the format 'src -> dest total_time color' """
            # I convert all of these to strings
        source_name = str((self.get_source()).get_address())
        dest_name = str((self.get_destination()).get_address())
        time = str(self.get_time())
        trans_type = str(self.get_trans_type())
        return source_name + ' -> ' + dest_name + ' ' + time + ' ' + trans_type
    

class Digraph(object):
    """Represents a directed graph of Node and WeightedEdge objects"""
    def __init__(self):
        self.nodes = set([])
        self.edges = {}  # must be a dictionary of Node -> list of edges starting at that node

    def __str__(self):
        edge_strs = []
        for edges in self.edges.values():
            for edge in edges:
                edge_strs.append(str(edge))
        edge_strs = sorted(edge_strs)  # sort alphabetically
        return '\n'.join(edge_strs)  # concat edge_strs with "\n"s between them
    
    def get_nodes(self):
        return self.nodes

    def get_edges_for_node(self, node):
        ''' param: node object
            return: a copy of the list of all of the edges for given node.
                    empty list if the node is not in the graph
        '''
        if node in self.edges:
            return (self.edges[node]).copy()
        else:
            return []
        #TODO
    def get_edge_between_two_nodes(self,start,end):
        edges = self.get_edges_for_node(start)
        for edge in edges:
            if edge.get_destination() == end:
                return edge

    def has_node(self, node):
        ''' param: node object
            return: True, if node is in the graph. False, otherwise.
        '''
        if node in self.nodes:
            return True
        else:
            return False
         

    def add_node(self, node):
        """ param: node object
            Adds a Node object to the Digraph.
            Raises a ValueError if it is already in the graph."""
        
        if node in self.nodes or node in self.edges:
            raise ValueError('This node is already in the graph')
        else:
            self.nodes.add(node)
            self.edges[node] = []
     #TODO

    def add_edge(self, edge):
        """ param: node object
            Adds an WeightedEdge instance to the Digraph.
            Raises a ValueError if either of the nodes associated with the edge is not in the graph."""
            
        edge_start = edge.get_source()
        edge_end = edge.get_destination()
        if edge_start not in self.nodes:
            raise ValueError('The source node is not in the graph')
        elif edge_end not in self.nodes:
            raise ValueError('The destination node is not in the graph')
        else:
            self.edges[edge_start].append(edge)
