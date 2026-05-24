from Operations import *

######## Plus #########

def test_plus():
    stack = [1, 2]
    result = Plus(stack)
    assert stack == [3]
    assert result == False

def test_plus_2():
    stack = [1.25, 3.5]
    result = Plus(stack)
    assert stack == [4.75]
    assert result == False

def test_plus_3():
    stack = [5, 0.5]
    result = Plus(stack)
    assert stack == [5.5]
    assert result == False

######## Minus #########

def test_minus():
    stack = [1, 2]
    result = Minus(stack)
    assert stack == [-1]
    assert result == False

def test_minus_2():
    stack = [1.25, 3.5]
    result = Minus(stack)
    assert stack == [-2.25]
    assert result == False

def test_minus_3():
    stack = [5, 0.5]
    result = Minus(stack)
    assert stack == [4.5]
    assert result == False

######## Mult #########

def test_mult():
    stack = [3, 4]
    result = Mult(stack)
    assert stack == [12]
    assert result == False

def test_mult_2():
    stack = [1.25, 3.5]
    result = Mult(stack)
    assert stack == [4.375]
    assert result == False

def test_mult_3():
    stack = [5, 0.5]
    result = Mult(stack)
    assert stack == [2.5]
    assert result == False

######## Div #########

def test_div():
    stack = [3, 4]
    result = Div(stack)
    assert stack == [0]
    assert result == False

def test_div_2():
    stack = [12, 4]
    result = Div(stack)
    assert stack == [3]
    assert result == False

def test_div_3():
    stack = [12, 0]
    result = Div(stack)
    assert result == True

def test_div_4():
    stack = [12.25, 0.5]
    result = Div(stack)
    assert stack == [24.5]
    assert result == False

######## DivRemainder #########

def test_div_rem():
    stack = [3, 4]
    result = DivRem(stack)
    assert stack == [3]
    assert result == False

def test_div_rem_2():
    stack = [12, 4]
    result = DivRem(stack)
    assert stack == [0]
    assert result == False

def test_div_rem_3():
    stack = [12, 0]
    result = DivRem(stack)
    assert result == True

def test_div_rem_4():
    stack = [12, 0.5]
    result = DivRem(stack)
    assert result == True

######## Pow #########

def test_pow():
    stack = [3, 4]
    result = Pow(stack)
    assert stack == [81]
    assert result == False

def test_pow_2():
    stack = [0, -1]
    result = Pow(stack)
    assert result == True

def test_pow_3():
    stack = [0, 0]
    result = Pow(stack)
    assert result == True

def test_pow_4():
    stack = [4, 0.5]
    result = Pow(stack)
    assert stack == [2.0]
    assert result == False

######## Sqrt #########

def test_sqrt():
    stack = [25]
    result = Sqrt(stack)
    assert stack == [5]
    assert result == False

def test_sqrt_2():
    stack = [-4]
    result = Sqrt(stack)
    assert result == True

######## Abs #########

def test_abs():
    stack = [4]
    result = Abs(stack)
    assert stack == [4]
    assert result == False

def test_abs_2():
    stack = [-4]
    result = Abs(stack)
    assert stack == [4]
    assert result == False