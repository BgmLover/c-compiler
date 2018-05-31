from . import logger
from .logger import Loggable

class ParserError(Exception, Loggable):
  def __init__(self, node, message):
    self.row = node['row']
    self.col = node['col']
    self.message = message


class Parser:
  ir_writer = None
  syntax_tree = None

  def __init__(self, syntax_tree, ir_writer):
    self.syntax_tree = syntax_tree
    self.ir_writer = ir_writer

  def parse(self):
    if self.syntax_tree['name'] != 'c_program':
      err = ParserError(self.syntax_tree, 'Root node must be an "c_program"')
      logger.error(err)

