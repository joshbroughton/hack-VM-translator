class CodeWriter:
    program_in_hack = ['@256', 'D=A', '@SP', 'M=D']

    def write_arithmetic(self, command):
        if command['command'] == 'add':
            commands = ['@SP', 'A=M-1', 'D=M', '@SP', 'M=M-1', 'A=M-1', 'M=D+M']
            for line in commands:
                self.add_command(line)
        elif command == 'sub':
            pass #pop y pop x push x - y
        elif command == 'neg':
            pass #pop y push -y
        elif command == 'eq':
            pass #pop y pop x push x == y
        elif command == 'gt':
            pass #pop y pop x push x > y
        elif command == 'lt':
            pass #pop y pop x push x < y
        elif command == 'and':
            pass #pop y pop x push x && y
        elif command == 'or':
            pass #pop y pop x push x || y
        elif command == 'not':
            pass#pop y push not y

    def add_command(self, command):
        self.program_in_hack.append(command)

    def write_push_pop(self, command):
        if command['segment'] == 'constant':
            self.add_command(f'@{command["address"]}')
            self.add_command('D=A')
        self.add_command('@SP')
        if command['command'] == 'push':
            self.add_command('A=M')
            self.add_command('M=D')
            self.add_command('@SP')
            self.add_command('M=M+1')

    def handle_command(self, command):
        if command['command'] == 'push' or command['command'] == 'pop':
            self.write_push_pop(command)
        else:
            self.write_arithmetic(command)

    def write_to_file(self, filename):
        with open(f'{filename}.asm', 'w', encoding='utf-8') as outfile:
            for command in self.program_in_hack:
                outfile.write(command + '\n')
        