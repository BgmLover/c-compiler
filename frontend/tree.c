#include "tree.h"
#include <stdlib.h> 


treeNode *create_tree(char *name, int row, int col){
  treeNode *new_node = malloc(sizeof(treeNode));
  new_node->name = name;
  new_node->content = NULL;
  new_node->row = row;
  new_node->col = col;
  new_node->first_child = NULL;
  new_node->next_sibling = NULL;
  return new_node;
}
