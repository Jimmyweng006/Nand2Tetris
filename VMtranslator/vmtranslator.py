from pathlib import Path
import os


def main(initial_file_name):
    # no matter file or directory >> change to directory and find file(s)
    if ".vm" in initial_file_name:
        initial_file_name = initial_file_name.strip(".vm")

    # move to working directory first
    dir_name = "\\" + initial_file_name
    pathname = r"C:\Users\Jimmy\Desktop\Nand2Tetris\VMtranslator"
    pathname = pathname + dir_name
    os.chdir(pathname)

    # Bootstrap code
    extend_filename = initial_file_name + ".asm"
    first_file = open(extend_filename, "a")
    first_file.write("@256\n")
    first_file.write("D=A\n")
    first_file.write("@SP\n")
    first_file.write("M=D\n")
    first_file.close()

    first_file = open(extend_filename, "a")
    codewriter(extend_filename, 7, ["call", "Sys.init", "0"], initial_file_name)
    first_file.close()

    # move back to original directory
    pathname = r"C:\Users\Jimmy\Desktop\Nand2Tetris\VMtranslator"
    os.chdir(pathname)

    entries = Path(initial_file_name)
    for entry in entries.iterdir():
        if ".vm" in entry.name:
            parser(entry.name, initial_file_name)

# pass file to parser
# deal with only Arithmetic / Logical commands
# and Memory access commands


def parser(file_name, initial_file_name):
    # move to working directory
    dir_name = "\\" + initial_file_name
    pathname = r"C:\Users\Jimmy\Desktop\Nand2Tetris\VMtranslator"
    pathname = pathname + dir_name
    os.chdir(pathname)

    commandtype_list = {
        "add": 0, "sub": 0, "neg": 0, "eq": 0, "gt": 0,
        "lt": 0, "and": 0, "or": 0, "not": 0, "push": 1,
        "pop": 2, "label": 3, "goto": 4, "if-goto": 5,
        "function": 6, "call": 7, "return": 8
    }

    # open current xxx.vm file
    parse_file = open(file_name, "r")
    # write to final.asm file
    extend_filename = initial_file_name + ".asm"

    # iterate each line
    for line in parse_file.readlines():
        items = line.split()
        # check white space or comments
        if len(items) != 0:
            if items[0] != "//":
                # finished_file.write(line)
                # decide which command it is
                commandtype = commandtype_list[items[0]]
                # file_name like Class1.vm
                codewriter(extend_filename, commandtype, items, file_name)

    parse_file.close()


