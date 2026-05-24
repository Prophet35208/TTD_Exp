import math

def _parse_tokens(tokens):
    if len(tokens) == 1:
        return int(tokens[0]), None, None
    return int(tokens[0]), int(tokens[1]), tokens[2]

def _is_invalid_power(base, exponent):
    return base == 0 and exponent <= 0

def _is_division_by_zero(operator, second_operand):
    return operator in ('/', '%') and second_operand == 0

def _apply_operator(first, second, operator):
    operations = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a // b,
        '%': lambda a, b: a % b,
        '^': lambda a, b: a ** b,
    }
    return operations[operator](first, second)

def _is_unary_operator(token):
    return token in ('sqrt', 'abs')

def _apply_unary(operand, operator):
    if operator == 'sqrt':
        if operand < 0:
            return None
        return int(math.isqrt(operand))
    elif operator == 'abs':
        return abs(operand)
    return None

def _is_binary_operator(token):
    return token in ('+', '-', '*', '/', '%', '^')

def calculate(expression):
    if not expression.strip():
        return None
    
    tokens = expression.split()
    
    if len(tokens) == 1:
        token = tokens[0]
        if token.lstrip('-').isdigit():
            return int(token)
        return None
    
    if len(tokens) == 2:
        if tokens[1] in ('sqrt', 'abs'):
            if tokens[0].lstrip('-').isdigit():
                return _apply_unary(int(tokens[0]), tokens[1])
            return None
        if _is_binary_operator(tokens[1]):
            return None
        return None
    
    if len(tokens) == 3:
        if _is_binary_operator(tokens[2]):
            if not (tokens[0].lstrip('-').isdigit() and tokens[1].lstrip('-').isdigit()):
                return None
            first, second, operator = _parse_tokens(tokens)
            if _is_division_by_zero(operator, second):
                return None
            if operator == '^' and _is_invalid_power(first, second):
                return None
            return _apply_operator(first, second, operator)
        return None
    
    stack = []
    for token in tokens:
        if token.lstrip('-').isdigit():
            stack.append(int(token))
        elif _is_binary_operator(token):
            if len(stack) < 2:
                return None
            b = stack.pop()
            a = stack.pop()
            if _is_division_by_zero(token, b):
                return None
            if token == '^' and _is_invalid_power(a, b):
                return None
            stack.append(_apply_operator(a, b, token))
        elif token in ('sqrt', 'abs'):
            if len(stack) < 1:
                return None
            a = stack.pop()
            result = _apply_unary(a, token)
            if result is None:
                return None
            stack.append(result)
        else:
            return None
    
    if len(stack) != 1:
        return None
    return stack[0]