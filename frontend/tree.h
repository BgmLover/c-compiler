#ifndef _TREE_H_

#define _TREE_H_

extern char *yytext;
extern int yylineno;

class treeNode {
public:
    char content;
    char name;
    int row;
    int col;
    treeNode &first_child;
    treeNode &next_sibling;
    treeNode();
    treeNode(char *name, int row, int col);
    treeNode(char *name, int row, int col, ...);
    toJson();
}

extern treeNode root;

#endif
