class MIPSWriter:
  outfile = None

  CodeList=[]

  def write(self, code):
    self.outfile.write('\t'+code+'\n')

  def write_label(self, label):
    self.outfile.write(label+'\n')

  def __init__(self, path):
    self.outfile = open(path,"w")

  def sw(self, reg, address, offset=0):
    self.write('sw $'+reg+','+str(offset)+'($'+address+')')

  def lw(self, reg, address, offset=0):
    self.write('sw $'+reg+','+str(offset)+'($'+address+')')

  def addi(self, dst, src, immediate=0):
    self.write('addi $'+str(dst)+',$'+str(src)+','+str(immediate))

  def jal(self, label):
    self.write('jal '+label)

  def jr(self, reg):
    self.write('jr $'+reg)

