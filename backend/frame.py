
stack_frames = []

class StackFrame:
  use_amount = 0
  params = None
  def request_space(self, amount:int):
    self.use_amount += amount
    return self.use_amount
