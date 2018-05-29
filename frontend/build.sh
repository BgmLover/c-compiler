flex --outfile=dist/frontend.lex.yy.cpp frontend.l
yacc --output=dist/y.tab.cpp -d frontend.y
cp tree.cpp dist/tree.cpp
cp tree.h dist/tree.h
cd dist
sed -i '1i#include"tree.h"' y.tab.hpp
g++ -std=c++11 -o compiler tree.cpp frontend.lex.yy.cpp y.tab.cpp
./compiler demo.c
