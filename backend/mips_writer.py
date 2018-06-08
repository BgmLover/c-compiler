class MIPSWriter:
  outfile = None

  CodeList=[]

  def write(self, code):
    self.outfile.write('\t'+code+'\n')
  def li(self,dst,constant):
    self.write('li $'+dst+','+constant)
  def move(self,dst,src):
    self.write('move $'+dst+','+src)
  def sw(self, reg, address, offset=0):
    self.write('sw $'+reg+','+str(offset)+'($'+address+')')

  def lw(self, reg, address, offset=0):
    self.write('sw $'+reg+','+str(offset)+'($'+address+')')

  def addi(self, dst, src, immediate=0):
    self.write('addi $'+str(dst)+',$'+str(src)+','+str(immediate))
  def ori(self, dst, src, immediate=0):
    self.write('ori $'+str(dst)+',$'+str(src)+','+str(immediate))
  def xori(self, dst, src, immediate=0):
    self.write('xori $'+str(dst)+',$'+str(src)+','+str(immediate))

  def subi(self, dst, src, immediate=0):
    self.write('subi $'+str(dst)+',$'+str(src)+','+str(immediate))

  def add(self,dst,src1,src2):
    self.write('add $' + str(dst) + ',$' + str(src1) + ',' + str(src2))

  def xor(self,dst,src1,src2):
    self.write('xor $' + str(dst) + ',$' + str(src1) + ',' + str(src2))

  def slt(self,dst,src1,src2):
    self.write('slt $' + str(dst) + ',$' + str(src1) + ',' + str(src2))
  def slti(self,dst,src1,constant):
    self.write('slt $' + str(dst) + ',$' + str(src1) + ',' + str(constant))
  def sll(self,dst,src1,src2):
    self.write('sll $' + str(dst) + ',$' + str(src1) + ',' + str(src2))

  def sllv(self,dst,src1,src2):
    self.write('sllv $' + str(dst) + ',$' + str(src1) + ',' + str(src2))

  def srl(self,dst,src1,src2):
    self.write('srl $' + str(dst) + ',$' + str(src1) + ',' + str(src2))

  def srlv(self,dst,src1,src2):
    self.write('srlv $' + str(dst) + ',$' + str(src1) + ',' + str(src2))

  def and_(self,dst,src1,src2):
    self.write('and $' + str(dst) + ',$' + str(src1) + ',' + str(src2))

  def or_(self,dst,src1,src2):
    self.write('or $' + str(dst) + ',$' + str(src1) + ',' + str(src2))

  def sub(self,dst,src1,src2):
    self.write('sub $' + str(dst) + ',$' + str(src1) + ',' + str(src2))

  def mul(self, dst, src1, src2):
    self.write('mul $' + str(dst) + ',$' + str(src1) + ',' + str(src2))

  def div(self, dst, src1, src2):
    self.write('div $' + str(dst) + ',$' + str(src1) + ',' + str(src2))

  def jal(self, label):
    self.write('jal '+label)

  def jr(self, reg):
    self.write('jr $'+reg)
  def j(self,label):
    self.write('j ' + label)
  def write_label(self, label):
    self.outfile.write(label+'\n')
  def le(self,reg1,reg2,reg3):
    self.write('slt $'+reg1+','+reg2+','+reg3)
    self.write('nor $'+reg1+','+reg1+','+'$zero')

  def lei(self,reg1,reg2,constant):
    self.write('slti $'+reg1+','+reg2+','+constant)
    self.write('nor $'+reg1+','+reg1+','+'$zero')

  def write_function_label(self, function_name):
    self.outfile.write(function_name + ':\n')

  def bne(self,reg,label):
    self.write('bne $'+reg+','+'$zero,'+label)

  def beq(self,reg,label):
    self.write('bne $'+reg+','+'$zero,'+label)

  def __init__(self, path):
    self.outfile = open(path, "w")
    template = '''.data
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
   jr $ra\n\n'''
    self.outfile.write(template)

