import Operations as op

def PrefixCalculation(expression: str):
    tokens = expression.split()
    stack = []
    error_flag = False
    def Convert2Number(token: str):
        number = None
        try:
            number = float(token)
            if number.is_integer():
                number = int(token)
        except:
            pass
        return number
        
    for token in tokens:
        stack.append(token)

        reduction = True
        while reduction:
            if len(stack) >= 2 and stack[-2] == "abs":
                operand = Convert2Number(stack[-1])
                if operand is None:
                    reduction = False
                else:
                    stack.pop(-2)
                    stack[-1] = operand
                    error_flag = op.Abs(stack)
            elif len(stack) >= 2 and stack[-2] == "sqrt":
                operand = Convert2Number(stack[-1])
                if operand is None:
                    reduction = False
                else:
                    stack.pop(-2)
                    stack[-1] = operand
                    error_flag = op.Sqrt(stack)
            elif len(stack) >= 3 and stack[-3] == "+":
                operand2 = Convert2Number(stack[-1])
                operand1 = Convert2Number(stack[-2])
                if operand2 is None or operand1 is None:
                    reduction = False
                else:
                    stack.pop(-3)
                    stack[-1] = operand2
                    stack[-2] = operand1
                    error_flag = op.Plus(stack)
            elif len(stack) >= 3 and stack[-3] == "-":
                operand2 = Convert2Number(stack[-1])
                operand1 = Convert2Number(stack[-2])
                if operand2 is None or operand1 is None:
                    reduction = False
                else:
                    stack.pop(-3)
                    stack[-1] = operand2
                    stack[-2] = operand1
                    error_flag = op.Minus(stack)
            elif len(stack) >= 3 and stack[-3] == "*":
                operand2 = Convert2Number(stack[-1])
                operand1 = Convert2Number(stack[-2])
                if operand2 is None or operand1 is None:
                    reduction = False
                else:
                    stack.pop(-3)
                    stack[-1] = operand2
                    stack[-2] = operand1
                    error_flag = op.Mult(stack)
            elif len(stack) >= 3 and stack[-3] == "/":
                operand2 = Convert2Number(stack[-1])
                operand1 = Convert2Number(stack[-2])
                if operand2 is None or operand1 is None:
                    reduction = False
                else:
                    stack.pop(-3)
                    stack[-1] = operand2
                    stack[-2] = operand1
                    error_flag = op.Div(stack)
            elif len(stack) >= 3 and stack[-3] == "%":
                operand2 = Convert2Number(stack[-1])
                operand1 = Convert2Number(stack[-2])
                if operand2 is None or operand1 is None:
                    reduction = False
                else:
                    stack.pop(-3)
                    stack[-1] = operand2
                    stack[-2] = operand1
                    error_flag = op.DivRem(stack)
            elif len(stack) >= 3 and stack[-3] == "^":
                operand2 = Convert2Number(stack[-1])
                operand1 = Convert2Number(stack[-2])
                if operand2 is None or operand1 is None:
                    reduction = False
                else:
                    stack.pop(-3)
                    stack[-1] = operand2
                    stack[-2] = operand1
                    error_flag = op.Pow(stack)
            else:
                reduction = False

            if error_flag:
                return None

    if len(stack) != 1:
        return None
    if isinstance(stack[0], str):
        stack[0] = Convert2Number(stack[0])
    return stack[0]
