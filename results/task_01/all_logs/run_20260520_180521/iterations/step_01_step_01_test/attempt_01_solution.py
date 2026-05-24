def calculate(notation, expression):
    tokens = expression.split()
    if notation == "postfix":
        a, b, op = int(tokens[0]), int(tokens[1]), tokens[2]
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
    elif notation == "prefix":
        op, a, b = tokens[0], int(tokens[1]), int(tokens[2])
        if op == "+":
            return a + b
        elif op == "-":
            return a - b