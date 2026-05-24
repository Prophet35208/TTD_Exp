import Tokens as tok

# Terminals

class Terminal:
    def execute(self, context):
        if context.next_terminal_index < len(context.terminal_list):
            if type(self) != type(context.get_next_terminal()):
                context.error_flag = True
                context.error_msg = "expected terminal " + str(type(self))
            context.next_terminal_index += 1
        else:
            context.error_flag = True
            context.error_msg = "end of file but expected terminal " + str(type(self))


class TermInt(Terminal):
    pass


class TermDouble(Terminal):
    pass


class TermIf(Terminal):
    pass


class TermAssignment(Terminal):
    pass


class TermOpenParenthesis(Terminal):
    pass


class TermClosingParenthesis(Terminal):
    pass


class TermOpenCurlyBrace(Terminal):
    pass


class TermClosingCurlyBrace(Terminal):
    pass


class TermSemicolon(Terminal):
    pass


class TermIntLiteral(Terminal):
    def __init__(self, figure = None):
        self.figure = figure


class TermRealLiteral(Terminal):
    def __init__(self, figure = None):
        self.figure = figure


class TermId(Terminal):
    def __init__(self, figure = None):
        self.figure = figure


class TermReturn(Terminal):
    pass


class TermMain(Terminal):
    pass


class TermPlus(Terminal):
    pass


class TermMinus(Terminal):
    pass


class TermAsterisk(Terminal):
    pass


class TermSlash(Terminal):
    pass


class TermPercent(Terminal):
    pass


class TermLess(Terminal):
    pass


class TermGreater(Terminal):
    pass


class TermLessOrEqual(Terminal):
    pass


class TermGreaterOrEqual(Terminal):
    pass


class TermEquation(Terminal):
    pass


class TermInequality(Terminal):
    pass


class TermComma(Terminal):
    pass


### Non-terminals


class Program:
    def execute(self, context):
        if isinstance(context.get_next_terminal(), tok.TermInt) or\
              isinstance(context.get_next_terminal(), tok.TermDouble):
            context.push_in_tape([tok.Datatype(), tok.ObjectWithDatatype(), tok.Program()])


class Datatype:
    def execute(self, context):
        if isinstance(context.get_next_terminal(), TermInt):
            context.push_in_tape([TermInt()])
        elif isinstance(context.get_next_terminal(), TermDouble):
            context.push_in_tape([TermDouble()])
        else:
            context.error_flag = True
            context.error_msg = "Unknown datatype " + type(context.get_next_terminal())


class ObjectWithDatatype:
    def execute(self, context):
        if isinstance(context.get_next_terminal(), TermMain):
            context.push_in_tape([tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(), tok.CompoundStatement()])
        elif isinstance(context.get_next_terminal(), TermId):
            context.push_in_tape([tok.TermId(), tok.Initialization(), tok.VarList(), tok.TermSemicolon()])
        else:
            context.error_flag = True
            context.error_msg = "Expected id"


class VarList:
    def execute(self, context):
        if isinstance(context.get_next_terminal(), tok.TermComma):
            context.push_in_tape([tok.TermComma(), tok.TermId(), tok.Initialization(), tok.VarList()])
        elif isinstance(context.get_next_terminal(), tok.TermSemicolon):
            pass
        else:
            context.error_flag = True
            context.error_msg = "Expected ','"


class Initialization:
    def execute(self, context):
        if isinstance(context.get_next_terminal(), tok.TermAssignment):
            context.push_in_tape([tok.TermAssignment(), tok.Expression()])
        elif isinstance(context.get_next_terminal(), tok.TermSemicolon) or\
                isinstance(context.get_next_terminal(), tok.TermComma):
            pass
        else:
            context.error_flag = True
            context.error_msg = "Expected '='"


class CompoundStatement:
    def execute(self, context):
        context.push_in_tape([tok.TermOpenCurlyBrace(), tok.StatementList(), tok.TermClosingCurlyBrace()])


class StatementList:
    def execute(self, context):
        if isinstance(context.get_next_terminal(), tok.TermInt) or\
                isinstance(context.get_next_terminal(), tok.TermDouble) or\
                isinstance(context.get_next_terminal(), tok.TermReturn) or\
                isinstance(context.get_next_terminal(), tok.TermIf) or\
                isinstance(context.get_next_terminal(), tok.TermId) or\
                isinstance(context.get_next_terminal(), tok.TermOpenCurlyBrace) or\
                isinstance(context.get_next_terminal(), tok.TermSemicolon):
            context.push_in_tape([tok.Statement(), tok.StatementList()])
        elif isinstance(context.get_next_terminal(), tok.TermClosingCurlyBrace):
            pass
        else:
            context.error_flag = True
            context.error_msg = "Expected statement"


class Statement:
    def execute(self, context):
        if isinstance(context.get_next_terminal(), tok.TermOpenCurlyBrace):
            context.push_in_tape([tok.CompoundStatement()])
        elif isinstance(context.get_next_terminal(), tok.TermId):
            context.push_in_tape([tok.TermId(), tok.TermAssignment(), tok.Expression(), tok.TermSemicolon()])
        elif isinstance(context.get_next_terminal(), tok.TermInt):
            context.push_in_tape([tok.Datatype(), tok.TermId(), tok.Initialization(), tok.VarList(), tok.TermSemicolon()])
        elif isinstance(context.get_next_terminal(), tok.TermDouble):
            context.push_in_tape([tok.Datatype(), tok.TermId(), tok.Initialization(), tok.VarList(), tok.TermSemicolon()])
        elif isinstance(context.get_next_terminal(), tok.TermIf):
            context.push_in_tape([tok.TermIf(), tok.TermOpenParenthesis(), tok.Expression(), tok.TermClosingParenthesis(), tok.Statement()])
        elif isinstance(context.get_next_terminal(), tok.TermReturn):
            context.push_in_tape([tok.TermReturn(), tok.Expression()])
        elif isinstance(context.get_next_terminal(), tok.TermSemicolon):
            context.push_in_tape([tok.TermSemicolon()])
        else:
            context.error_flag = True
            context.error_msg = "Expected statement"


