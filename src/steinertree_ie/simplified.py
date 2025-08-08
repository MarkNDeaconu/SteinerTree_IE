
from steinertree_ie.graph_classes import Vertex_collection
from steinertree_ie.convolution_solvers import tree_combination_sum_fft, tree_combination_sum
#The goal of this piece of code is to be able to solve the Simplified problem for one input

#Simplified problem:

#input: root, max_weight, avoided_terminals
#counts all branching walks of max_weight or less, starting at root, avoiding a subset of terminals
#returns: number of branching walks

#FOR NOW THIS ONLY CONSIDERS THE UNIT WEIGHT STEINER TREE


def simplified_problem(root:int, max_weight:int, v: Vertex_collection, avoided_terminals, fft):

    #solution for the simplified problem here. The vertex collection is simply the datastructure we use to encode relations in between vertices
    bf_table = dict()

    #Lets fill the dynamic programming table for elementary values, weight 1 and weight 0 paths. The insight is that this is the only info 
    #you need in order to compute the whole table, and we never need to look at the grid again after this.
    for vert in range(len(v)):
        if vert not in avoided_terminals:
            bf_table[(vert, 0)] = 1


            #here we can gain marginal efficiency boost by precomputing some values 
            '''Unit Steiner'''
            # bf_table[(vert, 1)] = len([neighbor for neighbor in v[vert].neighbors if neighbor[0] not in avoided_terminals and neighbor[1] <= 1])
            
            '''Regular Steiner'''
            adjacent = sorted(v[vert].neighbors, key=lambda x: x[1])
            curr_num_neighbors = 0
            for neighbor in adjacent:
                if neighbor[0] not in avoided_terminals:
                    curr_num_neighbors += 1
                    bf_table[(vert, neighbor[1])] = curr_num_neighbors



    def bf(curr_vert,weight):
        #instead of filling the bf_table row by row, here we encapsulate the table into a function. The function calls the table if the 
        #key is in the table (if we have already computing this value). Otherwise, we use the recursive formula to split the branching tree
        #into a 'double rooted' tree with the root and each of it's neighbors one by one. This is the big summation from the paper.
        try:
            return(bf_table[(curr_vert, weight)])
        except Exception:
            if fft:
                bf_table[(curr_vert,weight)] = sum([tree_combination_sum_fft(curr_vert,neighbor[0], weight-neighbor[1], bf) for neighbor in v[curr_vert].neighbors if neighbor[0] not in avoided_terminals and weight-neighbor[1]>0])
                return(bf_table[(curr_vert,weight)])
            else:
                bf_table[(curr_vert,weight)] = sum([tree_combination_sum(curr_vert,neighbor[0], weight-neighbor[1], bf) for neighbor in v[curr_vert].neighbors if neighbor[0] not in avoided_terminals and weight-neighbor[1]>0])
                return(bf_table[(curr_vert,weight)])


    #computes the 'pyramid' within the table that lets you climb to the desired table entry
    bf(root,max_weight)

    #print the table for debugging reasons
    # print(bf_table)

    return(bf(root, max_weight))

