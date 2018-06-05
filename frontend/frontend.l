D            [0-9]
L            [a-zA-Z_]
H            [a-fA-F0-9]
E            ([Ee][+-]?{D}+)
P                       ([Pp][+-]?{D}+)
FS            (f|F|l|L)
IS                      ((u|U)|(u|U)?(l|L|ll|LL)|(l|L|ll|LL)(u|U))

%{

#include <stdio.h>
#include "y.tab.hpp"
#include "tree.h"
#include<iostream>
using namespace std;
void count_col(void);
void count_row();
extern YYSTYPE yylval;
%}

%%

"/*" { count_col(); 
/*comment(); */
}

"//"[^\n]* { /* consume //-comment */ }

 /*"auto"           { count_col(); return(AUTO); }*/
 /*"_Bool"            { count_col(); return(BOOL); }*/
"break"           {yylval.node = new TreeNode("break"); count_col(); return(BREAK); }

"case"            {yylval.node = new TreeNode("case"); count_col(); return(CASE); }
"char"            {yylval.node = new TreeNode("char"); count_col(); return(CHAR); }
 /*"_Complex"        { count_col(); return(COMPLEX); }*/
 /*"const"           {yylval.node = new TreeNode("const"); count_col(); return(CONST); }*/
"continue"        {yylval.node = new TreeNode("continue"); count_col(); return(CONTINUE); }
 "default"         {yylval.node = new TreeNode("default"); count_col(); return(DEFAULT); }
"do"              {yylval.node = new TreeNode("do"); count_col(); return(DO); }
"double"          {yylval.node = new TreeNode("double"); count_col(); return(DOUBLE); }
"else"            {yylval.node = new TreeNode("else"); count_col(); return(ELSE); }
 /*"enum"            { count_col(); return(ENUM); }*/
 /*"extern"        { count_col(); return(EXTERN); }*/
 /*"float"            { count_col(); return(FLOAT); }*/
"for"             {yylval.node = new TreeNode("for"); count_col(); return(FOR); }
"goto"            {yylval.node = new TreeNode("goto"); count_col(); return(GOTO); }
"if"              {yylval.node = new TreeNode("if"); count_col(); return(IF); }
 /*"_Imaginary"        { count_col(); return(IMAGINARY); }*/
 /*"inline"        { count_col(); return(INLINE); }*/
"int"             {yylval.node = new TreeNode("int"); count_col(); return(INT); }
 /*"long"            { count_col(); return(LONG); }*/
 /*"register"        { count_col(); return(REGISTER); }*/
 /*"restrict"        { count_col(); return(RESTRICT); }*/
"return"          {yylval.node = new TreeNode("return"); count_col(); return(RETURN); }
 /*"short"            { count_col(); return(SHORT); }*/
 /*"signed"        { count_col(); return(SIGNED); }*/
"sizeof"          {yylval.node = new TreeNode("sizeof"); count_col(); return(SIZEOF); }
 /*"static"        { count_col(); return(STATIC); }*/
 /*"struct"        { count_col(); return(STRUCT); }*/
"switch"          {yylval.node = new TreeNode("switch"); count_col(); return(SWITCH); }
 /*"typedef"         {yylval.node = new TreeNode("typedef"); count_col(); return(TYPEDEF); }*/
 /*"union"            { count_col(); return(UNION); }*/
 /*"unsigned"        { count_col(); return(UNSIGNED); }*/
"void"            {yylval.node = new TreeNode("void"); count_col(); return(VOID); }
 /*"volatile"        { count_col(); return(VOLATILE); }*/
"while"           {yylval.node = new TreeNode("while"); count_col(); return(WHILE); }

{L}({L}|{D})*     {yylval.node = new TreeNode("identifier", yytext); count_col(); return(IDENTIFIER); }
0[xX]{H}+        {yylval.node = new TreeNode("constant_int", yytext); count_col(); return(CONSTANT_INT); }
0[0-7]*        {yylval.node = new TreeNode("constant_int", yytext); count_col(); return(CONSTANT_INT); }
[1-9]{D}*        {yylval.node = new TreeNode("constant_int", yytext); count_col(); return(CONSTANT_INT); }
 /*TODO negative constants? */
 /*
0[xX]{H}+{IS}?        { count_col(); return(CONSTANT); }
0[0-7]*{IS}?        { count_col(); return(CONSTANT); }
[1-9]{D}*{IS}?        { count_col(); return(CONSTANT); }
L?'(\\.|[^\\'\n])+'    { count_col(); return(CONSTANT); }

{D}+{E}{FS}?        { count_col(); return(CONSTANT); }
{D}*"."{D}+{E}?{FS}?    { count_col(); return(CONSTANT); }
{D}+"."{D}*{E}?{FS}?    { count_col(); return(CONSTANT); }
0[xX]{H}+{P}{FS}?    { count_col(); return(CONSTANT); }
0[xX]{H}*"."{H}+{P}{FS}?     { count_col(); return(CONSTANT); }
0[xX]{H}+"."{H}*{P}{FS}?     { count_col(); return(CONSTANT); }
 */

 /*TODO string*/
 /*L?\"(\\.|[^\\"\n])*\"    { count_col(); return(STRING_LITERAL); }*/

 /*"..."           {yylval.node = new TreeNode("..."); count_col(); return(ELLIPSIS); }*/
