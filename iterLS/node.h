#pragma once

extern int DIMENSIONS;
extern int N_POINTS;
extern int N_LABELLED;

// setter/getter functions for globals

void set_dimensions(int dims);

void set_n_points(int n);

void set_n_labelled(int n);

typedef struct Node {
    int index;
    int label;
    double dist;
    struct Node* next;
    struct Node* prev;
} Node;

// not used in the python wrapper
Node* init_node(int ind, int lab, double dist);

Node* insert(Node* head, Node* to_insert);

Node* remove_node(Node* to_remove);

// used in python wrapper
void free_ll(Node* head, int lent);

void free_out(int* labs, int* ords, double* dists);

int* extract_labels(Node* output, int lent, int first_index);

int* extract_ordering(Node* output, int lent, int first_index);

double* extract_distances(Node* output, int lent, int first_index);

Node* spread_labels(int labelled_inds[], int unlabelled_inds[], int labels[], double* points);
