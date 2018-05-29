#include "tree.h"


TreeNode::TreeNode(string name)
{
    
    this->name=name;
    this->col=column;
    this->row=row;
    //分配
    if(this->name=="CONSTANT_INT"){//整型
        int value;
        if(strlen(yytext) > 1 && yytext[0] == '0' && yytext[1] != 'x') {
            sscanf(yytext,"%o",&value); //8进制整数
        }
        else if(strlen(yytext) > 1 && yytext[1] == 'x'){
            sscanf(yytext,"%x",&value); //16进制整数
        }
        else value = atoi(yytext);      //10进制整数
        this->content = to_string(value);   
    }
    else if(this->name == "CONSTANT_DOUBLE") {//浮点数
        this->content = yytext;
    }
    else if(this->name == "TRUE") {//bool
        this->content = to_string(1);
    }
    else if(this->name == "FALSE") {
        this->content = to_string(0);
    }
    else if(this->name == "STRING_LITERAL") {//string
        this->content = yytext;
    }
    else {
        this->content = yytext;
    }
}

TreeNode::TreeNode(string name, string content)
{
    this->name=name;
    this->content=content;
    this->col=column;
    this->row=row;
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
    outfile << "\"content\:\"" << node->content << "\",";
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
}

