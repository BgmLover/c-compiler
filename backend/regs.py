class Regs:
  #normal_regs=['t0','t1','t2','t3','t4','t5','t6','t7','t8','t9','s0','s1','s2','s3','s4','s5','s6','s7']
  normal_regs=[]

  def __init__(self):
    for t in range(10):
      new_t_reg=Reg('t'+str(t))
      self.normal_regs.append(new_t_reg)
    for s in range(8):
      new_s_reg=Reg('s'+str(s))
      self.normal_regs.append(new_s_reg)

  def get_normal_reg(self):
    pass

class Reg:
  name=None
  available=False
  variable_name=None

  def __init__(self,reg_name):
    self.name=reg_name
    self.available=True
    self.variable_name=None


class Liveness_analysis:
  code_list=[]
  code_lines=[]
  label_line={}
  def __init__(self,code_lines):
    self.code_lines=code_lines
  def is_temp(self,item):
    if item[0]=='t':
      return True
    else:
      return False

  def init_code_list(self):
    line_no=0
    for line in self.code_lines:
      if line[0]=='LABEL':
        self.label_line[line[1]]=line_no
        code=Code(line_no, line_no + 1)
        self.code_list.append(code)
      if line[1] == ':=':
        code = Code(line_no, line_no + 1)
        code.define[line[0]] = True#TODO
        if line[2] !='CALL':
          if len(line) == 3:
            if  self.is_temp(line[-1]):
              code.use[line[2]]=True
          if len(line) == 5:
            if self.is_temp(line[2]):
              code.use[line[2]]=True
            if self.is_temp(line[4]):
              code.use[line[4]]=True
        else:
          function_item=line[3]
          items=function_item.split('(')
          items=items[1].split(')')
          if items[0]!='':
            arguments=items[0].split(',')
            for argument in arguments:
              code.use[argument]=True



        if line[2] == 'CALL':
          if line[3] == 'read' or line[3] == 'print':
            return '\taddi $sp,$sp,-4\n\tsw $ra,0($sp)\n\tjal %s\n\tlw $ra,0($sp)\n\tmove %s,$v0\n\taddi $sp,$sp,4' % (
            line[-1], Get_R(line[0]))
          else:
            return '\taddi $sp,$sp,-24\n\tsw $t0,0($sp)\n\tsw $ra,4($sp)\n\tsw $t1,8($sp)\n\tsw $t2,12($sp)\n\tsw $t3,16($sp)\n\tsw $t4,20($sp)\n\tjal %s\n\tlw $a0,0($sp)\n\tlw $ra,4($sp)\n\tlw $t1,8($sp)\n\tlw $t2,12($sp)\n\tlw $t3,16($sp)\n\tlw $t4,20($sp)\n\taddi $sp,$sp,24\n\tmove %s $v0' % (
            line[-1], Get_R(line[0]))
      if line[0] == 'GOTO':
        return '\tj %s' % line[1]
      if line[0] == 'RETURN':
        return '\tmove $v0,%s\n\tjr $ra' % Get_R(line[1])
      if line[0] == 'IF':
        if line[2] == '==':
          return '\tbeq %s,%s,%s' % (Get_R(line[1]), Get_R(line[3]), line[-1])
        if line[2] == '!=':
          return '\tbne %s,%s,%s' % (Get_R(line[1]), Get_R(line[3]), line[-1])
        if line[2] == '>':
          return '\tbgt %s,%s,%s' % (Get_R(line[1]), Get_R(line[3]), line[-1])
        if line[2] == '<':
          return '\tblt %s,%s,%s' % (Get_R(line[1]), Get_R(line[3]), line[-1])
        if line[2] == '>=':
          return '\tbge %s,%s,%s' % (Get_R(line[1]), Get_R(line[3]), line[-1])
        if line[2] == '<=':
          return '\tble %s,%s,%s' % (Get_R(line[1]), Get_R(line[3]), line[-1])
      if line[0] == 'FUNCTION':
        return '%s:' % line[1]
      if line[0] == 'CALL':
        if line[-1] == 'read' or line[-1] == 'print':
          return '\taddi $sp,$sp,-4\n\tsw $ra,0($sp)\n\tjal %s\n\tlw $ra,0($sp)\n\taddi $sp,$sp,4' % (line[-1])
        else:
          return '\taddi $sp,$sp,-24\n\tsw $t0,0($sp)\n\tsw $ra,4($sp)\n\tsw $t1,8($sp)\n\tsw $t2,12($sp)\n\tsw $t3,16($sp)\n\tsw $t4,20($sp)\n\tjal %s\n\tlw $a0,0($sp)\n\tlw $ra,4($sp)\n\tlw $t1,8($sp)\n\tlw $t2,12($sp)\n\tlw $t3,16($sp)\n\tlw $t4,20($sp)\n\taddi $sp,$sp,24\n\tmove %s $v0' % (
          line[-1], Get_R(line[0]))


class Code:
  line_no=-1    #行号
  succeed=[]
  define={}
  use={}
  var_in={}
  var_out={}

  def __init__(self,line_no,succeed_no=None):
    self.line_no=line_no
    if succeed_no is not None:
      self.succeed.append(succeed_no)
