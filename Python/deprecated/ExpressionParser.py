# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 17:46:40 2023

@author: 160047412
"""

import pyparsing as pp
import numpy as np

class ExpressionParser:
    def eval(s='2*2', variables={}, functions={}):
        for var_name in variables.keys():
            EvalConstant.vars_[var_name] = variables[var_name]
        
        for fun_name in functions.keys():
            EvalFunction.funs_[fun_name] = functions[fun_name]
            
        return expression.parseString(s)[0].eval()

class EvalTuple:
    "Class to evaluate a parsed tuple"
    
    def __init__(self, tokens):
        self.values = [i for j in tokens for i in j]
    
    def eval(self):
        print(self.values)
        return tuple([arg.eval() for arg in self.values])

class EvalList:
    "Class to evaluate a parsed list"
    
    def __init__(self, tokens):
        self.values = [i for j in tokens for i in j]
    
    def eval(self):
        return [arg[0].eval() for arg in self.values]

class EvalFunction:
    "Class to evaluate a parsed function"
    funs_ = {
        'array': np.array,
        'ndarray': np.ndarray,
        'linspace': np.linspace,
        'arange': np.arange,
        'meshgrid': np.meshgrid,
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        'asin': np.arcsin,
        'acos': np.arccos,
        'atan': np.arctan,
        'atan2': np.arctan2,
        'sinh': np.sinh,
        'cosh': np.cosh,
        'tanh': np.tanh,
        'sinc': np.sinc,
        'exp': np.exp,
        'degrees': np.degrees,
        'radians': np.radians,
        'abs': np.absolute,
        'angle': np.angle,
        'mod': np.mod,
        'real': np.real,
        'imag': np.imag,
        'conj': np.conj,
        'max': np.max,
        'min': np.min,
        'sqrt': np.sqrt,
        'cbrt': np.cbrt,
        'log': np.log,
        'log10': np.log10,
        'log2': np.log2,
        'in_db': lambda G: 20*np.log10(G),
        'sign': np.sign,
        'interp': np.interp,
        'floor': np.floor,
        'ceil': np.ceil,
        'sum': np.sum,
        'cumsum': np.cumsum,
        'prod': np.prod,
        'U': lambda a,t: np.array(t)>=np.array(a)
    }

    def __init__(self, tokens):
        self.name = tokens.pop(0)
        self.values = [i for j in tokens for i in j]

    def eval(self):
        if self.name in EvalFunction.funs_:
            args = [arg[0].eval() for arg in self.values]
            return EvalFunction.funs_[self.name](*args)
        else:
            raise Exception('Unknown function ' + str(self.name))

class EvalConstant:
    "Class to evaluate a parsed constant or variable"
    vars_ = {}

    def __init__(self, tokens):
        self.value = tokens[0]

    def eval(self):
        # print(self.value)
        if self.value in EvalConstant.vars_:
            return EvalConstant.vars_[self.value]
        else:
            try:
                return int(self.value)
            except ValueError:
                try:
                    return float(self.value)
                except ValueError:
                    return complex(self.value)

class EvalSignOp:
    "Class to evaluate expressions with a leading + or - sign"

    def __init__(self, tokens):
        self.sign, self.value = tokens[0]

    def eval(self):
        mult = {"+": 1, "-": -1}[self.sign]
        return mult * self.value.eval()


def operatorOperands(tokenlist):
    "generator to extract operators and operands in pairs"
    it = iter(tokenlist)
    while 1:
        try:
            yield (next(it), next(it))
        except StopIteration:
            break


class EvalPowerOp:
    "Class to evaluate power expressions"

    def __init__(self, tokens):
        self.value = tokens[0]

    def eval(self):
        res = self.value[-1].eval()
        for val in self.value[-3::-2]:
            res = val.eval() ** res
        return res


class EvalMultOp:
    "Class to evaluate multiplication and division expressions"

    def __init__(self, tokens):
        self.value = tokens[0]

    def eval(self):
        prod = self.value[0].eval()
        for op, val in operatorOperands(self.value[1:]):
            if op == "*":
                prod *= val.eval()
            if op == "/":
                prod /= val.eval()
        return prod


class EvalAddOp:
    "Class to evaluate addition and subtraction expressions"

    def __init__(self, tokens):
        self.value = tokens[0]

    def eval(self):
        value = self.value[0].eval()
        print(value)
        for op, val in operatorOperands(self.value[1:]):
            if op == "+":
                print(val.eval())
                value = value + val.eval()
            if op == "-":
                value = value - val.eval()
        return value


class EvalFactOp:
    "Class to evaluate factorial expressions"

    def __init__(self, tokens):
        self.value = tokens[0]

    def eval(self):
        N = self.value[0].eval()
        prod = 1
        for i in range(1,N+1):
            prod *= i
        return prod


class EvalComparisonOp:
    "Class to evaluate comparison expressions"
    opMap = {
        "<": lambda a, b: a < b,
        "<=": lambda a, b: a <= b,
        ">": lambda a, b: a > b,
        ">=": lambda a, b: a >= b,
        "!=": lambda a, b: a != b,
        "=": lambda a, b: a == b,
        "LT": lambda a, b: a < b,
        "LE": lambda a, b: a <= b,
        "GT": lambda a, b: a > b,
        "GE": lambda a, b: a >= b,
        "NE": lambda a, b: a != b,
        "EQ": lambda a, b: a == b,
        "<>": lambda a, b: a != b,
    }

    def __init__(self, tokens):
        self.value = tokens[0]

    def eval(self):
        val1 = self.value[0].eval()
        for op, val in operatorOperands(self.value[1:]):
            fn = EvalComparisonOp.opMap[op]
            val2 = val.eval()
            val1 = fn(val1, val2)
        return val1

debug_flag = False

integer = pp.Word(pp.nums)
real = pp.Combine(integer + '.' + integer) | integer
imaginary = pp.Combine(real + 'j')
cmplx = pp.Combine(real + '+' + imaginary)
variable = pp.Word(pp.alphanums + '_')
number = cmplx | imaginary | real | integer
# operand = cmplx | imaginary | real | integer | variable

signop = pp.oneOf("+ -")
multop = pp.oneOf("* /")
plusop = pp.oneOf("+ -")
expop = pp.Literal("**")

operand = pp.Forward()
expression = pp.Forward()
expression_list = pp.delimitedList(pp.Group(expression))
lpar = pp.Literal('(').suppress()
rpar = pp.Literal(')').suppress()
fn_call = pp.Word(pp.alphanums + '_') + lpar + pp.Optional(pp.Group(expression_list)) + rpar

lpar = pp.Literal('(').suppress()
rpar = pp.Literal(')').suppress()
tpl = lpar + pp.Group(expression) + pp.Literal(',').suppress() + pp.Optional(pp.delimitedList(pp.Group(expression),allow_trailing_delim=True)) + rpar

lpar = pp.Literal('[').suppress()
rpar = pp.Literal(']').suppress()
lst = lpar + pp.Group(expression) + pp.Literal(',').suppress() + pp.Optional(pp.delimitedList(pp.Group(expression),allow_trailing_delim=True)) + rpar

operand <<= number | fn_call | lst | tpl | variable

# use parse actions to attach EvalXXX constructors to sub-expressions
# operand.setParseAction(EvalConstant)

number.setParseAction(EvalConstant)
variable.setParseAction(EvalConstant)
tpl.setParseAction(EvalTuple)
lst.setParseAction(EvalList)
fn_call.setParseAction(EvalFunction)

comparisonop = pp.oneOf("< <= > >= != = <> LT GT LE GE EQ NE")
arith_expr = pp.infixNotation(
    operand,
    [
        ("!", 1, pp.opAssoc.LEFT, EvalFactOp),
        (expop, 2, pp.opAssoc.RIGHT, EvalPowerOp),
        (signop, 1, pp.opAssoc.RIGHT, EvalSignOp),
        (multop, 2, pp.opAssoc.LEFT, EvalMultOp),
        (plusop, 2, pp.opAssoc.LEFT, EvalAddOp),
        (comparisonop, 2, pp.opAssoc.LEFT, EvalComparisonOp),
    ],
)

comp_expr = pp.infixNotation(
    operand,
    [
    ],
)

expression <<= arith_expr


if __name__=='__main__':
    debug_flag = True
    dbg_step = 11
    if debug_flag:
        if dbg_step==1:
            EvalConstant.vars_['newvar'] = 10
            EvalConstant.vars_['another_var_'] = 3.61+8.41j
            EvalConstant.vars_['yet_4n0ther_v4r'] = 900
            EvalConstant.vars_['pi'] = np.pi
            EvalConstant.vars_['e'] = np.e
            EvalConstant.vars_['epp'] = np.e+np.pi
            
            print(real.parseString('3.4'))
            print(imaginary.parseString('3j'))
            print(cmplx.parseString('3.4+4.36j'))
            s = 'newvar'
            print(s + ' = ' + str(variable.parseString(s)[0].eval()))
            s = 'another_var_'
            print(s + ' = ' + str(variable.parseString(s)[0].eval()))
            s = 'yet_4n0ther_v4r'
            print(s + ' = ' + str(variable.parseString(s)[0].eval()))
        elif dbg_step==2:
            EvalFunction.funs_['f'] = lambda a: a+5
            EvalFunction.funs_['g'] = lambda a,b: a*b
            EvalFunction.funs_['h'] = lambda : 41
            EvalFunction.funs_['sin'] = np.sin
            
            s = 'f(2)'
            ret = fn_call.parseString(s)
            parsedValue = ret[0].eval()
            print(s + ' = ' + str(parsedValue))
            # print(fn_call.parseString(s))
            
            s = 'f(2+3)'
            print(s + ' = ' + str(fn_call.parseString(s)[0].eval()))
            # print(fn_call.parseString(s))
            
            s = '4 + f(2)'
            print(s + ' = ' + str(expression.parseString(s)[0].eval()))
            # print(expression.parseString(s))
            
            s = 'g(2,3)'
            print(s + ' = ' + str(expression.parseString(s)[0].eval()))
            # print(expression.parseString(s))
            
            s = 'g(45-h(),3)'
            print(s + ' = ' + str(expression.parseString(s)[0].eval()))
            # print(expression.parseString(s))
            
            s = '3+3.4j + (newvar + pi) + sin(2)'
            
            ret = expression.parseString(s)
            parsedValue = ret[0].eval()
            print(s + ' = ' + str(parsedValue))
            
            s = 'pi'
            print(s + ' = ' + str(expression.parseString(s)[0].eval()))
            # print(expression.parseString(s))
            
            s = 'e'
            print(s + ' = ' + str(expression.parseString(s)[0].eval()))
            # print(expression.parseString(s))
            
            s = 'epp'
            print(s + ' = ' + str(expression.parseString(s)[0].eval()))
            # print(expression.parseString(s))
            
            s = 'e+pi'
            print(s + ' = ' + str(expression.parseString(s)[0].eval()))
            # print(expression.parseString(s))
        elif dbg_step==3:
            array = np.array([1,2,3])
            new_variables = {
                'array' : array
            }
            new_functions = {
                'linspace' : np.linspace,
                'array' : np.array
            }
            s = 'array + linspace(1,3,3)'
            print(s + ' = ' + str(ExpressionParser.eval(s=s,variables=new_variables,functions=new_functions)))
            # print(expression.parseString(s))
        elif dbg_step==4:
            s = '(1,2,3)'
            print(s + ' = ' + str(ExpressionParser.eval(s=s)))
        elif dbg_step==5:
            s = '[1,2,3]'
            print(s + ' = ' + str(ExpressionParser.eval(s=s)))
        elif dbg_step==6:
            s = '(1,2,3)*2'
            print(s + ' = ' + str(ExpressionParser.eval(s=s)))
        elif dbg_step==7:
            s = 'array([1,2,3]) + linspace(1,3,3)'
            print(s + ' = ' + str(ExpressionParser.eval(s=s,functions=new_functions)))
        elif dbg_step==8:
            s = 'in_db(0.5)'
            print(s + ' = ' + str(ExpressionParser.eval(s=s)))
        elif dbg_step==9:
            s = '(1)'
            print(s + ' = ' + str(ExpressionParser.eval(s=s)))
            s = '(1,)'
            print(s + ' = ' + str(ExpressionParser.eval(s=s)))
            s = '(1,2,)'
            print(s + ' = ' + str(ExpressionParser.eval(s=s)))
        elif dbg_step==10:
            s = '3 < 1.5'
            print(s + ' = ' + str(ExpressionParser.eval(s=s)))
            s = 'linspace(1,3,11) >= 1.5'
            print(s + ' = ' + str(ExpressionParser.eval(s=s)))
        elif dbg_step==11:
            theta = np.radians(np.linspace(0,180,21))
            phi = np.radians(np.linspace(-180,180,21))
            mesh_phi,mesh_theta = np.meshgrid(phi,theta)
            v = {
                'theta': mesh_theta,
                'phi': mesh_phi,
                'pi': np.pi
            }
            s = '(cos(pi/2*cos(theta)) - cos(pi/2))/(sin(theta))'
            print(s + ' = ' + str(ExpressionParser.eval(s=s,variables=v)))
        
    else:
        # Display instructions on how to quit the program
        print("Type in the string to be parsed or 'quit' to exit the program")
        input_string = input("> ")
        
        while input_string.strip().lower() != "quit":
            if input_string.strip().lower() == "debug":
                debug_flag = True
                input_string = input("> ")
                continue
    
            if input_string != "":
                # try parsing the input string
                try:
                    L = expression.parseString(input_string)
                except pp.ParseException as err:
                    L = ["Parse Failure", input_string, (str(err), err.line, err.column)]
    
                # show result of parsing the input string
                if len(L) == 0 or L[0] != "Parse Failure":
                    print(input_string, "=", L[0].eval())
    
            # obtain new input string
            input_string = input("> ")
    
        # if user type 'quit' then say goodbye
        print("Good bye!")