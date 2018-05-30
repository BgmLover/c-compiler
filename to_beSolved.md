Target: Tree   ->  intermediate code

* 语言 python 3.6 + 虚拟环境
1. 中间代码的定义和接口
   - 基本形式：三地址码  模仿mips?
   - 接口类型：
        * 生成代码 (string)
            1. 算术型
            2. move型
            3. declaration型 (label,function,parameter)
            4. 函数返回
        * 添加代码
            1. add code(string)
        * 输出代码
            1. print()
            2. write(string path)
    * 全局变量管理 list codelist
2. 数据结构
    * node（不同类型的node）
    * block
3. 分析语法树生成初步的中间代码
    * 全局变量
        * function_pool//函数声明
        * BlockStack
    * 解析部分
        * 文法分类（这里主要针对我们写的文法来一步步分类定义）
        * 递归解析（每一层应有的中间代码生成）
        * 一些辅助函数
            1. 各种get\set\find\create
            2. error()\print()提供可视化debug
        * 难点
            1. block的定义（每个compoud_statement就算一个？）
            2. 函数（声明检查、类型检查、返回类型）
            3. 跳转语句（break,continue,return,goto）
            4. 数组（内存的申请、管理）
            5. 栈帧(参数传递、静态链、返回地址)
        * 注意事项
            1. expression中的类型检查
            2. label的管理
            3. 默认有input(),print()函数

4. 优化中间代码
    * 去除不必要的多余代码
    * 待续
