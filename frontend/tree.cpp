#include "tree.h"


TreeNode::TreeNode(string name):name(name),row(yyrow),col(yycol){}

TreeNode::TreeNode(string name, string content):TreeNode(name){
    this->content = content;
}

TreeNode::TreeNode(string name,int num,...){
    va_list valist;
    //创建节点
    
    this->name=name;
    //TreeNode->row=0;
    //TreeNode->col=0;
    //连接子树
    va_start(valist,num);
    if(num>0){
        TreeNode *temp=va_arg(valist,TreeNode*);
        this->first_child=temp;
        this->content="";
        if(num>1){
            while(--num){
                TreeNode *temp2=va_arg(valist,TreeNode*);
                temp->next_sibling=temp2;
                temp=temp2;
            }
        }
    }
}

void TreeNode::write_json(string path){
    ofstream outfile;
    outfile.open (path);
    traverse(this, outfile);
    outfile.close();

}


void TreeNode::traverse(TreeNode *node, ofstream &outfile){
    outfile << "{";
    outfile << "\"name\":\"" << node->name << "\",";
    outfile << "\"content\":\"" << node->content << "\",";
    outfile << "\"row\":" << to_string(node->row) << ",";
    outfile << "\"col\":" << to_string(node->col) << ",";
    outfile << "\"children\":[";
    if(node->first_child){
        traverse(node->first_child, outfile);
    }
    outfile << "]";
    if(node->next_sibling){
        outfile << ",";
        traverse(node->next_sibling, outfile);
    }
    outfile << "";
}

