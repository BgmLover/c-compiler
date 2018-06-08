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
