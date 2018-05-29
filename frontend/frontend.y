%{
#include<stdlib.h>
#include<stdio.h>
#include<string>
#include"tree.h"

extern char* yytext;
extern int column;
extern FILE* yyin;
extern FILE* yyout;
extern int yylineno;

int yylex(void);
TreeNode *root;
void yyerror(const char*s);

%}


%union{
  TreeNode* node;
}

%token <node> IDENTIFIER CONSTANT STRING_LITERAL SIZEOF CONSTANT_INT CONSTANT_DOUBLE
%token <node> PTR_OP INC_OP DEC_OP LEFT_OP RIGHT_OP LE_OP GE_OP EQ_OP NE_OP
%token <node> AND_OP OR_OP MUL_ASSIGN DIV_ASSIGN MOD_ASSIGN ADD_ASSIGN
%token <node> SUB_ASSIGN LEFT_ASSIGN RIGHT_ASSIGN AND_ASSIGN
%token <node> XOR_ASSIGN OR_ASSIGN TYPE_NAME
%token <node> CHAR INT DOUBLE VOID BOOL 
%token <node> CASE IF ELSE SWITCH WHILE DO FOR GOTO CONTINUE BREAK RETURN
%token <node> TRUE FALSE
%token <node> ';' ',' ':' '=' '[' ']' '.' '&' '!' '~' '-' '+' '*' '/' '%' '<' '>' '^' '|' '?' '{' '}' '(' ')'

%type <node> additive_expression and_expression argument_expression_list assignment_expression assignment_operator 
%type <node> block_item block_item_list
%type <node> c_program compound_statement 
%type <node> declaration declaration_list declaration_specifiers declarator 
%type <node> equality_expression exclusive_or_expression expression expression_statement external_declaration
%type <node> function_definition 
%type <node> identifier_list inclusive_or_expression init_declarator init_declarator_list initializer initializer_list iteration_statement
%type <node> jump_statement
%type <node> labeled_statement logical_and_expression logical_or_expression
%type <node> multiplicative_expression
%type <node> parameter_declaration parameter_list postfix_expression primary_expression 
%type <node> relational_expression 
%type <node> selection_statement shift_expression statement 
%type <node> translation_unit type_specifier
%type <node> unary_expression unary_operator 

%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%start c_program


%%

c_program: 
    translation_unit{
        root = new TreeNode("c_program",1,$1);
    };
translation_unit:
    external_declaration{
        $$=new TreeNode("translation_unit",1,$1);
    }
    | translation_unit external_declaration{
        $$=new TreeNode("translation_unit",2,$1,$2);
    };
external_declaration:
    function_definition{
        $$=new TreeNode("external_declaration",1,$1);
    }
    | declaration{
        $$=new TreeNode("external_declaration",1,$1);
    };
function_definition:
    declaration_specifiers declarator declaration_list compound_statement{//声明符
        $$=new TreeNode("function_definition",4,$1,$2,$3,$4);
    }
    | declaration_specifiers declarator compound_statement{
        $$=new TreeNode("function_definition",3,$1,$2,$3);
    };

declaration_specifiers:			
    type_specifier{//省略存储类型声明符等，这里只保留类型声明
        $$=new TreeNode("declaration_specifiers",1,$1);
    };

type_specifier:
      VOID{
      $$=new TreeNode("type_specifier",1,$1);
      }
    | CHAR{
      $$=new TreeNode("type_specifier",1,$1);
      }
    | INT{
      $$=new TreeNode("type_specifier",1,$1);
      }
    | DOUBLE{
      $$=new TreeNode("type_specifier",1,$1);
      };

declarator:
      IDENTIFIER{
      $$=new TreeNode("declarator",1,$1);
    }
    | declarator '[' assignment_expression ']'{//数组
      $$=new TreeNode("declarator",4,$1,$2,$3,$4);
    }
    | declarator '[' ']'{//数组
      $$=new TreeNode("declarator",3,$1,$2,$3);
    }
    | declarator '(' parameter_list ')'{//带参函数
      $$=new TreeNode("declarator",4,$1,$2,$3,$4);    
    }
    | declarator '(' identifier_list ')'{
      $$=new TreeNode("declarator",4,$1,$2,$3,$4);      
    }
    | declarator '(' ')'{//无参函数
      $$=new TreeNode("declarator",3,$1,$2,$3);    
    };

declaration_list:
      declaration{
      $$=new TreeNode("declaration_list",1,$1);      
    }
    | declaration_list declaration{
      $$=new TreeNode("declaration_list",2,$1,$2);            
    };

