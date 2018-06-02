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

  tmp_counter = 0
  def get_tmp(self):
    self.tmp_counter += 1
    return 'temp%d'%self.tmp_counter

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

  """
  expression
	  : assignment_expression
	  | expression ',' assignment_expression
  """
  def parse_expression(self, node):
    children = node['children']
    if children[0]['name'] == 'assignment_expression':
      self.parse_assignment_expression(children[0])
    else:
      self.parse_expression(children[0])
      self.parse_assignment_expression(children[1])

  """
  assignment_expression
    : logical_or_expression
    | unary_expression assignment_operator assignment_expression
  """
  def parse_assignment_expression(self, node):
    children = node['children']
    if children[0]['name'] == 'logical_or_expression':
      self.parse_logical_or_expression(children[0])
    else:
      pass #TODO

  """
  logical_or_expression
    : logical_and_expression
    | logical_or_expression OR_OP logical_and_expression
  """
  def parse_logical_or_expression(self, node):
    children = node['children']
    if children[0]['name'] == 'logical_and_expression':
      self.parse_logical_and_expression(children[0])


  """
  logical_and_expression
    : inclusive_or_expression
    | logical_and_expression AND_OP inclusive_or_expression
  """
  def parse_logical_and_expression(self, node):
    children = node['children']
    if children[0]['name'] == 'inclusive_or_expression':

  """
  inclusive_or_expression
    : exclusive_or_expression
    | inclusive_or_expression '|' exclusive_or_expression
  """
  def parse_inclusive_or_expression(self, node):
    children = node['children']
    if children[0]['name'] == 'exclusive_or_expression':
      return self.parse_exclusive_or_expression(children[0])
    else:
      pass #TODO

  """
  exclusive_or_expression
    : and_expression
    | exclusive_or_expression '^' and_expression
  """
  def parse_exclusive_or_expression(self, node):
    children = node['children']
    return children[0]['name'] == 'and_expression'





