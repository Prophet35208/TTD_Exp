def _parse_tokens(expression):
    return expression.split()


def _parse_single_operand(tokens):
    return int(tokens[0])


def _parse_binary_operation(tokens):
    a = int(tokens[0])
    b = int(tokens[1])
    op = tokens[2]
    return a, b, op


def _is_zero_division(op, b):
    return b == 0 and op in ('/', '%')


def _is_invalid_power(a, b):
    return a == 0 and b <= 0


def _apply_operator(a, b, op):
    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x // y,
        '%': lambda x, y: x % y,
        '^': lambda x, y: x ** y,
    }
    return operations[op](a, b)


def calculate(expression):
    tokens = _parse_tokens(expression)
    if len(tokens) == 1:
        return _parse_single_operand(tokens)

    a, b, op = _parse_binary_operation(tokens)

    if _is_zero_division(op, b):
        return None
    if op == '^' and _is_invalid_power(a, b):
        return None

    return _apply_operator(a, b, op)