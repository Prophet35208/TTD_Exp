def calculate(expression):
    tokens = expression.split()
    if len(tokens) == 1:
        return int(tokens[0])
    
    a = int(tokens[0])
    b = int(tokens[1])
    op = tokens[2]
    
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            return None
        return a // b
    elif op == '%':
        if b == 0:
            return None
        return a % b
    elif op == '^':
        if a == 0 and b <= 0:
            return None
        return a ** b