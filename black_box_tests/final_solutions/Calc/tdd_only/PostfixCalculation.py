import Operations as op

def PostfixCalculation(expression: str):
    tokens = expression.split()
    stack = []
    for token in tokens:
        result = False
        if token == "+":
            result = op.Plus(stack)
        elif token == "-":
            result = op.Minus(stack)
        elif token == "*":
            result = op.Mult(stack)
        elif token == "/":
            result = op.Div(stack)
        elif token == "%":
            result = op.DivRem(stack)
        elif token == "^":
            result = op.Pow(stack)
        elif token == "sqrt":
            result = op.Sqrt(stack)
        elif token == "abs":
            result = op.Abs(stack)
        else:
            number = None
            try:
                number = float(token)
                if number.is_integer():
                    number = int(token)
            except:
                pass
            if number is None:
                return None
            stack.append(number)

        if result:
            return None
    
    if len(stack) != 1:
        return None
    return stack[0]
