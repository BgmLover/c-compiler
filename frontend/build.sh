if [ ! -d "dist" ]; then
  mkdir dist
fi
flex --outfile=dist/frontend.lex.yy.cpp frontend.l
yacc --output=dist/y.tab.cpp -d frontend.y
cp tree.cpp dist/tree.cpp
cp tree.h dist/tree.h
cd dist
echo '#include"tree.h"\n' | cat - y.tab.hpp > y.tab.hpp.temp && rm y.tab.hpp && mv y.tab.hpp.temp y.tab.hpp
g++ -std=c++11 -o compiler tree.cpp frontend.lex.yy.cpp y.tab.cpp
./compiler ../../demo/demo.c
