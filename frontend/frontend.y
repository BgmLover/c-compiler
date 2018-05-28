%{
#include<stdlib.h>
#include<stdio.h>

extern char* yytext;
extern int column;
extern FILE* yyin;
extern FILE* yyout;
extern int yylineno;

TreeNode *root;
void yyerror(const char*s);
}%



%token <t> IDENTIFIER CONSTANT STRING_LITERAL SIZEOF CONSTANT_INT CONSTANT_DOUBLE
%token<t> PTR_OP INC_OP DEC_OP LEFT_OP RIGHT_OP LE_OP GE_OP EQ_OP NE_OP
%token<t> AND_OP OR_OP MUL_ASSIGN DIV_ASSIGN MOD_ASSIGN ADD_ASSIGN
%token<t> SUB_ASSIGN LEFT_ASSIGN RIGHT_ASSIGN AND_ASSIGN
%token<t> XOR_ASSIGN OR_ASSIGN TYPE_NAME
%token<t> CHAR INT DOUBLE VOID BOOL 
%token<t> CASE IF ELSE SWITCH WHILE DO FOR GOTO CONTINUE BREAK RETURN
%token<t> TRUE FALSE
%token<t> ';' ',' ':' '=' '[' ']' '.' '&' '!' '~' '-' '+' '*' '/' '%' '<' '>' '^' '|' '?' '{' '}' '(' ')'

%start c_program

%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%union{
    struct TreeNode *t;
}
%%

c_program
    :translation_unit{
        
    };
translation_unit
    : external_declaration{

    }
    | translation_unit external_declaration{

    };
external_declaration
    : function_definition{

    }
    | declaration{

    };
function_definition
    : declaration_specifiers declarator declaration_list compound_statement{
        //声明符
    }
    | declaration_specifiers declarator compound_statement{
    };

declaration_specifiers				
    : type_specifier{
        //省略存储类型声明符等，这里只保留类型声明
    };

type_specifier
    : VOID{}
    | CHAR{}
    | INT{}
    | DOUBLE{}
    | BOOL{};

declarator
    : IDENTIFIER{}
    | declarator '[' assignment_expression ']'{//数组
    }
    | declarator '[' ']'{//数组
    }
    | '(' declarator ')'{//?
    }
    | declarator '(' parameter_list ')'{//带参函数
    }
    | declarator '(' identifier_list ')'{
    }
    | declarator '(' ')'{//无参函数
    };

declaration_list
    : declaration{
    }
    | declaration_list declaration{
    };

parameter_list
    : parameter_declaration{

    }
    | parameter_list ',' parameter_declaration{

    };

parameter_declaration
    : type_specifier declarator{

    }
    | type_specifier{//只有类型符的参数
    };

identifier_list
    : IDENTIFIER{

    }
    | identifier_list ',' IDENTIFIER{

    };

statement:
    : compound_statement{//复合语句
    }
    | labeled_statement{

    }
    | expression_statement{

    }
    | selection_statement{

    }
    | iteration_statement{

    }
    | jump_statement{

    };

compound_statement
    : '{' '}'{

    }
    | '{' block_item_list '}'{

    };

block_item_list
    : block_item{

    }
    | block_item_list block_item{

    };

block_item
    : declaration{

    }
    | statement{

    };

labeled_statement
    : IDENTIFIER ':' statement{

    }
    | CASE logical_or_expression ':' statement{

    };

expression_statement
    : ';'{

    }
    | expression ';'{

    };

selection_statement 
    : IF '(' expression ')' statement ELSE statement{

    }
    | IF '(' expression ')' statement %prec LOWER_THAN_ELSE{//这条语句的优先级更低

    }
    | SWITCH '(' expression ')' statement{

    };

iteration_statement
    : WHILE '(' expression ')' statement{

    }
    | DO statement WHILE '(' expression ')' ';'{

    }
    | FOR '(' expression_statement expression_statement ')' statement{

    }
    | FOR '(' expression_statement expression_statement expression ')' statement{

    };

