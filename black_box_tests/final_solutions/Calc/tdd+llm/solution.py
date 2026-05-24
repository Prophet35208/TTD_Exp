import math

def _is_integer_string(s: str) -> bool:
    return s.lstrip('-').isdigit()

def _parse_integer(s: str) -> int:
    return int(s)

def _is_binary_operator(token: str) -> bool:
    return token in ('+', '-', '*', '/', '%', '^')

def _is_unary_operator(token: str) -> bool:
    return token in ('sqrt', 'abs')

def _is_division_by_zero(operator: str, divisor: int) -> bool:
    return operator in ('/', '%') and divisor == 0

def _is_invalid_power(base: int, exponent: int) -> bool:
    return base == 0 and exponent <= 0

def _apply_binary(left: int, right: int, operator: str) -> int:
    operations = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a // b,
        '%': lambda a, b: a % b,
        '^': lambda a, b: a ** b,
    }
    return operations[operator](left, right)

def _apply_unary(operand: int, operator: str):
    if operator == 'sqrt':
        if operand < 0:
            return None
        return int(math.isqrt(operand))
    if operator == 'abs':
        return abs(operand)
    return None

def _validate_binary_operation(operator: str, right: int, left: int = None) -> bool:
    if _is_division_by_zero(operator, right):
        return False
    if operator == '^' and left is not None and _is_invalid_power(left, right):
        return False
    return True

def _parse_simple_expression(tokens):
    if len(tokens) == 1:
        if _is_integer_string(tokens[0]):
            return _parse_integer(tokens[0])
        return None

    if len(tokens) == 2:
        if not _is_unary_operator(tokens[1]) or not _is_integer_string(tokens[0]):
            return None
        return _apply_unary(_parse_integer(tokens[0]), tokens[1])

    if len(tokens) == 3:
        if not _is_binary_operator(tokens[2]):
            return None
        if not (_is_integer_string(tokens[0]) and _is_integer_string(tokens[1])):
            return None
        left = _parse_integer(tokens[0])
        right = _parse_integer(tokens[1])
        operator = tokens[2]
        if not _validate_binary_operation(operator, right, left):
            return None
        return _apply_binary(left, right, operator)

    return None

def _evaluate_rpn(tokens):
    stack = []
    for token in tokens:
        if _is_integer_string(token):
            stack.append(_parse_integer(token))
        elif _is_binary_operator(token):
            if len(stack) < 2:
                return None
            right = stack.pop()
            left = stack.pop()
            if not _validate_binary_operation(token, right, left):
                return None
            stack.append(_apply_binary(left, right, token))
        elif _is_unary_operator(token):
            if not stack:
                return None
            operand = stack.pop()
            result = _apply_unary(operand, token)
            if result is None:
                return None
            stack.append(result)
        else:
            return None

    return stack[0] if len(stack) == 1 else None

def calculate(expression: str):
    if not expression.strip():
        return None

    tokens = expression.split()

    if len(tokens) <= 3:
        return _parse_simple_expression(tokens)

    return _evaluate_rpn(tokens)

def _evaluate_prefix(tokens, index):
    if index >= len(tokens):
        return None, index

    token = tokens[index]
    if _is_integer_string(token):
        return _parse_integer(token), index + 1

    if _is_binary_operator(token):
        left, next_idx = _evaluate_prefix(tokens, index + 1)
        if left is None:
            return None, index
        right, next_idx = _evaluate_prefix(tokens, next_idx)
        if right is None:
            return None, index
        if not _validate_binary_operation(token, right, left):
            return None, index
        return _apply_binary(left, right, token), next_idx

    if _is_unary_operator(token):
        operand, next_idx = _evaluate_prefix(tokens, index + 1)
        if operand is None:
            return None, index
        result = _apply_unary(operand, token)
        if result is None:
            return None, index
        return result, next_idx

    return None, index

def calculate_prefix(expression: str):
    if not expression.strip():
        return None

    tokens = expression.split()

    if len(tokens) == 1:
        if _is_integer_string(tokens[0]):
            return _parse_integer(tokens[0])
        return None

    result, final_idx = _evaluate_prefix(tokens, 0)
    if result is None or final_idx != len(tokens):
        return None
    return result

def _read_input_file():
    try:
        with open("In.txt", "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return None

def _write_output(content: str):
    with open("Out.txt", "w") as f:
        f.write(content)

def _parse_input(lines):
    if not lines or not lines[0].strip():
        return None, None
    mode = lines[0].strip()
    if len(lines) < 2 or not lines[1].strip():
        return None, None
    expression = lines[1].strip()
    return mode, expression

def _evaluate_expression(mode: str, expression: str):
    if mode == "postfix":
        return calculate(expression)
    if mode == "prefix":
        return calculate_prefix(expression)
    return None

def main():
    lines = _read_input_file()
    if lines is None:
        _write_output("Error")
        return 1

    mode, expression = _parse_input(lines)
    if mode is None:
        _write_output("Error")
        return 1

    result = _evaluate_expression(mode, expression)
    if result is None:
        _write_output("Error")
        return 1

    _write_output(str(result))
    return 0