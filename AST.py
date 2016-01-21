class Node(object):
    pass


class BinExpr(Node):
    def __init__(self, line, left, op, right):
        self.line = line
        self.op = op
        self.left = left
        self.right = right


class Const(Node):
    def __init__(self, line, value):
        self.line = line
        self.value = value


class Integer(Const):
    def __init__(self, line, value):
        Const.__init__(self, line, value)


class Float(Const):
    def __init__(self, line, value):
        Const.__init__(self, line, value)


class String(Const):
    def __init__(self, line, value):
        Const.__init__(self, line, value)


class Variable(Node):
    def __init__(self, line, id):
        self.line = line
        self.id = id


class Blocks(Node):
    def __init__(self):
        self.children = []

    def addBlock(self, block):
        self.children.append(block)


class Declarations(Node):
    def __init__(self):
        self.children = []

    def addDeclaration(self, decl):
        self.children.append(decl)


class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type
        self.inits = inits


class Inits(Node):
    def __init__(self):
        self.children = []

    def addInit(self, init):
        self.children.append(init)


class Init(Node):
    def __init__(self, line, id, expression):
        self.line = line
        self.id = id
        self.expression = expression


class Instructions(Node):
    def __init__(self):
        self.children = []

    def addInstruction(self, inst):
        self.children.append(inst)


class PrintInstruction(Node):
    def __init__(self, line, expression):
        self.line = line
        self.expression = expression


class Assignment(Node):
    def __init__(self, line, id, expression):
        self.line = line
        self.id = id
        self.expression = expression


class IfInstruction(Node):
    def __init__(self, condition, ifInstruction, elseInstruction=None):
        self.condition = condition
        self.ifInstruction = ifInstruction
        self.elseInstruction = elseInstruction


class WhileInstruction(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class RepeatInstruction(Node):
    def __init__(self, instructions, condition):
        self.condition = condition
        self.instructions = instructions


class ReturnInstruction(Node):
    def __init__(self, line, expression):
        self.line = line
        self.expression = expression


class Continue(Node):
    def __init__(self, line):
        self.line = line


class Break(Node):
    def __init__(self, line):
        self.line = line


class CompoundInstruction(Node):
    def __init__(self, line, declarations, instructions):
        self.line = line
        self.declarations = declarations
        self.instructions = instructions


class FunctionCall(Node):
    def __init__(self, line, id, arglist):
        self.line = line
        self.id = id
        self.argList = arglist


class Expressions(Node):
    def __init__(self):
        self.children = []

    def addExpression(self, expr):
        self.children.append(expr)


class FunctionDefinition(Node):
    def __init__(self, line, type, id, args, body):
        self.line = line
        self.type = type
        self.id = id
        self.args = args
        self.body = body


class Args(Node):
    def __init__(self):
        self.children = []

    def addArg(self, arg):
        self.children.append(arg)


class Arg(Node):
    def __init__(self, line, type, id):
        self.line = line
        self.type = type
        self.id = id
