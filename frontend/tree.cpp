#include "tree.h"

TreeNode root;

TreeNode::TreeNode(char *name, int row, int col)
:name(name),row(row),col(col),content(NULL),first_child(NULL),next_sibling(NULL){}


