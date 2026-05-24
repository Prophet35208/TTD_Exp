from solution import tokenize, compute_first, compute_follow, build_parsing_table, parse
from solution import FULL_RULES, FULL_NONTERMINALS, FULL_TERMINALS


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