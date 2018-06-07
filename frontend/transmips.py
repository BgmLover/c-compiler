
#处理寄存器
def varDistribution()：


#记录所有变量 读取所有的中间代码 然后把换行的分开进不同点line
def Load_Inter(filename):
    lines=[] #列表
    for line in #中间代码
        line = line.replace('\r','').replace('\n','') #换行分割 
        if line == '': #line没有内容 跳过
            continue
        lines.append(line.split(' ')) #放入list里
    return lines

#这个我也不懂
def Get_R(string):

#翻译成汇编
def translate(line):
    if line[0]=='LABEL': #LABEL n: -> n:
        return line[1]+':'
    if line[1]==':=': #left := right -> 

    if line[0]=='GOTO': #GOTO label1

    if line[0]=='IF': #IF var GOTO label1

    if line[0]=='IFNOT': #IFNOT var GOTO label1

    if line[0]=='RETURN': #RETURN var1

    if line[0]=='MALLOC': #MALLOC var1[size]

    if line[0]=='CALL': #CALL f (var1,var2,var3...)

    if line[0]=='FUNCTION': #FUNCTION f(var1,var2,var3...)

def parser():
    for reg in regs:
        reg_ok[reg]=1  #初始化，所有寄存器都可用
    Inter=Load_Inter('？？？')  #读取中间代码 需修改
    Load_Var(Inter)    #第一遍扫描，记录所有变量
    Obj=[]
    for line in Inter:#对于list里的每个元素
        obj_line=translate(line) #翻译中间代码成MIPS汇编
        if obj_line=='':
            continue
        Obj.append(obj_line)
    write_to_txt(Obj)

parser() #主函数