">>="           {yylval.node = new TreeNode(">>="); count_col(); return(RIGHT_ASSIGN); }
"<<="           {yylval.node = new TreeNode("<<="); count_col(); return(LEFT_ASSIGN); }
"+="            {yylval.node = new TreeNode("+="); count_col(); return(ADD_ASSIGN); }
"-="            {yylval.node = new TreeNode("-="); count_col(); return(SUB_ASSIGN); }
"*="            {yylval.node = new TreeNode("*="); count_col(); return(MUL_ASSIGN); }
"/="            {yylval.node = new TreeNode("/="); count_col(); return(DIV_ASSIGN); }
"%="            {yylval.node = new TreeNode("%="); count_col(); return(MOD_ASSIGN); }
"&="            {yylval.node = new TreeNode("&="); count_col(); return(AND_ASSIGN); }
"^="            {yylval.node = new TreeNode("^="); count_col(); return(XOR_ASSIGN); }
"|="            {yylval.node = new TreeNode("|="); count_col(); return(OR_ASSIGN); }
">>"            {yylval.node = new TreeNode(">>"); count_col(); return(RIGHT_OP); }
"<<"            {yylval.node = new TreeNode("<<"); count_col(); return(LEFT_OP); }
"++"            {yylval.node = new TreeNode("++"); count_col(); return(INC_OP); }
"--"            {yylval.node = new TreeNode("--"); count_col(); return(DEC_OP); }
"->"            {yylval.node = new TreeNode("->"); count_col(); return(PTR_OP); }
"&&"            {yylval.node = new TreeNode("&&"); count_col(); return(AND_OP); }
"||"            {yylval.node = new TreeNode("||"); count_col(); return(OR_OP); }
"<="            {yylval.node = new TreeNode("<="); count_col(); return(LE_OP); }
">="            {yylval.node = new TreeNode(">="); count_col(); return(GE_OP); }
"=="            {yylval.node = new TreeNode("=="); count_col(); return(EQ_OP); }
"!="            {yylval.node = new TreeNode("!="); count_col(); return(NE_OP); }
";"             {yylval.node = new TreeNode(";"); count_col(); return(';'); }
("{"|"<%")      {yylval.node = new TreeNode("{"); count_col(); return('{'); }
("}"|"%>")      {yylval.node = new TreeNode("}"); count_col(); return('}'); }
","             {yylval.node = new TreeNode(","); count_col(); return(','); }
":"             {yylval.node = new TreeNode(":"); count_col(); return(':'); }
"="             {yylval.node = new TreeNode("="); count_col(); return('='); }
"("             {yylval.node = new TreeNode("("); count_col(); return('('); }
")"             {yylval.node = new TreeNode(")"); count_col(); return(')'); }
("["|"<:")      {yylval.node = new TreeNode("["); count_col(); return('['); }
("]"|":>")      {yylval.node = new TreeNode("]"); count_col(); return(']'); }
"."             {yylval.node = new TreeNode("."); count_col(); return('.'); }
"&"             {yylval.node = new TreeNode("&"); count_col(); return('&'); }
"!"             {yylval.node = new TreeNode("!"); count_col(); return('!'); }
"~"             {yylval.node = new TreeNode("~"); count_col(); return('~'); }
"-"             {yylval.node = new TreeNode("-"); count_col(); return('-'); }
"+"             {yylval.node = new TreeNode("+"); count_col(); return('+'); }
"*"             {yylval.node = new TreeNode("*"); count_col(); return('*'); }
"/"             {yylval.node = new TreeNode("/"); count_col(); return('/'); }
"%"             {yylval.node = new TreeNode("%"); count_col(); return('%'); }
"<"             {yylval.node = new TreeNode("<"); count_col(); return('<'); }
">"             {yylval.node = new TreeNode(">"); count_col(); return('>'); }
"^"             {yylval.node = new TreeNode("^"); count_col(); return('^'); }
"|"             {yylval.node = new TreeNode("|"); count_col(); return('|'); }
"?"             {yylval.node = new TreeNode("?"); count_col(); return('?'); }

[ \t\v\f]     { count_col();  }
"\n"              { count_row(); }
.               { /* Add code to complain about unmatched characters */ }

%%


int yywrap(void){
  return 1;
}


// void comment(void){
//   char c, prev = 0;

//   while ((c = input()) != 0)      /* (EOF maps to 0) */
//   {
//     if (c == '/' && prev == '*')
//       return;
//     prev = c;
//   }
//   error("unterminated comment");
// }


int yycol = 1;
int yyrow = 1;

void count_col(void){
  int i;

  for (i = 0; yytext[i] != '\0'; i++){
    if(yytext[i] == '\t'){
      yycol += 8 - (yycol % 8);
    }else{
      yycol++;
    }
  }

  ECHO;
}

void count_row(){
  yycol = 1;
  yyrow++;
}

