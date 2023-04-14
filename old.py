import re
import sys
import argparse
from curses.ascii import isdigit
from enum import Enum
from xml.etree import ElementTree as ET
import abc

DEBUG = False


class TypeEnum(Enum):
    INT = 1
    FLOAT = 2
    STRING = 3
    BOOL = 4
    NIL = 5


class ArgTypeEnum(Enum):
    LABEL = 1
    SYMBOL = 2
    TYPE = 3
    VARIABLE = 4

    @staticmethod
    def get_type(arg):
        if arg == 'int':
            return ArgTypeEnum.SYMBOL
        elif arg == 'bool':
            return ArgTypeEnum.SYMBOL
        elif arg == 'string':
            return ArgTypeEnum.SYMBOL
        elif arg == 'nil':
            return ArgTypeEnum.SYMBOL
        elif arg == 'var':
            return ArgTypeEnum.VARIABLE
        elif arg == 'label':
            return ArgTypeEnum.LABEL
        elif arg == 'type':
            return ArgTypeEnum.TYPE
        else:
            return None

    @staticmethod
    def compare_types(type, expected):
        if type:
            return True
        if type == ArgTypeEnum.VARIABLE and expected == ArgTypeEnum.SYMBOL:
            return True


instructions_map = {
    "MOVE": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL],
    "CREATEFRAME": [],
    "PUSHFRAME": [],
    "POPFRAME": [],
    "DEFVAR": [ArgTypeEnum.VARIABLE],
    "CALL": [ArgTypeEnum.LABEL],
    "RETURN": [],
    "PUSHS": [ArgTypeEnum.SYMBOL],
    "POPS": [ArgTypeEnum.VARIABLE],
    "ADD": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "SUB": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "MUL": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "IDIV": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "LT": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "GT": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "EQ": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "AND": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "OR": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "NOT": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL],
    "INT2CHAR": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL],
    "STRI2INT": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "READ": [ArgTypeEnum.VARIABLE, ArgTypeEnum.TYPE],
    "WRITE": [ArgTypeEnum.SYMBOL],
    "CONCAT": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "STRLEN": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL],
    "GETCHAR": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "SETCHAR": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "TYPE": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL],
    "LABEL": [ArgTypeEnum.LABEL],
    "JUMP": [ArgTypeEnum.LABEL],
    "JUMPIFEQ": [ArgTypeEnum.LABEL, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "JUMPIFNEQ": [ArgTypeEnum.LABEL, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
    "EXIT": [ArgTypeEnum.SYMBOL],
    "DPRINT": [ArgTypeEnum.SYMBOL],
    "BREAK": [],
    # TODO might delete these
    "CLEARS": [],
    "ADDS": [],
    "SUBS": [],
    "MULS": [],
    "IDIVS": [],
    "LTS": [],
    "GTS": [],
    "EQS": [],
    "ANDS": [],
    "ORS": [],
    "NOTS": [],
    "INT2CHARS": [],
    "STRI2INTS": [],
    "JUMPIFEQS": [],
    "JUMPIFNEQS": [],
    "INT2FLOAT": [],
    "FLOAT2INT": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL],
    "DIV": [],
}


class Argument:
    arg_typeBIG = None
    arg_typeSMALL = None
    is_var = False

    def __init__(self, arg_type, arg_value, arg_order, arg_frame):
        if arg_type == 'int' or arg_type == 'float' or arg_type == 'bool' or arg_type == 'string' or arg_type == 'nil':
            self.arg_typeBIG = ArgTypeEnum.SYMBOL
            self.arg_typeSMALL = arg_type
            self.arg_value = arg_value
            self.arg_order = arg_order
        elif arg_type == 'var':
            self.arg_typeBIG = ArgTypeEnum.VARIABLE
            self.arg_typeSMALL = None
            self.arg_var_frame = arg_frame
            self.arg_var_name = arg_value
            self.is_var = True
            self.arg_order = arg_order
        elif arg_type == 'label':
            self.arg_typeBIG = ArgTypeEnum.LABEL
            self.arg_typeSMALL = arg_type
            self.arg_value = arg_value
            self.arg_order = arg_order
        elif arg_type == 'type':
            self.arg_typeBIG = ArgTypeEnum.TYPE
            self.arg_typeSMALL = arg_type
            self.arg_value = arg_value
            self.arg_order = arg_order

    def print_arg(self):
        print(self.arg_typeBIG, self.arg_value, self.arg_order)


class Symbol(Argument):
    type = None
    pass


class Variable(Symbol):
    pass


class Constant(Symbol):
    pass


class Label:
    pass


class Instruction(abc.ABC):
    order = None
    opcode = None

    def __init__(self, opcode):
        self.args = []
        self.opcode = opcode

    @abc.abstractmethod
    def execute(self):
        pass

    def add_order(self, order):
        self.order = order

    def add_arg(self, arg_type, arg_value, arg_order, arg_frame):
        self.args.append(Argument(arg_type, arg_value, arg_order, arg_frame))

    def print_instruction(self):
        print(self.opcode)
        for arg in self.args:
            arg.print_arg()


class ADD(Instruction):
    def __init__(self):
        super().__init__()

    def execute(self):
        # first check the number of arguments
        if len(self.args) != len(instructions_map[self.opcode]):
            exit(32)
        # check the types of arguments
        # for i in range(len(self.args)):


class DEFVAR(Instruction):
    def execute(self):
        pass


