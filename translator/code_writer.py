"""
Contains the CodeWriter class, which takes individual Hack VM commands and
translates them into Hack assembly language to perform the desired task.
"""


class CodeWriter:
    """
    CodeWriter class, which contains methods to translate a hack VM command into
    Hack assembly language
    """

    def __init__(self, filename):
        self.filename = filename.replace('/', '')
    # initalize the assembly output
    program_in_hack = []

    def write_arithmetic(self, command_in):
        """
        Given a Hack VM command_in which belongs to the arithmetic commands,
        translates it into Hack assembly code which accomplishes the desired
        memory manipulations
        """
        command = command_in['command']
        commands = []
        if command == 'eq' or command == 'gt' or command == 'lt':
            commands.extend(['// equals?',
                             '@SP', 'A=M-1', 'D=M', '@SP', 'M=M-1', 'A=M-1', 'D=M-D',
                             '@JUMP', 'D;JEQ', '@SP', 'A=M-1', 'M=0', '@END', '0;JMP', '(JUMP)',
                             '@SP', 'A=M-1', 'M=-1', '(END)'
                            ])
        if command == 'gt':
            commands[0] = '// greater than?'
            commands[9] = 'D;JGT'
        if command == 'lt':
            commands[0] = '// less than?'
            commands[9] = 'D;JLT'
        if command == 'neg':
            commands.extend(['// negate y', '@SP', 'A=M-1', 'M=-M'])
        if command == 'not':
            commands.extend(['// not y', '@SP', 'A=M-1', 'M=!M'])
        if command == 'add' or command == 'sub' or command == 'and' or command == 'or':
            commands.extend(['// add', '@SP', 'A=M-1', 'D=M',
                             '@SP', 'M=M-1', 'A=M-1', 'M=D+M'])
        if command == 'sub':
            commands[0] = '// sub'
            commands[7] = 'M=M-D'
        if command == 'and':
            commands[0] = '// and'
            commands[7] = 'M=D&M'
        if command == 'or':
            commands[0] = '// or'
            commands[7] = 'M=D|M'
        for line in commands:
            self.add_command(line)

    def add_command(self, command):
        """Helper function to append a translated assembly command onto the assembly program"""
        self.program_in_hack.append(command)

    def write_push_pop(self, command_in):
        """Given a push or pop VM command, generates hack assembly code to realize the VM command"""
        command = command_in['command']
        segment = command_in['segment']
        address = command_in['address']
        commands = []
        if command == 'push':
            if segment == 'constant':
                commands.extend(
                    [f'// push constant {address}', f'@{address}', 'D=A'])
            elif segment == 'argument':
                commands.extend([f'// push argument {address}', f'@{address}',
                                 'D=A', '@ARG', 'A=D+M', 'D=M'])
            elif segment == 'local':
                commands.extend([f'// push local {address}', f'@{address}',
                                 'D=A', '@LCL', 'A=D+M', 'D=M'])
            elif segment == 'static':
                commands.extend(
                    [f'// push static {address}', f'@{self.filename}.{address}', 'D=M'])
            elif segment == 'this':
                commands.extend([f'// push this {address}', f'@{address}',
                                 'D=A', '@THIS', 'A=D+M', 'D=M'])
            elif segment == 'that':
                commands.extend([f'// push that {address}', f'@{address}',
                                 'D=A', '@THAT', 'A=D+M', 'D=M'])
            elif segment == 'pointer':
                if address == '0':
                    commands.extend(
                        [f'// push pointer {address}', '@THIS', 'D=M'])
                elif address == '1':
                    commands.extend(
                        [f'// push pointer {address}', '@THAT', 'D=M'])
            elif segment == 'temp':
                commands.extend([f'// push temp {address}', f'@{address}', 'D=A',
                                 '@5', 'A=D+A', 'D=M'])
            commands.extend(['@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])
        elif command == 'pop':
            commands.extend(
                [f'// pop {segment} {address}', '@SP', 'AM=M-1', 'D=M'])
            if segment == 'argument':
                commands.extend(['@ARG', 'A=M'])
                commands.extend(self.iterate_address(address))
            elif segment == 'local':
                commands.extend(['@LCL', 'A=M'])
                commands.extend(self.iterate_address(address))
            elif segment == 'static':
                commands.extend([f'@{self.filename}.{address}', 'M=D'])
            elif segment == 'this':
                commands.extend(['@THIS', 'A=M'])
                commands.extend(self.iterate_address(address))
            elif segment == 'that':
                commands.extend(['@THAT', 'A=M'])
                commands.extend(self.iterate_address(address))
            elif segment == 'pointer':
                if address == '0':
                    commands.extend(['@THIS', 'M=D'])
                elif address == '1':
                    commands.extend(['@THAT', 'M=D'])
            elif segment == 'temp':
                commands.extend(['@5'])
                commands.extend(self.iterate_address(address))
        for line in commands:
            self.add_command(line)

    def iterate_address(self, address):
        """Helper function to iterate the pointer address of a segment"""
        commands = []
        address = int(address)
        for i in range(address):
            commands.append('A=A+1')
        commands.append('M=D')
        return commands

    def handle_command(self, command_in):
        """
        Handles logic of determining the type of VM command and calling the
        the appropriate write function to translte the command
        """
        command = command_in['command']
        if command == 'push' or command == 'pop':
            self.write_push_pop(command_in)
        elif command == 'label':
            self.write_label(command_in)
        elif command == 'goto':
            self.write_goto(command_in)
        elif command == 'if-goto':
            self.write_if_goto(command_in)
        elif command == 'call':
            self.call_function(command_in)
        elif command == 'function':
            self.write_function(command_in)
        elif command == 'return':
            self.return_function()
        else:
            self.write_arithmetic(command_in)

    def change_duplicate_labels(self):
        """
        The most intuitive approach to writing JUMP and END labels resulted in duplicate labelling;
        this method identifies and replaces duplicated @JUMP and @ENDs, and replaces both the GOTO
        calls and the labels with unique identifiers
        """
        count = 0
        self.replace_label('@JUMP', count)
        count = self.replace_label('(JUMP)', count)
        self.replace_label('@END', count)
        count = self.replace_label('(END)', count)

    def replace_label(self, label, count):
        """
        Helper method to replace duplicate labels. Uses the count variable to assign unique
        identifers (e.g. the first duplicate @JUMP becomes @JUMP1, and so on)
        """
        while self.program_in_hack.count(label) > 1:
            i = self.program_in_hack.index(label)
            if label[0] == '(':
                self.program_in_hack[i] = f'{label[:-1]}.{count})'
            else:
                self.program_in_hack[i] = f'{label}.{count}'
            count += 1
        return count

    def write_label(self, command_in):
        """
        handles an explicit VM label command, by creating a label in the assembly code
        at the current point in the assembly program
        """
        label = command_in['segment']
        self.program_in_hack.append(f'({label})')

    def write_goto(self, command_in):
        """
        writes hack assembly code to effect an unconditional goto label operation
        """
        label = command_in['segment']
        self.program_in_hack.extend([f'// goto {label}', f'@{label}', '0;JMP'])

    def write_if_goto(self, command_in):
        """
        writes hack assembly code to effect a conditional goto label operation
        pops the top value off the stack; if the value is not 0, goes to the label;
        if the value is 0, execution continues normally
        """
        label = command_in['segment']
        self.program_in_hack.extend([f'//if-goto {label}', '@SP', 'AM=M-1', 'D=M',
                                     f'@{label}', 'D;JNE'])

    def call_function(self, command_in):
        """
        Write hack assembly to call a function:
        1) Housekeeping to save the state of the caller
        2) Unconditional GOTO Label for the function
        Return to the caller will be handled separately
        """
        commands = []
        #push return label onto stack - I THINK JUST PUSH THE LABEL
        # AND THE ASSEMBLER WILL MAKE IT A NUMBER
        # this pushes whatever is in D onto the stack
        commands.extend(['@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])
        #push LCL 

    def return_label(self, function_name):
        '''
        Generates a label for a function call. To handle multiple calls
        to the same function in a single program, checks and iterates i
        to generate a unqiue return lable for each call.
        '''
        i = 0
        while f'{function_name}$ret.{i}' in self.program_in_hack:
            i += 1 
        label = f'{function_name}$ret.{i}'
        return label

    def write_function(self, command_in):
        '''
        writes hack assembly code for a function functionName nVars command,
        i.e. for declaring a function
        '''
        function_name = command_in['segment']
        n_vars = int(command_in['address'])
        # insert a label (function_name)
        self.program_in_hack.extend([f'//function {function_name} {n_vars}',
                                    f'({function_name})'])
        # set the LCL pointer to point to current SP 
        self.program_in_hack.extend(['@SP', 'D=M', '@LCL', 'M=D'])
        # push n_vars 0s onto the stack
        count = 0
        while count < n_vars:
            self.write_push_pop({'command': 'push', 'segment': 'constant', 'address': '0'})
            count += 1

    def return_function(self):
        # push the return value to arg 0
        self.program_in_hack.extend(['//return', '@SP', 'A=M-1', 'D=M', '@ARG', 'A=M', 'M=D'])
        # let @5 be end_frame and @6 be return_address
        # set @5 to end_frame address
        self.program_in_hack.extend(['@LCL', 'D=M', '@5', 'M=D'])
        # set @6 to be value of end_frame (still stored in D) - 5
        self.program_in_hack.extend(['@5', 'A=D-A', 'D=M', '@6', 'M=D'])
        # repostion SP to ARG + 1
        self.program_in_hack.extend(['@ARG', 'D=M+1', '@SP', 'M=D'])
        # restore THAT, THIS, ARG, and LCL to caller state
        self.program_in_hack.extend(['@5', 'A=M-1', 'D=M', '@THAT', 'M=D'])
        self.program_in_hack.extend(['@5', 'D=M', '@2', 'A=D-A', 'D=M', '@THIS', 'M=D'])
        self.program_in_hack.extend(['@5', 'D=M', '@3', 'A=D-A', 'D=M', '@ARG', 'M=D'])
        self.program_in_hack.extend(['@5', 'D=M', '@4', 'A=D-A', 'D=M', '@LCL', 'M=D'])
        self.program_in_hack.extend(['@6', 'A=M', '0;JMP'])

    def write_to_file(self, filename):
        """
        Performs final file cleaning (fixing labels) then write the hack
        assembly program to an output file of the same name as the input
        file, with a .asm file extension
        """
        self.change_duplicate_labels()
        with open(f'{filename}.asm', 'w', encoding='utf-8') as outfile:
            for command in self.program_in_hack:
                outfile.write(command + '\n')
