#  编译原理大作业实验报告

* 小组成员：
  * 张清		3150105495
  * 郝广博     3150104785  
  * 桂晓婉     3150104802  	

## 总体设计

* 我们将C语言文法进行修改，设计了一个可以解析简单C语言程序的编译器，可以生成我们自定义的一套中间代码，并且最终可以将中间代码翻译为MIPS汇编代码

* 根据编译器的通常设计方法（源程序--中间代码--目标代码），我们将编译器的设计分为了三个部分：
  1. 前端部分：对源程序进行词法分析和语法分析，生成语法分析树
  2. 中端部分：解析语法分析树，生成中间代码
  3. 后端部分：翻译中间代码，生成目标代码
* 使用语言/工具：
  1. 前端：C++ / flex, bison
  2. 中段：Python 3.6
  3. 后端：Python 3.6
  4. 效果展示：
     * 运行MIPS代码：SPIM 模拟器
     * 语法分析树展示：**awmleer**
* 运行方式：
  1. 在frontend目录中运行./build.sh生成语法分析器，运行./test.sh解析demo/demo.c，并生成demo/syntax-tree.json
  2. 在middleend目录中运行main.py，生成demo/intermediate.txt
  3. 在backtend目录中运行main.py，生成demo/result.asm
  4. 在模拟器SPIM中打开result.asm，运行即可

## 前端部分

### 总体思路 

在前端部分我们定义了一棵"first child,brother"型的二叉树作为我们的语法分析树，从文法的起始符号开始解析，每解析一个非终结符将生成一个二叉树的非叶节点，每解析到一个终结符（token）将生成一个二叉树的叶节点；最后为了方便后面生成中间代码，我们遍历整棵二叉树，根据树节点的成员变量生成一个json文件用来表示语法分析树

### 数据结构
### 词法分析
### 语法分析

* 语言文法

  语言文法部分我们主要是对C语言进行修改，使用了其部分文法。支持了C语言中包括变量声明和初始化，函数定义和调用，数组和指针，选择、跳转、循环、标签、复合、表达式语句。详细的文法请参阅我们的工程中的frontend/frontend.y

* 语义动作

  在语法分析部分的语义动作比较简单，主要是根据非终结符的文法来生成对应的二叉树节点，以下面的function_definition文法为例：

  ```c++
  function_definition:
      declaration_specifiers declarator declaration_list compound_statement{
          $$=new TreeNode("function_definition",4,$1,$2,$3,$4);
  //树节点的构造函数第一个参数为非终结符名字，第二个参数为对应生成式的非终结符个数，剩下几个参数分别为指向各个非终结符对应的数节点的指针
      }
      | declaration_specifiers declarator compound_statement{
          $$=new TreeNode("function_definition",3,$1,$2,$3);
      };
  ```

* 规约优先级设置

  在使用yacc来进行语法分析的过程中常常会产生“移进——规约”冲突，我们对于必要的冲突进行了处理，这里以"if "和"if else"两种选择语句为例来进行说明：

  ```c++
  %nonassoc LOWER_THAN_ELSE
  %nonassoc ELSE
  //这里声明了两个没有结合性的token，其中ELSE拥有更高的优先级，而在下面选择语句文法的第二项末尾中使用%prec LOWER_THAN_ELSE表明了这条操作的优先级和LOWER_THAN_ELSE一样，而LOWER_THAN_ELSE的优先级低于ELSE，所以在这个移进规约冲突中，会优先执行移进操作
  selection_statement:
        IF '(' expression ')' statement ELSE statement{
        $$=new TreeNode("selection_statement",7,$1,$2,$3,$4,$5,$6,$7);    
      }
      | IF '(' expression ')' statement %prec LOWER_THAN_ELSE{//这条语句的优先级更低
        $$=new TreeNode("selection_statement",5,$1,$2,$3,$4,$5);    
      }
  ```

* 错误恢复

  在语法分析阶段我们也做了错误恢复处理，为了使得扫描器在遇到错误时能够跳过当前错误继续扫描以输出全部的错误信息，在yacc中支持使用error关键字来实现错误恢复：

  ```c++
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
        }
      | error IDENTIFIER {
        flag=1;  };
  //在最后一句这里加上了error关键字，表明在解析的时候这里可能会遇到错误。在后面加上IDENTIFIER这个token表示告诉扫描器继续扫描直到遇到一个IDENTIFIER token为止
  ```

## 中端部分
### 数据结构
### 解析语法树
## 后端部分
### 数据结构
### 翻译中间代码
## 效果展示
### 语法树可视化
### 执行目标代码
## 小组分工
## 心得体会
