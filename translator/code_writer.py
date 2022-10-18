class CodeWriter:
    def __init__(self, filename):
        self.filename = filename

    program_in_hack = ['@256', 'D=A', '@SP', 'M=D']

    def write_arithmetic(self, command_in):
        command = command_in['command']
        commands = []
        if command == 'eq' or command == 'gt' or command == 'lt':
            commands.extend(['// equals?', '@SP', 'A=M-1', 'D=M', '@SP', 'M=M-1', 'A=M-1', 'D=M-D', '@JUMP', 
            'D;JEQ', '@SP', 'A=M-1', 'M=0', '@END', '0;JMP', '(JUMP)', '@SP', 'A=M-1', 'M=-1', '(END)'])
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
            commands.extend(['// add', '@SP', 'A=M-1', 'D=M', '@SP', 'M=M-1', 'A=M-1', 'M=D+M'])
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
        self.program_in_hack.append(command)

    def write_push_pop(self, command_in):
        command = command_in['command']
        segment = command_in['segment']
        address = command_in['address']
        commands = []
        if command == 'push':
            if segment == 'constant':
                commands.extend([f'// push constant {address}', f'@{address}', 'D=A'])
            elif segment == 'argument':
                commands.extend([f'// push argument {address}', f'@{address}', 'D=A', '@ARG', 'A=D+M', 'D=M'])
            elif segment == 'local':
                commands.extend([f'// push local {address}', f'@{address}', 'D=A', '@LCL', 'A=D+M', 'D=M'])
            elif segment == 'static':
                commands.extend([f'// push static {address}', f'@foo.{address}', 'D=M'])
            elif segment == 'this':
                commands.extend([f'// push this {address}', f'@{address}', 'D=A', '@THIS', 'A=D+M', 'D=M'])
            elif segment == 'that':
                commands.extend([f'// push that {address}', f'@{address}', 'D=A', '@THAT', 'A=D+M', 'D=M'])
            elif segment == 'pointer':
                if address == '0':
                    commands.extend([f'// push pointer {address}', '@THIS', 'D=M'])
                elif address == '1':
                    commands.extend([f'// push pointer {address}', '@THAT', 'D=M'])
            elif segment == 'temp':
                commands.extend([f'// push temp {address}', f'@{address}', 'D=A', '@5','A=D+A', 'D=M'])
            commands.extend(['@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])
        elif command == 'pop':
            commands.extend([f'// pop {segment} {address}', '@SP', 'AM=M-1', 'D=M'])
            if segment == 'argument':
                commands.extend(['@ARG', 'A=M'])
                commands.extend(self.iterate_address(address))
            elif segment == 'local':
                commands.extend(['@LCL', 'A=M'])
                commands.extend(self.iterate_address(address))
            elif segment == 'static':
                commands.extend([f'@foo.{address}', 'M=D'])
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
        commands = []
        address = int(address)
        for i in range(address):
            commands.append('A=A+1')
        commands.append('M=D')
        return commands
                    
    def handle_command(self, command):
        if command['command'] == 'push' or command['command'] == 'pop':
            self.write_push_pop(command)
        else:
            self.write_arithmetic(command)

    def change_duplicate_labels(self):
        count = 0
        self.replace_label('@JUMP', count)
        count = self.replace_label('(JUMP)', count)
        self.replace_label('@END', count)
        count = self.replace_label('(END)', count)

    def replace_label(self, label, count):
        while self.program_in_hack.count(label) > 1:
            i = self.program_in_hack.index(label)
            if label[0] == '(':
                self.program_in_hack[i] = f'{label[:-1]}{count})'
            else:
                self.program_in_hack[i] = f'{label}{count}'
            count += 1
        return count

    def write_to_file(self, filename):
        self.change_duplicate_labels()
        with open(f'{filename}.asm', 'w', encoding='utf-8') as outfile:
            for command in self.program_in_hack:
                outfile.write(command + '\n')
        