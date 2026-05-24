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
            i, col = _skip_whitespace(i, col)
            continue

        if ch == '\n':
            i, line, col = _skip_newline(i, line)
            continue

        if ch == '/' and _peek(source, i) == '/':
            i, col = _skip_comment(source, i, col)
            continue

        compound_token = _try_compound_token(source, i, ch)
        if compound_token:
            tokens.append(Token(compound_token, line=line, col=col))
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


def _skip_whitespace(i, col):
    return i + 1, col + 1


def _skip_newline(i, line):
    return i + 1, line + 1, 1


def _peek(source, i):
    if i + 1 < len(source):
        return source[i + 1]
    return None


def _skip_comment(source, i, col):
    i += 2
    col += 2
    while i < len(source) and source[i] != '\n':
        i += 1
        col += 1
    return i, col


def _try_compound_token(source, i, ch):
    if i + 1 >= len(source):
        return None
    pair = ch + source[i + 1]
    return COMPOUND_TOKENS.get(pair)


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
            if len(rhs) == 0:
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
                if sym in nonterminals:
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