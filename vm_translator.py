from translator.parser import Parser

parser = Parser('./StackArithmetic/SimpleAdd/SimpleAdd.vm')

print(parser.load_and_parse())