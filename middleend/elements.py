class TempElement:
  name=None
  type=None #'int'|...
  is_pointer=False

  def __init__(self, name=None, type=None, is_pointer=False):
    self.name=name
    self.type=type
    self.is_pointer=is_pointer

  def __str__(self):
    return self.name


class ConstantElement:
  type = None #'int'|...
  value = None

  def __init__(self, type=None, value=None):
    self.type = type
    self.value = value

  def __str__(self):
    return self.value


class ArrayItemElement:
  array:TempElement = None
  index: TempElement or ConstantElement = None

  def __init__(self, array:TempElement=None, index: TempElement or ConstantElement=None):
    self.array = array
    self.index = index

  def __str__(self):
    return str(self.array) +'[' + str(self.index) + ']'



class IdentifierElement:
  name = None

  def __init__(self, name=None):
    self.name = name

  def __str__(self):
    return self.name


class FunctionElement:
  is_defined=False
  name=None
  return_type=None
  arguments=[]

  def __init__(self, name=None, return_type=None, is_definition=False, arguments=None):
    self.is_defined=is_definition
    self.name=name
    self.type=return_type
    self.arguments=arguments

  def __str__(self):
    return self.name

