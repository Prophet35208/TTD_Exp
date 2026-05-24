from solution import tokenize, Token
from solution import compute_first, compute_follow
from solution import tokenize, compute_first, compute_follow, build_parsing_table, parse
from solution import FULL_RULES, FULL_NONTERMINALS, FULL_TERMINALS

# Этап 1: Лексер
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

# Этап 2
# Тестовая грамматика (упрощённая, для проверки логики)
# Program → int main ( ) { Declarations }
# Declarations → Declaration Declarations | ε
# Declaration → Type id ;
# Type → int | double

RULES = [
    ("Program", ("int", "main", "(", ")", "{", "Declarations", "}")),
    ("Declarations", ("Declaration", "Declarations")),
    ("Declarations", ()),  # ε
    ("Declaration", ("Type", "id", ";")),
    ("Type", ("int",)),
    ("Type", ("double",)),
]

NONTERMINALS = {"Program", "Declarations", "Declaration", "Type"}
TERMINALS = {"int", "main", "(", ")", "{", "}", "id", ";", "double"}


def test_rules_format():
    """Правила — список кортежей (LHS, RHS)."""
    assert isinstance(RULES, list)
    assert len(RULES) > 0
    for rule in RULES:
        assert isinstance(rule, tuple)
        assert len(rule) == 2
        lhs, rhs = rule
        assert isinstance(lhs, str)
        assert isinstance(rhs, tuple)
        for sym in rhs:
            assert isinstance(sym, str)


def test_first_terminal():
    """FIRST для правила, начинающегося с терминала."""
    first = compute_first(RULES, NONTERMINALS, TERMINALS)
    assert first["Program"] == {"int"}
    assert first["Type"] == {"int", "double"}


def test_first_nonterminal():
    """FIRST для правила, начинающегося с нетерминала."""
    first = compute_first(RULES, NONTERMINALS, TERMINALS)
    assert first["Declaration"] == {"int", "double"}


def test_first_epsilon():
    """FIRST для ε-правила содержит ε."""
    first = compute_first(RULES, NONTERMINALS, TERMINALS)
    assert "" in first["Declarations"]


def test_first_combined():
    """FIRST для нетерминала с несколькими правилами."""
    first = compute_first(RULES, NONTERMINALS, TERMINALS)
    assert first["Declarations"] == {"int", "double", ""}


def test_follow_start_symbol():
    """FOLLOW стартового символа содержит EOF."""
    follow = compute_follow(RULES, compute_first(RULES, NONTERMINALS, TERMINALS), NONTERMINALS)
    assert "EOF" in follow["Program"]


def test_follow_after_terminal():
    """FOLLOW для нетерминала, за которым следует другой символ."""
    follow = compute_follow(RULES, compute_first(RULES, NONTERMINALS, TERMINALS), NONTERMINALS)
    # Declaration → Type id ;
    # После Type идёт id, значит FOLLOW[Type] содержит "id"
    assert "id" in follow["Type"]


def test_follow_transitive():
    """FOLLOW с учётом транзитивности (ε-нетерминал)."""
    follow = compute_follow(RULES, compute_first(RULES, NONTERMINALS, TERMINALS), NONTERMINALS)
    # Declaration → Type id ;
    # Type → int | double
    # FOLLOW[Type] должен содержать "id" (то, что идёт после Type в Declaration)
    assert "id" in follow["Type"]


def test_follow_end_of_rule():
    """FOLLOW для нетерминала в конце правила включает FOLLOW левой части."""
    follow = compute_follow(RULES, compute_first(RULES, NONTERMINALS, TERMINALS), NONTERMINALS)
    # Declarations в конце правила Program → ... Declarations }
    # FOLLOW[Declarations] должен содержать "}" (терминал после Declarations в Program)
    assert "}" in follow["Declarations"]


def test_first_follow_full_grammar():
    """Полная проверка FIRST и FOLLOW на всей грамматике."""
    first = compute_first(RULES, NONTERMINALS, TERMINALS)
    follow = compute_follow(RULES, first, NONTERMINALS)
    
    # FIRST
    assert first["Program"] == {"int"}
    assert first["Declarations"] == {"int", "double", ""}
    assert first["Declaration"] == {"int", "double"}
    assert first["Type"] == {"int", "double"}
    
    # FOLLOW
    assert "EOF" in follow["Program"]
    assert "}" in follow["Declarations"]
    assert "id" in follow["Type"]
    assert ";" not in follow["Type"]  # ; не после Type, а после id

