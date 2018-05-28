#ifndef _TREE_H_

#define _TREE_H_

#include <string>
#include<cstdio>
#include<cstdlib>
#include<cstring>
#include<cstdarg>
#include <iostream>
#include <fstream>
//#include "json/json.h"

extern char *yytext;
extern int column,row;

using namespace std;

class TreeNode {
public:
    string content;
    string name;
    int row;
    int col;
    TreeNode *first_child;
    TreeNode *next_sibling;
    TreeNode()=default;
    TreeNode(string name);
    TreeNode(string name, string content);
    TreeNode(string name, int num, ...);
    //void write_json(string path);
    //void in_order(TreeNode* head,Json::Value jroot);
};



#endif
