D            [0-9]
L            [a-zA-Z_]
H            [a-fA-F0-9]
E            ([Ee][+-]?{D}+)
P                       ([Pp][+-]?{D}+)
FS            (f|F|l|L)
IS                      ((u|U)|(u|U)?(l|L|ll|LL)|(l|L|ll|LL)(u|U))

%{

#include <stdio.h>
#include "y.tab.h"

void count_col(void);
%}

%%

"/*"            { comment(); }
"//"[^\n]*              { /* consume //-comment */ }


"auto"            { count_col(); return(AUTO); }
"_Bool"            { count_col(); return(BOOL); }
"break"            { count_col(); return(BREAK); }
"case"            { count_col(); return(CASE); }
"char"            { count_col(); return(CHAR); }
"_Complex"        { count_col(); return(COMPLEX); }
"const"            { count_col(); return(CONST); }
"continue"        { count_col(); return(CONTINUE); }
"default"        { count_col(); return(DEFAULT); }
"do"            { count_col(); return(DO); }
"double"        { count_col(); return(DOUBLE); }
"else"            { count_col(); return(ELSE); }
"enum"            { count_col(); return(ENUM); }
"extern"        { count_col(); return(EXTERN); }
"float"            { count_col(); return(FLOAT); }
"for"            { count_col(); return(FOR); }
"goto"            { count_col(); return(GOTO); }
"if"            { count_col(); return(IF); }
"_Imaginary"        { count_col(); return(IMAGINARY); }
"inline"        { count_col(); return(INLINE); }
"int"            { count_col(); return(INT); }
"long"            { count_col(); return(LONG); }
"register"        { count_col(); return(REGISTER); }
"restrict"        { count_col(); return(RESTRICT); }
"return"        { count_col(); return(RETURN); }
"short"            { count_col(); return(SHORT); }
"signed"        { count_col(); return(SIGNED); }
"sizeof"        { count_col(); return(SIZEOF); }
"static"        { count_col(); return(STATIC); }
"struct"        { count_col(); return(STRUCT); }
"switch"        { count_col(); return(SWITCH); }
"typedef"        { count_col(); return(TYPEDEF); }
"union"            { count_col(); return(UNION); }
"unsigned"        { count_col(); return(UNSIGNED); }
"void"            { count_col(); return(VOID); }
"volatile"        { count_col(); return(VOLATILE); }
"while"            { count_col(); return(WHILE); }

{L}({L}|{D})*        { count_col(); return(check_type()); }

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


L?\"(\\.|[^\\"\n])*\"    { count_col(); return(STRING_LITERAL); }

"..."            { count_col(); return(ELLIPSIS); }
">>="            { count_col(); return(RIGHT_ASSIGN); }
"<<="            { count_col(); return(LEFT_ASSIGN); }
"+="            { count_col(); return(ADD_ASSIGN); }
"-="            { count_col(); return(SUB_ASSIGN); }
"*="            { count_col(); return(MUL_ASSIGN); }
"/="            { count_col(); return(DIV_ASSIGN); }
"%="            { count_col(); return(MOD_ASSIGN); }
"&="            { count_col(); return(AND_ASSIGN); }
"^="            { count_col(); return(XOR_ASSIGN); }
"|="            { count_col(); return(OR_ASSIGN); }
">>"            { count_col(); return(RIGHT_OP); }
"<<"            { count_col(); return(LEFT_OP); }
"++"            { count_col(); return(INC_OP); }
"--"            { count_col(); return(DEC_OP); }
"->"            { count_col(); return(PTR_OP); }
"&&"            { count_col(); return(AND_OP); }
"||"            { count_col(); return(OR_OP); }
"<="            { count_col(); return(LE_OP); }
">="            { count_col(); return(GE_OP); }
"=="            { count_col(); return(EQ_OP); }
"!="            { count_col(); return(NE_OP); }
";"            { count_col(); return(';'); }
("{"|"<%")        { count_col(); return('{'); }
("}"|"%>")        { count_col(); return('}'); }
","            { count_col(); return(','); }
":"            { count_col(); return(':'); }
"="            { count_col(); return('='); }
"("            { count_col(); return('('); }
")"            { count_col(); return(')'); }
("["|"<:")        { count_col(); return('['); }
("]"|":>")        { count_col(); return(']'); }
"."            { count_col(); return('.'); }
"&"            { count_col(); return('&'); }
"!"            { count_col(); return('!'); }
"~"            { count_col(); return('~'); }
"-"            { count_col(); return('-'); }
"+"            { count_col(); return('+'); }
"*"            { count_col(); return('*'); }
"/"            { count_col(); return('/'); }
"%"            { count_col(); return('%'); }
"<"            { count_col(); return('<'); }
">"            { count_col(); return('>'); }
"^"            { count_col(); return('^'); }
"|"            { count_col(); return('|'); }
"?"            { count_col(); return('?'); }

[ \t\v\n\f]    { count_col(); }
\n             {count_row()}
.            { /* Add code to complain about unmatched characters */ }

%%


int yywrap(void){
  return 1;
}


void comment(void){
  char c, prev = 0;

  while ((c = input()) != 0)      /* (EOF maps to 0) */
  {
    if (c == '/' && prev == '*')
      return;
    prev = c;
  }
  error("unterminated comment");
}


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

int check_type(void)
{
  /*
   * pseudo code --- this is what it should check
   *
   *    if (yytext == type_name)
   *        return TYPE_NAME;
   *
   *    return IDENTIFIER;
   */

  /*
   *    it actually will only return IDENTIFIER
   */

  return IDENTIFIER;
}
%}