parameter_list:
      parameter_declaration{
      $$=new TreeNode("parameter_list",1,$1);      
    }
    | parameter_list ',' parameter_declaration{
      $$=new TreeNode("parameter_list",3,$1,$2,$3);    
    };

parameter_declaration:
      type_specifier declarator{
      $$=new TreeNode("parameter_declaration",2,$1,$2);            
    }
    | type_specifier{//只有类型符的参数
      $$=new TreeNode("parameter_declaration",1,$1);          
    };

identifier_list:
      IDENTIFIER{
      $$=new TreeNode("identifier_list",1,$1);      
    }
    | identifier_list ',' IDENTIFIER{
      $$=new TreeNode("identifier_list",3,$1,$2,$3);    
    };

statement:
      compound_statement{//复合语句
      $$=new TreeNode("statement",1,$1);          
    }
    | labeled_statement{
      $$=new TreeNode("statement",1,$1);          
    }
    | expression_statement{
      $$=new TreeNode("statement",1,$1);          
    }
    | selection_statement{
      $$=new TreeNode("statement",1,$1);          
    }
    | iteration_statement{
      $$=new TreeNode("statement",1,$1);          
    }
    | jump_statement{
      $$=new TreeNode("statement",1,$1);          
    };

compound_statement:
     '{' '}'{
      $$=new TreeNode("compound_statement",2,$1,$2);            
    }
    | '{' block_item_list '}'{
      $$=new TreeNode("compound_statement",3,$1,$2,$3);    
    };

block_item_list:
      block_item{
      $$=new TreeNode("block_item_list",1,$1);          
    }
    | block_item_list block_item{
      $$=new TreeNode("block_item_list",2,$1,$2);            
    };

block_item:
      declaration{
      $$=new TreeNode("block_item",1,$1);          
    }
    | statement{
      $$=new TreeNode("block_item",1,$1);          
    };

labeled_statement:
      IDENTIFIER ':' statement{
      $$=new TreeNode("labeled_statement",3,$1,$2,$3);    
    }
    | CASE logical_or_expression ':' statement{
      $$=new TreeNode("labeled_statement",4,$1,$2,$3,$4);    
    };

expression_statement:
      ';'{
      $$=new TreeNode("expression_statement",1,$1);          
    }
    | expression ';'{
      $$=new TreeNode("expression_statement",2,$1,$2);            
    };

selection_statement:
      IF '(' expression ')' statement ELSE statement{
      $$=new TreeNode("selection_statement",7,$1,$2,$3,$4,$5,$6,$7);    
    }
    | IF '(' expression ')' statement %prec LOWER_THAN_ELSE{//这条语句的优先级更低
      $$=new TreeNode("selection_statement",5,$1,$2,$3,$4,$5);    
    }
    | SWITCH '(' expression ')' statement{
      $$=new TreeNode("selection_statement",5,$1,$2,$3,$4,$5);    
    };

iteration_statement:
      WHILE '(' expression ')' statement{
      $$=new TreeNode("iteration_statement",5,$1,$2,$3,$4,$5);            
    }
    | DO statement WHILE '(' expression ')' ';'{
      $$=new TreeNode("iteration_statement",7,$1,$2,$3,$4,$5,$6,$7);    
    }
    | FOR '(' expression_statement expression_statement ')' statement{
      $$=new TreeNode("iteration_statement",6,$1,$2,$3,$4,$5,$6);    
    }
    | FOR '(' expression_statement expression_statement expression ')' statement{
      $$=new TreeNode("iteration_statement",7,$1,$2,$3,$4,$5,$6,$7);    
    };

jump_statement:
      GOTO IDENTIFIER ';'{
      $$=new TreeNode("jump_statement",3,$1,$2,$3);    
    }
    | CONTINUE ';'{
      $$=new TreeNode("jump_statement",2,$1,$2);    
    }
    | BREAK ';'{
      $$=new TreeNode("jump_statement",2,$1,$2);    
    }
    | RETURN ';'{
      $$=new TreeNode("jump_statement",2,$1,$2);    
    }
    | RETURN expression ';'{
      $$=new TreeNode("jump_statement",3,$1,$2,$3);    
    };

expression:
      assignment_expression{//赋值   
      $$=new TreeNode("expression",1,$1);                
    }
    | expression ',' assignment_expression{
      $$=new TreeNode("expression",3,$1,$2,$3);    
    };

assignment_expression:
      logical_or_expression{//逻辑或表达式
      $$=new TreeNode("assignment_expression",1,$1);                
    }
    | unary_expression assignment_operator assignment_expression{
      $$=new TreeNode("assignment_expression",3,$1,$2,$3);    
    };

