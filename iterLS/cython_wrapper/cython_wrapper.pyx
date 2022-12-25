import cython
cimport cython

import numpy as np
cimport numpy as np

cdef extern from "../c_functions/node.h":

    # setters for global variables
    void set_dimensions(int dims)
    void set_n_points(int n)
    void set_n_labelled(int n)
    
    # extraction is performed in c so we don't need struct definition
    ctypedef struct Node:
        int index
        int label
        double dist
        Node* next
        Node* prev

    # node methods
    void free_ll(Node* head, int lent)
    Node* init_node(int ind, int lab, double dist)
    Node* insert(Node* head, Node* to_insert)
    Node* remove_node(Node* to_remove)

    # main functinos
    Node* spread_labels(int labelled_inds[], int unlabelled_inds[], 
                        int labels[], double* points)


def ils_spread(int[:] labelled, int[:] unlabelled_inds, double[:] points, 
               int[:] labels, int dimensions, int n_points, int n_labelled):

    first_index = labelled[0];
    
    # set global variables in c files
    set_dimensions(dimensions)
    set_n_points(n_points)
    set_n_labelled(n_labelled)
    
    node_out = spread_labels(&labelled[0], &unlabelled_inds[0], &labels[0], &points[0])

    cdef:
        int[:] labels_memview = np.empty(n_points, dtype = np.intc)
        int[:] ordering_memview = np.empty(n_points, dtype = np.intc)
        double[:] distances_memview = np.empty(n_points, dtype = np.double)
    
    labels, ordering, distances = extract_output(node_out, n_points, first_index, 
                                                 n_labelled, labels_memview, ordering_memview, distances_memview)
    
    lab = [labels[i] for i in range(n_labelled, n_points)] 
    ord_ = [ordering[i] for i in range(n_labelled, n_points) if distances[i] != -1]
    dist = [distances[i] for i in range(n_labelled, n_points) if distances[i] != -1]

    # free memory from node structure
    free_ll(node_out, n_points)

    return lab, ord_, dist

cdef extract_output(Node* output, int lent, int first_index, int n_labelled,
                    int[:] labels, int[:] ordering, double[:] distances):
    # extract outputs in one loop

    cdef:
        Py_ssize_t i
    
    i = 0
    # find start of linked list
    while (output.index != first_index):
        output = output.next
    
    # extract labels of initial point
    # iterate backwards as nodes we inserted at the head
    labels[i] = output.label
    ordering[i] = output.index
    distances[i] = output.dist
    output = output.prev
    i += 1

    while (output.index != first_index):
        labels[i] = output.label
        ordering[i] = output.index
        distances[i] = output.dist
        output = output.prev
        i += 1

    return labels, ordering, distances
