#include <stdio.h>
#include <stdlib.h>
#include "node.h"

// NOTE: This linked list implementation is specific for use in ILS

Node* init_node(int ind, int lab, double dist) {

    Node* new_node = malloc(sizeof(Node));
    new_node->index = ind;
    new_node->dist = dist;
    new_node->label = lab;
    new_node->next = new_node; // circular ll definition
    new_node->prev = new_node;

    return new_node;
}

Node* insert(Node* head, Node* to_insert) {
    // prepending

    Node* prev = head->prev;
    
    to_insert->prev = prev;
    to_insert->next = head;

    head->prev = to_insert;
    prev->next = to_insert;

    return to_insert; // return new head
}

Node* remove_node(Node* to_remove) {
    // next and prev links will be reassigned when add to other list
    Node* prev = to_remove->prev;
    Node* next = to_remove->next;

    to_remove->next = NULL;
    to_remove->prev = NULL;

    if (next == to_remove) {
        return NULL;
    }

    prev->next = next;
    next->prev = prev;

    return next;
}

void free_ll(Node* head, int lent) {
    // free memory
    Node* next;

    for (int i = 0; i < lent; i++) {
        next = head->next;
        free(head);
        head = next;
    }

}

