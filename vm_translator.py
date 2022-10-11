from translator.parser import Parser
from translator.code_writer import CodeWriter

parser = Parser('./StackArithmetic/SimpleAdd/SimpleAdd.vm')
code_writer = CodeWriter()

commands = parser.load_and_parse()
print(commands)

for command in commands:
  code_writer.handle_command(command)

code_writer.write_to_file('SimpleAdd')