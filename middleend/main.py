import json
from .parser import Parser
from .ir_writer import IRWriter

with open('../demo/syntax-tree.json') as syntax_tree_file:
  syntax_tree = json.load(syntax_tree_file)
ir_writer = IRWriter(path='../demo/intermediate')
parser = Parser(syntax_tree=syntax_tree, ir_writer=ir_writer)
parser.parse()
