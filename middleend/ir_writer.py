from .elements import TempElement

class IRWriter:
  outfile = None
  id_temp=0
  id_label=0
  id_var=0      #var 和 array 也许不需要用到数字id来命名
  id_array=0

  CodeList=[]

  def __init__(self, path):
    self.outfile = open(path)

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

  def assignment(self, dist, src):
    code = str(dist) + ' := ' + str(src)
    self.CodeList.append(code)

  def create_function(self,function_element):
    code='Function '+function_element.name+'('
    for param in function_element.argument:
      code+=param.name+','
    code+=')'
    self.CodeList.append(code)

  def assignment(self, dist, src):
    code = str(dist)+' := '+str(src)
    self.CodeList.append(code)






