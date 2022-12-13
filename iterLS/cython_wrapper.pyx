import cython
cimport cython

cdef extern from "node.h":

    # setters for global variables
    void set_dimensions(int dims)
    void set_n_points(int n)
    void set_n_labelled(int n)

    ctypedef struct Node:
        pass

    # node methods
    void free_ll(Node* head, int lent)
    void free_out(int* labs, int* ords, double* dists)
    Node* init_node(int ind, int lab, double dist)
    Node* insert(Node* head, Node* to_insert)
    Node* remove_node(Node* to_remove)

    int* extract_labels(Node* output, int lent, int first_index)
    int* extract_ordering(Node* output, int lent, int first_index)
    double* extract_distances(Node* output, int lent, int first_index)
    
    # main functinos
    Node* spread_labels(int labelled_inds[], int unlabelled_inds[], 
                        int labels[], double* points)


def ils_spread(int[:] labelled, int[:] unlabelled_inds, double[:] points, int[:] labels, int dimensions, int n_points, int n_labelled):

    first_index = labelled[0];
    
    # set global variables in c files
    set_dimensions(dimensions)
    set_n_points(n_points)
    set_n_labelled(n_labelled)
    
    node_out = spread_labels(&labelled[0], &unlabelled_inds[0], &labels[0], &points[0])
    
    # extract ordering, indices and distances from node structures
    labs = extract_labels(node_out, n_points, first_index)
    ords = extract_ordering(node_out, n_points, first_index)
    dists = extract_distances(node_out, n_points, first_index)
    
    # convert ctypes to python data types
    lab = [labs[i] for i in range(n_labelled, n_points)] 
    ord_ = [ords[i] for i in range(n_labelled, n_points) if dists[i] != -1]
    dist = [dists[i] for i in range(n_labelled, n_points) if dists[i] != -1]
    
    # free memory from node structure
    free_ll(node_out, n_points)
    free_out(labs, ords, dists)

    return lab, ord_, dist