class MOVE(Instruction):
    def execute(self):
        pass


# Class to represent an instruction
# class Instruction:
#     order = None
#     arithmetic = ['ADD', 'SUB', 'MUL']
#
#     def __init__(self, opcode):
#         self.args = []
#         self.opcode = opcode
#
#     def add_arg(self, arg_type, arg_value, arg_order):
#         if arg_type == 'int' and not arg_value.isdigit():
#             # print(isinstance(arg_value, int))
#             # print(arg_value)
#             # print("Invalid argument value for opcode: " + self.opcode)
#             exit(32)
#         self.args.append(Argument(arg_type, arg_value, arg_order))
#
#     def set_order(self, order):
#         self.order = order
#
#     def print_instruction(self):
#         print("opcode :" + self.opcode)
#         for arg in self.args:
#             print(arg.arg_type, arg.arg_value, arg.arg_order)
#         print('-------------')
#
#     def validate_args(self):
#         self.args = sorted(self.args, key=lambda x: x.arg_order)
#         if self.opcode not in instructions_map:
#             if DEBUG:
#                 print("Invalid opcode: " + self.opcode)
#             exit(32)
#         if len(instructions_map[self.opcode]) != len(self.args):
#             print("Invalid number of arguments for opcode: " + self.opcode)
#             print(len(instructions_map[self.opcode]))
#             print(len(self.args))
#             exit(32)
#         for i in range(len(self.args)):
#             if ArgTypeEnum.compare_types(self.args[i].arg_type, instructions_map[self.opcode][i]) is False:
#                 # print("Invalid argument type for opcode: " + self.opcode)
#                 exit(53)
#
#     def execute(self, interpreter):
#         pass
#         # TODO: Implement the execution logic for each instruction here


# Class to represent the interpreter
class Interpreter:
    def __init__(self):
        self.instructions = []
        self.global_frame = {}

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def execute_instructions(self):
        for instruction in sorted(self.instructions, key=lambda x: x.order):
            instruction.execute(self)


class Parser:
    # source = None
    # input = None
    arg_pattern = "<arg[1-9][0-9]*"
    orders = []
    instructions = []

    def order_valid(self, order):
        if order == None:
            return False
        try:
            if int(order) < 1:
                return False
        except Exception:
            return False
        if order in self.orders:
            return False
        self.orders.append(order)
        return True

    def __init__(self):
        self.instructions = []
        self.expected_opcode = 1
        self.valid_arg_types = ['label', 'var', 'type', 'symb', 'int', 'bool', 'string', 'nil', 'float']

    def verify_xml(self, args):
        root = self.parse_xml(args)
        if root == None:
            sys.exit(31)
        if root.tag != 'program' or root.attrib.get('language') != 'IPPcode23':
            print("Invalid root tag or language")
            exit(32)

        for child in root:
            if child.tag != 'instruction':
                print("Invalid instruction tag")
                exit(32)
            opcode = child.attrib.get('opcode')
            order = child.attrib.get('order')

            if opcode is None or not self.order_valid(order):
                print("Invalid order or opcode")
                exit(32)

            # invalid  instruction name
            if opcode not in instructions_map:
                # print(opcode)
                # print(instructions)
                print("Invalid opcode: " + opcode)
                exit(32)

            instruction = globals().get(opcode)
            args = []
            for arg in child:
                arg_string = ET.tostring(arg, encoding='unicode', method='xml').strip().split(' ')
                arg_string0 = (arg_string[0])
                arg_string1 = (arg_string[1])
                # bad argument
                if not re.match(self.arg_pattern, arg_string0):
                    print("Invalid argument: " + arg_string0)
                    exit(32)
                else:
                    arg_type = arg.attrib.get('type')
                    if arg_type not in self.valid_arg_types:
                        print("Invalid argument type: " + arg_type)
                        exit(56)
                    if arg_type == 'var':
                        instruction.add_arg(arg_type, arg.text, arg_string0[4:], 3,2)#arg_string1[11:13])
                    else:
                        instruction.add_arg(arg_type, arg.text, arg_string0[4:], None)
            # instruction.set_order(order)
            # instruction.validate_args()
            self.instructions.append(instruction)

    def parse_xml(self, xml):
        try:
            root = ET.fromstring(xml)
            return root
        except Exception:
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
            sys.exit(10)

        if not args.source and not args.input:
            parser.error('At least one of --source or --input must be provided')
            sys.exit(10)

        if not args.source and args.input:
            (print("Source file is not provided"))
            args.source = sys.stdin.read()
            args.input = self.read_file_content(args.input)
            return args

        if args.source and not args.input:
            print("Input file is not provided")
            args.input = sys.stdin.read()
            args.source = self.read_file_content(args.source)
            return args

        if args.source and args.input:
            # print("Both source and input files are provided")
            args.input = self.read_file_content(args.input)
            args.source = self.read_file_content(args.source)
            return args

        return args


def main():
    # my_var = Variable()
    # print(my_var.type)
    # print(isinstance(my_var, Symbol))

    # string = "ADD"
    # instruction_class = globals()[string]
    # ins = instruction_class()
    # ins.execute()

    parser = Parser()
    args = parser.parse_arguments()
    parser.verify_xml(args.source)
    print('test')
    # print out all the instructions with its arguments
    for instruction in parser.instructions:
        instruction.print_instruction()
    print(f"Source file: {args.source}")
    print(f"Input file: {args.input}")


if __name__ == "__main__":
    main()