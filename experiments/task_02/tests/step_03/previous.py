from solution import tokenize, Token
from solution import compute_first, compute_follow

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