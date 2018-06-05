import json
from middleend.parser import Parser
from middleend.ir_writer import IRWriter

with open('../demo/syntax-tree.json') as syntax_tree_file:
  syntax_tree = json.load(syntax_tree_file)
ir_writer = IRWriter(path='../demo/intermediate.txt')
parser = Parser(syntax_tree=syntax_tree, ir_writer=ir_writer)
parser.parse()
ir_writer.write()
