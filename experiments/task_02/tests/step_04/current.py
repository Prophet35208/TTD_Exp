import os
from solution import main

def test_main_valid_postfix():
    """Корректная программа с постфиксным выражением: a = 5;"""
    with open("In.txt", "w") as f:
        f.write("int main() { int a = 5; }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"

def test_main_valid_prefix():
    """Корректная программа с префиксным выражением: a = 5;"""
    with open("In.txt", "w") as f:
        f.write("int main() { double b = 3.14; }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"

def test_main_valid_complex():
    """Корректная программа с несколькими операторами."""
    source = """int main() {
    int a = 10;
    double b = 2.5;
    a = a + 1;
    if (a > b) {
        a = 0;
    }
    return a;
}"""
    with open("In.txt", "w") as f:
        f.write(source)
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"

def test_main_valid_empty_body():
    """Пустое тело main: int main() { }"""
    with open("In.txt", "w") as f:
        f.write("int main() { }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"

def test_main_valid_empty_statement():
    """Пустой оператор: ;"""
    with open("In.txt", "w") as f:
        f.write("int main() { ; }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"

def test_main_valid_return_value():
    """return с выражением: return 0;"""
    with open("In.txt", "w") as f:
        f.write("int main() { return 0; }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"

def test_main_valid_return_void():
    """return без выражения: return;"""
    with open("In.txt", "w") as f:
        f.write("int main() { return; }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"

def test_main_valid_if_with_braces():
    """if с составным оператором: if (a > b) { ... }"""
    with open("In.txt", "w") as f:
        f.write("int main() { int a = 5; if (a > 0) { a = 1; } }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"

def test_main_valid_if_without_braces():
    """if без фигурных скобок: if (a > 0) a = 1;"""
    with open("In.txt", "w") as f:
        f.write("int main() { int a = 5; if (a > 0) a = 1; }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"

def test_main_valid_nested_blocks():
    """Вложенные блоки: { { int a; } }"""
    with open("In.txt", "w") as f:
        f.write("int main() { { int a = 5; } }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"

def test_main_valid_comparison_ops():
    """Все операторы сравнения в выражениях."""
    with open("In.txt", "w") as f:
        f.write("int main() { int a = 5; if (a < 10) a = 1; if (a >= 1) a = 2; }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"

def test_main_valid_comments():
    """Программа с комментариями."""
    source = """// This is a comment
int main() {
    int a = 5; // inline comment
    // another comment
    return 0;
}"""
    with open("In.txt", "w") as f:
        f.write(source)
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"

def test_main_error_missing_semicolon():
    """Ошибка: пропущена ; после объявления."""
    with open("In.txt", "w") as f:
        f.write("int main() { int a }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 1
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "1"

def test_main_error_invalid_type():
    """Ошибка: неверный тип string."""
    with open("In.txt", "w") as f:
        f.write("int main() { string a; }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 1
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "1"

def test_main_error_missing_closing_brace():
    """Ошибка: не закрыта фигурная скобка."""
    with open("In.txt", "w") as f:
        f.write("int main() { int a = 5;")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 1
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "1"

def test_main_error_missing_opening_paren():
    """Ошибка: пропущена ( в main."""
    with open("In.txt", "w") as f:
        f.write("int main) { }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 1
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "1"

def test_main_error_unexpected_token():
    """Ошибка: неожиданный токен в неверном месте."""
    with open("In.txt", "w") as f:
        f.write("int main() { = a; }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 1
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "1"

def test_main_no_file():
    """Файл In.txt отсутствует → ошибка."""
    if os.path.exists("In.txt"):
        os.remove("In.txt")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 1
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "1"

def test_main_empty_file():
    """Файл In.txt пуст → ошибка."""
    with open("In.txt", "w") as f:
        f.write("")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 1
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "1"

def test_main_valid_arithmetic():
    """Программа с арифметическими выражениями."""
    source = """int main() {
    int a = 10;
    int b = 3;
    a = a + b;
    a = a - b;
    a = a * b;
    a = a / b;
    return 0;
}"""
    with open("In.txt", "w") as f:
        f.write(source)
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"

def test_main_valid_unary_minus():
    """Унарный минус в выражении."""
    with open("In.txt", "w") as f:
        f.write("int main() { int a = -5; }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"

def test_main_valid_parenthesized_expr():
    """Выражение в скобках: (a + b)"""
    with open("In.txt", "w") as f:
        f.write("int main() { int a = (5 + 3); }")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "0"