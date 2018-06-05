from . import logger
from .logger import Loggable
from .block import Block
from .elements import TempElement, ConstantElement, FunctionElement, IdentifierElement, ArrayItemElement
from typing import List



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

  def add_label_to_current_block(self,label,identifier,node):
    if str(identifier) in self.block_stack[-1]:
      message='the label has been declared'
      raise ParserError(node,message)
    self.block_stack[-1].label_map[str(identifier)]=label

  def lookup_variable(self, identifier,node):
    for block in reversed(self.block_stack):
      if str(identifier) in block.variable_map:
        return block.variable_map[str(identifier)]
    message="can't find the variable"+str(identifier)+" in all blocks"
    raise ParserError(node,message)

  def lookup_variable_current_block(self,identifier,node):
    if str(identifier) in self.block_stack[-1]:
      return self.block_stack[-1][str(identifier)]
    message = "can't find the variable" + str(identifier) + " in the current block"
    raise ParserError(node, message)

  def lookup_label(self,identifier,node):
    for block in reversed(self.block_stack):
      if str(identifier) in block.label_map:
        return block.label_map[str(identifier)]
    message = "can't find the label" + str(identifier) + " in all blocks"
    raise ParserError(node, message)


  def lookup_function(self,identifier,node):
    if str(identifier) in self.function_pool:
      return self.function_pool[str(identifier)]
    else:
      message = "can't find the function" + str(identifier) + " in the block_stack"
      raise ParserError(node,message)

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
        logger.error(ParserError(node,'The function'+function_name+'has been defined before'))
      else:
        declared_node=self.function_pool[function_name]
    #函数名与全局变量名冲突
    if self.lookup_variable_current_block(function_name):
      logger.error(ParserError(node,'The function'+function_name+'has been declared as variable before'))

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
        logger.error(ParserError(node,'The types are different between the defined and the declared'))
      if function_node.arguments.__len__()!=declared_node.arguments.__len__():
        logger.error(ParserError(node,'The number of parameters are different between the defined and the declared'))
      for i in range(function_node.arguments.__len__()):
        if function_node.arguments[i].type!=declared_node.arguments[i].type:
          logger.error(ParserError(node, 'The type of parameters are different between the defined and the declared'))

    self.ir_writer.create_function(function_node) #此处输出代码   Function f(var1,var2...)这样形式

    self.parse_compound_statement(compound_statement)

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
      logger.error(ParserError(node,message))
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
          logger.error(ParserError(node,r'the IDENTIFIER'+var_name+'has been declared before'))
      else:
        # 数组(这里还没有考虑int 和 double的问题）
        if declarator['children'][1]['name']=='[':
          #pointer_name=declarator['children'][0]['children'][0]['content']
          var_element=self.create_temp(var_type)
          self.block_stack[-1].variable_map[var_element.name]=var_element
          assignment_exp=declarator['children'][2]
          #这里返回一个Temp_element
          assignment_element=self.parse_assignment_expression(assignment_exp)
          if assignment_element.type!='int':
            logger.error(ParserError(node,r'the size of the array must be integer'))
            array_item_element=ArrayItemElement(var_element,assignment_element)
            self.ir_writer.malloc_array(array_item_element)
        # 函数
        if declarator['children'][1]['name']=='(':
          function_name=declarator['children'][0]['children'][0]['content']
          if self.block_stack.__len__()>1:
            logger.error(ParserError(node,"Function declaration must be at global environment"))
          #有参函数
          if declarator['children'][2]['name']=='parameter_list':
            parameter_list =declarator['children'][2]
            function_element=FunctionElement(function_name,var_type)
            self.function_pool[function_name]=function_element
            self.parse_parameter_list(parameter_list,function_name)
    else:
      if node['children'][1]['name']=='=':
        var_element = self.create_temp(var_type)
        if declarator['children'][0]['name']=='IDENTIFIER':
          identifier=declarator['children'][0]
          var_name=IdentifierElement(identifier['name'])
          try:
            self.lookup_variable_current_block(var_name,node)
          except:
            var_element.name=var_name
            self.block_stack[-1].variable_map[var_name]=var_element
          else:
            logger.error(ParserError(node,"the variable has been declared before"))
        else:
          logger.error(ParserError(node, "it's not a variable"))
        if node['children'][2]['children'][0]['name']=='assignment_expression':
          assignment_element=self.parse_assignment_expression(node['children'][2]['children'][0])
          self.ir_writer.assignment(var_element,assignment_element)

  '''
  compound_statement:
     '{' '}'
    | '{' block_item_list '}'
  '''
  def parse_compound_statement(self,node):
    if node['children'][1]['name']=='block_item_list':
      block_item_list=node['children'][1]
      self.parse_block_item_list(block_item_list)

  '''
  block_item_list:
      block_item
    | block_item_list block_item
  '''
  def parse_block_item_list(self,node):
    if node['children'][0]['name']=='block_item_list':
      self.parse_block_item_list(node)
      self.parse_block_item(node)
    else:
      self.parse_block_item(node)

  '''
  block_item:
      declaration
    | statement
  '''
  def parse_block_item(self,node):
    if node['children'][0]['name']=='declaration':
      self.parse_statement(node)
    else:
      self.parse_declaration(node)

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
      logger.error(ParserError(node,message))

    var_name=declarator['children'][0]['content']
    var_node=self.create_temp(var_type)

    self.function_pool[function_name].arguments.append(var_node)  #把参数写到function_element里的参数列表里
    self.block_stack[-1].variable_map[var_name]=var_node


  """
  expression
	  : assignment_expression
	  | expression ',' assignment_expression
  """
  def parse_expression(self, node:dict) -> TempElement or ConstantElement or ArrayItemElement:
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
  def parse_assignment_expression(self, node:dict) -> TempElement or ConstantElement or ArrayItemElement:
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
  def parse_logical_or_expression(self, node:dict) -> TempElement or ConstantElement or ArrayItemElement:
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
  def parse_logical_and_expression(self, node:dict) -> TempElement or ConstantElement or ArrayItemElement:
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
  def parse_inclusive_or_expression(self, node:dict) -> TempElement or ConstantElement or ArrayItemElement:
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
  def parse_exclusive_or_expression(self, node:dict) -> TempElement or ConstantElement or ArrayItemElement:
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
  def parse_and_expression(self, node:dict) -> TempElement or ConstantElement or ArrayItemElement:
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
  def parse_equality_expression(self, node:dict) -> TempElement or ConstantElement or ArrayItemElement:
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
  def parse_relational_expression(self, node:dict) -> TempElement or ConstantElement or ArrayItemElement:
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
  def parse_shift_expression(self, node:dict) -> TempElement or ConstantElement or ArrayItemElement:
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
  def parse_additive_expression(self, node:dict) -> TempElement or ConstantElement or ArrayItemElement:
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
  def parse_multiplicative_expression(self, node:dict) -> TempElement or ConstantElement or ArrayItemElement:
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
  def parse_unary_expression(self, node:dict) -> TempElement or ConstantElement or ArrayItemElement:
    children = node['children']
    if children[0]['name']:
      return self.parse_postfix_expression(children[0])
    else:
      u = self.parse_unary_expression(children[1])
      if isinstance(u, ConstantElement):
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
  def parse_postfix_expression(self, node:dict, target_type:str='temp') -> TempElement or ConstantElement or ArrayItemElement or FunctionElement:
    children = node['children']
    if len(children) == 0:
      e = self.parse_primary_expression(children[0])
      if isinstance(e, IdentifierElement):
        if target_type == 'function':
          return self.lookup_function(e, children[0])
        else:
          return self.lookup_variable(e, children[0])
      else:
        return e
    else:
      if children[1]['name'] == '[':
        v = self.parse_postfix_expression(children[0])
        return ArrayItemElement(v, self.parse_expression(children[2]))
      elif children[1]['name'] == '(':
        f = self.parse_postfix_expression(children[0], 'function')
        if len(children) == 4:
          arguments = self.parse_argument_expression_list(children[2])
        else:
          arguments = []
        self.ir_writer.call_function(f, arguments)
      else: # ++ and --
        v = self.parse_postfix_expression(children[0])
        result = self.create_temp(v.type)
        self.ir_writer.assignment(
          result,
          v
        )
        self.ir_writer.binomial_operation(
          v,
          v,
          children[1]['name'][:1],
          1
        )
        return result


  """
  primary_expression
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

  """
  argument_expression_list
    : assignment_expression
    | argument_expression_list ',' assignment_expression
  """
  def parse_argument_expression_list(self, node:dict) -> List[TempElement or ConstantElement or ArrayItemElement]:
    children = node['children']
    if len(children) == 1:
      return [self.parse_assignment_expression(children[0])]
    else:
      arguments = self.parse_argument_expression_list(children[0])
      arguments.append(self.parse_assignment_expression(children[2]))
      return arguments

  """
  statement
    : compound_statement
    | labeled_statement
    | expression_statement
    | selection_statement
    | iteration_statement
    | jump_statement
  """
  def parse_statement(self, node:dict, case_compare_element=None):
    child = node['children'][0]
    child_name = child['name']
    if child_name == 'compound_statement':
      self.parse_compound_statement(child)
    elif child_name == 'labeled_statement':
      self.parse_labeled_statement(child, case_compare_element)
    elif child_name == 'expression_statement':
      self.parse_expression_statement(child)
    elif child_name == 'selection_statement':
      self.parse_selection_statement(child)
    elif child_name == 'iteration_statement':
      self.parse_iteration_statement(child)
    else:
      self.parse_jump_statement(child)

  """
  expression_statement
    : ';'
    | expression ';'
  """
  def parse_expression_statement(self, node:dict) -> None:
    children = node['children']
    if len(children) == 2:
      self.parse_expression(children[0])

  """
  labeled_statement
    : IDENTIFIER ':' statement
    | CASE logical_or_expression ':' statement
    | DEFAULT ':' statement
  """
  def parse_labeled_statement(self, node:dict, case_compare_element=None) -> None:
    children = node['children']
    label = self.create_label()
    finish_label = self.create_label()
    if children[0]['name'] == 'case':
      condition = self.create_temp('int')
      self.ir_writer.binomial_operation(
        condition,
        case_compare_element,
        '==',
        self.parse_logical_or_expression(children[1])
      )
      self.ir_writer.conditional_goto(condition, label)
      self.ir_writer.goto(finish_label)
    elif children[0]['name'] == 'default':
      pass # do nothing
    else:
      self.add_label_to_current_block(label, children[0]['content'], children[0])
    self.ir_writer.create_label(label)
    self.parse_statement(children[-1], case_compare_element)
    self.ir_writer.create_label(finish_label)
    



  """
  selection_statement
    : IF '(' expression ')' statement ELSE statement
    | IF '(' expression ')' statement %prec LOWER_THAN_ELSE
    | SWITCH '(' expression ')' statement
  """
  def parse_selection_statement(self, node:dict):
    children = node['children']
    if children[0]['name'] == 'switch':
      t = self.parse_expression(children[2])
      nodes = children[4]['children']
      if nodes[0]['name'] != 'compound_statement':
        raise ParserError(node[0], 'Compound statement needed.')
      nodes = children[0]['children']
      if len(nodes) == 2:
        return
      nodes = children[1]['children']
      def handle_block_item(n:dict):
        if n['name'] != 'statement':
          raise ParserError(n, 'Switch block can only contain statements.')
        self.parse_statement(n, t)
      while len(nodes) == 2:
        handle_block_item(nodes[1])
        nodes = nodes[0]['children']
      handle_block_item(nodes[0])





  '''
  iteration_statement:
      WHILE '(' expression ')' statement
    | DO statement WHILE '(' expression ')' ';'
    | FOR '(' expression_statement expression_statement ')' statement
    | FOR '(' expression_statement expression_statement expression ')' statement
  '''
  def parse_iteration_statement:



