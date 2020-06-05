def main(file):
    parser(file)


def parser(file):

    parse_file = open(file, "r")
    hack_file = file.replace("asm", "hack")

    def a_instruction(instruction):
        # split(for string) @21 to ["", "21"]
        return instruction[0].split("@")

    def get_c_instruction(instruction):
        # unpack instruction into different fields
        if "=" in instruction[0]:
            return "="
        if ";" in instruction[0]:
            return ";"

    f = parse_file.readlines()

    # first pass
    for line in f:
        items = line.split()
        if len(items) != 0:
            if items[0] != "//":
                # add label symbol
                global number_instruction
                if items[0][0] == "(":
                    label_symbol = items[0][1:-1]
                    # set label to current number_instruction
                    symbol_table[label_symbol] = str(number_instruction)
                    # number_instruction go back
                    number_instruction -= 1
                number_instruction += 1

    # readline"s"
    # second pass
    for line in f:
        # get rid of space and \n
        items = line.split()
        # check white space or comments
        if len(items) != 0:
            if items[0] != "//":
                # check not label symbol
                if items[0][0] != "(":
                    # decide A/C instruction or label
                    if items[0][0] == "@":
                        # a list pass to code function
                        # ['', '@', '21']
                        parse_instruction_a = a_instruction(items)
                        parse_instruction_a.insert(1, "@")
                        # label or var symbol translate to number
                        if not (parse_instruction_a[2].isnumeric()):
                            # if not label symbol >> var_symbol
                            if parse_instruction_a[2] in symbol_table:
                                parse_instruction_a[2] = symbol_table[parse_instruction_a[2]]
                            else:
                                global n
                                symbol_table[parse_instruction_a[2]] = str(n)
                                n += 1

                        code(hack_file, parse_instruction_a)
                    else:
                        # ['M', 'M+D']
                        sign = get_c_instruction(items)
                        if sign == "=":
                            parse_instruction_c = items[0].split("=")
                            parse_instruction_c.insert(1, "=")
                        elif sign == ";":
                            parse_instruction_c = items[0].split(";")
                            parse_instruction_c.insert(1, ";")
                        code(hack_file, parse_instruction_c)
    parse_file.close()


def code(file, list_instruction):
    coded_file = open(file, "a")

    comp = {"0": "101010", "1": "111111", "-1": "111010",
            "D": "001100", "A": "110000", "!D": "001101",
            "!A": "110001", "-D": "001111", "-A": "110011",
            "D+1": "011111", "A+1": "110111", "D-1": "001110",
            "A-1": "110010", "D+A": "000010", "D-A": "010011",
            "A-D": "000111", "D&A": "000000", "D|A": "010101"
            }

    dest = {"null": "000", "M": "001", "D": "010", "MD": "011",
            "A": "100", "AM": "101", "AD": "110", "AMD": "111"}

    jump = {"null": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
            "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

    def binary_constant(value):
        binary_code = []
        while value >= 1:
            binary_code.insert(0, value % 2)
            value = value // 2
        while len(binary_code) < 16:
            binary_code.insert(0, 0)

        temp = "".join(str(e) for e in binary_code)
        return temp

    if "@" in list_instruction:
        if list_instruction[2].isnumeric():
            coded_file.write(binary_constant(int(list_instruction[2])) + "\n")
        else:
            coded_file.write(binary_constant(int(symbol_table[list_instruction[2]])) + "\n")

    if "=" in list_instruction:
        # a = 1
        flag = 0
        # check something like M in D-M
        for letter in list_instruction[2]:
            if letter == "M":
                flag = 1
        if flag:
            # replace "M" in the list_instruction[2] to "A", correspond to comp table
            list_instruction[2] = list_instruction[2].replace("M", "A")
            coded_file.write("1111" + comp[list_instruction[2]] + dest[list_instruction[0]] + "000\n")
        else:
            coded_file.write("1110" + comp[list_instruction[2]] + dest[list_instruction[0]] + "000\n")

    if ";" in list_instruction:
        # a = 1
        flag = 0
        for letter in list_instruction[0]:
            if letter == "M":
                flag = 1
        if flag:
            list_instruction[0] = list_instruction[0].replace("M", "A")
            coded_file.write("1111" + comp[list_instruction[0]] + "000" + jump[list_instruction[2]] + "\n")
        else:
            coded_file.write("1110" + comp[list_instruction[0]] + "000" + jump[list_instruction[2]] + "\n")

    coded_file.close()


symbol_table = {"R0": "0", "R1": "1", "R2": "2", "R3": "3",
                "R4": "4", "R5": "5", "R6": "6", "R7": "7",
                "R8": "8", "R9": "9", "R10": "10", "R11": "11",
                "R12": "12", "R13": "13", "R14": "14", "R15": "15",
                "SCREEN": "16384", "KBD": "24576", "SP": "0", "LCL": "1",
                "ARG": "2", "THIS": "3", "THAT": "4"
                }

number_instruction = 0
n = 16
main(input())
