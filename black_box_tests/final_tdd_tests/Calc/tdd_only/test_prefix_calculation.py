from PrefixCalculation import *

######## Plus #########

def test_plus():
    expr = "+ 1 2"
    result = PrefixCalculation(expr)
    assert result == 3

######## Minus #########

def test_minus():
    expr = "- 1 2"
    result = PrefixCalculation(expr)
    assert result == -1

######## Mult #########

def test_mult():
    expr = "* 3 4"
    result = PrefixCalculation(expr)
    assert result == 12

######## Div #########

def test_div():
    expr = "/ 3 4"
    result = PrefixCalculation(expr)
    assert result == 0

def test_div_2():
    expr = "/ 12 4"
    result = PrefixCalculation(expr)
    assert result == 3

def test_div_3():
    expr = "/ 12 0"
    result = PrefixCalculation(expr)
    assert result is None

######## DivRemainder #########

def test_div_rem():
    expr = "% 3 4"
    result = PrefixCalculation(expr)
    assert result == 3

def test_div_rem_2():
    expr = "% 12 4"
    result = PrefixCalculation(expr)
    assert result == 0

def test_div_rem_3():
    expr = "% 12 0"
    result = PrefixCalculation(expr)
    assert result is None

######## Pow #########

def test_pow():
    expr = "^ 3 4"
    result = PrefixCalculation(expr)
    assert result == 81

def test_pow_2():
    expr = "^ 0 -1"
    result = PrefixCalculation(expr)
    assert result is None

def test_pow_3():
    expr = "^ 0 0"
    result = PrefixCalculation(expr)
    assert result is None

######## Sqrt #########

def test_sqrt():
    expr = "sqrt 25"
    result = PrefixCalculation(expr)
    assert result == 5

def test_sqrt_2():
    expr = "sqrt -4"
    result = PrefixCalculation(expr)
    assert result is None

######## Abs #########

def test_abs():
    expr = "abs 4"
    result = PrefixCalculation(expr)
    assert result == 4

def test_abs_2():
    expr = "abs -4"
    result = PrefixCalculation(expr)
    assert result == 4

######## Not enough operands ######### 

def test_no_operands():
    expr = "+"
    result = PrefixCalculation(expr)
    assert result is None

def test_no_operands_2():
    expr = "+ 3"
    result = PrefixCalculation(expr)
    assert result is None

def test_no_operands_3():
    expr = "*"
    result = PrefixCalculation(expr)
    assert result is None

def test_no_operands_4():
    expr = "* 3"
    result = PrefixCalculation(expr)
    assert result is None

def test_no_operands_5():
    expr = "-"
    result = PrefixCalculation(expr)
    assert result is None

def test_no_operands_6():
    expr = "- 3"
    result = PrefixCalculation(expr)
    assert result is None

def test_no_operands_7():
    expr = "/"
    result = PrefixCalculation(expr)
    assert result is None

def test_no_operands_8():
    expr = "/ 3"
    result = PrefixCalculation(expr)
    assert result is None

def test_no_operands_9():
    expr = "%"
    result = PrefixCalculation(expr)
    assert result is None

def test_no_operands_10():
    expr = "% 3"
    result = PrefixCalculation(expr)
    assert result is None

def test_no_operands_11():
    expr = "abs"
    result = PrefixCalculation(expr)
    assert result is None

def test_no_operands_12():
    expr = "sqrt"
    result = PrefixCalculation(expr)
    assert result is None

def test_no_operands_13():
    expr = "^"
    result = PrefixCalculation(expr)
    assert result is None

def test_no_operands_14():
    expr = "^ 3"
    result = PrefixCalculation(expr)
    assert result is None

######## Other tests #########    

def test_empty_expr():
    expr = ""
    result = PrefixCalculation(expr)
    assert result is None

def test_unknown_operation():
    expr = "** 3 4"
    result = PrefixCalculation(expr)
    assert result is None

def test_unknow_operation_2():
    expr = "mult"
    result = PrefixCalculation(expr)
    assert result is None

def test_unknow_operation_3():
    expr = "+ add * 3 4 5 6"
    result = PrefixCalculation(expr)
    assert result is None

def test_no_operations():
    expr = "3"
    result = PrefixCalculation(expr)
    assert result == 3

def test_no_operations_2():
    expr = "3 4"
    result = PrefixCalculation(expr)
    assert result is None

def test_complex_expr():
    expr = "+ - + 1 * 2 3 4 % 5 6"
    result = PrefixCalculation(expr)
    assert result == 8
