#寄存器 我感觉这个不够啊 没有zero 但是我现在不敢轻举妄动
regs=['t1','t2','t3','t4','t5','t6','t7','t8','t9','s0','s1','s2','s3','s4','s5','s6','s7']
table={}
reg_ok={}
variables=[]

#处理变量
def varDistribution()：
    global variables
    temp_re='(temp\d+)'
    for line in Inter:
        temps=re.findall(temp_re,' '.join(line))
        variables+=temps

#记录所有变量 读取所有的中间代码 然后把换行的分开进不同点line
def Load_Inter(filename):
    lines=[] #列表
    for line in #中间代码
        line = line.replace('\r','').replace('\n','') #换行分割 
        if line == '': #line没有内容 跳过
            continue
        lines.append(line.split(' ')) #放入list里
    return lines

#取得变量的寄存器
def Get_R(string):
    try:
        variables.remove(string)
    except:
        pass
    if string in table:
        return '$'+table[string]  #如果已经存在寄存器分配，那么直接返回寄存器
    else:
        keys=[]
        for key in table:         #已经分配寄存器的变量key
            keys.append(key)
        for key in keys:          #当遇到未分配寄存器的变量时，清空之前所有分配的临时变量的映射关系！！！
            if 'temp' in  key and key not in variables: #
                reg_ok[table[key]]=1
                del table[key]
        for reg in regs:          #对于所有寄存器
            if reg_ok[reg]==1:    #如果寄存器可用
                table[string]=reg #将可用寄存器分配给该变量，映射关系存到table中
                reg_ok[reg]=0     #寄存器reg设置为已用
                return '$'+reg
                
