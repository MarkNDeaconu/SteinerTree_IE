from src.vertex_example_setups.test_setups import make_grid_graph

from src.steinertree_ie.graph_classes import Vertex_collection

from src.steinertree_ie.steiner_weight import steiner
import time
#-----------setup-----------------
v= Vertex_collection()

make_grid_graph(v,10,10,8)

#-----------------------------------

# print(simplified_problem(4,20, v, v.terminal_indicies))

# print(steiner_count(1, 17, v))

# for i in range(50):
#     print(steiner_count(v.terminal_indicies[0], i+5, v))

start_time = time.time()

print(steiner(v))

end_time = time.time()

elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time} seconds")

v.visualize()


#--------Example that somehow doesnt work-----------------
# make_grid_graph(v,5,5,7)
# print(steiner_count(18, v.terminal_indicies[0], v))