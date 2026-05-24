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
    if not tokens:
        return None
    if len(tokens) == 1:
        try:
            return int(tokens[0])
        except ValueError:
            return None
    if len(tokens) == 2:
        return None
    if len(tokens) > 3:
        stack = []
        for token in tokens:
            if token.lstrip('-').isdigit():
                stack.append(int(token))
            elif token in ('+', '-', '*', '/', '%', '^'):
                if len(stack) < 2:
                    return None
                b = stack.pop()
                a = stack.pop()
                if _is_division_by_zero(token, b):
                    return None
                if token == '^' and _is_invalid_power(a, b):
                    return None
                stack.append(_apply_operator(a, b, token))
            else:
                return None
        return stack[0] if len(stack) == 1 else None
    first, second, operator = _parse_tokens(tokens)
    if operator is None:
        return None
    if _is_division_by_zero(operator, second):
        return None
    if operator == '^' and _is_invalid_power(first, second):
        return None
    return _apply_operator(first, second, operator)

def calculate_prefix(expression):
    tokens = expression.split()
    if not tokens:
        return None
    if len(tokens) == 1:
        try:
            return int(tokens[0])
        except ValueError:
            return None
    stack = []
    for token in reversed(tokens):
        if token.lstrip('-').isdigit():
            stack.append(int(token))
        elif token in ('+', '-', '*', '/', '%', '^'):
            if len(stack) < 2:
                return None
            a = stack.pop()
            b = stack.pop()
            if _is_division_by_zero(token, b):
                return None
            if token == '^' and _is_invalid_power(a, b):
                return None
            stack.append(_apply_operator(a, b, token))
        elif token == 'sqrt':
            if len(stack) < 1:
                return None
            a = stack.pop()
            if a < 0:
                return None
            stack.append(int(a ** 0.5))
        elif token == 'abs':
            if len(stack) < 1:
                return None
            a = stack.pop()
            stack.append(abs(a))
        else:
            return None
    return stack[0] if len(stack) == 1 else None