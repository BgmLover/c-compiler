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
"break"           { count_col(); yylval.node = new TreeNode("break"); return(BREAK); }

"case"            { count_col(); yylval.node = new TreeNode("case"); return(CASE); }
"char"            { count_col(); yylval.node = new TreeNode("char"); return(CHAR); }
 /*"_Complex"        { count_col(); return(COMPLEX); }*/
 /*"const"           { count_col(); yylval.node = new TreeNode("const"); return(CONST); }*/
"continue"        { count_col(); yylval.node = new TreeNode("continue"); return(CONTINUE); }
 /*"default"         { count_col(); yylval.node = new TreeNode("default"); return(DEFAULT); }*/
"do"              { count_col(); yylval.node = new TreeNode("do"); return(DO); }
"double"          { count_col(); yylval.node = new TreeNode("double"); return(DOUBLE); }
"else"            { count_col(); yylval.node = new TreeNode("else"); return(ELSE); }
 /*"enum"            { count_col(); return(ENUM); }*/
 /*"extern"        { count_col(); return(EXTERN); }*/
 /*"float"            { count_col(); return(FLOAT); }*/
"for"             { count_col(); yylval.node = new TreeNode("for"); return(FOR); }
"goto"            { count_col(); yylval.node = new TreeNode("goto"); return(GOTO); }
"if"              { count_col(); yylval.node = new TreeNode("if"); return(IF); }
 /*"_Imaginary"        { count_col(); return(IMAGINARY); }*/
 /*"inline"        { count_col(); return(INLINE); }*/
"int"             { count_col(); yylval.node = new TreeNode("int"); return(INT); }
 /*"long"            { count_col(); return(LONG); }*/
 /*"register"        { count_col(); return(REGISTER); }*/
 /*"restrict"        { count_col(); return(RESTRICT); }*/
"return"          { count_col(); yylval.node = new TreeNode("return"); return(RETURN); }
 /*"short"            { count_col(); return(SHORT); }*/
 /*"signed"        { count_col(); return(SIGNED); }*/
"sizeof"          { count_col(); yylval.node = new TreeNode("sizeof"); return(SIZEOF); }
 /*"static"        { count_col(); return(STATIC); }*/
 /*"struct"        { count_col(); return(STRUCT); }*/
"switch"          { count_col(); yylval.node = new TreeNode("switch"); return(SWITCH); }
 /*"typedef"         { count_col(); yylval.node = new TreeNode("typedef"); return(TYPEDEF); }*/
 /*"union"            { count_col(); return(UNION); }*/
 /*"unsigned"        { count_col(); return(UNSIGNED); }*/
"void"            { count_col(); yylval.node = new TreeNode("void"); return(VOID); }
 /*"volatile"        { count_col(); return(VOLATILE); }*/
"while"           { count_col(); yylval.node = new TreeNode("while"); return(WHILE); }

{L}({L}|{D})*     { count_col(); yylval.node = new TreeNode("identifier", yytext); return(IDENTIFIER); }
0[xX]{H}+        { count_col(); yylval.node = new TreeNode("constant_int", yytext); return(CONSTANT); }
0[0-7]*        { count_col(); yylval.node = new TreeNode("constant_int", yytext); return(CONSTANT); }
[1-9]{D}*        { count_col(); yylval.node = new TreeNode("constant_int", yytext); return(CONSTANT); }
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

 /*"..."           { count_col(); yylval.node = new TreeNode("..."); return(ELLIPSIS); }*/
