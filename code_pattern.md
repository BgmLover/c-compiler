## The pattern of the intermidiate code 



| Grammer                      | Description                                                  |
| :--------------------------- | :----------------------------------------------------------- |
| LABEL n :                    | 声明标签（n=0,1,2,3....）                                    |
| left := right | 赋值语句 |
|  | right: var binomial_op var \| var \| unary_op var \| *temp \| &temp \| array_element \| CALL f(var1,var2,var3...) |
|  | var: temp \| constant |
|  | left: temp \| array_element \| *temp |
|  | array_item: temp[var] |
|  | temp必须只含有小写英文字母、数字、下划线，且首字符是字母 |
| GOTO label1               | 无条件跳转至标签处                                           |
| IF var GOTO label1 | 条件语句                                |
| RETURN var1                  | 函数返回                                                     |
| MALLOC var1[size]            | 申请大小为size的内存空间，并将申请到的连续内存首地址赋给var1 |
| CALL f (var1,var2,var3...)                       | 调用函数并不需要返回值     |
| FUNCTION f(var1,var2,var3...)                    | 声明函数f                                                    |



#### 关于运算符

| 类别       | 内容                                                   |
| ---------- | ------------------------------------------------------ |
| 单目运算符 | +   -   ~ !                                            |
| 关系运算符 | <   >   <=   >=   !=  ==                               |
| 算术运算符 | +   -   *   /   %   \|   ^   &                         |
| 逻辑运算符 | \|\|   &&                                              |
| 移位运算   | >>   <<                                                |
| 赋值运算符 | =   +=   -=   *=   /=   %=   &=   ^=   \|=   <<=   >>= |
|            |                                                        |
|            |                                                        |

