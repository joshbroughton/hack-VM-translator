from translator.parser import Parser
from translator.code_writer import CodeWriter
import sys

parser = Parser(sys.argv[1])
filename = sys.argv[1][0:-3]
code_writer = CodeWriter(filename)

commands = parser.load_and_parse()

for command in commands:
    code_writer.handle_command(command)

code_writer.write_to_file(f'{sys.argv[1][:-3]}')
