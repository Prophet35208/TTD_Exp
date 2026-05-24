import math

def _is_float_digit(s: str) -> bool:
    return s.lstrip('-').isdigit()

def _parse_binary_expression(tokens):
    if not (_is_float_digit(tokens[0]) and _is_float_digit(tokens[1])):
        return None
    return int(tokens[0]), int(tokens[1]), tokens[2]

def _is_invalid_power(base, exponent):
    return base == 0 and exponent <= 0

def _is_division_by_zero(operator, second_operand):
    return operator in ('/', '%') and second_operand == 0

def _apply_binary(first, second, operator):
    operations = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a // b,
        '%': lambda a, b: a % b,
        '^': lambda a, b: a ** b,
    }
    return operations[operator](first, second)

def _apply_unary(operand, operator):
    if operator == 'sqrt':
        if operand < 0:
            return None
        return int(math.isqrt(operand))
    if operator == 'abs':
        return abs(operand)
    return None

def _is_binary_operator(token):
    return token in ('+', '-', '*', '/', '%', '^')

def _is_unary_operator(token):
    return token in ('sqrt', 'abs')

def calculate(expression):
    if not expression.strip():
        return None

    tokens = expression.split()

    if len(tokens) == 1:
        if _is_float_digit(tokens[0]):
            return int(tokens[0])
        return None

    if len(tokens) == 2:
        if not _is_unary_operator(tokens[1]):
            return None
        if not _is_float_digit(tokens[0]):
            return None
        return _apply_unary(int(tokens[0]), tokens[1])

    if len(tokens) == 3:
        if not _is_binary_operator(tokens[2]):
            return None
        parsed = _parse_binary_expression(tokens)
        if parsed is None:
            return None
        first, second, operator = parsed
        if _is_division_by_zero(operator, second):
            return None
        if operator == '^' and _is_invalid_power(first, second):
            return None
        return _apply_binary(first, second, operator)

    stack = []
    for token in tokens:
        if _is_float_digit(token):
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
            stack.append(_apply_binary(a, b, token))
        elif _is_unary_operator(token):
            if len(stack) < 1:
                return None
            a = stack.pop()
            result = _apply_unary(a, token)
            if result is None:
                return None
            stack.append(result)
        else:
            return None

    return stack[0] if len(stack) == 1 else None