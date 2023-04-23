# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 20:24:44 2023

@author: 160047412
"""

import pyparsing as pp
import numpy as np

class EvalTuple:
    "Class to evaluate a parsed tuple"
    
    def __init__(self, tokens):
        self.values = [i for j in tokens for i in j]
    
    def eval(self):
        return tuple([arg.eval() for arg in self.values])

class EvalList:
    "Class to evaluate a parsed list"
    
    def __init__(self, tokens):
        self.values = [i for j in tokens for i in j]
    
    def eval(self):
        return [arg.eval() for arg in self.values]

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
        'U': lambda a,t: 1*(np.array(t)>=np.array(a))
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
    vars_ = {
        'pi': np.pi,
        'e': np.e
    }

    def __init__(self, tokens):
        self.value = tokens[0]

    def eval(self):
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
        for op, val in operatorOperands(self.value[1:]):
            if op == "+":
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

class NumpyExpressionParser:
    integer = pp.Word(pp.nums)
    real = pp.Combine(pp.Optional(integer) + '.' + integer) | pp.Combine(integer + '.' + pp.Optional(integer)) | integer
    imaginary = pp.Combine(real + 'j')
    cmplx = pp.Combine(real + '+' + imaginary)
    variable = pp.Word(pp.alphanums + '_')
    number = cmplx | imaginary | real | integer
    
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
    
    @staticmethod
    def eval(expression, variables={}, functions={}):
        for var_name in variables.keys():
            EvalConstant.vars_[var_name] = variables[var_name]
        
        for fun_name in functions.keys():
            EvalFunction.funs_[fun_name] = functions[fun_name]
        
        return NumpyExpressionParser.expression.parseString(expression)[0].eval()

if __name__=='__main__':
    theta = np.radians(np.linspace(0,180,21))
    phi = np.radians(np.linspace(-180,180,21))
    mesh_phi,mesh_theta = np.meshgrid(phi,theta)
    v = {
        'theta': mesh_theta,
        'phi': mesh_phi,
        'pi': np.pi
    }
    f = {
        
    }
    # s = '(cos(pi/2*cos(theta)) - cos(pi/2))/(sin(theta)+(sin(theta)==0))'
    # print(s + ' = ' + str(NumpyExpressionParser.eval(expression=s,variables=v,functions=f)))
    s = '[1,1.0,.1,1.]'
    print(s + ' = ' + str(NumpyExpressionParser.eval(expression=s,variables=v,functions=f)))