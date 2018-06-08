from backend.mips_writer import MIPSWriter
from backend.regs import Regs
from backend.transmips import Translator

filename='../demo/intermediate.txt'
path='../demo/result.asm'
translator=Translator(filename,path)
translator.translate()