logical_or_expression:
      logical_and_expression{//逻辑与
      $$=new TreeNode("logical_or_expression",1,$1);                
    }
    | logical_or_expression OR_OP logical_and_expression{
      $$=new TreeNode("logical_or_expression",3,$1,$2,$3);    
    };

assignment_operator:
      '='{
      $$=new TreeNode("assignment_operator",1,$1);                
    }
    | MUL_ASSIGN{
      $$=new TreeNode("assignment_operator",1,$1);                      
    }
    | DIV_ASSIGN{
      $$=new TreeNode("assignment_operator",1,$1);                      
    }
    | MOD_ASSIGN{
      $$=new TreeNode("assignment_operator",1,$1);                      
    }
    | ADD_ASSIGN{
      $$=new TreeNode("assignment_operator",1,$1);                      
    }
    | SUB_ASSIGN{
      $$=new TreeNode("assignment_operator",1,$1);                      
    }
    | LEFT_ASSIGN{
      $$=new TreeNode("assignment_operator",1,$1);                      
    }
    | RIGHT_ASSIGN{
      $$=new TreeNode("assignment_operator",1,$1);                      
    }
    | AND_ASSIGN{
      $$=new TreeNode("assignment_operator",1,$1);                      
    }
    | XOR_ASSIGN{
      $$=new TreeNode("assignment_operator",1,$1);                      
    }
    | OR_ASSIGN{
      $$=new TreeNode("assignment_operator",1,$1);                      
    };

logical_and_expression:
      inclusive_or_expression{//或 |
      $$=new TreeNode("logical_and_expression",1,$1);                      
    }
    | logical_and_expression AND_OP inclusive_or_expression{
      $$=new TreeNode("logical_and_expression",3,$1,$2,$3);          
    };

inclusive_or_expression:
      exclusive_or_expression{//异或 ^
      $$=new TreeNode("inclusive_or_expression",1,$1);                            
    }
    | inclusive_or_expression '|' exclusive_or_expression{
      $$=new TreeNode("inclusive_or_expression",3,$1,$2,$3);                
    };

exclusive_or_expression:
      and_expression{//与&
      $$=new TreeNode("exclusive_or_expression",1,$1);                            
    }
    | exclusive_or_expression '^' and_expression{
      $$=new TreeNode("exclusive_or_expression",3,$1,$2,$3);                      
    };

and_expression:
      equality_expression{//相等关系表达式
      $$=new TreeNode("and_expression",1,$1);                            
    }
    | and_expression '&' equality_expression{
      $$=new TreeNode("and_expression",3,$1,$2,$3);                            
    };

equality_expression:
      relational_expression{
      $$=new TreeNode("equality_expression",1,$1);                            
    }
    | equality_expression EQ_OP relational_expression{
      $$=new TreeNode("equality_expression",3,$1,$2,$3);                                  
    }
    | equality_expression NE_OP relational_expression{
      $$=new TreeNode("equality_expression",3,$1,$2,$3);                                        
    };

relational_expression:
      shift_expression{
      $$=new TreeNode("relational_expression",1,$1);                                    
      }
    | relational_expression '<' shift_expression{
      $$=new TreeNode("relational_expression",3,$1,$2,$3);                                              
    }
    | relational_expression '>' shift_expression{
      $$=new TreeNode("relational_expression",3,$1,$2,$3);                                                    
    }
    | relational_expression LE_OP shift_expression{
      $$=new TreeNode("relational_expression",3,$1,$2,$3);                                                    
    }
    | relational_expression GE_OP shift_expression{
      $$=new TreeNode("relational_expression",3,$1,$2,$3);                                                    
    };

shift_expression:
      additive_expression{//可加表达式
      $$=new TreeNode("shift_expression",1,$1);                                    
    }
    | shift_expression LEFT_OP additive_expression{
      $$=new TreeNode("shift_expression",3,$1,$2,$3);                                                          
    }
    | shift_expression RIGHT_OP additive_expression{
      $$=new TreeNode("shift_expression",3,$1,$2,$3);                                                          
    };
  
additive_expression:
      multiplicative_expression{
      $$=new TreeNode("additive_expression",1,$1);                                            
      }
    | additive_expression '+' multiplicative_expression{
      $$=new TreeNode("additive_expression",3,$1,$2,$3);                                                          
    }
    | additive_expression '-' multiplicative_expression{
      $$=new TreeNode("additive_expression",3,$1,$2,$3);                                                                
    };

