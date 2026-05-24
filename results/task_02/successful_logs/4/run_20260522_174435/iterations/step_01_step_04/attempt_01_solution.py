class Token:
    def __init__(self, type, value=None, line=0, col=0):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line={self.line}, col={self.col})"


KEYWORDS = {
    "int": "INT",
    "double": "DOUBLE",
    "if": "IF",
    "main": "MAIN",
    "return": "RETURN"
}

SINGLE_CHAR_TOKENS = {
    '{': "LBRACE",
    '}': "RBRACE",
    '(': "LPAREN",
    ')': "RPAREN",
    ';': "SEMICOLON",
    '+': "PLUS",
    '-': "MINUS",
    '*': "STAR",
    '/': "SLASH",
    '<': "LT",
    '>': "GT",
    '=': "ASSIGN"
}

COMPOUND_TOKENS = {
    '<=': "LE",
    '>=': "GE",
    '==': "EQ",
    '!=': "NEQ"
}


def tokenize(source):
    tokens = []
    i = 0
    line = 1
    col = 1

    while i < len(source):
        ch = source[i]

        if ch in ' \t':
            i += 1
            col += 1
            continue

        if ch == '\n':
            i += 1
            line += 1
            col = 1
            continue

        if ch == '/' and i + 1 < len(source) and source[i + 1] == '/':
            i, col = _skip_comment(source, i, col)
            continue

        if i + 1 < len(source):
            pair = ch + source[i + 1]
            if pair in COMPOUND_TOKENS:
                tokens.append(Token(COMPOUND_TOKENS[pair], line=line, col=col))
                i += 2
                col += 2
                continue

        if ch in SINGLE_CHAR_TOKENS:
            tokens.append(Token(SINGLE_CHAR_TOKENS[ch], line=line, col=col))
            i += 1
            col += 1
            continue

        if ch.isdigit():
            token, i, col = _read_number(source, i, line, col)
            tokens.append(token)
            continue

        if ch.isalpha() or ch == '_':
            token, i, col = _read_identifier(source, i, line, col)
            tokens.append(token)
            continue

        raise ValueError(f"Unexpected character: {ch} at line {line}, col {col}")

    tokens.append(Token("EOF", line=line, col=col))
    return tokens


def _skip_comment(source, i, col):
    i += 2
    col += 2
    while i < len(source) and source[i] != '\n':
        i += 1
        col += 1
    return i, col


def _read_number(source, i, line, col):
    start_col = col
    num_str = ""
    while i < len(source) and source[i].isdigit():
        num_str += source[i]
        i += 1
        col += 1

    if i < len(source) and source[i] == '.':
        num_str += '.'
        i += 1
        col += 1
        while i < len(source) and source[i].isdigit():
            num_str += source[i]
            i += 1
            col += 1
        return Token("FLOATCONST", float(num_str), line=line, col=start_col), i, col

    return Token("INTCONST", int(num_str), line=line, col=start_col), i, col


def _read_identifier(source, i, line, col):
    start_col = col
    ident = ""
    while i < len(source) and (source[i].isalnum() or source[i] == '_'):
        ident += source[i]
        i += 1
        col += 1

    token_type = KEYWORDS.get(ident, "ID")
    token_value = None if token_type != "ID" else ident
    return Token(token_type, token_value, line=line, col=start_col), i, col


def compute_first(rules, nonterminals, terminals):
    first = {nt: set() for nt in nonterminals}
    changed = True
    while changed:
        changed = False
        for lhs, rhs in rules:
            if not rhs:
                if "" not in first[lhs]:
                    first[lhs].add("")
                    changed = True
                continue
            all_epsilon = True
            for sym in rhs:
                if sym in terminals:
                    if sym not in first[lhs]:
                        first[lhs].add(sym)
                        changed = True
                    all_epsilon = False
                    break
                else:
                    for f in first[sym]:
                        if f != "" and f not in first[lhs]:
                            first[lhs].add(f)
                            changed = True
                    if "" not in first[sym]:
                        all_epsilon = False
                        break
            if all_epsilon:
                if "" not in first[lhs]:
                    first[lhs].add("")
                    changed = True
    return first


