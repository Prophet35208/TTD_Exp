def calculate(notation, expression):
    """
    Выполняет вычисления в постфиксной или префиксной нотации.
    
    :param notation: Тип нотации ('postfix' или 'prefix')
    :param expression: Строка с выражением
    :return: Результат вычисления
    """
    tokens = expression.split()
    
    if notation == 'postfix':
        stack = []
        for token in tokens:
            if token in ['+', '-']:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
            else:
                stack.append(int(token))
        return stack[0]
    
    elif notation == 'prefix':
