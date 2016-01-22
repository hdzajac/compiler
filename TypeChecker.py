#!/usr/bin/python

import AST
from SymbolTable import *
from collections import defaultdict

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
for op in ['+', '-', '*', '/', '%', '<', '>', '<<', '>>', '|', '&', '^', '<=', '>=', '==', '!=']:
    ttype[op]['int']['int'] = 'int'

for op in ['+', '-', '*', '/']:
    ttype[op]['int']['float'] = 'float'
    ttype[op]['float']['int'] = 'float'
    ttype[op]['float']['float'] = 'float'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['int']['float'] = 'int'
    ttype[op]['float']['int'] = 'int'
    ttype[op]['float']['float'] = 'int'

ttype['+']['string']['string'] = 'string'
ttype['*']['string']['int'] = 'string'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['string']['string'] = 'int'


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                import AST
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.table = SymbolTable(None, "root")
        self.currentType = ""
        self.currentFun = None
        self.isInLoop = False

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        if ttype[op][type1][type2] is None:
            print("Error: Illegal operation, '{} {} {}': line {}".format(type1, op, type2, node.line))
        return ttype[op][type1][type2]

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        definition = self.table.getGlobal(node.id)
        if definition is None:
            print("Error: Usage of undeclared variable '{}': line {}".format(node.id, node.line))
        else:
            return definition.type

    def visit_Declaration(self, node):
        self.currentType = node.type
        self.visit(node.inits)
        self.currentType = ""

    def visit_Init(self, node):
        exprType = self.visit(node.expression)
        if (self.currentType == exprType) or (self.currentType == "int" and exprType == "float") or (self.currentType == "float" and exprType == "int"):
            if self.table.get(node.id) is not None:
                print("Error: Variable '{}' already declared: line {}".format(node.id, node.line))
            else:
                self.table.put(node.id, VariableSymbol(node.id, self.currentType))
        else:
            print("Error: Assignment of '{}' to '{}': line {}".format(exprType, self.currentType, node.line))

    def visit_PrintInstruction(self, node):
        self.visit(node.expression)

    def visit_Assignment(self, node):
        declaration = self.table.getGlobal(node.id)
        exprType = self.visit(node.expression)
        if declaration is None:
            print("Error: Variable '{}' undefined in current scope: line {}".format(node.id, node.line))
        elif declaration.type == "int" and exprType == "float":
            print("Warning: Assignment of '{}' to '{}' may cause loss of precision: line {}".format(exprType, declaration.type, node.line))
        elif declaration.type == "float" and exprType == "int":
            pass
        elif exprType != declaration.type:
            print("Error: Assignment of '{}' to '{}': line {}". format(exprType, declaration.type, node.line))


    def visit_IfInstruction(self, node):
        self.visit(node.condition)
        self.isInLoop = True
        self.visit(node.ifInstruction)
        self.isInLoop = False
        if node.elseInstruction is not None:
            self.isInLoop = True
            self.visit(node.elseInstruction)
            self.isInLoop = False

    def visit_WhileInstruction(self, node):
        self.visit(node.condition)
        self.isInLoop = True
        self.visit(node.instruction)
        self.isInLoop = False

    def visit_RepeatInstruction(self, node):
        self.isInLoop = True
        self.visit(node.instructions)
        self.isInLoop = False
        self.visit(node.condition)


    def visit_ReturnInstruction(self, node):
        if self.currentFun is None:
            print("Error: return instruction outside a function: line {}".format(node.line))
        else:
            retType = self.visit(node.expression)
            if retType != self.currentFun.type and (self.currentFun.type != "float" or retType != "int"):
                print("Error: Improper returned type, expected {}, got {}: line {}".format(self.currentFun.type, retType, node.line))


    def visit_Continue(self, node):
        if not self.isInLoop:
            print("Error: continue instruction outside a loop: line {}".format(node.line))

    def visit_Break(self, node):
        if not self.isInLoop:
            print("Error: break instruction outside a loop: line {}".format(node.line))


    def visit_CompoundInstruction(self, node):
        innerScope = SymbolTable(self.table, "innerScope")
        self.table = innerScope
        if node.declarations is not None:
            self.visit(node.declarations)
        self.visit(node.instructions)
        self.table = self.table.getParentScope()

    def visit_FunctionCall(self, node):
        funDef = self.table.getGlobal(node.id)
        if funDef is None or not isinstance(funDef, FunctionSymbol):
            print("Error: Call of undefined fun: '{}': line {}".format(node.id, node.line))
        else:
            if len(node.argList.children) != len(funDef.params):
                print("Error: Improper number of args in '{}' call: line {}".format(funDef.id, node.line))
            else:
                types = [self.visit(x) for x in node.argList.children]
                expectedTypes = funDef.params
                for actual, expected in zip(types, expectedTypes):
                    if actual != expected and not (actual == "int" and expected == "float"):
                        print("Error: Improper type of args in {} call: line {}".format(node.id, node.line))
            return funDef.type

    def visit_FunctionDefinition(self, node):
        if self.table.get(node.id) is not None:
            print("Error: Redefinition of function '{}': line {}".format(node.id, node.line))
        else:
            function = FunctionSymbol(node.type, node.id, SymbolTable(self.table, node.id))
            self.table.put(node.id, function)
            self.table = function.symbolTable
            self.currentFun = function
            if node.args is not None:
                self.visit(node.args)
            function.extractParams()
            self.visit(node.body)
            self.table = self.table.getParentScope()
            self.currentFun = None

    def visit_Arg(self, node):
        if self.table.get(node.id) is not None:
            print("Error: Variable '{}' already declared: line {}".format(node.id, node.line))
        else:
            self.table.put(node.id, VariableSymbol(node.id, node.type))