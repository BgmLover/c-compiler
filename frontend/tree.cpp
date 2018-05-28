#include "tree.h"

TreeNode root;

TreeNode::TreeNode(string name)
{
    
    this->name=name;

}

TreeNode::TreeNode(string name,int num,...)
{
    va_list valist;
    //创建节点
    
    this->name=name;
    //TreeNode->row=0;
    //TreeNode->col=0;
    //连接子树
    va_start(valist,num);
    if(num>0){
        temp=va_arg(valist,TreeNode*);
        this->first_child=temp;
        this->content="";
        if(num>1){
            while(--num){
                temp2=va_arg(valist,TreeNode*);
                temp->next_sibling=temp2;
                temp=temp2;
            }
        }
    }

}