def compute_follow(rules, first, nonterminals):
    follow = {nt: set() for nt in nonterminals}
    start_symbol = rules[0][0]
    follow[start_symbol].add("EOF")
    changed = True
    while changed:
        changed = False
        for lhs, rhs in rules:
            for i, sym in enumerate(rhs):
                if sym not in nonterminals:
                    continue
                if i + 1 < len(rhs):
                    next_sym = rhs[i + 1]
                    if next_sym in first:
                        for f in first[next_sym]:
                            if f != "" and f not in follow[sym]:
                                follow[sym].add(f)
                                changed = True
                        if "" in first[next_sym]:
                            for f in follow[lhs]:
                                if f not in follow[sym]:
                                    follow[sym].add(f)
                                    changed = True
                    else:
                        if next_sym not in follow[sym]:
                            follow[sym].add(next_sym)
                            changed = True
                else:
                    for f in follow[lhs]:
                        if f not in follow[sym]:
                            follow[sym].add(f)
                            changed = True
    return follow


def build_parsing_table(rules, first, follow, terminals, nonterminals):
    table = {nt: {} for nt in nonterminals}
    for rule_id, (lhs, rhs) in enumerate(rules):
        first_set = _compute_rhs_first(rhs, first, terminals)
        for t in first_set:
            if t != "":
                table[lhs][t] = rule_id
        if "" in first_set:
            for t in follow[lhs]:
                table[lhs][t] = rule_id
    return table


def _compute_rhs_first(rhs, first, terminals):
    if not rhs:
        return {""}
    first_set = set()
    all_epsilon = True
    for sym in rhs:
        if sym in terminals:
            first_set.add(sym)
            all_epsilon = False
            break
        else:
            for f in first[sym]:
                if f != "":
                    first_set.add(f)
            if "" not in first[sym]:
                all_epsilon = False
                break
    if all_epsilon:
        first_set.add("")
    return first_set


def parse(tokens, rules, table, nonterminals, terminals):
    stack = ["EOF", "Program"]
    pos = 0

    while stack:
        top = stack.pop()
        current_token = tokens[pos]
        current_terminal = _token_to_terminal(current_token)

        if top in terminals:
            if top == current_terminal:
                pos += 1
            else:
                return 1
        elif top in nonterminals:
            if current_terminal in table[top]:
                rule_id = table[top][current_terminal]
                rhs = rules[rule_id][1]
                for sym in reversed(rhs):
                    stack.append(sym)
            else:
                return 1
        else:
            return 1

    return 0


def _token_to_terminal(tok):
    mapping = {
        "INT": "int",
        "DOUBLE": "double",
        "IF": "if",
        "MAIN": "main",
        "RETURN": "return",
        "ID": "id",
        "INTCONST": "intconst",
        "FLOATCONST": "floatconst",
        "LBRACE": "{",
        "RBRACE": "}",
        "LPAREN": "(",
        "RPAREN": ")",
        "SEMICOLON": ";",
        "ASSIGN": "=",
        "PLUS": "+",
        "MINUS": "-",
        "STAR": "*",
        "SLASH": "/",
        "LT": "<",
        "GT": ">",
        "LE": "<=",
        "GE": ">=",
        "EQ": "==",
        "NEQ": "!=",
        "EOF": "EOF"
    }
    return mapping.get(tok.type, tok.type)


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


def main():
    import os
    if not os.path.exists("In.txt"):
        with open("Out.txt", "w") as f:
            f.write("1")
        return 1

    with open("In.txt", "r") as f:
        source = f.read()

    if not source.strip():
        with open("Out.txt", "w") as f:
            f.write("1")
        return 1

    try:
        tokens = tokenize(source)
    except ValueError:
        with open("Out.txt", "w") as f:
            f.write("1")
        return 1

    first = compute_first(FULL_RULES, FULL_NONTERMINALS, FULL_TERMINALS)
    follow = compute_follow(FULL_RULES, first, FULL_NONTERMINALS)
    table = build_parsing_table(FULL_RULES, first, follow, FULL_TERMINALS, FULL_NONTERMINALS)
    result = parse(tokens, FULL_RULES, table, FULL_NONTERMINALS, FULL_TERMINALS)

    with open("Out.txt", "w") as f:
        f.write(str(result))
    return result