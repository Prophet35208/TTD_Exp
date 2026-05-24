import Tokens as tok
import Code2IR

def check_stack(actual_stack, expected_stack_types):
    expected_stack_types.reverse()
    assert len(expected_stack_types) == len(actual_stack), "Length of expected stack doesn't equal to legnth of actual stack"
    compare_result = list(map(lambda x, y: isinstance(x, y), actual_stack, expected_stack_types))
    for i in range(len(expected_stack_types)):
        assert compare_result[i], "Expected token " + str(expected_stack_types[i]) + "; actual " + str(type(actual_stack[i]))

def test_program():
    context = Code2IR.LL1([tok.TermInt()])
    token = tok.Program()
    token.execute(context)
    check_stack(context.tape, [tok.Datatype, tok.ObjectWithDatatype, tok.Program])

def test_program_2():
    context = Code2IR.LL1([tok.TermDouble()])
    token = tok.Program()
    token.execute(context)
    check_stack(context.tape, [tok.Datatype, tok.ObjectWithDatatype, tok.Program])

def test_program_3():
    context = Code2IR.LL1([])
    token = tok.Program()
    token.execute(context)
    check_stack(context.tape, [])

def test_datatype():
    context = Code2IR.LL1([tok.TermInt()])
    token = tok.Datatype()
    token.execute(context)
    check_stack(context.tape, [tok.TermInt])

def test_datatype_2():
    context = Code2IR.LL1([tok.TermDouble()])
    token = tok.Datatype()
    token.execute(context)
    check_stack(context.tape, [tok.TermDouble])

def test_object_with_datatype():
    context = Code2IR.LL1([tok.TermMain()])
    token = tok.ObjectWithDatatype()
    token.execute(context)
    check_stack(context.tape, [tok.TermMain, tok.TermOpenParenthesis, tok.TermClosingParenthesis, tok.CompoundStatement])

def test_object_with_datatype_2():
    context = Code2IR.LL1([tok.TermId()])
    token = tok.ObjectWithDatatype()
    token.execute(context)
    check_stack(context.tape, [tok.TermId, tok.Initialization, tok.VarList, tok.TermSemicolon])

def test_var_list():
    context = Code2IR.LL1([])
    token = tok.VarList()
    token.execute(context)
    check_stack(context.tape, [])

def test_var_list_2():
    context = Code2IR.LL1([tok.TermComma()])
    token = tok.VarList()
    token.execute(context)
    check_stack(context.tape, [tok.TermComma, tok.TermId, tok.Initialization, tok.VarList])

def test_initialization():
    context = Code2IR.LL1([tok.TermAssignment()])
    token = tok.Initialization()
    token.execute(context)
    check_stack(context.tape, [tok.TermAssignment, tok.Expression])

def test_initialization_2():
    context = Code2IR.LL1([])
    token = tok.Initialization()
    token.execute(context)
    check_stack(context.tape, [])

def test_compound_statement():
    context = Code2IR.LL1([])
    token = tok.CompoundStatement()
    token.execute(context)
    check_stack(context.tape, [tok.TermOpenCurlyBrace, tok.StatementList, tok.TermClosingCurlyBrace])

def test_statement():
    context = Code2IR.LL1([tok.TermOpenCurlyBrace()])
    token = tok.Statement()
    token.execute(context)
    check_stack(context.tape, [tok.CompoundStatement])

def test_statement_2():
    context = Code2IR.LL1([tok.TermId()])
    token = tok.Statement()
    token.execute(context)
    check_stack(context.tape, [tok.TermId, tok.TermAssignment, tok.Expression, tok.TermSemicolon])

def test_statement_3():
    context = Code2IR.LL1([tok.TermInt()])
    token = tok.Statement()
    token.execute(context)
    check_stack(context.tape, [tok.Datatype, tok.TermId, tok.Initialization, tok.VarList, tok.TermSemicolon])

def test_statement_4():
    context = Code2IR.LL1([tok.TermDouble()])
    token = tok.Statement()
    token.execute(context)
    check_stack(context.tape, [tok.Datatype, tok.TermId, tok.Initialization, tok.VarList, tok.TermSemicolon])