expr_follow_1 = [tok.TermPlus, 
                tok.TermMinus, 
                tok.TermAsterisk, 
                tok.TermSlash, 
                tok.TermPercent,
                tok.TermEquation,
                tok.TermInequality,
                tok.TermGreater,
                tok.TermGreaterOrEqual,
                tok.TermLess,
                tok.TermLessOrEqual,
                tok.TermOpenParenthesis,
                tok.TermClosingParenthesis,
                tok.TermSemicolon,
                tok.TermComma]


class Expression:
    def execute(self, context):
        context.push_in_tape([tok.Expr2(), tok.ExprOperationList()])


class ExprOperationList:
    def execute(self, context):
        if isinstance(context.get_next_terminal(), tok.TermEquation):
            context.push_in_tape([tok.TermEquation(), tok.Expr2(), tok.ExprOperationList()])
        elif isinstance(context.get_next_terminal(), tok.TermInequality):
            context.push_in_tape([tok.TermInequality(), tok.Expr2(), tok.ExprOperationList()])
        elif type(context.get_next_terminal()) in expr_follow_1:
            pass
        else:
            context.error_flag = True
            context.error_msg = "Expected operator in expression"


class Expr2:
    def execute(self, context):
        context.push_in_tape([tok.Expr3(), tok.Expr2OperationList()])


class Expr2OperationList:
    def execute(self, context):
        if isinstance(context.get_next_terminal(), tok.TermLess):
            context.push_in_tape([tok.TermLess(), tok.Expr3(), tok.Expr2OperationList()])
        elif isinstance(context.get_next_terminal(), tok.TermGreater):
            context.push_in_tape([tok.TermGreater(), tok.Expr3(), tok.Expr2OperationList()])
        elif isinstance(context.get_next_terminal(), tok.TermLessOrEqual):
            context.push_in_tape([tok.TermLessOrEqual(), tok.Expr3(), tok.Expr2OperationList()])
        elif isinstance(context.get_next_terminal(), tok.TermGreaterOrEqual):
            context.push_in_tape([tok.TermGreaterOrEqual(), tok.Expr3(), tok.Expr2OperationList()])
        elif type(context.get_next_terminal()) in expr_follow_1:
            pass
        else:
            context.error_flag = True
            context.error_msg = "Expected operator in expression"


class Expr3:
    def execute(self, context):
        context.push_in_tape([tok.Expr4(), tok.Expr3OperationList()])


class Expr3OperationList:
    def execute(self, context):
        if isinstance(context.get_next_terminal(), tok.TermPlus):
            context.push_in_tape([tok.TermPlus(), tok.Expr4(), tok.Expr3OperationList()])
        elif isinstance(context.get_next_terminal(), tok.TermMinus):
            context.push_in_tape([tok.TermMinus(), tok.Expr4(), tok.Expr3OperationList()])
        elif type(context.get_next_terminal()) in expr_follow_1:
            pass
        else:
            context.error_flag = True
            context.error_msg = "Expected operator in expression"


class Expr4:
    def execute(self, context):
        context.push_in_tape([tok.Expr5(), tok.Expr4OperationList()])


class Expr4OperationList:
    def execute(self, context):
        if isinstance(context.get_next_terminal(), tok.TermAsterisk):
            context.push_in_tape([tok.TermAsterisk(), tok.Expr5(), tok.Expr4OperationList()])
        elif isinstance(context.get_next_terminal(), tok.TermSlash):
            context.push_in_tape([tok.TermSlash(), tok.Expr5(), tok.Expr4OperationList()])
        elif isinstance(context.get_next_terminal(), tok.TermPercent):
            context.push_in_tape([tok.TermPercent(), tok.Expr5(), tok.Expr4OperationList()])
        elif type(context.get_next_terminal()) in expr_follow_1:
            pass
        else:
            context.error_flag = True
            context.error_msg = "Expected operator in expression"


class Expr5:
    def execute(self, context):
        if isinstance(context.get_next_terminal(), tok.TermPlus):
            context.push_in_tape([tok.TermPlus(), tok.Expr5()])
        elif isinstance(context.get_next_terminal(), tok.TermMinus):
            context.push_in_tape([tok.TermMinus(), tok.Expr5()])
        elif type(context.get_next_terminal()) in [tok.TermOpenParenthesis,
                                                   tok.TermIntLiteral,
                                                   tok.TermRealLiteral,
                                                   tok.TermId]:
            context.push_in_tape([tok.Expr6()])
        else:
            context.error_flag = True
            context.error_msg = "Expected operand in expression"


class Expr6:
    def execute(self, context):
        if isinstance(context.get_next_terminal(), tok.TermOpenParenthesis):
            context.push_in_tape([tok.TermOpenParenthesis(), tok.Expression(), tok.TermClosingParenthesis()])
        elif isinstance(context.get_next_terminal(), tok.TermId):
            context.push_in_tape([tok.TermId()])
        elif isinstance(context.get_next_terminal(), tok.TermIntLiteral):
            context.push_in_tape([tok.TermIntLiteral()])
        elif isinstance(context.get_next_terminal(), tok.TermRealLiteral):
            context.push_in_tape([tok.TermRealLiteral()])
        else:
            context.error_flag = True
            context.error_msg = "Expected operand in expression"
