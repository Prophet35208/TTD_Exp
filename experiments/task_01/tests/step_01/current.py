from solution import calculate

######## Plus #########
def test_plus():
    assert calculate("1 2 +") == 3

######## Minus #########
def test_minus():
    assert calculate("1 2 -") == -1

######## Mult #########
def test_mult():
    assert calculate("3 4 *") == 12

######## Div #########
def test_div():
    assert calculate("3 4 /") == 0

def test_div_2():
    assert calculate("12 4 /") == 3

def test_div_3():
    assert calculate("12 0 /") is None

######## DivRemainder #########
def test_div_rem():
    assert calculate("3 4 %") == 3

def test_div_rem_2():
    assert calculate("12 4 %") == 0

def test_div_rem_3():
    assert calculate("12 0 %") is None

######## Pow #########
def test_pow():
    assert calculate("3 4 ^") == 81

def test_pow_2():
    assert calculate("0 -1 ^") is None

def test_pow_3():
    assert calculate("0 0 ^") is None

######## Single number #########
def test_single_number():
    assert calculate("3") == 3