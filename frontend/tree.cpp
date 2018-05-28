#include "tree.h"

TreeNode root;

TreeNode::TreeNode(string name)
:name(name),row(0),col(0),content(NULL),first_child(NULL),next_sibling(NULL){}

TreeNode::TreeNode(string name,int num,TreeNode*t1, ...)
{
    va_list valist;
    //创建节点
    TreeNode* head = new TreeNode();
    TreeNode->name=name;
    //TreeNode->row=0;
    //TreeNode->col=0;
    //连接子树
    va_start(valist,num);
    if(num>0){
        temp=va_arg(valist,TreeNode*)；
        head->first_child=temp;
        if(num==1){
            head->content=temp->content;
        }
        else head->content="";
    }
    else{
        while(num--){

        }
    }
}


