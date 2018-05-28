#ifndef _TREE_H_

#define _TREE_H_

#include <string>

extern char *yytext;
extern int yylineno;

using namespace std;

class TreeNode {
public:
    string content;
    string name;
    int row;
    int col;
    TreeNode *first_child;
    TreeNode *next_sibling;
    TreeNode(string name);
    TreeNode(string name, string content);
    TreeNode(string name, int num, ...);
    void write_json(string path);
}

extern TreeNode *root;

#endif