jump_statement
    : GOTO IDENTIFIER ';'{

    }
    | CONTINUE ';'{

    }
    | BREAK ';'{

    }
    | RETURN ';'{

    }
    | RETURN expression ';'{

    };

expression
    : assignment_expression{//赋值   
    }
    | expression ',' assignment_expression{

    };

assignment_expression
    : logical_or_expression{//逻辑或表达式

    }
    | unary_expression assignment_operator assignment_expression{

    };
logical_or_expression
    : logical_and_expression{//逻辑与

    }
    | logical_or_expression OR_OP logical_and_expression{

    };

assignment_operator
    : '='{

    }
    | MUL_ASSIGN{}
    | DIV_ASSIGN{}
    | MOD_ASSIGN{}
    | ADD_ASSIGN{}
    | SUB_ASSIGN{}
    | LEFT_ASSIGN{}
    | RIGHT_ASSIGN{}
    | AND_ASSIGN{}
    | XOR_ASSIGN{}
    | OR_ASSIGN{};

logical_and_expression
    : inclusive_or_expression{//或 |

    }
    | logical_and_expression AND_OP inclusive_or_expression{};

inclusive_or_expression
    : exclusive_or_expression{//异或 ^
      
    }
    | inclusive_or_expression '|' exclusive_or_expression{};

exclusive_or_expression
    : and_expression{//与&

    }
    | exclusive_or_expression '^' and_expression{};

and_expression
    : equality_expression{//相等关系表达式

    }
    | and_expression '&' equality_expression{};

equality_expression
    : relational_expression{

    }
    | equality_expression EQ_OP relational_expression{}
    | equality_expression NE_OP relational_expression{};

relational_expression
    : shift_expression{}
    | relational_expression '<' shift_expression{}
    | relational_expression '>' shift_expression{}
    | relational_expression LE_OP shift_expression{}
    | relational_expression GE_OP shift_expression{};

shift_expression
    : additive_expression{//可加表达式

    }
    | shift_expression LEFT_OP additive_expression{}
    | shift_expression RIGHT_OP additive_expression{};
  
additive_expression
    : multiplicative_expression
    | additive_expression '+' multiplicative_expression
    | additive_expression '-' multiplicative_expression{};

multiplicative_expression
    : unary_expression{//单目运算表达式

    }
    | multiplicative_expression '*' unary_expression{}
    | multiplicative_expression '/' unary_expression{}
    | multiplicative_expression '%' unary_expression{};

unary_expression
    : postfix_expression{//后缀表达式

    }
    | INC_OP unary_expression{}
    | DEC_OP unary_expression{}
    | unary_operator unary_expression{};

unary_operator
    : '+'{}
    | '-'{}
    | '~'{}
    | '!'{};

postfix_expression
    : primary_expression{//基本表达式

    }
    | postfix_expression '[' expression ']'{}
    | postfix_expression '(' ')'{}
    | postfix_expression '(' argument_expression_list ')'
    | postfix_expression INC_OP{}
    | postfix_expression DEC_OP{};

argument_expression_list
    : assignment_expression{}
    | argument_expression_list ',' assignment_expression{};

primary_expression
    : IDENTIFIER{}
    | CONSTANT_INT{}
    | CONSTANT_DOUBLE{}
    | STRING_LITERAL{}
    | '(' expression ')'{};

declaration 
    : declaration_specifiers ';'{}
    | declaration_specifiers init_declarator_list{};

init_declarator_list
    : init_declarator{}
    | init_declarator_list ',' init_declarator{};

init_declarator
    : declarator{}
    | declarator '=' initializer{};

initializer
    : assignment_expression{}
    | '{' initializer_list '}' {}
    | '{' initializer_list ',' '}'{};

init_declarator_list
    : initializer{}
    | initializer_list ',' initializer{}
