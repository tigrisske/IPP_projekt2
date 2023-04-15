import re
import sys
import argparse
from curses.ascii import isdigit
from enum import Enum
from xml.etree import ElementTree as ET
import abc
import instructions_map

DEBUG = False


class Instruction:
    args = []

    def __init__(self, opcode, order):
        self.args = []
        self.opcode = opcode.upper()
        self.order = order

    def execute(self):
        pass

    def add_argument(self, arg):
        self.args.append(arg)

    def print_arguments(self):
        print('-----------------------------------------------------')
        print("opcode:", self.opcode, "\norder:", self.order)
        print()
        for arg in self.args:
            print("big type:", arg.big_type, "\narg type:", arg.arg_type, "\nvalue:", arg.value, "\norder:", arg.order,
                  "\nframe:", arg.frame)
            if arg.is_var:
                print("name:", arg.name)
            print('-----')
        print('-----------------------------------------------------')

    def sort_arguments(self):
        self.args.sort(key=lambda x: x.order)
        if len(self.args) != len(instructions_map.instructions_map[self.opcode]):
            if DEBUG:
                print("Wrong number of arguments for instruction", self.opcode)
            exit(32)
        # check whether arguments are numbered correctly

        order = 1
        for arg in self.args:
            # print('arg order: ', arg.order, 'order:', order)
            if int(arg.order)!= order:
                if DEBUG:
                    print("Wrong order of arguments for instruction", self.opcode)
                exit(32)
            order += 1

        # TODO this is maybe redundant
        for i in range(len(self.args)):
            if not (instructions_map.ArgTypeEnum.compare_types(self.args[i], self.args[i],
                                                               instructions_map.instructions_map[self.opcode][i])):
                if DEBUG:
                    print("Wrong type of arguments for instruction", self.opcode)
                    exit(53)


class Argument:
    is_var = False
    name = None

    def __init__(self, arg_type, arg_value, arg_order, arg_frame=None, var_name=None):
        if arg_type == 'var':
            self.is_var = True
            self.name = var_name
            self.big_type = instructions_map.ArgTypeEnum.VARIABLE
            self.arg_type = None
        elif arg_type == 'label':
            self.big_type = instructions_map.ArgTypeEnum.LABEL
            self.arg_type = arg_type
        elif arg_type == 'type':
            self.big_type = instructions_map.ArgTypeEnum.TYPE
            self.arg_type = arg_type
        elif arg_type in instructions_map.const:
            self.big_type = instructions_map.ArgTypeEnum.SYMBOL
            self.arg_type = arg_type
        self.value = arg_value
        self.order = arg_order
        self.frame = arg_frame