">>="           { count_col(); yylval.node = new TreeNode(">>="); return(RIGHT_ASSIGN); }
"<<="           { count_col(); yylval.node = new TreeNode("<<="); return(LEFT_ASSIGN); }
"+="            { count_col(); yylval.node = new TreeNode("+="); return(ADD_ASSIGN); }
"-="            { count_col(); yylval.node = new TreeNode("-="); return(SUB_ASSIGN); }
"*="            { count_col(); yylval.node = new TreeNode("*="); return(MUL_ASSIGN); }
"/="            { count_col(); yylval.node = new TreeNode("/="); return(DIV_ASSIGN); }
"%="            { count_col(); yylval.node = new TreeNode("%="); return(MOD_ASSIGN); }
"&="            { count_col(); yylval.node = new TreeNode("&="); return(AND_ASSIGN); }
"^="            { count_col(); yylval.node = new TreeNode("^="); return(XOR_ASSIGN); }
"|="            { count_col(); yylval.node = new TreeNode("|="); return(OR_ASSIGN); }
">>"            { count_col(); yylval.node = new TreeNode(">>"); return(RIGHT_OP); }
"<<"            { count_col(); yylval.node = new TreeNode("<<"); return(LEFT_OP); }
"++"            { count_col(); yylval.node = new TreeNode("++"); return(INC_OP); }
"--"            { count_col(); yylval.node = new TreeNode("--"); return(DEC_OP); }
"->"            { count_col(); yylval.node = new TreeNode("->"); return(PTR_OP); }
"&&"            { count_col(); yylval.node = new TreeNode("&&"); return(AND_OP); }
"||"            { count_col(); yylval.node = new TreeNode("||"); return(OR_OP); }
"<="            { count_col(); yylval.node = new TreeNode("<="); return(LE_OP); }
">="            { count_col(); yylval.node = new TreeNode(">="); return(GE_OP); }
"=="            { count_col(); yylval.node = new TreeNode("=="); return(EQ_OP); }
"!="            { count_col(); yylval.node = new TreeNode("!="); return(NE_OP); }
";"             { count_col(); yylval.node = new TreeNode(";"); return(';'); }
("{"|"<%")      { count_col(); yylval.node = new TreeNode("{"); return('{'); }
("}"|"%>")      { count_col(); yylval.node = new TreeNode("}"); return('}'); }
","             { count_col(); yylval.node = new TreeNode(","); return(','); }
":"             { count_col(); yylval.node = new TreeNode(":"); return(':'); }
"="             { count_col(); yylval.node = new TreeNode("="); return('='); }
"("             { count_col(); yylval.node = new TreeNode("("); return('('); }
")"             { count_col(); yylval.node = new TreeNode(")"); return(')'); }
("["|"<:")      { count_col(); yylval.node = new TreeNode("["); return('['); }
("]"|":>")      { count_col(); yylval.node = new TreeNode("]"); return(']'); }
"."             { count_col(); yylval.node = new TreeNode("."); return('.'); }
"&"             { count_col(); yylval.node = new TreeNode("&"); return('&'); }
"!"             { count_col(); yylval.node = new TreeNode("!"); return('!'); }
"~"             { count_col(); yylval.node = new TreeNode("~"); return('~'); }
"-"             { count_col(); yylval.node = new TreeNode("-"); return('-'); }
"+"             { count_col(); yylval.node = new TreeNode("+"); return('+'); }
"*"             { count_col(); yylval.node = new TreeNode("*"); return('*'); }
"/"             { count_col(); yylval.node = new TreeNode("/"); return('/'); }
"%"             { count_col(); yylval.node = new TreeNode("%"); return('%'); }
"<"             { count_col(); yylval.node = new TreeNode("<"); return('<'); }
">"             { count_col(); yylval.node = new TreeNode(">"); return('>'); }
"^"             { count_col(); yylval.node = new TreeNode("^"); return('^'); }
"|"             { count_col(); yylval.node = new TreeNode("|"); return('|'); }
"?"             { count_col(); yylval.node = new TreeNode("?"); return('?'); }

[ \t\v\f]     { count_col(); return(' '); }
\n              { count_row(); return('\n'); }
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


int column = 0;
int row = 0;

void count_col(void){
  int i;

  for (i = 0; yytext[i] != '\0'; i++){
    if(yytext[i] == '\t'){
      column += 8 - (column % 8);
    }else{
      column++;
    }
  }

  ECHO;
}

void count_row(){
  column = 0;
  row++;
}

