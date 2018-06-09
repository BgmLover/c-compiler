from backend.frame import stack_frames
from backend.mips_writer import MIPSWriter
import random
class Regs:
  #normal_regs=['t0','t1','t2','t3','t4','t5','t6','t7','t8','t9','s0','s1','s2','s3','s4','s5','s6','s7']
  normal_regs=[]
  liveness_analysis = None
  mips_writer=None
  def __init__(self,code_lines,mips_writer):
    for t in range(1,10):
      new_t_reg=Reg('t'+str(t))
      self.normal_regs.append(new_t_reg)
    for s in range(8):
      new_s_reg=Reg('s'+str(s))
      self.normal_regs.append(new_s_reg)
    self.liveness_analysis = Liveness_analysis(code_lines)
    self.mips_writer=mips_writer

  def get_normal_reg(self,variable,line_no):
    for reg in self.normal_regs:
      if reg.variable_name==variable:
        return reg.name
    result=self.find_available_reg(variable)
    if result!=False:
      #self.normal_regs[result].available=False
      return result
    else:
      for reg in self.normal_regs:
        if reg.variable_name in self.liveness_analysis.code_list[line_no].var_out:
          pass
        else:
          reg.available=True
      result_2=self.find_available_reg(variable)
      if result_2!=False:
        return result_2
      else:#寄存器溢出
        while True:
          reg_id=random.randint(0,len(self.normal_regs))
          if self.normal_regs[reg_id].is_spilled==False:
            break
        offset=stack_frames[-1].request_space(4)
        self.mips_writer.addi('fp', 'fp', -offset)
        reg_to_spill=self.normal_regs[reg_id]
        self.mips_writer.sw(reg_to_spill.name, 'fp')
        self.mips_writer.addi('fp', 'fp', -offset)

        reg_to_spill.is_spilled=True
        reg_to_spill.spilled_var=reg_to_spill.variable
        reg_to_spill.variable=variable
        return reg_to_spill.name


  def find_available_reg(self,variable):
    for reg in self.normal_regs:
      if reg.available == True:
        reg.variable_name = variable
        reg.available=False
        return reg.name
    return False


class Reg:
  name=None
  available=None
  variable_name=None
  is_spilled=None
  spilled_var=None
  def __init__(self,reg_name):
    self.name=reg_name
    self.available=True
    self.variable_name=None
    self.is_spilled=False
    self.spilled_var=None

class Liveness_analysis:
  code_list=None
  code_lines=None
  label_line=None
  variable_line=None
  def __init__(self,code_lines):
    self.code_lines=code_lines
    self.code_list=[]
    self.label_line={}
    self.variable_line={}

    self.init_code_list()
    self.cal_liveness()
    self.show_liveness()

  def show_liveness(self):
    for code in self.code_list:
      string='line:'+str(code.line_no+1)
      string=string+' use:'
      for use in code.use:
        string=string+use+','
      string = string + ' define:'
      for define in code.define:
        string = string + define + ','
      string =string+'in:'
      for var_in in code.var_in:
        string =string + var_in+','
      string = string + 'out:'
      for var_out in code.var_out:
        string = string + var_out + ','
      print(string)
  def is_temp(self,item):
    if item[0]=='t':
      return True
    else:
      return False

  def init_code_list(self):
    line_no=0
    for line in self.code_lines:
      if line[0]=='LABEL':
        label=line[1].split(':')[0]
        self.label_line[label]=line_no
      if line[0]=='Function':
        function_name = line[1].split('(')[0]
        self.label_line[function_name]=line_no
      line_no=line_no+1

    line_no=0
    function_name=None
    for line in self.code_lines:
      if line[0]=='LABEL':
        code=Code(line_no,function_name, line_no + 1)

      elif line[1] == ':=':
        code = Code(line_no,function_name, line_no + 1)
        if len(line[0].split('['))==1:
          code.define.append(line[0])
          self.variable_line[line[0]]=line_no
        else:#数组
          array_name=line[0].split('[')[0]
          code.use.append(array_name)
          size=line[0].split('[')[1].split(']')[0]
          if self.is_temp(size):
            code.use.append(size)
        if line[2] !='CALL':
          if len(line) == 3:
            if  self.is_temp(line[-1]):
              code.use.append(line[2])
          if len(line) == 5:
            if self.is_temp(line[2]):
              code.use.append(line[2])
            if self.is_temp(line[4]):
              code.use.append(line[4])
        else:
          function_item=line[3]
          items=function_item.split('(')
          items=items[1].split(')')
          if items[0]!='':
            arguments=items[0].split(',')
            for argument in arguments:
              code.use.append(argument)

      elif line[0] == 'GOTO':
        if line_no-1!=0 and self.code_lines[line_no-1][0]=='RETURN':#goto 的上一句是return就没有意义了
            code=Code(line_no,None)
            line_no=line_no+1
            self.code_list.append(code)
            continue
        code=Code(line_no,function_name)
        line_id=self.label_line[line[1]]
        code.succeed.append(line_id)

      elif line[0] == 'RETURN':
        code=Code(line_no,function_name)
        if len(line)==2:
          if self.is_temp(line[1]):
            code.use.append(line[1])
        function_name=None

      elif line[0] == 'IF' or line[0]=='IFNOT':
        code=Code(line_no,function_name)
        code.use.append(line[1])
        code.succeed.append(self.label_line[line[3]])
        if line_no+1!=len(self.code_lines):
          code.succeed.append(line_no+1)

      elif line[0] == 'Function':
        function_name=line[1].split('(')[0]
        code=Code(line_no,function_name)
        if line_no+1!=len(self.code_lines):
          code.succeed.append(line_no+1)

      elif line[0] == 'CALL':
        code=Code(line_no,function_name)
        function_item = line[1]
        items = function_item.split('(')
        items = items[1].split(')')
        if items[0] != '':
          arguments = items[0].split(',')
          for argument in arguments:
            code.use.append(argument)
        if line_no+1!=len(self.code_lines):
          code.succeed.append(line_no+1)

      elif line[0]=='MALLOC':
        code=Code(line_no,function_name,line_no+1)
        array_name=line[1].split('[')[0]
        code.define.append(array_name)
        size=line[1].split('[')[1].split(']')[0]
        if self.is_temp(size):
          code.use.append(size)
      else:
        code=Code(line_no,None,None)
        error_message="error: invalid code: line"+str(line_no+1)+'  '
        for item in self.code_lines[line_no]:
          error_message=error_message+item+' '
        print(error_message)
      line_no=line_no+1
      self.code_list.append(code)

  def cal_liveness(self):
    while(True):
      can_break=True
      for code in self.code_list:
        var_in_final=code.var_in.copy()
        var_out_final=code.var_out.copy()
        code.var_in=set(code.use)|(code.var_out-set(code.define))
        code.var_out=set()
        for succ in code.succeed:
          code.var_out=code.var_out|self.code_list[int(succ)].var_in
        if code.var_in-var_in_final==set() and code.var_out-var_out_final==set():
          pass
        else:
          can_break=False
      if can_break==True:
        break

class Code:
  line_no=None    #行号
  function_name=None
  succeed=None
  define=None
  use=None
  var_in=None
  var_out=None

  def __init__(self,line_no,function_name,succeed_no=None):
    self.line_no=line_no
    self.function_name=function_name
    self.succeed = []
    self.define = []
    self.use = []
    self.var_in = set()
    self.var_out = set()

    if succeed_no is not None:
      self.succeed.append(succeed_no)