multiplicative_expression:
      unary_expression{//单目运算表达式
      $$=new TreeNode("multiplicative_expression",1,$1);                                            
    }
    | multiplicative_expression '*' unary_expression{
      $$=new TreeNode("multiplicative_expression",3,$1,$2,$3);                                                                
    }
    | multiplicative_expression '/' unary_expression{
      $$=new TreeNode("multiplicative_expression",3,$1,$2,$3);                                                                
    }
    | multiplicative_expression '%' unary_expression{
      $$=new TreeNode("multiplicative_expression",3,$1,$2,$3);                                                                
    };

unary_expression:
      postfix_expression{//后缀表达式
      $$=new TreeNode("unary_expression",1,$1);                                            
    }
    | INC_OP unary_expression{
      $$=new TreeNode("unary_expression",2,$1,$2);         
    }
    | DEC_OP unary_expression{
      $$=new TreeNode("unary_expression",2,$1,$2);    
    }
    | unary_operator unary_expression{
      $$=new TreeNode("unary_expression",2,$1,$2);         
    };

unary_operator:
      '+'{
      $$=new TreeNode("unary_operator",1,$1);                                                    
      }
    | '-'{
      $$=new TreeNode("unary_operator",1,$1);                                                  
    }
    | '~'{
      $$=new TreeNode("unary_operator",1,$1);                                                  
    }
    | '!'{
      $$=new TreeNode("unary_operator",1,$1);                                                  
    };

postfix_expression:
      primary_expression{//基本表达式
      $$=new TreeNode("postfix_expression",1,$1);                                                    
    }
    | postfix_expression '[' expression ']'{
      $$=new TreeNode("postfix_expression",4,$1,$2,$3,$4);                                                                
    }
    | postfix_expression '(' ')'{
      $$=new TreeNode("postfix_expression",3,$1,$2,$3);                                                                    
    }
    | postfix_expression '(' argument_expression_list ')'{
      $$=new TreeNode("postfix_expression",4,$1,$2,$3,$4);                                                                
    }
    | postfix_expression INC_OP{
      $$=new TreeNode("postfix_expression",2,$1,$2);                                                                     
    }
    | postfix_expression DEC_OP{
      $$=new TreeNode("postfix_expression",2,$1,$2);                                                                  
    };

argument_expression_list:
      assignment_expression{
      $$=new TreeNode("argument_expression_list",1,$1);                                                    
      }
    | argument_expression_list ',' assignment_expression{
      $$=new TreeNode("argument_expression_list",3,$1,$2,$3);                                                                          
    };

primary_expression:
      IDENTIFIER{
      $$=new TreeNode("primary_expression",1,$1);                                                           
      }
    | CONSTANT_INT{
      $$=new TreeNode("primary_expression",1,$1);                                                          
    }
    | CONSTANT_DOUBLE{
      $$=new TreeNode("primary_expression",1,$1);                                                          
    }
    | STRING_LITERAL{
      $$=new TreeNode("primary_expression",1,$1);                                                          
    }
    | '(' expression ')'{
      $$=new TreeNode("primary_expression",3,$1,$2,$3);                                                                                
    };

declaration:
      declaration_specifiers ';'{
      $$=new TreeNode("declaration",1,$1);                                                          
      }
    | declaration_specifiers init_declarator_list{
      $$=new TreeNode("declaration",2,$1,$2);                                                                       
    };

init_declarator_list:
      init_declarator{
      $$=new TreeNode("init_declarator_list",1,$1);                                                                  
      }
    | init_declarator_list ',' init_declarator{
      $$=new TreeNode("init_declarator_list",3,$1,$2,$3);                                                                                      
    };

init_declarator:
      declarator{
      $$=new TreeNode("init_declarator",1,$1);                                                                  
      }
    | declarator '=' initializer{
      $$=new TreeNode("init_declarator",3,$1,$2,$3);                                                                                           
    };

initializer:
      assignment_expression{}
    | '{' initializer_list '}' {
      $$=new TreeNode("initializer",3,$1,$2,$3);                                                                                                 
    }
    | '{' initializer_list ',' '}'{
      $$=new TreeNode("initializer",4,$1,$2,$3,$4);                                                                      
    };

initializer_list:
      initializer{
      $$=new TreeNode("initializer_list",1,$1);                                                                  
      }
    | initializer_list ',' initializer{
      $$=new TreeNode("initializer_list",3,$1,$2,$3);                                                                                                      
    };

%%

int main(int argc,char* argv[]){
    yyin = fopen(argv[1],"r");
    yyparse();
    root->write_json("result.json");
    //yyclose(yyin);
    return 0;
}
void yyerror(char const *s)
{
	//fflush(stdout);
  printf("\n line:%d  %s",yylineno,s);
	//printf("\n%*s\n%*s\n", column, "^", column, s);
}
