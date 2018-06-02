from . import logger
from .logger import Loggable
from .block import Block
from .elements import TempElement
from .elements import FunctionElement


class ParserError(Exception, Loggable):
  def __init__(self, node, message):
    self.row = node['row']
    self.col = node['col']
    self.message = message


class Parser:
  ir_writer = None
  syntax_tree = None
  block_stack = []
  function_pool = {}
  temp_counter = 0

  def lookup_variable(self, name):
    for block in reversed(self.block_stack):
      if name in block.variable_map:
        return block.variable_map[name]
    return None

  def create_temp(self, type):
    self.temp_counter += 1
    temp = TempElement(name='temp%d'%self.temp_counter, type=type)
    return temp

  def __init__(self, syntax_tree, ir_writer):
    self.syntax_tree = syntax_tree
    self.ir_writer = ir_writer
    #预置一个最大的Block
    whole_block=Block()
    self.block_stack.append(whole_block)

  def parse(self):
    #预定义两个已有函数
    printNode=FunctionElement("print", "void", True)
    paramNode=VarNode(type="int")
    printNode.arguments.append(paramNode)

    readNode=FunctionElement("read", "int", True)

    self.function_pool["print"]=printNode
    self.function_pool["read"]=readNode

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
    children=node['children']
    declaration_specifier=children[0]
    declarator=children[1]
    compound_statement=None

    if children[2]['name']=='declaration_list':
      declaration_list=children[2]
      compound_statement=children[3]
    else:
      compound_statement=children[2]

    #type_specifier
    function_type=declaration_specifier['children'][0]['content']
    function_name=declarator['children'][0]['children'][0]

    #function_node=FunctionElement(Name=function_name,Type=function_type,IsDefined=True)
    isDeclared=False
    declared_node=FunctionElement()

    if function_name in self.function_pool:
      if self.function_pool[function_name].isDefined :
        ParserError(node,'The function'+function_name+'has been defined before')
      else:
        declared_node=self.function_pool[function_name]

    function_block=Block()
    function_block.isfunction=True
    function_block.function_node=FunctionElement(name=function_name, return_type=function_type, is_definition=True)


    self.block_stack.append(function_block)
    self.function_pool[function_name]=function_block.function_node

    self.parse_parameter_list(declarator['children'][2],function_name)

    function_node=self.function_pool[function_name]
    if isDeclared:
      if function_node.type !=declared_node.type:
        ParserError(node,'The types are different between the defined and the declared')
      if function_node.arguments.__len__()!=declared_node.arguments.__len__():
        ParserError(node,'The number of parameters are different between the defined and the declared')
      for i in range(function_node.arguments.__len__()):
        if function_node.arguments[i].type!=declared_node.arguments[i].type:
          ParserError(node, 'The type of parameters are different between the defined and the declared')

    self.parser_compound_statement()

    self.block_stack.pop(-1)

    return None




  """
  declaration
    : declaration_specifiers ';'
    | declaration_specifiers init_declarator_list
  """
  def parse_declaration(self, node):
    return None
  def parser_compound_statement(self):
    pass

  def parse_parameter_list(self,node,function_name):
    if node['children'][0]['name']=='parameter_list':
      self.parse_parameter_list(node['children'][0],function_name)
      self.parse_parameter_declaration(node['children'][2])
    else:
      self.parse_parameter_declaration(node['children'][0],function_name)

  def parse_parameter_declaration(self,node,function_name):
    type_specifier=node['children'][0]
    declarator=node['children'][1]
    var_type=type_specifier['children'][0]['content']
    if var_type=='VOID':
      message=r"var with type void can't be parameter"
      ParserError(node,message)

    var_name=declarator['children'][0]['content']
    var_node=VarNode(name=var_name,type=var_type)


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





