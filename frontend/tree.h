#ifndef _TREE_H_

#define _TREE_H_

#include <string>

extern char *yytext;
extern int yylineno;

class TreeNode {
public:
    string content;
    string name;
    int row;
    int col;
    TreeNode &first_child;
    TreeNode &next_sibling;
    TreeNode();
    TreeNode(char *name, int row, int col);
    TreeNode(char *name, int row, int col, ...);
    TreeNode(string name,int num,TreeNode*t1, ...);
    void to_json();
}

extern TreeNode root;

#endif
