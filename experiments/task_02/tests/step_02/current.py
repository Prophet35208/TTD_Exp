from solution import compute_first, compute_follow
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