class Interpreter:
    def __init__(self, parser,args):
        self.defined_vars = []
        self.defined_vars_names = []
        self.labels = []
        self.data_stack = []
        self.parser = parser
        self.arithmetic = ['ADD', 'SUB', 'MUL', 'IDIV', 'DIV']
        self.input = args.input.split('\n')
        self.read_index = 0

    def is_number_with_optional_minus(self, value):
        value_str = str(value)
        pattern = r'^-?\d+$'
        return bool(re.match(pattern, value_str))

    def find_arg(self,argument):
        # if not var is given, original argument is returned
        if argument.big_type != instructions_map.ArgTypeEnum.VARIABLE:
            return argument
        # if var is given, it is searched in defined variables
        for arg in self.defined_vars:
            if argument.name == arg.name and argument.frame == arg.frame:
                return arg
        if DEBUG:
            print("Variable not defined")
            print(argument.name, self.defined_vars)
        exit(54)


    def check_var(self, arg):
        if arg.arg_type == 'var':
            if arg.name not in self.defined_vars:
                if DEBUG:
                    print("Variable not defined")
                    print(arg.name, self.defined_vars)
                exit(54)

    def set_var(self, var, value, value_type):
        self.check_var(var)
        for arg in self.defined_vars:
            if arg.name == var.name:
                arg.value = value
                arg.arg_type = value_type

    def check_arithmetic(self, instruction):
        if not (self.find_arg(instruction.args[1]).arg_type == 'int' and self.find_arg(instruction.args[2]).arg_type == 'int') and not (
                self.find_arg(instruction.args[1]).arg_type == 'float' and self.find_arg(instruction.args[2]).arg_type == 'float'):
            if DEBUG:
                print("Invalid types for arithmetic operation")
                #print names of variables
                print()
                print(self.find_arg(instruction.args[1]).name, self.find_arg(instruction.args[2]).name)
                print(self.find_arg(instruction.args[1]).arg_type, self.find_arg(instruction.args[2]).arg_type)
                for arg in self.defined_vars:
                    print(arg.name, arg.value, arg.arg_type, arg.frame)
            exit(53)

    def execute(self):
        if DEBUG:
            print("Executing instructions")

        for instruction in self.parser.instructions:
            if instruction.opcode == 'DEFVAR':
                self.defined_vars_names.append(instruction.args[0].name)
                self.defined_vars.append(instruction.args[0])

            if instruction.opcode == 'READ':
                var = self.find_arg(instruction.args[0])
                typ = self.find_arg(instruction.args[1])
                input = self.input[self.read_index]
                self.set_var(var, input, typ.value)
                self.read_index += 1

            elif instruction.opcode == 'MOVE':
                var = self.find_arg(instruction.args[0])
                symb = self.find_arg(instruction.args[1])
                self.set_var(var, symb.value, symb.arg_type)

            elif instruction.opcode in self.arithmetic:
                self.check_arithmetic(instruction)
                float_flag = self.find_arg(instruction.args[1]).arg_type == 'float'
                var = self.find_arg(instruction.args[0])
                symb1 = self.find_arg(instruction.args[1])
                symb2 = self.find_arg(instruction.args[2])
                if not float_flag:
                    if not (self.is_number_with_optional_minus(symb1.value) and self.is_number_with_optional_minus(symb2.value)):
                        if DEBUG:
                            print("Invalid types for arithmetic operation")
                            print(symb1.value, symb2.value)
                        exit(32)
                    if instruction.opcode == 'ADD':
                        self.set_var(var, int(symb1.value) + int(symb2.value), symb1.arg_type)
                    elif instruction.opcode == 'SUB':
                        self.set_var(var, int(symb1.value) - int(symb2.value), symb1.arg_type)
                    elif instruction.opcode == 'MUL':
                        self.set_var(var, int(symb1.value) * int(symb2.value), symb1.arg_type)
                    elif instruction.opcode == 'IDIV':
                        if symb2.value == '0':
                            if DEBUG:
                                print("Division by zero")
                            exit(57)
                        self.set_var(var, int(symb1.value) // int(symb2.value), symb1.arg_type)
                else:
                    number1 = float.fromhex(symb1.value)
                    number2 = float.fromhex(symb2.value)
                    if instruction.opcode == 'ADD':
                        self.set_var(var, float.hex(number1 + number2), symb1.arg_type)
                    elif instruction.opcode == 'SUB':
                        self.set_var(var, float.hex(number1 - number2), symb1.arg_type)
                    elif instruction.opcode == 'MUL':
                        self.set_var(var, float.hex(number1 * number2), symb1.arg_type)
                    elif instruction.opcode == 'DIV':
                        if number2 == 0:
                            if DEBUG:
                                print("Division by zero")
                            exit(57)
                        self.set_var(var, float.hex(number1 // number2), symb1.arg_type)


            elif instruction.opcode == 'WRITE':
                symb = self.find_arg(instruction.args[0])
                if symb.value == 'nil':
                    print('', end='')
                if symb.value is not None:
                    print(symb.value, end='')



        #print the defined variables
        if DEBUG:
            for arg in self.defined_vars:
                print("debug print:", arg.name, arg.value, arg.arg_type, arg.frame)

class Parser:
    def __init__(self):
        self.instructions = []
        self.orders = []
        self.arg_pattern = "arg[1-9][0-9]*"
        # self.valid_arg_types = ['label', 'var', 'type', 'symb', 'int', 'bool', 'string', 'nil', 'float']

    def sort_instructions(self):
        self.instructions.sort(key=lambda x: x.order)

    def is_valid_order(self, order):
        if order is None:
            return False
        try:
            if int(order) < 1:
                return False
        except ValueError:
            return False
        if order in self.orders:
            return False
        self.orders.append(order)
        return True

    def is_valid_opcode(self, opcode):
        if opcode is None:
            return False
        opcode = opcode.upper()
        if opcode not in instructions_map.instructions_map:
            return False
        return True

    def verify_xml(self, xml):
        root = self.parse_xml(xml)
        # check if root element is valid
        if root is None:
            if DEBUG:
                print("No root element")
            sys.exit(31)

        # check if root element is program
        if root.tag != "program" or root.attrib["language"] != "IPPcode23":
            if DEBUG:
                print("Invalid root element")
            sys.exit(32)

        for instruction in root:
            if instruction.tag != "instruction":
                if DEBUG:
                    print("Invalid instruction")
                sys.exit(32)
            opcode = instruction.attrib.get("opcode")
            order = instruction.attrib.get("order")

            if not self.is_valid_opcode(opcode) or not self.is_valid_order(order):
                if DEBUG:
                    print("Invalid opcode or order")
                sys.exit(32)

            ins = Instruction(opcode, order)
            for arg in instruction:
                # check whether the tag is valid
                if not re.match(self.arg_pattern, arg.tag):
                    if DEBUG:
                        print("Invalid argument")
                    sys.exit(32)
                arg_word = ET.tostring(arg, encoding='unicode', method='xml').strip()
                arg_num = arg_word.split(" ")[0][4:]
                arg_frame = arg_word.split(" ")[1][11:13]
                arg_type = arg.attrib.get("type")
                var_name = arg_word.split(" ")[1][14:-7]
                if arg_type == 'var':
                    argument = Argument(arg_type, None, arg_num, arg_frame, var_name)
                else:
                    argument = Argument(arg_type, arg.text, arg_num)
                ins.add_argument(argument)
            self.instructions.append(ins)
            # print the arguments of instructions
            ins.sort_arguments()
        self.sort_instructions()
        # for ins in self.instructions:
        #     ins.print_arguments()

    def parse_xml(self, xml):
        try:
            root = ET.fromstring(xml)
            return root
        except Exception:
            if DEBUG:
                print("Invalid XML")
            sys.exit(31)

    def read_file_content(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def parse_arguments(self):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--source', type=str, metavar='file',
                            help='Input file with the XML representation of the source code.')
        parser.add_argument('--input', type=str, metavar='file',
                            help='File with inputs for the actual interpretation of the source code.')
        parser.add_argument("--help", "--h", action="store_true",
                            help="Show this help message")
        args = parser.parse_args()

        # help argument is not allowed with --source or --input
        if args.help and (args.source or args.input):
            if DEBUG:
                print("Help argument is not allowed with --source or --input")
            sys.exit(10)

        if not args.source and not args.input:
            if DEBUG:
                print("No arguments provided")
            sys.exit(10)

        if not args.source and args.input:
            if DEBUG:
                (print("Source file is not provided"))
            args.source = sys.stdin.read()
            args.input = self.read_file_content(args.input)
            return args

        if args.source and not args.input:
            if DEBUG:
                print("Input file is not provided")
            args.input = sys.stdin.read()
            args.source = self.read_file_content(args.source)
            return args

        if args.source and args.input:
            if DEBUG:
                print("Both source and input files are provided")
            args.input = self.read_file_content(args.input)
            args.source = self.read_file_content(args.source)
            return args

        return args


def main():
    parser = Parser()
    args = parser.parse_arguments()
    parser.verify_xml(args.source)
    interpreter = Interpreter(parser,args)
    interpreter.execute()

    if DEBUG:
        print(f"Source file: {args.source}")
        print(f"Input file: {args.input}")


if __name__ == "__main__":
    main()
