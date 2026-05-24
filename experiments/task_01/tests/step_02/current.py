from solution import calculate

######## Sqrt #########
def test_sqrt():
    assert calculate("25 sqrt") == 5

def test_sqrt_2():
    assert calculate("-4 sqrt") is None

######## Abs #########
def test_abs():
    assert calculate("4 abs") == 4

def test_abs_2():
    assert calculate("-4 abs") == 4

######## Not enough operands ######### 
def test_no_operands_plus():
    assert calculate("+") is None

def test_no_operands_plus_one():
    assert calculate("3 +") is None

def test_no_operands_mult():
    assert calculate("*") is None

def test_no_operands_mult_one():
    assert calculate("3 *") is None

def test_no_operands_minus():
    assert calculate("-") is None

def test_no_operands_minus_one():
    assert calculate("3 -") is None

def test_no_operands_div():
    assert calculate("/") is None

def test_no_operands_div_one():
    assert calculate("3 /") is None

def test_no_operands_rem():
    assert calculate("%") is None

def test_no_operands_rem_one():
    assert calculate("3 %") is None

def test_no_operands_abs():
    assert calculate("abs") is None

def test_no_operands_sqrt():
    assert calculate("sqrt") is None

def test_no_operands_pow():
    assert calculate("^") is None

def test_no_operands_pow_one():
    assert calculate("3 ^") is None

######## Other tests #########    
def test_empty_expr():
    assert calculate("") is None

def test_unknown_operator():
    assert calculate("3 4 **") is None

def test_unknown_operation():
    assert calculate("mult") is None

def test_too_many_operands():
    assert calculate("3 4") is None

######## Complex expression #########
def test_complex_expr():
    assert calculate("1 2 3 * + 4 - 5 6 % +") == 8