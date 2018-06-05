import json
from middleend.parser import Parser, ParserError
from middleend.ir_writer import IRWriter
from middleend.logger import error
with open('../demo/syntax-tree.json') as syntax_tree_file:
  syntax_tree = json.load(syntax_tree_file)
ir_writer = IRWriter(path='../demo/intermediate.txt')
parser = Parser(syntax_tree=syntax_tree, ir_writer=ir_writer)
try:
  parser.parse()
except ParserError as e:
  error(e)
  quit(1)
ir_writer.write()