# Этап 3: Грамматика (спецификация)
FULL_RULES = [
    ("Program", ("int", "main", "(", ")", "{", "BlockItems", "}")),
    ("BlockItems", ("BlockItem", "BlockItems")),
    ("BlockItems", ()),
    ("BlockItem", ("Declaration",)),
    ("BlockItem", ("Statement",)),
    ("Declaration", ("Type", "id", "InitOpt", ";")),
    ("Type", ("int",)),
    ("Type", ("double",)),
    ("InitOpt", ("=", "Expr")),
    ("InitOpt", ()),
    ("Statement", ("{", "BlockItems", "}")),
    ("Statement", ("id", "=", "Expr", ";")),
    ("Statement", ("if", "(", "Expr", ")", "Statement")),
    ("Statement", ("return", "ReturnRest")),
    ("Statement", (";",)),
    ("ReturnRest", ("Expr", ";")),
    ("ReturnRest", (";",)),
    ("Expr", ("CompExpr",)),
    ("CompExpr", ("AddExpr", "CompRest")),
    ("CompRest", ("CompOp", "AddExpr")),
    ("CompRest", ()),
    ("CompOp", ("<",)),
    ("CompOp", (">",)),
    ("CompOp", ("<=",)),
    ("CompOp", (">=",)),
    ("CompOp", ("==",)),
    ("CompOp", ("!=",)),
    ("AddExpr", ("MulExpr", "AddRest")),
    ("AddRest", ("+", "MulExpr", "AddRest")),
    ("AddRest", ("-", "MulExpr", "AddRest")),
    ("AddRest", ()),
    ("MulExpr", ("UnaryExpr", "MulRest")),
    ("MulRest", ("*", "UnaryExpr", "MulRest")),
    ("MulRest", ("/", "UnaryExpr", "MulRest")),
    ("MulRest", ()),
    ("UnaryExpr", ("-", "UnaryExpr")),
    ("UnaryExpr", ("PrimaryExpr",)),
    ("PrimaryExpr", ("id",)),
    ("PrimaryExpr", ("Const",)),
    ("PrimaryExpr", ("(", "Expr", ")")),
    ("Const", ("intconst",)),
    ("Const", ("floatconst",)),
]

FULL_NONTERMINALS = {
    "Program", "BlockItems", "BlockItem", "Declaration", "Type", "InitOpt",
    "Statement", "ReturnRest", "Expr", "CompExpr", "CompRest", "CompOp",
    "AddExpr", "AddRest", "MulExpr", "MulRest", "UnaryExpr", "PrimaryExpr", "Const"
}

FULL_TERMINALS = {
    "int", "double", "if", "main", "return", "id", "intconst", "floatconst",
    "{", "}", "(", ")", ";", "=", "+", "-", "*", "/",
    "<", ">", "<=", ">=", "==", "!=", "EOF"
}

# Этап 3 
def test_parsing_table_no_conflicts():
    """Таблица разбора строится без конфликтов."""
    first = compute_first(FULL_RULES, FULL_NONTERMINALS, FULL_TERMINALS)
    follow = compute_follow(FULL_RULES, first, FULL_NONTERMINALS)
    table = build_parsing_table(FULL_RULES, first, follow, FULL_TERMINALS, FULL_NONTERMINALS)
    for nt, row in table.items():
        for t, rule_id in row.items():
            assert isinstance(rule_id, int)


def test_parse_empty_main():
    """Пустая программа: int main() { }"""
    source = "int main() { }"
    tokens = tokenize(source)
    first = compute_first(FULL_RULES, FULL_NONTERMINALS, FULL_TERMINALS)
    follow = compute_follow(FULL_RULES, first, FULL_NONTERMINALS)
    table = build_parsing_table(FULL_RULES, first, follow, FULL_TERMINALS, FULL_NONTERMINALS)
    result = parse(tokens, FULL_RULES, table, FULL_NONTERMINALS, FULL_TERMINALS)
    assert result == 0


def test_parse_simple_declaration():
    """Простое объявление: int main() { int a = 5; }"""
    source = "int main() { int a = 5; }"
    tokens = tokenize(source)
    first = compute_first(FULL_RULES, FULL_NONTERMINALS, FULL_TERMINALS)
    follow = compute_follow(FULL_RULES, first, FULL_NONTERMINALS)
    table = build_parsing_table(FULL_RULES, first, follow, FULL_TERMINALS, FULL_NONTERMINALS)
    result = parse(tokens, FULL_RULES, table, FULL_NONTERMINALS, FULL_TERMINALS)
    assert result == 0


def test_parse_declaration_without_init():
    """Объявление без инициализации: int a;"""
    source = "int main() { int a; }"
    tokens = tokenize(source)
    first = compute_first(FULL_RULES, FULL_NONTERMINALS, FULL_TERMINALS)
    follow = compute_follow(FULL_RULES, first, FULL_NONTERMINALS)
    table = build_parsing_table(FULL_RULES, first, follow, FULL_TERMINALS, FULL_NONTERMINALS)
    result = parse(tokens, FULL_RULES, table, FULL_NONTERMINALS, FULL_TERMINALS)
    assert result == 0


def test_parse_multiple_declarations():
    """Несколько объявлений: int a; double b;"""
    source = "int main() { int a; double b; }"
    tokens = tokenize(source)
    first = compute_first(FULL_RULES, FULL_NONTERMINALS, FULL_TERMINALS)
    follow = compute_follow(FULL_RULES, first, FULL_NONTERMINALS)
    table = build_parsing_table(FULL_RULES, first, follow, FULL_TERMINALS, FULL_NONTERMINALS)
    result = parse(tokens, FULL_RULES, table, FULL_NONTERMINALS, FULL_TERMINALS)
    assert result == 0


