
stack_frames = []

class StackFrame:
  # TODO fp寄存器是什么时候被初始化的？
  use_amount = 0
  params = None
  def request_space(self, amount:int):
    self.use_amount += amount
    return self.use_amount - 4
