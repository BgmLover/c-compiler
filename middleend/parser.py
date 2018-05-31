class Parser:
  ir_writer = None
  syntax_tree = None

  def __init__(self, syntax_tree, ir_writer):
    self.syntax_tree = syntax_tree
    self.ir_writer = ir_writer

  def parse(self):
    pass

