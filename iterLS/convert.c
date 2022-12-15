#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "node.h"

// extract final results from the linked list structure and return arrays usable in python
// TODO: Consider implementation cython to combine into one loop instead of three
// ALOT OF REPEATED CODE :(

int* extract_labels(Node* output, int lent, int first_index) {
    // assign memory
    int* labels = malloc(sizeof(int) * lent);
    
    // go to start of list
    while (output->index != first_index) {
        output = output->next;
    }

    // perform first iteration
    labels[0] = output->label;
    output = output->prev;
    int i = 1;
    
    // linked list order is reversed as we prepended elements so iterate backwards
    while (output->index != first_index) {
        labels[i] = output->label;
        output = output->prev;
        i++;
    }

    return labels;
}

int* extract_ordering(Node* output, int lent, int first_index) {
    
    int* indices = malloc(sizeof(int) * lent);

    while (output->index != first_index) {
        output = output->next;
    }

    indices[0] = output->index;
    output = output->prev;
    int i = 1;

    while (output->index != first_index) {
        indices[i] = output->index;
        output = output->prev;
        i++;
    }

    return indices;
}

double* extract_distances(Node* output, int lent, int first_index) {
    
    double* dists = malloc(sizeof(double) * lent);

    while (output->index != first_index) {
        output = output->next;
    }

    dists[0] = output->dist;
    output = output->prev;
    int i = 1;

    while (output->index != first_index) {
        dists[i] = output->dist;
        output = output->prev;
        i++;
    }

    return dists;
}

void free_out(int* labs, int* ords, double* dists) {

    free(labs);
    free(ords);
    free(dists);

}
