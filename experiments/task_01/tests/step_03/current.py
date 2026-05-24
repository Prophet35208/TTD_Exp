from solution import calculate_prefix

######## Prefix Plus #########
def test_prefix_plus():
    assert calculate_prefix("+ 1 2") == 3

######## Prefix Minus #########
def test_prefix_minus():
    assert calculate_prefix("- 1 2") == -1

######## Prefix Mult #########
def test_prefix_mult():
    assert calculate_prefix("* 3 4") == 12

######## Prefix Div #########
def test_prefix_div():
    assert calculate_prefix("/ 3 4") == 0

def test_prefix_div_2():
    assert calculate_prefix("/ 12 4") == 3

def test_prefix_div_3():
    assert calculate_prefix("/ 12 0") is None

######## Prefix DivRemainder #########
def test_prefix_div_rem():
    assert calculate_prefix("% 3 4") == 3

def test_prefix_div_rem_2():
    assert calculate_prefix("% 12 4") == 0

def test_prefix_div_rem_3():
    assert calculate_prefix("% 12 0") is None

######## Prefix Pow #########
def test_prefix_pow():
    assert calculate_prefix("^ 3 4") == 81

def test_prefix_pow_2():
    assert calculate_prefix("^ 0 -1") is None

def test_prefix_pow_3():
    assert calculate_prefix("^ 0 0") is None

######## Prefix Sqrt #########
def test_prefix_sqrt():
    assert calculate_prefix("sqrt 25") == 5

def test_prefix_sqrt_2():
    assert calculate_prefix("sqrt -4") is None

######## Prefix Abs #########
def test_prefix_abs():
    assert calculate_prefix("abs 4") == 4

def test_prefix_abs_2():
    assert calculate_prefix("abs -4") == 4

######## Prefix error handling #########
def test_prefix_no_operands_plus():
    assert calculate_prefix("+") is None

def test_prefix_no_operands_plus_one():
    assert calculate_prefix("+ 3") is None

def test_prefix_no_operands_sqrt():
    assert calculate_prefix("sqrt") is None

def test_prefix_empty():
    assert calculate_prefix("") is None

def test_prefix_unknown():
    assert calculate_prefix("** 3 4") is None

def test_prefix_unknown_2():
    assert calculate_prefix("mult") is None

def test_prefix_single_number():
    assert calculate_prefix("3") == 3

def test_prefix_too_many():
    assert calculate_prefix("3 4") is None

def test_prefix_complex():
    assert calculate_prefix("+ - + 1 * 2 3 4 % 5 6") == 8