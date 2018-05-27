#ifndef _TREE_H_

#define _TREE_H_

extern char *yytext;
extern int yylineno;

struct treeNodeStruct {
    char content;
    char name;
    int row;
    int col;
    struct treeNode *first_child;
    struct treeNode *next_sibling;
};

typedef struct treeNodeStruct treeNode;

extern treeNode *root;

treeNode *create_tree(char *name, int row, int col);

// void eval(struct treeNode *head, int leavel);
// char *my_substring(char *s, int begin, int end);
// void freeGramTree(treeNode *node);

#endif
