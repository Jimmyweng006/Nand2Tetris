def main(initial_file_name):
    parser(initial_file_name)

# pass file to parser
# deal with only Arithmetic / Logical commands
# and Memory access commands


def parser(file_name):
    commandtype_list = {
        "add": 0, "sub": 0, "neg": 0, "eq": 0, "gt": 0,
        "lt": 0, "and": 0, "or": 0, "not": 0, "push": 1, "pop": 2
    }
    parse_file = open(file_name, "r")
    extend_filename = file_name.replace("vm", "asm")

    # iterate each line
    for line in parse_file.readlines():
        items = line.split()
        # check white space or comments
        if len(items) != 0:
            if items[0] != "//":
                # finished_file.write(line)
                # decide which command it is
                commandtype = commandtype_list[items[0]]
                codewriter(extend_filename, commandtype, items)

    parse_file.close()


def codewriter(file, commandtype, sentence):
    finished_file = open(file, "a")
    # for arithmetic operation

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

    # label problems 需要決定label的編號

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

    # for push/pop operation

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
                static_var = file.replace("asm", str(index))
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
                static_var = file.replace("asm", str(index))
                finished_file.write("// pop " + segment + " " + index + "\n")
                finished_file.write("@SP\n")
                finished_file.write("M=M-1\n")
                finished_file.write("@SP\n")
                finished_file.write("A=M\n")
                finished_file.write("D=M\n")
                finished_file.write("@" + static_var + "\n")
                finished_file.write("M=D\n")

    if commandtype == 0:
        global arithmetic_label
        writeArithmetic(sentence[0], arithmetic_label)
        arithmetic_label += 2

    elif commandtype == 1 or commandtype == 2:
        writePushPop(sentence[0], sentence[1], sentence[2])

    finished_file.close()


arithmetic_label = 0
main(input())
