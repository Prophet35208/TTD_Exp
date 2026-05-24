import math

def Plus(stack: list) -> bool:
    if len(stack) < 2:
        return True
    operand2 = stack.pop()
    operand1 = stack.pop()
    try:
        stack.append(operand1 + operand2)
    except:
        return True
    return False

def Minus(stack: list) -> bool:
    if len(stack) < 2:
        return True
    operand2 = stack.pop()
    operand1 = stack.pop()
    try:
        stack.append(operand1 - operand2)
    except:
        return True
    return False

def Mult(stack: list) -> bool:
    if len(stack) < 2:
        return True
    operand2 = stack.pop()
    operand1 = stack.pop()
    try:
        stack.append(operand1 * operand2)
    except:
        return True
    return False

def Div(stack: list) -> bool:
    if len(stack) < 2:
        return True
    operand2 = stack.pop()
    if operand2 == 0:
        return True
    operand1 = stack.pop()
    try:
        if isinstance(operand2, float) or isinstance(operand1, float):
            stack.append(operand1 / operand2)
        else:
            stack.append(operand1 // operand2)
    except:
        return True
    return False

def DivRem(stack: list) -> bool:
    if len(stack) < 2:
        return True
    operand2 = stack.pop()
    if operand2 == 0:
        return True
    operand1 = stack.pop()
    if isinstance(operand2, float) or isinstance(operand1, float):
        return True
    try:
        stack.append(operand1 % operand2)
    except:
        return True
    return False

def Pow(stack: list) -> bool:
    if len(stack) < 2:
        return True
    operand2 = stack.pop()
    operand1 = stack.pop()
    if operand1 == 0 and operand2 <= 0:
        return True
    try:
        stack.append(operand1 ** operand2)
    except:
        return True
    return False

def Sqrt(stack: list) -> bool:
    if len(stack) < 1:
        return True
    operand = stack.pop()
    if operand < 0:
        return True
    try:
        result = math.sqrt(operand)
        if result.is_integer():
            result = int(result)
        stack.append(result)
    except:
        return True
    return False

def Abs(stack: list) -> bool:
    if len(stack) < 1:
        return True
    stack[-1] = stack[-1] if stack[-1] >= 0 else -stack[-1]
    return False