def test_statement_5():
    context = Code2IR.LL1([tok.TermIf()])
    token = tok.Statement()
    token.execute(context)
    check_stack(context.tape, [tok.TermIf, tok.TermOpenParenthesis, tok.Expression, tok.TermClosingParenthesis, tok.Statement])

def test_statement_6():
    context = Code2IR.LL1([tok.TermReturn()])
    token = tok.Statement()
    token.execute(context)
    check_stack(context.tape, [tok.TermReturn, tok.Expression])

def test_statement_7():
    context = Code2IR.LL1([tok.TermSemicolon()])
    token = tok.Statement()
    token.execute(context)
    check_stack(context.tape, [tok.TermSemicolon])

def test_statement_list():
    context = Code2IR.LL1([tok.TermOpenCurlyBrace()])
    token = tok.StatementList()
    token.execute(context)
    check_stack(context.tape, [tok.Statement, tok.StatementList])

def test_statement_list_2():
    context = Code2IR.LL1([tok.TermId()])
    token = tok.StatementList()
    token.execute(context)
    check_stack(context.tape, [tok.Statement, tok.StatementList])

def test_statement_list_3():
    context = Code2IR.LL1([tok.TermInt()])
    token = tok.StatementList()
    token.execute(context)
    check_stack(context.tape, [tok.Statement, tok.StatementList])

def test_statement_list_4():
    context = Code2IR.LL1([tok.TermDouble()])
    token = tok.StatementList()
    token.execute(context)
    check_stack(context.tape, [tok.Statement, tok.StatementList])

def test_statement_list_5():
    context = Code2IR.LL1([tok.TermIf()])
    token = tok.StatementList()
    token.execute(context)
    check_stack(context.tape, [tok.Statement, tok.StatementList])

def test_statement_list_6():
    context = Code2IR.LL1([tok.TermReturn()])
    token = tok.StatementList()
    token.execute(context)
    check_stack(context.tape, [tok.Statement, tok.StatementList])

def test_statement_list_7():
    context = Code2IR.LL1([tok.TermSemicolon()])
    token = tok.StatementList()
    token.execute(context)
    check_stack(context.tape, [tok.Statement, tok.StatementList])

def test_statement_list_8():
    context = Code2IR.LL1([])
    token = tok.StatementList()
    token.execute(context)
    check_stack(context.tape, [])

### Expressions

def test_expression():
    context = Code2IR.LL1([])
    token = tok.Expression()
    token.execute(context)
    check_stack(context.tape, [tok.Expr2, tok.ExprOperationList])

def test_expr2():
    context = Code2IR.LL1([])
    token = tok.Expr2()
    token.execute(context)
    check_stack(context.tape, [tok.Expr3, tok.Expr2OperationList])

def test_expr3():
    context = Code2IR.LL1([])
    token = tok.Expr3()
    token.execute(context)
    check_stack(context.tape, [tok.Expr4, tok.Expr3OperationList])

def test_expr4():
    context = Code2IR.LL1([])
    token = tok.Expr4()
    token.execute(context)
    check_stack(context.tape, [tok.Expr5, tok.Expr4OperationList])

def test_expr5():
    context = Code2IR.LL1([tok.TermId()])
    token = tok.Expr5()
    token.execute(context)
    check_stack(context.tape, [tok.Expr6])

def test_expr5_2():
    context = Code2IR.LL1([tok.TermPlus()])
    token = tok.Expr5()
    token.execute(context)
    check_stack(context.tape, [tok.TermPlus, tok.Expr5])

def test_expr5_3():
    context = Code2IR.LL1([tok.TermMinus()])
    token = tok.Expr5()
    token.execute(context)
    check_stack(context.tape, [tok.TermMinus, tok.Expr5])

def test_expr6():
    context = Code2IR.LL1([tok.TermOpenParenthesis()])
    token = tok.Expr6()
    token.execute(context)
    check_stack(context.tape, [tok.TermOpenParenthesis, tok.Expression, tok.TermClosingParenthesis])

def test_expr6_2():
    context = Code2IR.LL1([tok.TermId()])
    token = tok.Expr6()
    token.execute(context)
    check_stack(context.tape, [tok.TermId])

