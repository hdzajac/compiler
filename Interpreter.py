import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys
import operator

ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.div,
       "%": operator.mod, "|": operator.or_, "&": operator.and_, "^": operator.xor,
       "&&": operator.and_, "||": operator.or_, "<<": operator.lshift, ">>": operator.rshift,
       "==": operator.eq, "!=": operator.ne, ">": operator.gt, "<": operator.lt,
       "<=": operator.le, ">=": operator.ge}
sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.variableStack = MemoryStack()
        self.functionStack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return ops[node.op](r1, r2)

    @when(AST.Integer)
    def visit(self, node):
        return int(node.value)

    @when(AST.Float)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Variable)
    def visit(self, node):
        return self.variableStack.get(node.id)

    @when(AST.Blocks)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.Declarations)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.Declaration)
    def visit(self, node):
        node.inits.accept(self)

    @when(AST.Inits)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.Init)
    def visit(self, node):
        expression = node.expression.accept(self)
        self.variableStack.insert(node.id, expression)
        return expression

    @when(AST.Instructions)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.PrintInstruction)
    def visit(self, node):
        string = ""
        for expr in node.expression.accept(self):
            string += str(expr)
        print string

    @when(AST.Assignment)
    def visit(self, node):
        expression = node.expression.accept(self)
        self.variableStack.set(node.id, expression)
        return expression

    @when(AST.IfInstruction)
    def visit(self, node):
        if node.condition.accept(self):
            node.ifInstruction.accept(self)
        elif node.elseInstruction is not None:
            node.elseInstruction.accept(self)

    @when(AST.WhileInstruction)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.RepeatInstruction)
    def visit(self, node):
        while True:
            try:
                node.instructions.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass
            if node.condition.accept(self):
                break

    @when(AST.ReturnInstruction)
    def visit(self, node):
        value = node.expression.accept(self)
        raise ReturnValueException(value)

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()

    @when(AST.Break)
    def visit(self, node):
        raise BreakException()

    @when(AST.CompoundInstruction)
    def visit(self, node):
        compound_memory = Memory("compoundScope")
        self.variableStack.push(compound_memory)
        node.declarations.accept(self)
        try:
            node.instructions.accept(self)
        finally:
            self.variableStack.pop()

    @when(AST.FunctionCall)
    def visit(self, node):
        fun = self.functionStack.get(node.id)
        function_memory = Memory(node.id)
        for actualArg, argExpr in zip(fun.args.accept(self), node.argList.accept(self)):
            function_memory.put(actualArg, argExpr)
        self.variableStack.push(function_memory)
        try:
            fun.body.accept(self)
        except ReturnValueException as e:
            return e.value
        finally:
            self.variableStack.pop()

    @when(AST.Expressions)
    def visit(self, node):
        expr_list = []
        for child in node.children:
            expr_list.append(child.accept(self))
        return expr_list

    @when(AST.FunctionDefinition)
    def visit(self, node):
        self.functionStack.insert(node.id, node)

    @when(AST.Args)
    def visit(self, node):
        arg_list = []
        for child in node.children:
            arg_list.append(child.accept(self))
        return arg_list

    @when(AST.Arg)
    def visit(self, node):
        return node.id
