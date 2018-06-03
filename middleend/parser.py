from . import logger
from .logger import Loggable
from .block import Block
from .elements import TempElement, ConstantElement, FunctionElement, IdentifierElement


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
  label_counter = 0

  def lookup_variable(self, identifier):
    if isinstance(identifier, IdentifierElement):
      identifier = identifier.name
    for block in reversed(self.block_stack):
      if identifier in block.variable_map:
        return block.variable_map[identifier]
    return None

  def lookup_variable_current_block(self,name):
    if name in self.block_stack[-1]:
      return self.block_stack[-1][name]
    return None

  def create_temp(self, type):
    self.temp_counter += 1
    temp = TempElement(name='temp%d'%self.temp_counter, type=type)
    return temp

  def create_label(self):
    self.label_counter += 1
    return 'label%d'%self.label_counter

  def do_binomial_operation(self, src1, operand, src2, type='int'):
    result = self.create_temp(type)
    self.ir_writer.binomial_operation(
      result,
      src1,
      operand,
      src2
    )
    return result

  def __init__(self, syntax_tree, ir_writer):
    self.syntax_tree = syntax_tree
    self.ir_writer = ir_writer
    #预置一个最大的Block
    whole_block=Block()
    self.block_stack.append(whole_block)

  def parse(self):
    #预定义两个已有函数
    print_node=FunctionElement("print", "void", True)
    param_node=TempElement(type="int")
    print_node.arguments.append(param_node)

    read_node=FunctionElement("read", "int", True)

    self.function_pool["print"]=print_node
    self.function_pool["read"]=read_node

    if self.syntax_tree['name'] != 'c_program':
      err = ParserError(self.syntax_tree, 'Root node must be an "c_program"')
      logger.error(err)
    else:
      self.parse_c_program(self.syntax_tree)

  """
  c_program
    : translation_unit
  """
  def parse_c_program(self, node:dict):
    children = node['children']
    self.parse_translation_unit(children[0])

  """
  translation_unit
    : external_declaration
    | translation_unit external_declaration
  """
  def parse_translation_unit(self, node:dict):
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
  def parse_external_declaration(self, node:dict):
    children = node['children']
    if children[0]['name'] == 'function_definition':
      self.parse_function_definition(children[0])
    else:
      self.parse_declaration(children[0])

  def parse_function_definition(self, node:dict):
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
    function_name=declarator['children'][0]['children'][0]['content']

    #function_node=FunctionElement(Name=function_name,Type=function_type,IsDefined=True)
    is_declared=False
    declared_node=FunctionElement()
    #函数名和已有定义函数重复
    if function_name in self.function_pool:
      if self.function_pool[function_name].isDefined :
        ParserError(node,'The function'+function_name+'has been defined before')
      else:
        declared_node=self.function_pool[function_name]
    #函数名与全局变量名冲突
    if self.lookup_variable_current_block(function_name):
      ParserError(node,'The function'+function_name+'has been declared as variable before')

    function_block=Block()
    function_block.function_node=FunctionElement(name=function_name, return_type=function_type, is_definition=True)


    self.block_stack.append(function_block)
    self.function_pool[function_name]=function_block.function_node
    #带参函数
    if declarator['children'][2]['name']=='parameter_list':
      self.parse_parameter_list(declarator['children'][2],function_name)


    function_node=self.function_pool[function_name]
    if is_declared:
      if function_node.type !=declared_node.type:
        ParserError(node,'The types are different between the defined and the declared')
      if function_node.arguments.__len__()!=declared_node.arguments.__len__():
        ParserError(node,'The number of parameters are different between the defined and the declared')
      for i in range(function_node.arguments.__len__()):
        if function_node.arguments[i].type!=declared_node.arguments[i].type:
          ParserError(node, 'The type of parameters are different between the defined and the declared')

    self.ir_writer.create_function(function_node) #此处输出代码   Function f(var1,var2...)这样形式

    self.parser_compound_statement()

    self.block_stack.pop(-1)

    return None




  """
  declaration
    : declaration_specifiers ';'
    | declaration_specifiers init_declarator_list
  """
  def parse_declaration(self, node:dict):
    declaration_specifiers=node['children'][0]
    #这种情况形如  int ;  不需要继续解析
    if node['children'][1]['content']==';':
      return None

    var_type=declaration_specifiers['childern'][0]['content']
    if var_type=='void':
      message=r"void can't be declaration specifier"
      ParserError(node,message)
    init_declarator_list=node['children'][1]
    self.parse_init_declarator_list(var_type,init_declarator_list)
    return None

  """
  init_declarator_list:
      init_declarator
    | init_declarator_list ',' init_declarator
  """
  def parse_init_declarator_list(self,var_type,node):
    if node['children'][0]['name'] == 'init_declarator_list':
      self.parse_init_declarator_list(var_type,node['children'][0])
      self.parse_init_declarator(var_type,node['children'][2])
    else:
      self.parse_init_declarator(var_type, node['children'][0])
    return  None

  """
  init_declarator:
      declarator
    | declarator '=' initializer
  """
  def parse_init_declarator(self, var_type, node):
    declarator=node['children'][0]
    if node['children'].__len__()==1:
      if declarator['children'][0]['name']=='IDENTIFIER':
        id=declarator['children'][0]
        var_name=id['content']
        if self.lookup_variable_current_block(var_name)==None:  #在当前作用域查找，这个变量不能重复定义
          var_element=self.create_temp(var_type)
          self.block_stack[-1][var_name]=var_element
        else:
          ParserError(node,r'the IDENTIFIER'+var_name+'has been declared before')
      else:
        # 数组
        if declarator['children'][1]['name']=='[':
          pointer_name=declarator['children'][0]['children'][0]['content']
          assignment_exp=declarator['children'][2]
          #这里返回一个Temp_element
          assignment_element=self.parse_assignment_expression(assignment_exp)
          if assignment_element.type!='int':
            ParserError(node,r'the size of the array must be integer')
          


  def parser_compound_statement(self):
    pass#TODO

  """
  parameter_list
	: parameter_declaration
	| parameter_list ',' parameter_declaration
	
	"""

  def parse_parameter_list(self,node,function_name):
    if node['children'][0]['name']=='parameter_list':
      self.parse_parameter_list(node['children'][0],function_name)
      self.parse_parameter_declaration(node['children'][2],function_name)
    else:
      self.parse_parameter_declaration(node['children'][0],function_name)

  """
    parameter_declaration:
      type_specifier declarator
    | type_specifier    //这种情况先不管
  """

  def parse_parameter_declaration(self,node,function_name):
    type_specifier=node['children'][0]
    declarator=node['children'][1]
    var_type=type_specifier['children'][0]['content']
    if var_type=='void':
      message=r"var with type void can't be parameter"
      ParserError(node,message)

    var_name=declarator['children'][0]['content']
    var_node=self.create_temp(var_type)

    self.function_pool[function_name].arguments.append(var_node)  #把参数写到function_element里的参数列表里
    self.block_stack[-1].variable_map[var_name]=var_node


  """
  expression
	  : assignment_expression
	  | expression ',' assignment_expression
  """
  def parse_expression(self, node:dict) -> TempElement or ConstantElement:
    children = node['children']
    if children[0]['name'] == 'assignment_expression':
      return self.parse_assignment_expression(children[0])
    else:
      self.parse_expression(children[0])
      return self.parse_assignment_expression(children[1])

  """
  assignment_expression
    : logical_or_expression
    | unary_expression assignment_operator assignment_expression
  """
  def parse_assignment_expression(self, node:dict) -> TempElement or ConstantElement:
    children = node['children']
    if children[0]['name'] == 'logical_or_expression':
      return self.parse_logical_or_expression(children[0])
    else:
      left = self.parse_unary_expression(children[0])
      right = self.parse_assignment_expression(children[2])
      if children[1]['name'] == '=':
        self.ir_writer.assignment(
          left,
          right
        )
      else:
        self.ir_writer.binomial_operation(
          left,
          left,
          children[1]['name'][:-1],
          right
        )
      return left

  """
  logical_or_expression
    : logical_and_expression
    | logical_or_expression OR_OP logical_and_expression
  """
  def parse_logical_or_expression(self, node:dict) -> TempElement or ConstantElement:
    children = node['children']
    if children[0]['name'] == 'logical_and_expression':
      self.parse_logical_and_expression(children[0])
    else:
      return self.do_binomial_operation(
        self.parse_logical_or_expression(children[0]),
        '||',
        self.parse_logical_and_expression(children[2])
      )


  """
  logical_and_expression
    : inclusive_or_expression
    | logical_and_expression AND_OP inclusive_or_expression
  """
  def parse_logical_and_expression(self, node:dict) -> TempElement or ConstantElement:
    children = node['children']
    if children[0]['name'] == 'inclusive_or_expression':
      return self.parse_inclusive_or_expression(children[0])
    else:
      return self.do_binomial_operation(
        self.parse_logical_and_expression(children[0]),
        '&&',
        self.parse_inclusive_or_expression(children[2])
      )

  """
  inclusive_or_expression
    : exclusive_or_expression
    | inclusive_or_expression '|' exclusive_or_expression
  """
  def parse_inclusive_or_expression(self, node:dict) -> TempElement or ConstantElement:
    children = node['children']
    if children[0]['name'] == 'exclusive_or_expression':
      return self.parse_exclusive_or_expression(children[0])
    else:
      return self.do_binomial_operation(
        self.parse_inclusive_or_expression(children[0]),
        '|',
        self.parse_exclusive_or_expression(children[2])
      )

  """
  exclusive_or_expression
    : and_expression
    | exclusive_or_expression '^' and_expression
  """
  def parse_exclusive_or_expression(self, node:dict) -> TempElement or ConstantElement:
    children = node['children']
    if children[0]['name'] == 'and_expression':
      return self.parse_and_expression(children[0])
    else:
      return self.do_binomial_operation(
        self.parse_exclusive_or_expression(children[0]),
        '^',
        self.parse_and_expression(children[2])
      )

  """
  and_expression
    : equality_expression
    | and_expression '&' equality_expression
  """
  def parse_and_expression(self, node:dict) -> TempElement or ConstantElement:
    children = node['children']
    if children[0]['name'] == 'equality_expression':
      return self.parse_equality_expression(children[0])
    else:
      return self.do_binomial_operation(
        self.parse_and_expression(children[0]),
        '&',
        self.parse_equality_expression(children[2])
      )

  """
  equality_expression
    : relational_expression
    | equality_expression EQ_OP relational_expression
    | equality_expression NE_OP relational_expression
  """
  def parse_equality_expression(self, node:dict) -> TempElement or ConstantElement:
    children = node['children']
    if children[0]['name'] == 'relational_expression':
      return self.parse_relational_expression(children[0])
    else:
      return self.do_binomial_operation(
        self.parse_equality_expression(children[0]),
        children[1]['name'],
        self.parse_relational_expression(children[2])
      )

  """
  relational_expression
    : shift_expression
    | relational_expression '<' shift_expression
    | relational_expression '>' shift_expression
    | relational_expression LE_OP shift_expression
    | relational_expression GE_OP shift_expression
  """
  def parse_relational_expression(self, node:dict) -> TempElement or ConstantElement:
    children = node['children']
    if len(children) == 1:
      return self.parse_shift_expression(children[0])
    else:
      return self.do_binomial_operation(
        self.parse_relational_expression(children[0]),
        children[1]['name'],
        self.parse_shift_expression(children[2])
      )

  """
  shift_expression
    : additive_expression
    | shift_expression LEFT_OP additive_expression
    | shift_expression RIGHT_OP additive_expression
  """
  def parse_shift_expression(self, node:dict) -> TempElement or ConstantElement:
    children = node['children']
    if len(children) == 1:
      return self.parse_additive_expression(children[0])
    else:
      return self.do_binomial_operation(
        self.parse_relational_expression(children[0]),
        children[1]['name'],
        self.parse_shift_expression(children[2])
      )

  """
  additive_expression
    : multiplicative_expression
    | additive_expression '+' multiplicative_expression
    | additive_expression '-' multiplicative_expression
  """
  def parse_additive_expression(self, node:dict) -> TempElement or ConstantElement:
    children = node['children']
    if len(children) == 1:
      return self.parse_multiplicative_expression(children[0])
    else:
      return self.do_binomial_operation(
        self.parse_additive_expression(children[0]),
        children[1]['name'],
        self.parse_multiplicative_expression(children[2])
      )

  """
  multiplicative_expression
    : unary_expression
    | multiplicative_expression '*' unary_expression
    | multiplicative_expression '/' unary_expression
    | multiplicative_expression '%' unary_expression
  """
  def parse_multiplicative_expression(self, node:dict) -> TempElement or ConstantElement:
    children = node['children']
    if len(children) == 1:
      return self.parse_unary_expression(children[0])
    else:
      return self.do_binomial_operation(
        self.parse_multiplicative_expression(children[0]),
        children[1]['name'],
        self.parse_unary_expression(children[2])
      )

  """
  unary_expression
    : postfix_expression
    | INC_OP unary_expression
    | DEC_OP unary_expression
    | unary_operator unary_expression
  """
  def parse_unary_expression(self, node:dict, target_type:str='temp') -> TempElement or ConstantElement:
    children = node['children']
    if children[0]['name']:
      e = self.parse_postfix_expression(children[0])
      if isinstance(e, IdentifierElement):
        if target_type == 'function':
          return self.lookup_function(e)
        else:
          return self.lookup_variable(e)
      else:
        return e
    else:
      u = self.parse_unary_expression(children[1])
      if isinstance(u, IdentifierElement):
        u = self.lookup_variable(u)
      if isinstance(u, TempElement):
        err = ParserError(node, 'Expression should be modifiable.')
        logger.error(err)
      if children[0]['name'] == '++' or children[0]['name'] == '++':
        self.ir_writer.binomial_operation(
          u,
          u,
          children[0]['name'][:1],
          1
        )
      else:
        self.ir_writer.unary_operation(
          u,
          children[0],
          u
        )
      return u

  """
  postfix_expression
    : primary_expression
    | postfix_expression '[' expression ']'
    | postfix_expression '(' ')'
    | postfix_expression '(' argument_expression_list ')'
    | postfix_expression INC_OP
    | postfix_expression DEC_OP
  """
  def parse_postfix_expression(self, node:dict) -> TempElement or ConstantElement or IdentifierElement:
    children = node['children']
    if len(children):
      return self.parse_primary_expression(children[0])
    else:
      e = self.parse_postfix_expression(children[0])
      if children[1]['name'] == '[':
        if isinstance(e, IdentifierElement):
          e = self.lookup_variable(e)
        result = self.create_temp(e.type)
        self.ir_writer.unary_operation(
          result,
          str(e)+'['+str(self.parse_expression(children[2]))+']'
        )
        return result
      elif children[1]['name'] == '(':
        pass
      elif children[1]['name'] == '++':
        if isinstance(e, IdentifierElement):
          e = self.lookup_variable(e)
        result = self.create_temp(e.type)


  """
  primary_expression:
    : IDENTIFIER
    | CONSTANT_INT
    # | CONSTANT_DOUBLE
    # | STRING_LITERAL
    | '(' expression ')'
  """
  def parse_primary_expression(self, node:dict) -> TempElement or IdentifierElement or ConstantElement:
    children = node['children']
    if children[0]['name'] == 'identifier':
      return IdentifierElement(children[0]['content'])
    elif children[0]['name'] == 'constant_int':
      return ConstantElement('int', children[0]['content'])
    else:
      return self.parse_expression(children[1])









