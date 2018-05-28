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

// TreeNode::void write_json(string path)
// {
//     //遍历整棵树
//     //root
//     Json::jroot;
//     in_order(root, jroot);

//     //输出
//     ofstream os;
//     os.open(path);
//     os << sw.write(jroot);
//     os.close();

// }

// TreeNode::void in_order(TreeNode* head,Json::Value jroot)
// {
//     //Json::Value jroot;
//     jroot["name"] = Json::value(head->name);
//     jroot["content"] = Json::value(head->content);
//     jroot["col"] = Json::value(head->col);
//     jroot["row"] = Json::value(head->row);
//     //subtree
//     Json::Value jsub1,jsub2;

//     root["children"].append(jsub1);
//     root["children"].append(jsub2);

//     if(head->first_child!=NULL){
//         Json::Value jsub1;
//         root["children"].append(jsub1);
//         in_order(head->first_child,jsub1);
//     }
//     if(head->next_sibling!=NULL){
//         Json::Value jsub2;
//         root["children"].append(jsub2);
//         in_order(head->next_sibling,jsub2);
//     }
// }

