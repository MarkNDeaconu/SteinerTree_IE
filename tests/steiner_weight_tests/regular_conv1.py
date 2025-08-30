from vertex_example_setups.test_setups import make_grid_graph

from steinertree_ie.graph_classes import Vertex_collection
from steinertree_ie.steiner_weight import steiner
import time
#-----------setup-----------------
v= Vertex_collection()

make_grid_graph(v,5,5,4)

start_time = time.time()

print(steiner(v))

end_time = time.time()

elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time} seconds")

v.visualize()


#--------Example that is 1 off I believe-----------------
# make_grid_graph(v,5,5,7)
# print(steiner_count(18, v.terminal_indicies[0], v))