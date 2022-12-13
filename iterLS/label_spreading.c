#include <stdio.h>
#include <stdlib.h>
#include "node.h"

// global variables
int DIMENSIONS;
int N_POINTS;
int N_LABELLED;

void set_n_labelled(int num) {
    N_LABELLED = num;
}

int get_n_labelled() {
    return N_LABELLED;
}

void set_dimensions(int dims) {
    DIMENSIONS = dims;
}

int get_dimensions() {
    return N_POINTS;
}

void set_n_points(int n) {
    N_POINTS = n;
}

int get_n_points() {
    return N_POINTS;
}

// label_spreading functions

double euclidean_sq(double* p1, double* p2) {

    double temp;
    double sum = 0;

    for (int i = DIMENSIONS-1; i; i--) {
        temp = p1[i] - p2[i];
        sum += temp * temp;
    }
    return sum;
}

void update_dists(Node* dists, Node* m_recent, double* points) {
    int first_ind = dists->index;
    int new_ind = m_recent->index;
    double t_dist = euclidean_sq(&points[new_ind * DIMENSIONS],
            &points[dists->index * DIMENSIONS]);
    if (t_dist < dists->dist) {
        dists->dist = t_dist;
        dists->label = m_recent->label;
    }

    dists = dists->next;

    while (first_ind != dists->index) {
        t_dist = euclidean_sq(&points[new_ind * DIMENSIONS], &points[dists->index * DIMENSIONS]);
        if (t_dist < dists->dist) {
            dists->dist = t_dist;
            dists->label = m_recent->label;
        }
        dists = dists->next;
    }
}

Node* find_closest(Node* dists, Node* labelled, double* points) {
    
    int first_ind = dists->index;
    double t_min = dists->dist;
    Node* t_node = dists;

    dists = dists->next;
    while (dists->index != first_ind) {
        if (dists->dist < t_min) {
            t_min = dists->dist;
            t_node = dists;
        }
        dists = dists->next;
    }

    return t_node;
}

Node* spread_labels(int labelled_inds[], 
        int unlabelled_inds[], int labels[], double* points) {
    
    Node* labelled_head = init_node(labelled_inds[0], labels[0], -1.0);
    printf("%d", labelled_head->label);
    printf("%d \n", labels[0]);
    Node* new_node;
    printf("initialising label_nodes");
    for (int i = 1; i < N_LABELLED; i++) {
        new_node = init_node(labelled_inds[i], labels[i], -1.0);
        labelled_head = insert(labelled_head, new_node);
        printf("%d", labelled_head->label);
        printf("%d \n", labels[i]);
    }
    printf("\n \n");
    
    double t_distance = euclidean_sq(
            &points[labelled_head->index * DIMENSIONS], &points[unlabelled_inds[0] * DIMENSIONS]);

    Node* dists = init_node(unlabelled_inds[0], labelled_head->label, t_distance);
    int first_index = labelled_head->index;

    for (int i = 1; i < N_POINTS - N_LABELLED; i++) {
        t_distance = euclidean_sq(
                &points[labelled_head->index * DIMENSIONS], &points[unlabelled_inds[i] * DIMENSIONS]);
        new_node = init_node(unlabelled_inds[i], labelled_head->label, t_distance);
        dists = insert(dists, new_node);
    }
    labelled_head = labelled_head->next;
    while (labelled_head->index != first_index) {
        update_dists(dists, labelled_head, points);
        printf("init_dists: %d", labelled_head->label);
        labelled_head = labelled_head->next;
    }
    Node* closest;
    for (int i = 0; i < N_POINTS - N_LABELLED-1; i++) {
        closest = find_closest(dists, labelled_head, points);
        dists = remove_node(closest);
        labelled_head = insert(labelled_head, closest);
        update_dists(dists, labelled_head, points);
    }
    closest = find_closest(dists, labelled_head, points);
    dists = remove_node(closest);
    labelled_head = insert(labelled_head, closest);

    return labelled_head;
}

