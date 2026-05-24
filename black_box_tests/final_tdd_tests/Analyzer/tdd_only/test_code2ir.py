import Code2IR
import Tokens as tok

### Vars

def test_global_var():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_global_var_2():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermIntLiteral("1"), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_global_var_3():
    tokens = [tok.TermInt(), 
              tok.TermId("a"), tok.TermAssignment(), tok.TermIntLiteral("1"), tok.TermComma(), 
              tok.TermId("b"), tok.TermComma(),
              tok.TermId("c"), tok.TermAssignment(), tok.TermIntLiteral("3"),
              tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_global_var_4():
    tokens = [tok.TermInt(), tok.TermId("a")]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_global_var_5():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermIntLiteral("1"), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_global_var_6():
    tokens = [tok.TermInt(), tok.TermAssignment(), tok.TermIntLiteral("1"), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_global_var_7():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_global_var_8():
    tokens = [tok.TermDouble(), tok.TermId("a"), tok.TermAssignment(), tok.TermRealLiteral("1.0"), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_global_var_9():
    tokens = [tok.TermInt(), 
              tok.TermId("a"), tok.TermAssignment(), tok.TermIntLiteral("1"),
              tok.TermId("b"), tok.TermComma(),
              tok.TermId("c"), tok.TermAssignment(), tok.TermIntLiteral("3"),
              tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_global_var_10():
    tokens = [tok.TermInt(), 
              tok.TermId("a"), tok.TermAssignment(), tok.TermIntLiteral("1"), tok.TermComma(), 
              tok.TermComma(),
              tok.TermId("c"), tok.TermAssignment(), tok.TermIntLiteral("3"),
              tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_global_var_11():
    tokens = [tok.TermInt(), 
              tok.TermId("a"), tok.TermAssignment(), tok.TermIntLiteral("1"), tok.TermComma(), 
              tok.TermId("b"), tok.TermComma(),
              tok.TermId("c"), tok.TermIntLiteral("3"),
              tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_global_var_12():
    tokens = [tok.TermInt(), 
              tok.TermId("a"), tok.TermAssignment(), tok.TermIntLiteral("1"), tok.TermComma(), 
              tok.TermId("b"), tok.TermComma(),
              tok.TermId("c"), tok.TermAssignment(),
              tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1

### main

def test_main():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_main_2():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_main_3():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(),
              tok.TermOpenCurlyBrace(), tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_main_4():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_main_5():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


### local var


def test_local_var():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermInt(), tok.TermId("a"), tok.TermSemicolon(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_local_var_2():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermId("b"), tok.TermSemicolon(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_local_var_3():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermId("b"), tok.TermComma(), tok.TermId(), tok.TermSemicolon(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_local_var_4():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermInt(), tok.TermId("a"), tok.TermId("b"), tok.TermComma(), tok.TermId(), tok.TermSemicolon(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_local_var_5():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermInt(), tok.TermAssignment(), tok.TermId("b"), tok.TermComma(), tok.TermId(), tok.TermSemicolon(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


### if


def test_if():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermIf(), tok.TermOpenParenthesis(), tok.TermIntLiteral("1"), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), tok.TermClosingCurlyBrace(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_if_2():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermIf(), tok.TermOpenParenthesis(), tok.TermIntLiteral("1"), tok.TermClosingParenthesis(),
              tok.TermReturn(), tok.TermIntLiteral("1"), tok.TermSemicolon(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_if_3():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermIf(), tok.TermIntLiteral("1"), tok.TermClosingParenthesis(),
              tok.TermReturn(), tok.TermIntLiteral("1"), tok.TermSemicolon(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_if_4():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermIf(), tok.TermOpenParenthesis(), tok.TermIntLiteral("1"),
              tok.TermReturn(), tok.TermIntLiteral("1"), tok.TermSemicolon(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_if_5():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermIf(), tok.TermOpenParenthesis(), tok.TermIntLiteral("1"), tok.TermClosingParenthesis(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


### Expr


def test_expr():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermId(), tok.TermAssignment(), tok.TermOpenParenthesis(), tok.TermId(), tok.TermClosingParenthesis(), tok.TermPlus(), tok.TermIntLiteral("1"), tok.TermMinus(), tok.TermRealLiteral("2.0"), tok.TermSemicolon(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_expr_2():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermId("a"), tok.TermAssignment(), tok.TermId("b"), tok.TermSlash(), tok.TermOpenParenthesis(), tok.TermIntLiteral("1"), tok.TermClosingParenthesis(), tok.TermAsterisk(), tok.TermRealLiteral("2.0"), tok.TermPercent(), tok.TermId("c"), tok.TermSemicolon(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_expr_3():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermId("a"), tok.TermAssignment(), tok.TermId("a"), tok.TermLessOrEqual(), tok.TermId("a"), tok.TermLess(), tok.TermId("a"), tok.TermGreater(), tok.TermId("a"), tok.TermGreaterOrEqual(), tok.TermId("a"), tok.TermSemicolon(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_expr_4():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermId("a"), tok.TermAssignment(), tok.TermId("a"), tok.TermEquation(), tok.TermId("a"), tok.TermInequality(), tok.TermId("a"), tok.TermSemicolon(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_expr_5():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermId("a"), tok.TermAssignment(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_expr_6():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermId("a"), tok.TermAssignment(), tok.TermOpenParenthesis(), tok.TermId("a"), tok.TermPlus(), tok.TermId("b"),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_expr_7():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermPlus(), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_expr_8():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermId("b"), tok.TermPlus(), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_expr_9():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermId("b"), tok.TermMinus(), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_expr_10():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermId("b"), tok.TermAsterisk(), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_expr_11():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermId("b"), tok.TermSlash(), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_expr_12():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermId("b"), tok.TermPercent(), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_expr_13():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermId("b"), tok.TermGreater(), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_expr_14():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermId("b"), tok.TermGreaterOrEqual(), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_expr_15():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermId("b"), tok.TermLess(), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_expr_16():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermId("b"), tok.TermLessOrEqual(), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_expr_17():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermId("b"), tok.TermEquation(), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


def test_expr_18():
    tokens = [tok.TermInt(), tok.TermId("a"), tok.TermAssignment(), tok.TermId("b"), tok.TermInequality(), tok.TermSemicolon()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 1


### Other


def test_empty():
    tokens = []
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_extra_semicolon():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermSemicolon(),
              tok.TermSemicolon(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0


def test_many_compound_statements():
    tokens = [tok.TermInt(), tok.TermMain(), tok.TermOpenParenthesis(), tok.TermClosingParenthesis(),
              tok.TermOpenCurlyBrace(), 
              tok.TermOpenCurlyBrace(), 
              tok.TermClosingCurlyBrace(),
              tok.TermOpenCurlyBrace(),
              tok.TermOpenCurlyBrace(), 
              tok.TermClosingCurlyBrace(),
              tok.TermClosingCurlyBrace(),
              tok.TermClosingCurlyBrace()]
    ll1 = Code2IR.LL1(tokens)
    exit_code = ll1.run()
    assert exit_code == 0