def codewriter(file, commandtype, sentence, file_name):
    finished_file = open(file, "a")
    # for Arithmetic/Logical commands

    def get_element1(command):
        finished_file.write("// " + command + "\n")
        finished_file.write("@SP\n")
        finished_file.write("M=M-1\n")
        finished_file.write("@SP\n")
        finished_file.write("A=M\n")
        finished_file.write("D=M\n")

    def get_element2():
        finished_file.write("@SP\n")
        finished_file.write("M=M-1\n")
        finished_file.write("@SP\n")
        finished_file.write("A=M\n")
        finished_file.write("A=M\n")

    def give_element():
        finished_file.write("@SP\n")
        finished_file.write("A=M\n")
        finished_file.write("M=D\n")
        finished_file.write("@SP\n")
        finished_file.write("M=M+1\n")

    # label problem 需要決定label的編號

    def writeArithmetic(command, label):
        if command == "add":
            get_element1(command)
            get_element2()
            finished_file.write("D=A+D\n")
            give_element()
        if command == "sub":
            get_element1(command)
            get_element2()
            finished_file.write("D=A-D\n")
            give_element()
        if command == "neg":
            get_element1(command)
            finished_file.write("D=-D\n")
            give_element()
        if command == "eq":
            get_element1(command)
            get_element2()

            finished_file.write("D=A-D\n")
            finished_file.write("@LABEL" + str(label) + "\n")
            finished_file.write("D;JEQ\n")
            finished_file.write("@SP\n")
            finished_file.write("A=M\n")
            finished_file.write("M=0\n")

            finished_file.write("@LABEL" + str(label+1) + "\n")
            finished_file.write("0;JMP\n")

            finished_file.write("(LABEL" + str(label) + ")\n")
            finished_file.write("@SP\n")
            finished_file.write("A=M\n")
            finished_file.write("M=-1\n")

            finished_file.write("(LABEL" + str(label+1) + ")\n")
            finished_file.write("@SP\n")
            finished_file.write("M=M+1\n")
        if command == "gt":
            get_element1(command)
            get_element2()

            finished_file.write("D=A-D\n")
            finished_file.write("@LABEL" + str(label) + "\n")
            finished_file.write("D;JGT\n")
            finished_file.write("@SP\n")
            finished_file.write("A=M\n")
            finished_file.write("M=0\n")

            finished_file.write("@LABEL" + str(label+1) + "\n")
            finished_file.write("0;JMP\n")

            finished_file.write("(LABEL" + str(label) + ")\n")
            finished_file.write("@SP\n")
            finished_file.write("A=M\n")
            finished_file.write("M=-1\n")

            finished_file.write("(LABEL" + str(label+1) + ")\n")
            finished_file.write("@SP\n")
            finished_file.write("M=M+1\n")
        if command == "lt":
            get_element1(command)
            get_element2()

            finished_file.write("D=A-D\n")
            finished_file.write("@LABEL" + str(label) + "\n")
            finished_file.write("D;JLT\n")
            finished_file.write("@SP\n")
            finished_file.write("A=M\n")
            finished_file.write("M=0\n")

            finished_file.write("@LABEL" + str(label+1) + "\n")
            finished_file.write("0;JMP\n")

            finished_file.write("(LABEL" + str(label) + ")\n")
            finished_file.write("@SP\n")
            finished_file.write("A=M\n")
            finished_file.write("M=-1\n")

            finished_file.write("(LABEL" + str(label+1) + ")\n")
            finished_file.write("@SP\n")
            finished_file.write("M=M+1\n")
        if command == "and":
            get_element1(command)
            get_element2()
            finished_file.write("D=A&D\n")
            give_element()
        if command == "or":
            get_element1(command)
            get_element2()
            finished_file.write("D=A|D\n")
            give_element()
        if command == "not":
            get_element1(command)
            finished_file.write("D=!D\n")
            give_element()

    # for Memory access commands

    def assign_index_push(segment, index):
        finished_file.write("// push " + segment + " " + index + "\n")
        finished_file.write("@" + index + "\n")
        finished_file.write("D=A\n")

    def get_address_push(segment):
        finished_file.write("@" + segment + "\n")
        finished_file.write("A=M\n")
        finished_file.write("AD=D+A\n")
        finished_file.write("D=M\n")

    def push_element():
        finished_file.write("@SP\n")
        finished_file.write("A=M\n")
        finished_file.write("M=D\n")
        finished_file.write("@SP\n")
        finished_file.write("M=M+1\n")

    def assign_index_pop(segment, index):
        finished_file.write("// pop " + segment + " " + index + "\n")
        finished_file.write("@SP\n")
        finished_file.write("M=M-1\n")
        finished_file.write("@" + index + "\n")
        finished_file.write("D=A\n")

    def get_address_pop(segment):
        finished_file.write("@" + segment + "\n")
        finished_file.write("A=M\n")
        finished_file.write("AD=D+A\n")
        finished_file.write("@R15\n")
        finished_file.write("M=D\n")

    def pop_element():
        finished_file.write("@SP\n")
        finished_file.write("A=M\n")
        finished_file.write("D=M\n")
        finished_file.write("@R15\n")
        finished_file.write("A=M\n")
        finished_file.write("M=D\n")

    def writePushPop(command, segment, index):
        if command == "push":
            if segment == "local":
                assign_index_push(segment, index)
                get_address_push("LCL")
                push_element()
            if segment == "argument":
                assign_index_push(segment, index)
                get_address_push("ARG")
                push_element()
            if segment == "this":
                assign_index_push(segment, index)
                get_address_push("THIS")
                push_element()
            if segment == "that":
                assign_index_push(segment, index)
                get_address_push("THAT")
                push_element()
            if segment == "constant":
                assign_index_push(segment, index)
                push_element()
            if segment == "temp":
                finished_file.write("// push " + segment + " " + index + "\n")
                finished_file.write("@" + str(5+int(index)) + "\n")
                finished_file.write("D=M\n")
                push_element()
            if segment == "pointer":
                finished_file.write("// push " + segment + " " + index + "\n")
                finished_file.write("@R" + str(3+int(index)) + "\n")
                finished_file.write("D=M\n")
                push_element()
            if segment == "static":
                static_var = file_name.replace("vm", str(index))
                finished_file.write("// push " + segment + " " + index + "\n")
                finished_file.write("@" + static_var + "\n")
                finished_file.write("D=M\n")
                push_element()
        if command == "pop":
            if segment == "local":
                assign_index_pop(segment, index)
                get_address_pop("LCL")
                pop_element()
            if segment == "argument":
                assign_index_pop(segment, index)
                get_address_pop("ARG")
                pop_element()
            if segment == "this":
                assign_index_pop(segment, index)
                get_address_pop("THIS")
                pop_element()
            if segment == "that":
                assign_index_pop(segment, index)
                get_address_pop("THAT")
                pop_element()
            if segment == "temp":
                finished_file.write("// pop " + segment + " " + index + "\n")
                finished_file.write("@SP\n")
                finished_file.write("M=M-1\n")
                finished_file.write("@" + str(5+int(index)) + "\n")
                finished_file.write("D=A\n")
                finished_file.write("@R15\n")
                finished_file.write("M=D\n")
                pop_element()
            if segment == "pointer":
                finished_file.write("// pop " + segment + " " + index + "\n")
                finished_file.write("@SP\n")
                finished_file.write("M=M-1\n")
                finished_file.write("@SP\n")
                finished_file.write("A=M\n")
                finished_file.write("D=M\n")
                finished_file.write("@R" + str(3+int(index)) + "\n")
                finished_file.write("M=D\n")
            if segment == "static":
                static_var = file_name.replace("vm", str(index))
                finished_file.write("// pop " + segment + " " + index + "\n")
                finished_file.write("@SP\n")
                finished_file.write("M=M-1\n")
                finished_file.write("@SP\n")
                finished_file.write("A=M\n")
                finished_file.write("D=M\n")
                finished_file.write("@" + static_var + "\n")
                finished_file.write("M=D\n")

    # for Branching commands

    def Getelement():
        finished_file.write("@SP\n")
        finished_file.write("M=M-1\n")
        finished_file.write("@SP\n")
        finished_file.write("A=M\n")
        finished_file.write("D=M\n")

    # for Function commands

    def getsegment():
        finished_file.write("@R13\n")
        finished_file.write("D=M\n")
        finished_file.write("D=D-1\n")
        finished_file.write("@R13\n")
        finished_file.write("M=D\n")
        finished_file.write("A=D\n")
        finished_file.write("D=M\n")

    if commandtype == 0:
        global arithmetic_label
        writeArithmetic(sentence[0], arithmetic_label)
        arithmetic_label += 2
    elif commandtype == 1 or commandtype == 2:
        writePushPop(sentence[0], sentence[1], sentence[2])
    elif commandtype == 3:
        finished_file.write("// " + sentence[0] + " " + sentence[1] + "\n")
        finished_file.write("(" + sentence[1] + ")" + "\n")
    elif commandtype == 4:
        finished_file.write("// " + sentence[0] + " " + sentence[1] + "\n")
        finished_file.write("@" + sentence[1] + "\n")
        finished_file.write("0;JMP\n")
    elif commandtype == 5:
        finished_file.write("// " + sentence[0] + " " + sentence[1] + "\n")
        Getelement()
        finished_file.write("@" + sentence[1] + "\n")
        finished_file.write("D;JNE\n")
    elif commandtype == 6:
        finished_file.write("// " + sentence[0] + " " + sentence[1] + " " + sentence[2] + "\n")
        finished_file.write("(" + sentence[1] + ")" + "\n")
        for i in range(0, int(sentence[2])):
            finished_file.write("@0\n")
            finished_file.write("D=A\n")
            give_element()
    # label problem again(return address)
    elif commandtype == 7:
        global returnaddress_label
        finished_file.write("// " + sentence[0] + " " + sentence[1] + " " + sentence[2] + "\n")
        finished_file.write("@retaddr" + str(returnaddress_label) + "\n")
        finished_file.write("D=A\n")
        give_element()
        finished_file.write("@R1\n")
        finished_file.write("D=M\n")
        give_element()
        finished_file.write("@R2\n")
        finished_file.write("D=M\n")
        give_element()
        finished_file.write("@R3\n")
        finished_file.write("D=M\n")
        give_element()
        finished_file.write("@R4\n")
        finished_file.write("D=M\n")
        give_element()
        # ARG = SP - 5 - nArgs
        finished_file.write("@" + str(int(sentence[2]) + 5) + "\n")
        finished_file.write("D=A\n")
        finished_file.write("@R0\n")
        finished_file.write("A=M\n")
        finished_file.write("AD=A-D\n")
        finished_file.write("@R2\n")
        finished_file.write("M=D\n")
        # LCL = SP
        finished_file.write("@R0\n")
        finished_file.write("D=M\n")
        finished_file.write("@R1\n")
        finished_file.write("M=D\n")
        # goto function_name
        finished_file.write("@" + str(sentence[1]) + "\n")
        finished_file.write("0;JMP\n")
        finished_file.write("(retaddr" + str(returnaddress_label) + ")" + "\n")
        returnaddress_label += 1
    elif commandtype == 8:
        finished_file.write("// " + sentence[0] + "\n")
        finished_file.write("// endFrame = LCL\n")
        finished_file.write("@R1\n")
        finished_file.write("D=M\n")
        finished_file.write("@R13\n")
        finished_file.write("M=D\n")
        finished_file.write("// retAddr = *(endFrame - 5)\n")
        finished_file.write("@5\n")
        finished_file.write("A=D-A\n")
        finished_file.write("D=M\n")
        finished_file.write("@R14\n")
        finished_file.write("M=D\n")
        finished_file.write("// *ARG = pop()\n")
        finished_file.write("@SP\n")
        finished_file.write("M=M-1\n")
        finished_file.write("@ARG\n")
        finished_file.write("AD=M\n")
        finished_file.write("@R15\n")
        finished_file.write("M=D\n")
        finished_file.write("@SP\n")
        finished_file.write("A=M\n")
        finished_file.write("D=M\n")
        finished_file.write("@R15\n")
        finished_file.write("A=M\n")
        finished_file.write("M=D\n")
        finished_file.write("// SP = ARG + 1\n")
        finished_file.write("@R2\n")
        finished_file.write("D=M\n")
        finished_file.write("@R0\n")
        finished_file.write("M=D+1\n")
        finished_file.write("// THAT = *(endFrame - 1 )\n")
        getsegment()
        finished_file.write("@R4\n")
        finished_file.write("M=D\n")
        finished_file.write("// THIS = *(endFrame - 2 )\n")
        getsegment()
        finished_file.write("@R3\n")
        finished_file.write("M=D\n")
        finished_file.write("// ARG = *(endFrame - 3 )\n")
        getsegment()
        finished_file.write("@R2\n")
        finished_file.write("M=D\n")
        finished_file.write("// LCL = *(endFrame - 4 )\n")
        getsegment()
        finished_file.write("@R1\n")
        finished_file.write("M=D\n")
        # most tricky part
        finished_file.write("// goto retAddr\n")
        finished_file.write("@R14\n")
        finished_file.write("A=M\n")
        finished_file.write("0;JMP\n")
    finished_file.close()


arithmetic_label = 0
returnaddress_label = 0
main(input())
