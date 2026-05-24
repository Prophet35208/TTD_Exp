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

def calculate(expression):
    tokens = expression.split()
    first, second, operator = _parse_tokens(tokens)
    
    if operator is None:
        return first
    
    if _is_division_by_zero(operator, second):
        return None
    
    if operator == '^' and _is_invalid_power(first, second):
        return None
    
    return _apply_operator(first, second, operator)