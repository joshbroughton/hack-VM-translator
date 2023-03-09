"""
Contains the Parser class, which reads Hack virtual machine code
line by line and parses it into individual commands
"""
import os
import re


class Parser:
    '''
    Loads and reads a file containg hack virtual machine code, and parses
    it line by line into individual commands.
    ARGS:
        file_path (string): the path of the .vm file to be parsed.
    '''

    def __init__(self, file_path):
        self.file_path = file_path

    def load_file(self, file_path):
        """
        loads the data from the file specified by file_path into a list
        each element in the list is a line from the file
        """
        file_data = []
        if os.path.isdir(file_path):
            directory = os.fsencode(file_path)
    
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if filename.endswith(".vm"):
                    with open(os.path.join(file_path, filename), 'r', encoding='utf-8') as input_file:
                        file_data.extend(input_file.readlines())
        else:
            with open(file_path, 'r', encoding='utf-8') as input_file:
                file_data = input_file.readlines()
        return file_data

    def strip_line(self, line):
        """
        strips trailing comments from lines
        """
        regex = re.compile(r'//.*')
        clean_line = regex.sub('', line).strip()
        return clean_line

    def clean_file_data(self, file_data):
        """
        reads the imported data line by line, creates a new list
        containing only virtual machine commands
        """
        commands = []
        for line in file_data:
            if line.isspace():
                continue
            if line[0] == '/':
                continue
            commands.append(self.strip_line(line))
        return commands

    def create_command_dictionaries(self, commands):
        """
        splits each command into its component parts (command, segment, and
        address) and saves these as a list of dictionaries
        """
        split_commands = []
        for command in commands:
            split_command = command.split()
            command_dict = {'command': split_command[0]}
            if len(split_command) > 1:
                command_dict['segment'] = split_command[1]
            if len(split_command) > 2:
                command_dict['address'] = split_command[2]
            split_commands.append(command_dict)
        return split_commands

    def load_and_parse(self):
        """
        controller function which loads and parses a hack VM file into
        a format that a code_writer object can translate
        """
        file_data = self.load_file(self.file_path)
        commands = self.clean_file_data(file_data)
        return self.create_command_dictionaries(commands)