#翻译成汇编
def translate(line):
    if line[0]=='LABEL': #LABEL n: -> n:
        return line[1]+':'
    if line[1]=='=': #left := right -> 
        if len(line)==3:# vat *temp &temp array_element
            if line[-1][0]>='0' and line[-1][0]<='9':
                return '\taddi %s,$zero,%s'%(Get_R(line[0]),line[-1])
            else:
                return '\tmove $s,%s'%(Get_R(line[0]),line[2])
        if len(line)==4: #一元op CALL f 目前不能解决的 ～
            if line[2]=='CALL'
                return 
            else :
                if line[3]=='+':
                  if line[-1][0]>='0' and line[-1][0]<='9':
                    return '\taddi %s,$zero,%s'%(Get_R(line[0]),line[-1])
                  else:
                    return '\tadd %s,$zero,%s'%(Get_R(line[0]),Get_R(line[-1]))
                if line[3]=='-':
                  if line[-1][0]>='0' and line[-1][0]<='9':
                    return '\taddi %s,$zero,-%s'%(Get_R(line[0]),line[-1])
                  else:
                    return '\tadd %s,$zero,-%s'%(Get_R(line[0]),Get_R(line[-1]))
                if line[3]=='~': #mips实现按位取反 没写出来
                  if line[-1][0]>='0' and line[-1][0]<='9':
                    return '\taddi %s,$zero,%s'%(Get_R(line[0]),line[-1])
                if line[3]=='!': #mips实现非
                  if line[-1][0]>='0' and line[-1][0]<='9':
                    return '\tor %s,$zero,%s'%(Get_R(line[0]),line[-1])
                  else:
                    return '\tor %s,$zero,%s'%(Get_R(line[0]),Get_R(line[-1]))
        if len(line)==5: #目前不能解决的操作 >= <= == >> << mul立即数等 因为需要临时变量寄存器
            if line[3]=='+':
              if line[-1][0]>='0' and line[-1][0]<='9':
                return '\taddi %s,%s,%s'%(Get_R(line[0]),Get_R(line[2]),line[-1])
              else:
                return '\tadd %s,%s,%s'%(Get_R(line[0]),Get_R(line[2]),line[-1])
            if line[3]=='-':
              if line[-1][0]>='0' and line[-1][0]<='9':
                return '\taddi %s,%s,-%s'%(Get_R(line[0]),Get_R(line[2]),line[-1])
              else:
                return '\tsub %s,%s,%s'%(Get_R(line[0]),Get_R(line[2]),line[-1])
            if line[3]=='*':
                return '\tmul %s,%s,%s'%(Get_R(line[0]),Get_R(line[2]),line[-1])
            if line[3]=='/':
                return '\tdiv %s,%s,%s'%(Get_R(line[0]),Get_R(line[2]),line[-1])
            if line[3]=='<':
                return '\tslt %s,%s,%s'%(Get_R(line[0]),Get_R(line[2]),line[-1])
            if line[3]=='>':
                return '\tslt %s,%s,%s'%(Get_R(line[0]),Get_R(line[-1]),line[2])
            if line[3]=='&&':
                return '\tand %s,%s,%s'%(Get_R(line[0]),Get_R(line[2]),line[-1])
            if line[3]=='||':
                return '\tor %s,%s,%s'%(Get_R(line[0]),Get_R(line[2]),line[-1])
            if line[3]=='!=':
                return '\txor %s,%s,%s'%(Get_R(line[0]),Get_R(line[2]),line[-1])
      #这里竟然还有千奇百怪的赋值运算符qaq 
    if line[0]=='GOTO': #GOTO label1
        return '\tj %s'%line[1]
    if line[0]=='IF': #IF var GOTO label1
        if line[2]=='==':
            return '\tbeq %s,%s,%s'%(Get_R(line[1]),Get_R(line[3]),line[-1])
        if line[2]=='!=':
            return '\tbne %s,%s,%s'%(Get_R(line[1]),Get_R(line[3]),line[-1])
        if line[2]=='>':
            return '\tbgt %s,%s,%s'%(Get_R(line[1]),Get_R(line[3]),line[-1])
        if line[2]=='<':
            return '\tblt %s,%s,%s'%(Get_R(line[1]),Get_R(line[3]),line[-1])
        if line[2]=='>=':
            return '\tbge %s,%s,%s'%(Get_R(line[1]),Get_R(line[3]),line[-1])
        if line[2]=='<=':
            return '\tble %s,%s,%s'%(Get_R(line[1]),Get_R(line[3]),line[-1])
    if line[0]=='IFNOT': #IFNOT var GOTO label1
        if line[2]=='！=':
            return '\tbeq %s,%s,%s'%(Get_R(line[1]),Get_R(line[3]),line[-1])
        if line[2]=='==':
            return '\tbne %s,%s,%s'%(Get_R(line[1]),Get_R(line[3]),line[-1])
        if line[2]=='<=':
            return '\tbgt %s,%s,%s'%(Get_R(line[1]),Get_R(line[3]),line[-1])
        if line[2]=='>=':
            return '\tblt %s,%s,%s'%(Get_R(line[1]),Get_R(line[3]),line[-1])
        if line[2]=='<':
            return '\tbge %s,%s,%s'%(Get_R(line[1]),Get_R(line[3]),line[-1])
        if line[2]=='>':
            return '\tble %s,%s,%s'%(Get_R(line[1]),Get_R(line[3]),line[-1])
    if line[0]=='RETURN': #RETURN var1
        return '\tmove $v0,%s\n\tjr $ra'%Get_R(line[1])
    if line[0]=='MALLOC': #MALLOC var1[size]

    if line[0]=='CALL': #CALL f (var1,var2,var3...) 这里不太确定
        if line[3]=='read' or line[3]=='print':
                return '\taddi $sp,$sp,-4\n\tsw $ra,0($sp)\n\tjal %s\n\tlw $ra,0($sp)\n\tmove %s,$v0\n\taddi $sp,$sp,4'%(line[-1],Get_R(line[0]))
            else:
                return '\taddi $sp,$sp,-24\n\tsw $t0,0($sp)\n\tsw $ra,4($sp)\n\tsw $t1,8($sp)\n\tsw $t2,12($sp)\n\tsw $t3,16($sp)\n\tsw $t4,20($sp)\n\tjal %s\n\tlw $a0,0($sp)\n\tlw $ra,4($sp)\n\tlw $t1,8($sp)\n\tlw $t2,12($sp)\n\tlw $t3,16($sp)\n\tlw $t4,20($sp)\n\taddi $sp,$sp,24\n\tmove %s $v0'%(line[-1],Get_R(line[0]))
    if line[0]=='FUNCTION': #FUNCTION f(var1,var2,var3...)
        return '%s:'%line[1]
    return ''

def write_to_txt(Obj):
    f=open('result.asm','w')
    template='''
.data
_prompt: .asciiz "Enter an integer:"
_ret: .asciiz "\\n"
.globl main
.text
read:
    li $v0,4
    la $a0,_prompt
    syscall
    li $v0,5
    syscall
    jr $ra

print:
    li $v0,1
    syscall
    li $v0,4
    la $a0,_ret
    syscall
    move $v0,$0
    jr $ra
'''
    f.write(template)
    for line in Obj:
        f.write(line+'\n')
    f.close()

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
