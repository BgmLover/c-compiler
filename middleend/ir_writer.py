from middleend.elements import TempElement, FunctionElement, ConstantElement

class IRWriter:
  outfile = None

  CodeList=[]

  def write(self):
    for code in self.CodeList:
      self.outfile.write(code+'\n')

  def __init__(self, path):
    self.outfile = open(path,"w")

  def create_label(self, label):
    #self.outfile.write('LABEL %s:\n'%label)
    code='LABEL '+label+':'
    self.CodeList.append(code)

  def binomial_operation(self, dist, src1, operand, src2):
    self.assignment(
      dist,
      str(src1) + ' ' + operand + ' ' + str(src2)
    )

  def unary_operation(self, dist, operand, src):
    self.assignment(
      dist,
      operand + ' ' + str(src)
    )

  def malloc_array(self,src):
    code='MALLOC '+str(src)
    self.CodeList.append(code)

  def assignment(self, dist, src):
    code = str(dist) + ' := ' + str(src)
    self.CodeList.append(code)

  def create_function(self,function_element):
    code='Function '+function_element.name+'('
    param_list=''
    for param in function_element.arguments:
      param_list += str(param) + ','
    param_list=param_list[:-1]
    code=code+param_list+')'+':'
    self.CodeList.append(code)

  def call_function(self, function:FunctionElement, arguments, save_to:TempElement=None):
    arguments_str = ''
    for argument in arguments:
      arguments_str += str(argument) + ','
    arguments_str = arguments_str[:-1]
    code = 'CALL '+str(function)+'('+arguments_str+')'
    if save_to is not None:
      code = str(save_to) + ' := ' + code
    self.CodeList.append(code)

  def goto(self, label:str):
    code = 'GOTO '+label
    self.CodeList.append(code)

  def if_goto(self, condition: ConstantElement or TempElement, label:str):
    code = 'IF '+str(condition)+' GOTO '+label
    self.CodeList.append(code)

  def if_not_goto(self, condition: ConstantElement or TempElement, label:str):
    code = 'IFNOT '+str(condition)+' GOTO '+label
    self.CodeList.append(code)

  def return_null(self):
    code='RETURN'
    self.CodeList.append(code)

  def return_value(self,value):
    code='RETURN '+str(value)
    self.CodeList.append(code)

