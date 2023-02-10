# What is this project?
A virtual machine transator which translates Hack VM language into Hack assembly
code. Completed as part of the nand2tetris part 2 course on [Coursera](https://www.coursera.org/learn/nand2tetris2/home/week/1). The Hack software architecture is designed similarily 
to Java, in which programs written in the high-level language (Jack) are compiled to an
intermediary virtual machine code before being translated down to Hack assembly and finally
assembled into hack machine code.

To translate a `<filename>.vm` file into hack assembly, run `python3 vm_translator.py <relative_path_to_filename>.vm`

To run test scripts, launch the nand2tetris CPU Emulator, available in the tools directory from
the nand2tetris [website](https://www.nand2tetris.org/).