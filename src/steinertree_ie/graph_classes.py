from typing import List, Tuple
import networkx as nx
import matplotlib.pyplot as plt
import math
#we assume that vertices will be added like so: start from the top left of the diagram
#if inside the building and down and right are inside then add them as vertices and decide edges.
#repeat.

class Vertex_collection:
    def __init__(self):
        #high level class that keeps a list of each vertex belonging to it
        #allows us to call on vertices by names like v[0] and v[12]. Furthermore,
        #functions can we written as v.find_edge_weight(0,3)

        #all edge relations will be kept by the larger index vertex
        self.vertices = []

        self.terminal_indicies = []
    
    def __getitem__(self, index):
        return self.vertices[index]

    def __len__(self) -> int:
        return len(self.vertices)

    def add(self, neighbor_list = [], terminal = False) -> None:
        # neighbors = [(self.vertices.index(v[0]), v[1]) for v in neighbors_as_Vertex]

        #we add edges based on a list of vertex objects, but we store them as a list of indices
        
        for neighbor in neighbor_list:
            #if there is a single vertex already, we want the next vertex to only be able to have 0 as a neighbor
            if neighbor[0] >= len(self) or neighbor[0] <0:
                raise ValueError("neighbor must be an existing vertex")

            self[neighbor[0]].neighbors.append((len(self),neighbor[1]))
        
        if terminal:
            self.terminal_indicies.append(len(self))

        new_vertex = Vertex(self, neighbor_list)

    
    def remove(self, index):
        #not implemented or really needed
        pass

    def __repr__(self):
        return str(self.vertices)
    
    def visualize(self, layout='auto'):
        """
        Visualize the undirected graph with edge weights.
        Tries to lay out grid-like graphs as grids, and falls back to spring layout otherwise.
        
        layout:
            'auto'     - auto-detect grid structure (if nodes form a square)
            'spring'   - spring layout (force-directed)
            'kamada'   - kamada-kawai layout
            'circular' - circular layout
            'shell'    - shell layout
        """
        G = nx.Graph()

        # Add nodes with color tags
        node_colors = []
        for i in range(len(self)):
            G.add_node(i)
            if i in self.terminal_indicies:
                node_colors.append('red')
            else:
                node_colors.append('skyblue')

        # Add edges
        for i, v in enumerate(self.vertices):
            for neighbor_index, weight in v.neighbors:
                if not G.has_edge(i, neighbor_index):
                    G.add_edge(i, neighbor_index, weight=weight)

        # --- Determine layout ---
        if layout == 'auto':
            n = len(self)
            sqrt_n = int(math.sqrt(n))
            if sqrt_n * sqrt_n == n:
                # Use grid layout (flip y to go top-to-bottom)
                pos = {i: (i % sqrt_n, sqrt_n - 1 - (i // sqrt_n)) for i in range(n)}
            else:
                pos = nx.spring_layout(G)
        elif layout == 'spring':
            pos = nx.spring_layout(G)
        elif layout == 'kamada':
            pos = nx.kamada_kawai_layout(G)
        elif layout == 'circular':
            pos = nx.circular_layout(G)
        elif layout == 'shell':
            pos = nx.shell_layout(G)
        else:
            raise ValueError(f"Unknown layout '{layout}'")

        # Draw graph
        fig, ax = plt.subplots()
        edge_labels = nx.get_edge_attributes(G, 'weight')

        nx.draw(G, pos,
                with_labels=True,
                node_color=node_colors,
                node_size=800,
                font_size=9,
                edgecolors='black',
                ax=ax)

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                    font_color='black', font_size=8, ax=ax)

        ax.set_title("Graph Visualization")
        ax.axis('off')
        fig.tight_layout()
        plt.show()
    
    def visualize_with_steiner_tree(self, layout='auto'):
        """
        Visualize the graph with the Steiner tree overlaid.
        All nodes are points; terminal nodes are red.
        Edge labels scale with number of nodes.
        Steiner tree edges are bold and green.
        """
        G = nx.Graph()

        # Add nodes and edges with weights
        for i in range(len(self)):
            G.add_node(i)
        for i, v in enumerate(self.vertices):
            for neighbor_index, weight in v.neighbors:
                if not G.has_edge(i, neighbor_index):
                    G.add_edge(i, neighbor_index, weight=weight)

        # --- Layout ---
        n = len(self)
        sqrt_n = int(math.sqrt(n))
        if layout == 'auto' and sqrt_n * sqrt_n == n:
            pos = {i: (i % sqrt_n, sqrt_n - 1 - (i // sqrt_n)) for i in range(n)}
        elif layout == 'spring':
            pos = nx.spring_layout(G)
        elif layout == 'kamada':
            pos = nx.kamada_kawai_layout(G)
        elif layout == 'circular':
            pos = nx.circular_layout(G)
        elif layout == 'shell':
            pos = nx.shell_layout(G)
        else:
            pos = nx.spring_layout(G)

        # --- Draw base graph ---
        fig, ax = plt.subplots()
        edge_labels = nx.get_edge_attributes(G, 'weight')

        # Draw all edges
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.5, ax=ax)

        # Draw terminal and non-terminal nodes differently
        terminal_nodes = set(self.terminal_indicies)
        non_terminal_nodes = [i for i in G.nodes if i not in terminal_nodes]

        # Scatter terminal nodes (red)
        x_term, y_term = zip(*[pos[i] for i in terminal_nodes]) if terminal_nodes else ([], [])
        ax.scatter(x_term, y_term, s=20, c='red', zorder=3)

        # Scatter non-terminal nodes (black)
        x_nonterm, y_nonterm = zip(*[pos[i] for i in non_terminal_nodes]) if non_terminal_nodes else ([], [])
        ax.scatter(x_nonterm, y_nonterm, s=10, c='black', zorder=2)

        # Adjust font size for edge weights based on node count
        base_font_size = 12
        scale_factor = max(0.4, min(1.0, 200 / n))
        label_font_size = base_font_size * scale_factor

        nx.draw_networkx_edge_labels(G, pos,
                                    edge_labels=edge_labels,
                                    font_color='black',
                                    font_size=label_font_size,
                                    ax=ax)

        # --- Overlay Steiner tree ---
        from networkx.algorithms.approximation import steiner_tree
        steiner_subgraph = steiner_tree(G, terminal_nodes, weight='weight')

        nx.draw_networkx_edges(steiner_subgraph, pos,
                            edge_color='green',
                            width=2.5,
                            ax=ax)

        ax.set_title("Graph with Steiner Tree Overlay")
        ax.axis('off')
        fig.tight_layout()
        plt.show()




    


class Vertex:
    def __init__(self, owner_set: Vertex_collection, neighbors):
        self.name = len(owner_set)
        owner_set.vertices.append(self)

        #neighbors : List[Tuple[vertex: int, weight:int]]
        self.neighbors = neighbors
    
    def __repr__(self):
        return str(self.name)


# class Branching_walk:
#     def __init__(self, v: Vertex_collection, root: int, avoided_terminals = []):
#         self.v = v
#         self.root = root
#         self.vertex_directory = [None for vertex in v.vertices]
#         self.avoided_terminals = avoided_terminals
#         if root in v.terminal_indicies:
#             self.visited_terminals = [root]
#         else:
#             self.visited_terminals = []

#         self.weight = 0

#         self.add_edge(self.root, True)
    
#     def add_edge(self, new_vertex: int, new_root = False):
#         if new_vertex in self.avoided_terminals:
#             print('cannot add a avoided terminal')
#             return 

#         else:
#             if not(new_root):
#                 self.weight += self.vertex_directory[new_vertex]

#             for (vertex, weight) in self.v[new_vertex].neighbors:
#                 old_weight = self.vertex_directory[vertex]
#                 if (old_weight == None or old_weight > weight) and not(vertex in self.avoided_terminals):
#                     self.vertex_directory[vertex] = weight
            
#             self.vertex_directory[new_vertex] = 0

#             #I'll let this slide for convenience, but my typing doesnt like me changing None to an int

#             if new_vertex in self.v.terminal_indicies:
#                 self.visited_terminals.append(new_vertex)
    

#     def available_edges(self):
#         return([index for index, vertex in enumerate(self.vertex_directory) if vertex!=None and vertex!= 0] )

# example usage
#---------------------
'''
v= Vertex_collection()

v.add()

v.add([(0, 2)])

v.add([(0,5)], True)

print('all vertices: '+ str(v))
print('neighbors of 1 :' + str(v[1].neighbors))

print('the terminal vertices: ' + str(v.terminal_indicies))

'''

# b = Branching_walk(v, 1, [2])

# print('branching walk representation with root node at 1 with 2 a forbidden terminal: ' + str(b.vertex_directory))

# print('available next edges: '+ str(b.available_edges()))

# b.add_edge(0)

# print('branching walk after adding edge to 0: ' + str(b.vertex_directory))

# print('available vertices: ' + str(b.available_edges()))

# print('total_weight ' + str(b.weight))