def test_expr6_3():
    context = Code2IR.LL1([tok.TermIntLiteral()])
    token = tok.Expr6()
    token.execute(context)
    check_stack(context.tape, [tok.TermIntLiteral])

def test_expr6_4():
    context = Code2IR.LL1([tok.TermRealLiteral()])
    token = tok.Expr6()
    token.execute(context)
    check_stack(context.tape, [tok.TermRealLiteral])

def test_expr_operation_list():
    context = Code2IR.LL1([])
    token = tok.ExprOperationList()
    token.execute(context)
    check_stack(context.tape, [])

def test_expr_operation_list_2():
    context = Code2IR.LL1([tok.TermEquation()])
    token = tok.ExprOperationList()
    token.execute(context)
    check_stack(context.tape, [tok.TermEquation, tok.Expr2, tok.ExprOperationList])

def test_expr_operation_list_3():
    context = Code2IR.LL1([tok.TermInequality()])
    token = tok.ExprOperationList()
    token.execute(context)
    check_stack(context.tape, [tok.TermInequality, tok.Expr2, tok.ExprOperationList])

def test_expr2_operation_list():
    context = Code2IR.LL1([])
    token = tok.Expr2OperationList()
    token.execute(context)
    check_stack(context.tape, [])

def test_expr2_operation_list_2():
    context = Code2IR.LL1([tok.TermLess()])
    token = tok.Expr2OperationList()
    token.execute(context)
    check_stack(context.tape, [tok.TermLess, tok.Expr3, tok.Expr2OperationList])

def test_expr2_operation_list_3():
    context = Code2IR.LL1([tok.TermGreater()])
    token = tok.Expr2OperationList()
    token.execute(context)
    check_stack(context.tape, [tok.TermGreater, tok.Expr3, tok.Expr2OperationList])

def test_expr2_operation_list_4():
    context = Code2IR.LL1([tok.TermLessOrEqual()])
    token = tok.Expr2OperationList()
    token.execute(context)
    check_stack(context.tape, [tok.TermLessOrEqual, tok.Expr3, tok.Expr2OperationList])

def test_expr2_operation_list_5():
    context = Code2IR.LL1([tok.TermGreaterOrEqual()])
    token = tok.Expr2OperationList()
    token.execute(context)
    check_stack(context.tape, [tok.TermGreaterOrEqual, tok.Expr3, tok.Expr2OperationList])

def test_expr3_operation_list():
    context = Code2IR.LL1([])
    token = tok.Expr3OperationList()
    token.execute(context)
    check_stack(context.tape, [])

def test_expr3_operation_list_2():
    context = Code2IR.LL1([tok.TermPlus()])
    token = tok.Expr3OperationList()
    token.execute(context)
    check_stack(context.tape, [tok.TermPlus, tok.Expr4, tok.Expr3OperationList])

def test_expr3_operation_list_3():
    context = Code2IR.LL1([tok.TermMinus()])
    token = tok.Expr3OperationList()
    token.execute(context)
    check_stack(context.tape, [tok.TermMinus, tok.Expr4, tok.Expr3OperationList])

def test_expr4_operation_list():
    context = Code2IR.LL1([])
    token = tok.Expr4OperationList()
    token.execute(context)
    check_stack(context.tape, [])

def test_expr4_operation_list_2():
    context = Code2IR.LL1([tok.TermAsterisk()])
    token = tok.Expr4OperationList()
    token.execute(context)
    check_stack(context.tape, [tok.TermAsterisk, tok.Expr5, tok.Expr4OperationList])

def test_expr4_operation_list_3():
    context = Code2IR.LL1([tok.TermSlash()])
    token = tok.Expr4OperationList()
    token.execute(context)
    check_stack(context.tape, [tok.TermSlash, tok.Expr5, tok.Expr4OperationList])

def test_expr4_operation_list_4():
    context = Code2IR.LL1([tok.TermPercent()])
    token = tok.Expr4OperationList()
    token.execute(context)
    check_stack(context.tape, [tok.TermPercent, tok.Expr5, tok.Expr4OperationList])
