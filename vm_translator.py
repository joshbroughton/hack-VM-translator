from translator.parser import Parser
from translator.code_writer import CodeWriter
import sys
import os

parser = Parser(sys.argv[1])
path = sys.argv[1] #this it the path to file for single file or directory for dirs
filename = path.split('/')[-1]
code_writer = CodeWriter(filename)

commands = parser.load_and_parse()

for command in commands:
    code_writer.handle_command(command)

directory = os.fsdecode(sys.argv[1])
absolute_path_directory = os.fsdecode(os.path.abspath(sys.argv[1]))

if os.path.isdir(directory):
    code_writer.write_to_file(f'{path}/{filename}')
else:
    code_writer.write_to_file(path[0:-3]) # remove the .vm extension if single file
