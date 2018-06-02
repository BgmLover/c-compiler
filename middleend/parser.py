from . import logger
from .logger import Loggable
from .block import Block
from .block import VarNode
from .block import FunNode
from .block import ArrayNode


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
    else:
      self.parse_c_program(self.syntax_tree)

  """
  c_program
    : translation_unit
  """
  def parse_c_program(self, node):
    children = node['children']
    self.parse_translation_unit(children[0])

  """
  translation_unit
    : external_declaration
    | translation_unit external_declaration
  """
  def parse_translation_unit(self, node):
    children = node['children']
    if len(children) == 1:
      self.parse_external_declaration(children[0])
    else:
      self.parse_translation_unit(children[0])
      self.parse_external_declaration(children[1])

  """
  external_declaration
    : function_definition
    | declaration
  """
  def parse_external_declaration(self, node):
    children = node['children']
    if children[0]['name'] == 'function_definition':
      self.parse_function_definition(children[0])
    else:
      self.parse_declaration(children[0])

  def parse_function_definition(self, node):
    pass

  """
  declaration
    : declaration_specifiers ';'
    | declaration_specifiers init_declarator_list
  """
  def parse_declaration(self, node):
    pass

