class TempElement:
  name=None
  type=None #'int'|...
  is_pointer=False

  def __init__(self, name=None, type=None, is_pointer=False):
    self.name=name
    self.type=type
    self.id=id
    self.is_pointer=is_pointer


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

