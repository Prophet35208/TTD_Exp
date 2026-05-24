#!/usr/bin/env python3
"""
Консольное приложение calculator.
Вычисляет значение математического выражения в префиксной или постфиксной нотации.
Вход: файл In.txt
Выход: файл Out.txt
"""

import sys


# ------------------------------------------------------------
#  Вычисление постфиксного (обратная польская) выражения
# ------------------------------------------------------------
def evaluate_postfix(tokens):
    stack = []

    for token in tokens:
        # Бинарные операторы
        if token in ('+', '-', '*', '/', '%', '^'):
            if len(stack) < 2:
                return None
            b = stack.pop()
            a = stack.pop()

            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    return None
                stack.append(a / b)
            elif token == '%':
                if b == 0:
                    return None
                try:
                    stack.append(a % b)
                except (ValueError, ZeroDivisionError):
                    return None
            elif token == '^':
                try:
                    res = a ** b
                    if isinstance(res, complex):
                        return None
                    stack.append(res)
                except (ValueError, OverflowError):
                    return None

        # Унарные операторы
        elif token in ('sqrt', 'abs'):
            if len(stack) < 1:
                return None
            a = stack.pop()

            if token == 'sqrt':
                if a < 0:
                    return None
                try:
                    stack.append(a ** 0.5)
                except (ValueError, OverflowError):
                    return None
            elif token == 'abs':
                stack.append(abs(a))

        # Операнд (число)
        else:
            try:
                num = float(token)
                stack.append(num)
            except ValueError:
                return None   # некорректный токен

    if len(stack) != 1:
        return None          # остались лишние операнды

    return stack[0]


# ------------------------------------------------------------
#  Вычисление префиксного (польская) выражения
#  Обход справа налево, используется тот же стековый алгоритм
# ------------------------------------------------------------
def evaluate_prefix(tokens):
    stack = []

    for token in reversed(tokens):
        # Бинарные операторы
        if token in ('+', '-', '*', '/', '%', '^'):
            if len(stack) < 2:
                return None
            a = stack.pop()      # левый операнд
            b = stack.pop()      # правый операнд

            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    return None
                stack.append(a / b)
            elif token == '%':
                if b == 0:
                    return None
                try:
                    stack.append(a % b)
                except (ValueError, ZeroDivisionError):
                    return None
            elif token == '^':
                try:
                    res = a ** b
                    if isinstance(res, complex):
                        return None
                    stack.append(res)
                except (ValueError, OverflowError):
                    return None

        # Унарные операторы
        elif token in ('sqrt', 'abs'):
            if len(stack) < 1:
                return None
            a = stack.pop()

            if token == 'sqrt':
                if a < 0:
                    return None
                try:
                    stack.append(a ** 0.5)
                except (ValueError, OverflowError):
                    return None
            elif token == 'abs':
                stack.append(abs(a))

        # Операнд (число)
        else:
            try:
                num = float(token)
                stack.append(num)
            except ValueError:
                return None

    if len(stack) != 1:
        return None

    return stack[0]


# ------------------------------------------------------------
#  Форматирование результата
# ------------------------------------------------------------
def format_result(value: float) -> str:
    """Целое без дробной части, иначе с двумя знаками после точки."""
    if value.is_integer():
        return str(int(value))
    return f"{value:.2f}"


# ------------------------------------------------------------
#  Главная программа
# ------------------------------------------------------------
def main():
    try:
        with open('In.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() != '']
    except Exception:
        # Файл не найден или не читается
        with open('Out.txt', 'w', encoding='utf-8') as f:
            f.write('Error')
        sys.exit(1)

    if len(lines) < 2:
        with open('Out.txt', 'w', encoding='utf-8') as f:
            f.write('Error')
        sys.exit(1)

    mode = lines[0]
    expression = lines[1]
    tokens = expression.split()

    # Выбор режима вычисления
    if mode == 'postfix':
        result = evaluate_postfix(tokens)
    elif mode == 'prefix':
        result = evaluate_prefix(tokens)
    else:
        result = None

    # Запись результата
    if result is None:
        with open('Out.txt', 'w', encoding='utf-8') as f:
            f.write('Error')
        sys.exit(1)

    formatted = format_result(result)
    with open('Out.txt', 'w', encoding='utf-8') as f:
        f.write(formatted)
    sys.exit(0)


if __name__ == '__main__':
    main()