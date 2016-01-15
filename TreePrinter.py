import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.BinExpr)
    def printTree(self, depth):
        res = depth + str(self.op) + "\n"
        res += self.left.printTree(depth + "| ")
        res += self.right.printTree(depth + "| ")
        return res

    @addToClass(AST.Const)
    def printTree(self, depth):
        return depth + str(self.value) + "\n"

    @addToClass(AST.Variable)
    def printTree(self, depth):
        return depth + str(self.id) + "\n"

    @addToClass(AST.Blocks)
    def printTree(self, depth):
        res = ""
        for block in self.children:
            res += block.printTree(depth)
        return res

    @addToClass(AST.Declarations)
    def printTree(self, depth):
        res = ""
        for decl in self.children:
            res += decl.printTree(depth + "| ")
        return res

    @addToClass(AST.Declaration)
    def printTree(self, depth):
        return depth + "DECL\n" + self.inits.printTree(depth + "| ")

    @addToClass(AST.Inits)
    def printTree(self, depth):
        res = ""
        for init in self.children:
            res += init.printTree(depth)
        return res

    @addToClass(AST.Init)
    def printTree(self, depth):
        res = depth + "=\n"
        res += depth + "| " + str(self.id) + "\n"
        res += self.expression.printTree(depth + "| ")
        return res

    @addToClass(AST.FunctionDefinition)
    def printTree(self, depth):
        res = depth + "FUNDEF\n"
        depth += "| "
        res += depth + str(self.id) + "\n"
        res += depth + "RET " + str(self.type) + "\n"
        res += self.args.printTree(depth)
        res += self.body.printTree(depth)
        return res

    @addToClass(AST.Args)
    def printTree(self, depth):
        res = ""
        for arg in self.children:
            res += arg.printTree(depth)
        return res

    @addToClass(AST.Arg)
    def printTree(self, depth):
        return depth + "ARG " + str(self.type) + " " + str(self.id) + "\n"

    @addToClass(AST.Assignment)
    def printTree(self, depth):
        res = depth + "=\n"
        res += depth + "| " + str(self.id) + "\n"
        res += self.expression.printTree(depth + "| ")
        return res

    @addToClass(AST.Instructions)
    def printTree(self, depth):
        res = ""
        for instr in self.children:
            res += instr.printTree(depth)
        return res

    @addToClass(AST.PrintInstruction)
    def printTree(self, depth):
        res = depth + "PRINT\n"
        res += self.expression.printTree(depth + "| ")
        return res

    @addToClass(AST.IfInstruction)
    def printTree(self, depth):
        res = depth + "IF\n"
        res += self.condition.printTree(depth + "| ")
        res += self.ifInstruction.printTree(depth + "| ")
        if self.elseInstruction is not None:
            res += depth + "ELSE\n"
            res += self.elseInstruction.printTree(depth + "| ")
        return res

    @addToClass(AST.WhileInstruction)
    def printTree(self, depth):
        res = depth + "WHILE\n"
        res += self.condition.printTree(depth + "| ")
        res += self.instruction.printTree(depth + "| ")
        return res

    @addToClass(AST.RepeatInstruction)
    def printTree(self, depth):
        res = depth + "REPEAT\n"
        res += self.instructions.printTree(depth + "| ")
        res += depth + "UNTIL\n"
        res += self.condition.printTree(depth + "| ")
        return res

    @addToClass(AST.ReturnInstruction)
    def printTree(self, depth):
        res = depth + "RETURN\n"
        res += self.expression.printTree(depth + "| ")
        return res

    @addToClass(AST.Continue)
    def printTree(self, depth):
        return depth + "CONTINUE\n"

    @addToClass(AST.Break)
    def printTree(self, depth):
        return depth + "BREAK\n"

    @addToClass(AST.CompoundInstruction)
    def printTree(self, depth):
        res = ""
        if self.declarations is not None:
            res += self.declarations.printTree(depth + "| ")
        res += self.instructions.printTree(depth + "| ")
        return res

    @addToClass(AST.Expressions)
    def printTree(self, depth):
        res = ""
        for expr in self.children:
            res += expr.printTree(depth)
        return res

    @addToClass(AST.FunctionCall)
    def printTree(self, depth):
        res = depth + "FUNCALL\n"
        res += depth + "| " + str(self.id) + "\n"
        res += self.argList.printTree(depth + "| ")
        return res
