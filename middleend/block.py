class Block:
  function_node=None   #函数节点
  variable_map=None    #变量符号表
  label_map=None       #label映射表
  #arrayMap={}
  break_label=None     #如果break，将会跳到哪个label
  continue_label=None  #如果continue，将会跳到哪个label
  goto_label=None      #如果goto，将会跳到哪个label

  def __init__(self):
    self.variable_map={}
    self.label_map={}


