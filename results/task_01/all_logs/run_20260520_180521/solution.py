def calculate(notation, expression):
    tokens = expression.split()
    if notation == "postfix":
        a, b, op = int(tokens[0]), int(tokens[1]), tokens[2]
    elif notation == "prefix":
        op, a, b = tokens[0], int(tokens[1]), int(tokens[2])
    else:
        raise ValueError(f"Unknown notation: {notation}")

    operations = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
    }

    if op in operations:
        return operations[op](a, b)
    else:
        raise ValueError(f"Unknown operator: {op}")