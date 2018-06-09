from backend.frame import StackFrame, stack_frames
from backend.mips_writer import MIPSWriter
from backend.regs import Regs,Reg,Liveness_analysis
#寄存器 我感觉这个不够啊 没有zero 但是我现在不敢轻举妄动
normal_regs=['t0','t1','t2','t3','t4','t5','t6','t7','t8','t9','s0','s1','s2','s3','s4','s5','s6','s7']

class Translator:
  mips_writer=None
  regs=None
  code_lines=None
  line_no=None

  def __init__(self,file_name,path):
    self.code_lines=self.Load_Inter(file_name)
    self.mips_writer=MIPSWriter(path)
    self.regs=Regs(self.code_lines,self.mips_writer)
    self.line_no=-1

  def Load_Inter(self,filename):
    lines=[]
    file=open(filename,'r',encoding='utf-8')
    for line in file:#中间代码
      line = line.replace('\r','').replace('\n','') #换行分割
      if line == '': #line没有内容 跳过
        continue
      lines.append(line.split(' ')) #放入list里
    return lines


  def function_call(self,function_name, params):
    ra_offset = None
    if len(stack_frames) > 0:
      stack_frame = stack_frames[-1]
      ra_offset = stack_frame.request_space(4)
      self.mips_writer.sw('ra', 'fp', -ra_offset)
    stack_frame = StackFrame()
    stack_frame.params = params
    stack_frames.append(stack_frame)
    stack_frame.request_space(len(normal_regs))
    self.mips_writer.addi('fp', 'fp', -stack_frame.request_space(len(normal_regs)*4))
    count = 0
    for reg in ['ra']+normal_regs:
      self.mips_writer.sw(reg, 'fp', count)
      count += 4
    for param in params:
      offset = stack_frame.request_space(4)
      self.mips_writer.addi('fp', 'fp', -offset)
      self.mips_writer.sw(self.regs.get_normal_reg(param,self.line_no), 'fp')
      self.mips_writer.addi('fp', 'fp', offset)
    self.mips_writer.jal(function_name)
    self.mips_writer.lw('ra', 'fp', -ra_offset)


  def function_return(self, variable=None):
    stack_frames.pop()
    if variable is not None:
      self.mips_writer.addi('v0', self.regs.get_normal_reg(variable,self.line_no))
    self.mips_writer.addi('fp', 'fp', 4-len(normal_regs))
    count = 0
    for reg in normal_regs:
      self.mips_writer.lw(reg, 'fp', count)
      count += 4
    if len(stack_frames) == 0:
      offset = len(normal_regs)
    else:
      offset = len(normal_regs) + stack_frames[-1].use_amount
    self.mips_writer.addi('fp', 'fp', offset)
    self.mips_writer.jr('ra')

  #翻译成汇编
  def translate(self):
    self.line_no=0
    for line in self.code_lines:
      if line[0]=='LABEL': #LABEL n: -> n:
        self.mips_writer.write_label(line[1])
      if line[1]==':=': #left := right ->
        if len(line)==3:# vat *temp &temp array_element
          if line[-1][0]>='0' and line[-1][0]<='9':
            self.mips_writer.li(self.regs.get_normal_reg(line[0],self.line_no),line[-1])
          else:
            self.mips_writer.li(self.regs.get_normal_reg(line[0],self.line_no), line[2])
        if len(line)==4:
          if line[2]=='CALL':
            temp_str = line[3].split('(')
            function_name = temp_str[0]
            params = temp_str[1][:-1].split(',')
            self.function_call(function_name, params)
            self.mips_writer.addi(line[0], 'v0')
          # else :
          #   if line[3]=='+':
          #     if line[-1][0]>='0' and line[-1][0]<='9':
          #       return '\taddi %s,$zero,%s'%(self.regs.get_normal_reg(line[0],self.line_no),line[-1])
          #       self.mips_writer.addi()
          #     else:
          #       return '\tadd %s,$zero,%s'%(self.regs.get_normal_reg(line[0],self.line_no),self.regs.get_normal_reg(line[-1],self.line_no))
          #   if line[3]=='-':
          #     if line[-1][0]>='0' and line[-1][0]<='9':
          #       return '\taddi %s,$zero,-%s'%(self.regs.get_normal_reg(line[0],self.line_no),line[-1])
          #     else:
          #       return '\tadd %s,$zero,-%s'%(self.regs.get_normal_reg(line[0],self.line_no),self.regs.get_normal_reg(line[-1],self.line_no))
          #   if line[3]=='~': #mips实现按位取反 没写出来
          #     if line[-1][0]>='0' and line[-1][0]<='9':
          #       return '\taddi %s,$zero,%s'%(self.regs.get_normal_reg(line[0],self.line_no),line[-1])
          #   if line[3]=='!': #mips实现非
          #     if line[-1][0]>='0' and line[-1][0]<='9':
          #       return '\tor %s,$zero,%s'%(self.regs.get_normal_reg(line[0],self.line_no),line[-1])
          #     else:
          #       return '\tor %s,$zero,%s'%(self.regs.get_normal_reg(line[0],self.line_no),self.regs.get_normal_reg(line[-1],self.line_no))

        if len(line)==5: #目前不能解决的操作 >= <= ==  mul立即数等 因为需要临时变量寄存器
          if line[3]=='+':
            if line[-1][0]>='0' and line[-1][0]<='9':
              self.mips_writer.addi(self.regs.get_normal_reg(line[0],self.line_no),
                                    self.regs.get_normal_reg(line[2],self.line_no), line[-1])
            else:
              self.mips_writer.add(self.regs.get_normal_reg(line[0],self.line_no),
                                   self.regs.get_normal_reg(line[2],self.line_no),
                                   self.regs.get_normal_reg(line[-1],self.line_no))
          if line[3]=='-':
            if line[-1][0]>='0' and line[-1][0]<='9':
              self.mips_writer.addi(self.regs.get_normal_reg(line[0],self.line_no),
                                    self.regs.get_normal_reg(line[2],self.line_no), '-'+(line[-1]))
            else:
              self.mips_writer.sub(self.regs.get_normal_reg(line[0],self.line_no),
                                   self.regs.get_normal_reg(line[2],self.line_no),
                                   self.regs.get_normal_reg(line[-1],self.line_no))
          if line[3]=='*':
            self.mips_writer.mul(self.regs.get_normal_reg(line[0],self.line_no),
                                 self.regs.get_normal_reg(line[2],self.line_no),
                                 self.regs.get_normal_reg(line[-1],self.line_no))
          if line[3]=='/':
            self.mips_writer.div(self.regs.get_normal_reg(line[0],self.line_no),
                                 self.regs.get_normal_reg(line[2],self.line_no),
                                 self.regs.get_normal_reg(line[-1],self.line_no))
          if line[3]=='^':
            if line[-1][0]>='0' and line[-1][0]<='9':
              self.mips_writer.xori(self.regs.get_normal_reg(line[0],self.line_no),
                                   self.regs.get_normal_reg(line[2],self.line_no),line[-1])
            else:
              self.mips_writer.xor(self.regs.get_normal_reg(line[0],self.line_no),
                                   self.regs.get_normal_reg(line[2],self.line_no),
                                   self.regs.get_normal_reg(line[-1],self.line_no))
          if line[3]=='<':
            if line[-1][0] >= '0' and line[-1][0] <= '9':
              self.mips_writer.slti(self.regs.get_normal_reg(line[0], self.line_no),
                                   self.regs.get_normal_reg(line[-1], self.line_no), line[2])
            else:
              self.mips_writer.slt(self.regs.get_normal_reg(line[0],self.line_no),
                                   self.regs.get_normal_reg(line[2],self.line_no),
                                   self.regs.get_normal_reg(line[-1],self.line_no))
          if line[3]=='>':
            if line[-1][0] >= '0' and line[-1][0] <= '9':
              self.mips_writer.slti(self.regs.get_normal_reg(line[0], self.line_no),
                                   self.regs.get_normal_reg(line[-1], self.line_no), line[2])
            else:
              self.mips_writer.slt(self.regs.get_normal_reg(line[0],self.line_no),
                                    self.regs.get_normal_reg(line[-1],self.line_no),
                                    self.regs.get_normal_reg(line[2],self.line_no))
          if line[3]=='<=':
            if line[-1][0] >= '0' and line[-1][0] <= '9':
              self.mips_writer.lei(self.regs.get_normal_reg(line[0],self.line_no),
                                    self.regs.get_normal_reg(line[-1],self.line_no), line[2])
            else:
              self.mips_writer.le(self.regs.get_normal_reg(line[0],self.line_no),
                                   self.regs.get_normal_reg(line[-1],self.line_no),
                                   self.regs.get_normal_reg(line[2],self.line_no))
          if line[3]=='>=':
            if line[-1][0] >= '0' and line[-1][0] <= '9':
              self.mips_writer.lei(self.regs.get_normal_reg(line[0],self.line_no),
                                         self.regs.get_normal_reg(line[2],self.line_no), line[-1])
            else:
              self.mips_writer.le(self.regs.get_normal_reg(line[0],self.line_no),
                                   self.regs.get_normal_reg(line[2],self.line_no),
                                   self.regs.get_normal_reg(line[-1],self.line_no))

          if line[3]=='&&':
            if line[-1][0]>='0' and line[-1][0]<='9':
              self.mips_writer.and_(self.regs.get_normal_reg(line[0],self.line_no),
                                    self.regs.get_normal_reg(line[2],self.line_no),line[-1])
            else:
              self.mips_writer.and_(self.regs.get_normal_reg(line[0],self.line_no),
                                    self.regs.get_normal_reg(line[2],self.line_no),
                                    self.regs.get_normal_reg(line[-1],self.line_no))
          if line[3]=='||':
            if line[-1][0]>='0' and line[-1][0]<='9':
              self.mips_writer.ori(self.regs.get_normal_reg(line[0],self.line_no),
                                   self.regs.get_normal_reg(line[2],self.line_no),line[-1])
            else:
              self.mips_writer.or_(self.regs.get_normal_reg(line[0],self.line_no),
                                   self.regs.get_normal_reg(line[2],self.line_no),
                                   self.regs.get_normal_reg(line[-1],self.line_no))
          if line[3]=='<<':
            if line[-1][0]>='0' and line[-1][0]<='9':
              self.mips_writer.sll(self.regs.get_normal_reg(line[0],self.line_no),
                                   self.regs.get_normal_reg(line[2],self.line_no), line[-1])
            else:
              self.mips_writer.sll(self.regs.get_normal_reg(line[0],self.line_no),
                                   self.regs.get_normal_reg(line[2],self.line_no),
                                   self.regs.get_normal_reg(line[-1],self.line_no))
          if line[3]=='>>':
            if line[-1][0]>='0' and line[-1][0]<='9':
              self.mips_writer.srl(self.regs.get_normal_reg(line[0],self.line_no),
                                   self.regs.get_normal_reg(line[2],self.line_no), line[-1])
            else:
              self.mips_writer.srlv(self.regs.get_normal_reg(line[0],self.line_no),
                                    self.regs.get_normal_reg(line[2],self.line_no),
                                    self.regs.get_normal_reg(line[-1],self.line_no))
      if line[0]=='GOTO': #GOTO label1
        self.mips_writer.j(line[1])
      if line[0]=='IF': #IF var GOTO label1
        self.mips_writer.bne(line[1],line[-1])
      if line[0]=='IFNOT': #IFNOT var GOTO label1
        self.mips_writer.beq(line[1],line[-1])
      if line[0]=='RETURN': #RETURN var1
        #return '\tmove $v0,%s\n\tjr $ra'%self.regs.get_normal_reg(line[1],self.line_no)
        self.function_return(line[1] if len(line)>1 else None)
      if line[0]=='MALLOC': #MALLOC var1[size]
        s = line[1].split('[')
        offset = stack_frames[-1].request_space(s[1][:-1])
        self.mips_writer.addi(s[0], 'fp', -offset)
      if line[0]=='CALL': #CALL f (var1,var2,var3...) 这里不太确定
        if line[3]=='read' or line[3]=='print':
          # TODO 这个不知道能不能用，我暂时先不改了 -awmleer
          self.mips_writer.addi('sp', 'sp', -4)
          self.mips_writer.sw('ra', 'sp')

          return '\taddi $sp,$sp,-4\n\tsw $ra,0($sp)\n\tjal %s\n\tlw $ra,0($sp)\n\tmove %s,$v0\n\taddi $sp,$sp,4'%(line[-1],self.regs.get_normal_reg(line[0],self.line_no))
        else:
          temp_str = line[3].split('(')
          function_name = temp_str[0]
          params = temp_str[1][:-1].split(',')
          self.function_call(function_name, params)
      if line[0]=='Function': #FUNCTION f(var1,var2,var3...)
        function_name=line[1].split('(')[0]
        self.mips_writer.write_function_label(function_name)
      self.line_no=self.line_no+1

    # return '\tbeq %s,%s,%s' % (
    # self.regs.get_normal_reg(line[1],self.line_no), self.regs.get_normal_reg(line[3],self.line_no), line[-1])
    # if line[2] == '!=':
    #   return '\tbne %s,%s,%s' % (
    #   self.regs.get_normal_reg(line[1],self.line_no), self.regs.get_normal_reg(line[3],self.line_no), line[-1])
    # if line[2] == '>':
    #   return '\tbgt %s,%s,%s' % (
    #   self.regs.get_normal_reg(line[1],self.line_no), self.regs.get_normal_reg(line[3],self.line_no), line[-1])
    # if line[2] == '<':
    #   return '\tblt %s,%s,%s' % (
    #   self.regs.get_normal_reg(line[1],self.line_no), self.regs.get_normal_reg(line[3],self.line_no), line[-1])
    # if line[2] == '>=':
    #   return '\tbge %s,%s,%s' % (
    #   self.regs.get_normal_reg(line[1],self.line_no), self.regs.get_normal_reg(line[3],self.line_no), line[-1])
    # if line[2] == '<=':
    #   return '\tble %s,%s,%s' % (
    #   self.regs.get_normal_reg(line[1],self.line_no), self.regs.get_normal_reg(line[3],self.line_no), line

#parser() #主函数


# #处理变量
# def varDistribution(Inter):
#   global variables
#   temp_re='(temp\d+)'
#   for line in Inter:
#     temps=re.findall(temp_re,' '.join(line))
#     variables.append(temps)
#
# #记录所有变量 读取所有的中间代码 然后把换行的分开进不同点line

#
# #取得变量的寄存器
# def self.regs.get_normal_reg(string):
#   try:
#     variables.remove(string)
#   except:
#     pass
#   if string in table:
#     return '$'+table[string]  #如果已经存在寄存器分配，那么直接返回寄存器
#   else:
#     keys=[]
#     for key in table:         #已经分配寄存器的变量key
#       keys.append(key)
#     for key in keys:          #当遇到未分配寄存器的变量时，清空之前所有分配的临时变量的映射关系！！！
#       if 'temp' in  key and key not in variables: #
#         reg_ok[table[key]]=1
#         del table[key]
#     for reg in regs:          #对于所有寄存器
#       if reg_ok[reg]==1:    #如果寄存器可用
#         table[string]=reg #将可用寄存器分配给该变量，映射关系存到table中
#         reg_ok[reg]=0     #寄存器reg设置为已用
#         return '$'+reg

