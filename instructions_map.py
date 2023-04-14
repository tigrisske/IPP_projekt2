from enum import Enum

class ArgTypeEnum(Enum):


    LABEL = 1
    SYMBOL = 2
    TYPE = 3
    VARIABLE = 4

    @staticmethod
    def compare_types(self, given, expected):
        if expected == given.big_type:
            return True
        if expected == ArgTypeEnum.SYMBOL and given.big_type == ArgTypeEnum.VARIABLE:
            return True
        return False

const = ['int', 'bool', 'string', 'nil', 'float']
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
    "JUMPIFEQS": [ArgTypeEnum.LABEL],
    "JUMPIFNEQS": [ArgTypeEnum.LABEL],
    "INT2FLOAT": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL],
    "FLOAT2INT": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL],
    "DIV": [ArgTypeEnum.VARIABLE, ArgTypeEnum.SYMBOL, ArgTypeEnum.SYMBOL],
}