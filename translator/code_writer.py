class CodeWriter:
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

    def write_push_pop(self, command):
        if command['segment'] == 'constant' and command['command'] == 'push':
            self.add_command(f'// push constant {command["address"]}')
            self.add_command(f'@{command["address"]}')
            self.add_command('D=A')
            self.add_command('@SP')
            self.add_command('A=M')
            self.add_command('M=D')
            self.add_command('@SP')
            self.add_command('M=M+1')
        elif command['command'] == 'push':
            self.push(command['segment'], command['address'])

    def push(self, segment, address):
        pass
    def pop(self, segment, address):
        pass
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
        