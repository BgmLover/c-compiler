

stack_frames = []

class StackFrame:
  # TODO sp/fp寄存器是什么时候被初始化的？
  use_amount = 0
  params = None
  mips_writer = None
  def __init__(self, mips_writer):
    self.mips_writer = mips_writer
  def request_space(self, amount:int):
    self.mips_writer.addi('sp', 'sp', -amount)
    self.use_amount += amount
    return self.use_amount - 4
