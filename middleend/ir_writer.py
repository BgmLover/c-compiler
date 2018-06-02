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
    code='LABEL '+label+":"
    self.CodeList.append(code)




