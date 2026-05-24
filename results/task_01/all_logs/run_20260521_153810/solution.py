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
    if operator not in operations:
        return None
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
        if tokens[1] in ('sqrt', 'abs'):
            if tokens[1] == 'sqrt':
                try:
                    val = int(tokens[0])
                except ValueError:
                    return None
                if val < 0:
                    return None
                return int(val ** 0.5)
            elif tokens[1] == 'abs':
                try:
                    val = int(tokens[0])
                except ValueError:
                    return None
                return abs(val)
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
                result = _apply_operator(a, b, token)
                if result is None:
                    return None
                stack.append(result)
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
            result = _apply_operator(a, b, token)
            if result is None:
                return None
            stack.append(result)
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