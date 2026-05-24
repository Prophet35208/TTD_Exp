from solution import tokenize, Token

def test_tokenize_keywords():
    """Ключевые слова распознаются как соответствующие токены."""
    tokens = tokenize("int double if main return")
    types = [t.type for t in tokens if t.type != "EOF"]
    assert types == ["INT", "DOUBLE", "IF", "MAIN", "RETURN"]

def test_tokenize_identifiers():
    """Идентификаторы распознаются как ID со значением."""
    tokens = tokenize("a b x y z temp result")
    values = [t.value for t in tokens if t.type == "ID"]
    assert values == ["a", "b", "x", "y", "z", "temp", "result"]

def test_tokenize_integer_constants():
    """Целые числа распознаются как INTCONST."""
    tokens = tokenize("10 0 100 42")
    values = [t.value for t in tokens if t.type == "INTCONST"]
    assert values == [10, 0, 100, 42]

def test_tokenize_float_constants():
    """Вещественные числа распознаются как FLOATCONST."""
    tokens = tokenize("2.5 3.14 0.5 1.0")
    values = [t.value for t in tokens if t.type == "FLOATCONST"]
    assert values == [2.5, 3.14, 0.5, 1.0]

def test_tokenize_operators():
    """Операторы распознаются правильно."""
    tokens = tokenize("+ - * / = < > <= >= == !=")
    types = [t.type for t in tokens if t.type != "EOF"]
    assert types == ["PLUS", "MINUS", "STAR", "SLASH", "ASSIGN",
                     "LT", "GT", "LE", "GE", "EQ", "NEQ"]

def test_tokenize_braces_and_parens():
    """Скобки распознаются правильно."""
    tokens = tokenize("{ } ( ) ;")
    types = [t.type for t in tokens if t.type != "EOF"]
    assert types == ["LBRACE", "RBRACE", "LPAREN", "RPAREN", "SEMICOLON"]

def test_tokenize_simple_declaration():
    """Простое объявление: int a = 5;"""
    tokens = tokenize("int a = 5;")
    types = [t.type for t in tokens if t.type != "EOF"]
    assert types == ["INT", "ID", "ASSIGN", "INTCONST", "SEMICOLON"]
    assert tokens[1].value == "a"
    assert tokens[3].value == 5

def test_tokenize_comment_ignored():
    """Комментарий // ... игнорируется."""
    tokens = tokenize("int a; // this is a comment\nint b;")
    types = [t.type for t in tokens if t.type != "EOF"]
    assert types == ["INT", "ID", "SEMICOLON", "INT", "ID", "SEMICOLON"]

def test_tokenize_comment_at_end():
    """Комментарий в конце файла без перевода строки."""
    tokens = tokenize("int a; // comment")
    types = [t.type for t in tokens if t.type != "EOF"]
    assert types == ["INT", "ID", "SEMICOLON"]

def test_tokenize_eof():
    """В конце всегда токен EOF."""
    tokens = tokenize("int a;")
    assert tokens[-1].type == "EOF"

def test_tokenize_line_and_col():
    """Токены содержат информацию о строке и столбце."""
    tokens = tokenize("int a;\nint b;")
    assert tokens[0].line == 1  # int
    assert tokens[1].line == 1  # a
    assert tokens[2].line == 1  # ;
    assert tokens[3].line == 2  # int
    assert tokens[4].line == 2  # b
    assert tokens[5].line == 2  # ;