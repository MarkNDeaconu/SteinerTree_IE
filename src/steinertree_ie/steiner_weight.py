from src.steinertree_ie.simplified import simplified_problem
from src.steinertree_ie.graph_classes import Vertex_collection
from itertools import chain, combinations


import time

def powerset(iterable):
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))   

def steiner_count(weight:int, root:int, v: Vertex_collection):
    #summation from IE here

    IE_count = 0
    for subset_of_terminals in powerset(v.terminal_indicies):
        subset_of_terminals = list(subset_of_terminals)
        parity = len(subset_of_terminals)%2
        IE_count += (-1)**parity * simplified_problem(root, weight, v, subset_of_terminals)
    
    return(IE_count)
    
def clever_search(f, root, v, step = 5):
    # Step 1: Find upper bound where f(x, v) becomes nonzero
    x = 1
    while f(x, root, v) == 0:
        x += step

    # Step 2: Binary search between previous zero and this nonzero
    
    for i in range(step):
        if f(x-step+1+i, root, v) != 0:
            return(x-step+1+i)



def steiner(v: Vertex_collection):
    root = v.terminal_indicies[0]

    # num_solutions = steiner_count(root, weight, v)
    
    return(clever_search(steiner_count, root, v))

