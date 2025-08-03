from src.steinertree_ie.graph_classes import Vertex_collection

import random


def make_grid_graph(v: Vertex_collection, rows=10, cols=10, num_terminals=10, the_seed = 0):
    random.seed(the_seed)
    index_map = {}  # Maps (row, col) → vertex index
    total_nodes = rows * cols
    terminal_indices = set(random.sample(range(total_nodes), num_terminals))

    v.terminal_indicies = list(terminal_indices)
    for row in range(rows):
        for col in range(cols):
            neighbors = []

            current_index = row * cols + col
            # Add neighbor above
            if row > 0:
                neighbor_index = (row - 1) * cols + col
                neighbors.append((neighbor_index, random.randint(1,5)))
            # Add neighbor to the left
            if col > 0:
                neighbor_index = row * cols + (col - 1)
                neighbors.append((neighbor_index, random.randint(1,5)))

            # Determine if this vertex is a terminal
            is_terminal = current_index in terminal_indices
            v.add(neighbors, terminal=is_terminal)