class VarNode:
  name=None
  type=None
  id=-1
  useAddress=False

  def __init__(self,name=None,type=None,id=-1,use_address=False):
    self.name=name
    self.type=type
    self.id=id
    self.useAddress=use_address


class FunNode:
  isDefined=False
  name=None
  type=None
  arguments=[]

  def __init__(self,name=None,type=None,is_defined=False,arguments=None):
    self.isDefined=is_defined
    self.name=name
    self.type=type
    self.arguments=arguments


class ArrayNode:
  name=None
  type=None
  size=0

  def __init__(self,name,type,size):
    self.type=type
    self.name=name
    self.size=size

class Block:
  funcNode=None
  varMap={}
  #arrayMap={}
  BreakLabel=None     #如果break，将会跳到哪个label
  ContinueLable=None  #如果continue，将会跳到哪个label
  GotoLabel=None      #如果goto，将会跳到哪个label

  def __init__(self):
    pass