def test_parse_assignment():
    """Присваивание: int main() { a = 5; }"""
    source = "int main() { a = 5; }"
    tokens = tokenize(source)
    first = compute_first(FULL_RULES, FULL_NONTERMINALS, FULL_TERMINALS)
    follow = compute_follow(FULL_RULES, first, FULL_NONTERMINALS)
    table = build_parsing_table(FULL_RULES, first, follow, FULL_TERMINALS, FULL_NONTERMINALS)
    result = parse(tokens, FULL_RULES, table, FULL_NONTERMINALS, FULL_TERMINALS)
    assert result == 0


def test_parse_empty_statement():
    """Пустой оператор: int main() { ; }"""
    source = "int main() { ; }"
    tokens = tokenize(source)
    first = compute_first(FULL_RULES, FULL_NONTERMINALS, FULL_TERMINALS)
    follow = compute_follow(FULL_RULES, first, FULL_NONTERMINALS)
    table = build_parsing_table(FULL_RULES, first, follow, FULL_TERMINALS, FULL_NONTERMINALS)
    result = parse(tokens, FULL_RULES, table, FULL_NONTERMINALS, FULL_TERMINALS)
    assert result == 0


def test_parse_missing_semicolon():
    """Ошибка: пропущена ; → int main() { int a }"""
    source = "int main() { int a }"
    tokens = tokenize(source)
    first = compute_first(FULL_RULES, FULL_NONTERMINALS, FULL_TERMINALS)
    follow = compute_follow(FULL_RULES, first, FULL_NONTERMINALS)
    table = build_parsing_table(FULL_RULES, first, follow, FULL_TERMINALS, FULL_NONTERMINALS)
    result = parse(tokens, FULL_RULES, table, FULL_NONTERMINALS, FULL_TERMINALS)
    assert result == 1


def test_parse_invalid_type():
    """Ошибка: неверный тип → string a;"""
    source = "int main() { string a; }"
    tokens = tokenize(source)
    first = compute_first(FULL_RULES, FULL_NONTERMINALS, FULL_TERMINALS)
    follow = compute_follow(FULL_RULES, first, FULL_NONTERMINALS)
    table = build_parsing_table(FULL_RULES, first, follow, FULL_TERMINALS, FULL_NONTERMINALS)
    result = parse(tokens, FULL_RULES, table, FULL_NONTERMINALS, FULL_TERMINALS)
    assert result == 1


def test_parse_missing_closing_brace():
    """Ошибка: пропущена } → int main() { int a;"""
    source = "int main() { int a;"
    tokens = tokenize(source)
    first = compute_first(FULL_RULES, FULL_NONTERMINALS, FULL_TERMINALS)
    follow = compute_follow(FULL_RULES, first, FULL_NONTERMINALS)
    table = build_parsing_table(FULL_RULES, first, follow, FULL_TERMINALS, FULL_NONTERMINALS)
    result = parse(tokens, FULL_RULES, table, FULL_NONTERMINALS, FULL_TERMINALS)
    assert result == 1

def test_full_rules_structure():
    """FULL_RULES содержит правила для всех конструкций языка."""
    assert isinstance(FULL_RULES, list)
    assert len(FULL_RULES) > 10  # Должно быть много правил
    for lhs, rhs in FULL_RULES:
        assert isinstance(lhs, str)
        assert isinstance(rhs, tuple)
        for sym in rhs:
            assert isinstance(sym, str)
            assert sym in FULL_TERMINALS or sym in FULL_NONTERMINALS or sym == ""


def test_full_terminals_match_token_types():
    """Терминалы грамматики соответствуют токенам лексера."""
    expected = {"int", "double", "if", "main", "return", "id", "intconst", "floatconst",
                "{", "}", "(", ")", ";", "=", "+", "-", "*", "/",
                "<", ">", "<=", ">=", "==", "!=", "EOF"}
    for t in expected:
        assert t in FULL_TERMINALS, f"'{t}' отсутствует в FULL_TERMINALS"
    # Типы токенов (INT, SEMICOLON) не должны быть в терминалах
    assert "INT" not in FULL_TERMINALS
    assert "SEMICOLON" not in FULL_TERMINALS


def test_full_nonterminals_contain_required():
    """FULL_NONTERMINALS содержит ключевые нетерминалы."""
    required = {"Program", "BlockItems", "BlockItem", "Declaration", "Statement",
                "Expr", "Type", "InitOpt"}
    for nt in required:
        assert nt in FULL_NONTERMINALS, f"'{nt}' отсутствует в FULL_NONTERMINALS"

def test_full_terminals_exact_match():
    """FULL_TERMINALS содержит только те терминалы, которые есть в лексере."""
    allowed = {"int", "double", "if", "main", "return", "id", "intconst", "floatconst",
               "{", "}", "(", ")", ";", "=", "+", "-", "*", "/",
               "<", ">", "<=", ">=", "==", "!=", "EOF"}
    for t in FULL_TERMINALS:
        assert t in allowed, f"'{t}' не поддерживается лексером"
    for t in allowed:
        assert t in FULL_TERMINALS, f"'{t}' отсутствует в FULL_TERMINALS"

