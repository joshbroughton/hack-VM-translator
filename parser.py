import re

class Parser:
    '''
    Loads and reads a file containg hack virtual machine code, and parses
    it line by line into individual commands.
    ARGS:
        file_path (string): the path of the .vm file to be parsed.
    Returns:
        A list of single VM commands
    '''
    def __init__(self, file_path):
        self.file_path = file_path

    def load_file(self, file_path):
        file_data = []
        with open(file_path, 'r', encoding='utf-8') as input_file:
            file_data = input_file.readlines()
        return file_data

    def strip_line(self, line):
        regex = re.compile(r'//.*')
        clean_line= regex.sub('', line).strip()
        return clean_line

    def clean_file_data(self, file_data):
        commands = []
        for line in file_data:
            if line.isspace():
                continue
            commands.append(self.strip_line(line))
        return commands

    def create_command_dictionaries(self, commands):
        split_commands = []
        for command in commands:
            split_command = command.split()
            command_dict = {'command': split_command[0]}
            if split_command.length > 1:
                command_dict['segment'] = split_command[1]
            if split_command.length > 2:
                command_dict['address'] = split_command[2]
            split_commands.append(command_dict)
        return split_commands
    
    def load_and_parse(self):
        file_data = self.load_file(self.file_path)
        commands = self.clean_file_data(file_data)
        return self.create_command_dictionaries(commands)

            




    