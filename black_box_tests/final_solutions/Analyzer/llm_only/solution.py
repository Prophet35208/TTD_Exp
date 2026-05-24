#!/usr/bin/env python3
"""
LL(1) синтаксический анализатор для подмножества C++.
Поддерживает объявления во вложенных блоках и оператор return.

Грамматика (LL(1), факторизованная):
  Program       → 'int' 'main' '(' ')' '{' BlockItems '}'
  BlockItems    → BlockItem BlockItems | ε
  BlockItem     → Declaration | Statement
  Declaration   → Type ID InitOpt ';'
  Type          → 'int' | 'double'
  InitOpt       → '=' Expr | ε
  Statement     → '{' BlockItems '}'
                | ID '=' Expr ';'
                | 'if' '(' Expr ')' Statement
                | 'return' ReturnRest
                | ';'
  ReturnRest    → Expr ';' | ';'
  Expr          → CompExpr
  CompExpr      → AddExpr CompRest
  CompRest      → CompOp AddExpr | ε
  CompOp        → '<' | '>' | '<=' | '>=' | '==' | '!='
  AddExpr       → MulExpr AddRest
  AddRest       → '+' MulExpr AddRest | '-' MulExpr AddRest | ε
  MulExpr       → UnaryExpr MulRest
  MulRest       → '*' UnaryExpr MulRest | '/' UnaryExpr MulRest | ε
  UnaryExpr     → '-' UnaryExpr | PrimaryExpr
  PrimaryExpr   → ID | Const | '(' Expr ')'
  Const         → INTCONST | FLOATCONST
"""

import sys
from enum import Enum, auto
from collections import OrderedDict


# ═══════════════════════════════════════════════════════════════════════
# Token definitions
# ═══════════════════════════════════════════════════════════════════════

class TokenType(Enum):
    INT = auto()
    DOUBLE = auto()
    IF = auto()
    MAIN = auto()
    RETURN = auto()
    ID = auto()
    INTCONST = auto()
    FLOATCONST = auto()
    LBRACE = auto()
    RBRACE = auto()
    LPAREN = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    EQ = auto()
    NEQ = auto()
    EOF = auto()

    def __str__(self):
        return self.name


class Token:
    def __init__(self, typ: TokenType, value=None, line=0, col=0):
        self.type = typ
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        loc = f"line {self.line}, col {self.col}"
        if self.value is not None:
            return f"Token({self.type}, {self.value!r}, {loc})"
        return f"Token({self.type}, {loc})"


# ═══════════════════════════════════════════════════════════════════════
# Lexer
# ═══════════════════════════════════════════════════════════════════════

KEYWORDS = {
    "int":    TokenType.INT,
    "double": TokenType.DOUBLE,
    "if":     TokenType.IF,
    "main":   TokenType.MAIN,
    "return": TokenType.RETURN,
}


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.length = len(source)
        self.line = 1
        self.col = 1

    def peek(self):
        if self.pos < self.length:
            return self.source[self.pos]
        return None

    def advance(self):
        ch = self.peek()
        if ch is not None:
            self.pos += 1
            if ch == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
        return ch

    def skip_whitespace(self):
        while self.peek() is not None and self.peek().isspace():
            self.advance()

    def skip_comment(self):
        while self.peek() is not None and self.peek() != '\n':
            self.advance()

    def read_number(self, first_char: str, start_line: int, start_col: int):
        num_str = first_char
        while self.peek() is not None and self.peek().isdigit():
            num_str += self.advance()
        if self.peek() == '.':
            next_pos = self.pos + 1
            if next_pos < self.length and self.source[next_pos].isdigit():
                num_str += self.advance()
                while self.peek() is not None and self.peek().isdigit():
                    num_str += self.advance()
                return Token(TokenType.FLOATCONST, float(num_str),
                             start_line, start_col)
        return Token(TokenType.INTCONST, int(num_str),
                     start_line, start_col)

    def read_identifier(self, first_char: str, start_line: int, start_col: int):
        ident = first_char
        while self.peek() is not None and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.advance()
        typ = KEYWORDS.get(ident, TokenType.ID)
        value = None if typ != TokenType.ID else ident
        return Token(typ, value, start_line, start_col)

    def next_token(self):
        while self.peek() is not None:
            ch = self.peek()

            if ch.isspace():
                self.skip_whitespace()
                continue

            if ch == '/':
                if self.pos + 1 < self.length and self.source[self.pos + 1] == '/':
                    self.advance()
                    self.advance()
                    self.skip_comment()
                    continue
                else:
                    start_line, start_col = self.line, self.col
                    self.advance()
                    return Token(TokenType.SLASH, None, start_line, start_col)

            start_line, start_col = self.line, self.col

            if ch.isdigit():
                return self.read_number(self.advance(), start_line, start_col)

            if ch.isalpha() or ch == '_':
                return self.read_identifier(self.advance(), start_line, start_col)

            if ch in ('<', '>', '=', '!'):
                if self.pos + 1 < self.length:
                    two = ch + self.source[self.pos + 1]
                    if two == '<=':
                        self.advance(); self.advance()
                        return Token(TokenType.LE, None, start_line, start_col)
                    if two == '>=':
                        self.advance(); self.advance()
                        return Token(TokenType.GE, None, start_line, start_col)
                    if two == '==':
                        self.advance(); self.advance()
                        return Token(TokenType.EQ, None, start_line, start_col)
                    if two == '!=':
                        self.advance(); self.advance()
                        return Token(TokenType.NEQ, None, start_line, start_col)
                self.advance()
                if ch == '<':
                    return Token(TokenType.LT, None, start_line, start_col)
                if ch == '>':
                    return Token(TokenType.GT, None, start_line, start_col)
                if ch == '=':
                    return Token(TokenType.ASSIGN, None, start_line, start_col)
                return Token(TokenType.NEQ, f"unexpected:{ch!r}",
                             start_line, start_col)

            single_map = {
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                ';': TokenType.SEMICOLON,
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.STAR,
            }
            if ch in single_map:
                self.advance()
                return Token(single_map[ch], None, start_line, start_col)

            self.advance()
            return Token(TokenType.EOF, f"unexpected_char:{ch!r}",
                         start_line, start_col)

        return Token(TokenType.EOF, None, self.line, self.col)


# ═══════════════════════════════════════════════════════════════════════
# Grammar (LL(1) — факторизованный return)
# ═══════════════════════════════════════════════════════════════════════

RULES = OrderedDict()
RULES[0]  = ("Program",      ["int", "main", "(", ")", "{", "BlockItems", "}"])
RULES[1]  = ("BlockItems",   ["BlockItem", "BlockItems"])
RULES[2]  = ("BlockItems",   [])                     # ε
RULES[3]  = ("BlockItem",    ["Declaration"])
RULES[4]  = ("BlockItem",    ["Statement"])
RULES[5]  = ("Declaration",  ["Type", "id", "InitOpt", ";"])
RULES[6]  = ("Type",         ["int"])
RULES[7]  = ("Type",         ["double"])
RULES[8]  = ("InitOpt",      ["=", "Expr"])
RULES[9]  = ("InitOpt",      [])                     # ε
RULES[10] = ("Statement",    ["{", "BlockItems", "}"])
RULES[11] = ("Statement",    ["id", "=", "Expr", ";"])
RULES[12] = ("Statement",    ["if", "(", "Expr", ")", "Statement"])
RULES[13] = ("Statement",    ["return", "ReturnRest"])
RULES[14] = ("Statement",    [";"])
RULES[15] = ("ReturnRest",   ["Expr", ";"])          # return Expr ;
RULES[16] = ("ReturnRest",   [";"])                  # return ;
RULES[17] = ("Expr",         ["CompExpr"])
RULES[18] = ("CompExpr",     ["AddExpr", "CompRest"])
RULES[19] = ("CompRest",     ["CompOp", "AddExpr"])
RULES[20] = ("CompRest",     [])                     # ε
RULES[21] = ("CompOp",       ["<"])
RULES[22] = ("CompOp",       [">"])
RULES[23] = ("CompOp",       ["<="])
RULES[24] = ("CompOp",       [">="])
RULES[25] = ("CompOp",       ["=="])
RULES[26] = ("CompOp",       ["!="])
RULES[27] = ("AddExpr",      ["MulExpr", "AddRest"])
RULES[28] = ("AddRest",      ["+", "MulExpr", "AddRest"])
RULES[29] = ("AddRest",      ["-", "MulExpr", "AddRest"])
RULES[30] = ("AddRest",      [])                     # ε
RULES[31] = ("MulExpr",      ["UnaryExpr", "MulRest"])
RULES[32] = ("MulRest",      ["*", "UnaryExpr", "MulRest"])
RULES[33] = ("MulRest",      ["/", "UnaryExpr", "MulRest"])
RULES[34] = ("MulRest",      [])                     # ε
RULES[35] = ("UnaryExpr",    ["-", "UnaryExpr"])
RULES[36] = ("UnaryExpr",    ["PrimaryExpr"])
RULES[37] = ("PrimaryExpr",  ["id"])
RULES[38] = ("PrimaryExpr",  ["Const"])
RULES[39] = ("PrimaryExpr",  ["(", "Expr", ")"])
RULES[40] = ("Const",        ["intconst"])
RULES[41] = ("Const",        ["floatconst"])

TOKEN_TO_SYM = {
    TokenType.INT:        "int",
    TokenType.DOUBLE:     "double",
    TokenType.IF:         "if",
    TokenType.MAIN:       "main",
    TokenType.RETURN:     "return",
    TokenType.ID:         "id",
    TokenType.INTCONST:   "intconst",
    TokenType.FLOATCONST: "floatconst",
    TokenType.LBRACE:     "{",
    TokenType.RBRACE:     "}",
    TokenType.LPAREN:     "(",
    TokenType.RPAREN:     ")",
    TokenType.SEMICOLON:  ";",
    TokenType.ASSIGN:     "=",
    TokenType.PLUS:       "+",
    TokenType.MINUS:      "-",
    TokenType.STAR:       "*",
    TokenType.SLASH:      "/",
    TokenType.LT:         "<",
    TokenType.GT:         ">",
    TokenType.LE:         "<=",
    TokenType.GE:         ">=",
    TokenType.EQ:         "==",
    TokenType.NEQ:        "!=",
    TokenType.EOF:        "EOF",
}

TERMINALS = {
    "int", "double", "if", "main", "return",
    "id", "intconst", "floatconst",
    "{", "}", "(", ")", ";", "=",
    "+", "-", "*", "/",
    "<", ">", "<=", ">=", "==", "!=",
    "EOF"
}

NONTERMINALS = {
    "Program", "BlockItems", "BlockItem",
    "Declaration", "Type", "InitOpt",
    "Statement", "ReturnRest",
    "Expr", "CompExpr", "CompRest", "CompOp",
    "AddExpr", "AddRest", "MulExpr", "MulRest",
    "UnaryExpr", "PrimaryExpr", "Const"
}

SYMBOL_DISPLAY = {
    "int":       "'int'",
    "double":    "'double'",
    "if":        "'if'",
    "main":      "'main'",
    "return":    "'return'",
    "id":        "идентификатор",
    "intconst":  "целая константа",
    "floatconst":"вещественная константа",
    "{":         "'{'",
    "}":         "'}'",
    "(":         "'('",
    ")":         "')'",
    ";":         "';'",
    "=":         "'='",
    "+":         "'+'",
    "-":         "'-'",
    "*":         "'*'",
    "/":         "'/'",
    "<":         "'<'",
    ">":         "'>'",
    "<=":        "'<='",
    ">=":        "'>='",
    "==":        "'=='",
    "!=":        "'!='",
    "EOF":       "конец файла",
}


# ═══════════════════════════════════════════════════════════════════════
# FIRST / FOLLOW / Parsing table
# ═══════════════════════════════════════════════════════════════════════

def compute_first():
    first = {nt: set() for nt in NONTERMINALS}
    changed = True
    while changed:
        changed = False
        for lhs, rhs in RULES.values():
            if len(rhs) == 0:
                if "" not in first[lhs]:
                    first[lhs].add("")
                    changed = True
            else:
                all_nullable = True
                for sym in rhs:
                    if sym in TERMINALS:
                        if sym not in first[lhs]:
                            first[lhs].add(sym)
                            changed = True
                        all_nullable = False
                        break
                    else:
                        before = len(first[lhs])
                        first[lhs] |= (first[sym] - {""})
                        if before != len(first[lhs]):
                            changed = True
                        if "" not in first[sym]:
                            all_nullable = False
                            break
                if all_nullable:
                    if "" not in first[lhs]:
                        first[lhs].add("")
                        changed = True
    return first


def compute_follow(first):
    follow = {nt: set() for nt in NONTERMINALS}
    follow["Program"].add("EOF")
    changed = True
    while changed:
        changed = False
        for lhs, rhs in RULES.values():
            for i, sym in enumerate(rhs):
                if sym in NONTERMINALS:
                    after = rhs[i + 1:]
                    all_nullable = True
                    for nxt in after:
                        if nxt in TERMINALS:
                            if nxt not in follow[sym]:
                                follow[sym].add(nxt)
                                changed = True
                            all_nullable = False
                            break
                        else:
                            before = len(follow[sym])
                            follow[sym] |= (first[nxt] - {""})
                            if before != len(follow[sym]):
                                changed = True
                            if "" not in first[nxt]:
                                all_nullable = False
                                break
                    if all_nullable:
                        before = len(follow[sym])
                        follow[sym] |= follow[lhs]
                        if before != len(follow[sym]):
                            changed = True
    return follow


def build_parsing_table(first, follow):
    table = {nt: {} for nt in NONTERMINALS}
    conflicts = []
    for rule_id, (lhs, rhs) in RULES.items():
        first_rhs = set()
        nullable = True
        for sym in rhs:
            if sym in TERMINALS:
                first_rhs.add(sym)
                nullable = False
                break
            else:
                first_rhs |= (first[sym] - {""})
                if "" not in first[sym]:
                    nullable = False
                    break
        for a in first_rhs:
            if a in table[lhs]:
                conflicts.append(
                    f"Conflict: M[{lhs}, {a}] rules {table[lhs][a]} and {rule_id}"
                )
            table[lhs][a] = rule_id
        if nullable:
            for b in follow[lhs]:
                if b in table[lhs]:
                    conflicts.append(
                        f"Conflict: M[{lhs}, {b}] rules {table[lhs][b]} and {rule_id}"
                    )
                table[lhs][b] = rule_id
    if conflicts:
        sys.stderr.write("Грамматика не LL(1)! Найдены конфликты:\n")
        for c in conflicts:
            sys.stderr.write(f"  {c}\n")
        sys.exit(1)
    return table


# ═══════════════════════════════════════════════════════════════════════
# Parser
# ═══════════════════════════════════════════════════════════════════════

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.stack = []
        self.table = None
        self.first = None
        self.follow = None
        self.errors = []

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token(TokenType.EOF, None, 0, 0)

    def advance(self):
        if self.pos < len(self.tokens):
            self.pos += 1

    def error(self, msg: str, tok: Token = None):
        if tok is None:
            tok = self.current_token()
        self.errors.append(
            f"  Строка {tok.line}, столбец {tok.col}: {msg}  "
            f"(получен токен: {self._token_str(tok)})"
        )

    def _token_str(self, tok: Token) -> str:
        sym = TOKEN_TO_SYM.get(tok.type, "???")
        disp = SYMBOL_DISPLAY.get(sym, sym)
        if tok.type == TokenType.ID:
            return f"{disp} '{tok.value}'"
        if tok.type in (TokenType.INTCONST, TokenType.FLOATCONST):
            return f"{disp} ({tok.value})"
        if tok.type == TokenType.EOF:
            return "конец файла"
        return disp

    def _expected_str(self, nonterminal: str) -> str:
        row = self.table.get(nonterminal, {})
        expected = [SYMBOL_DISPLAY.get(s, s) for s in row.keys()]
        if not expected:
            return "ничего (пустое множество)"
        return ", ".join(expected)

    def parse(self):
        self.first = compute_first()
        self.follow = compute_follow(self.first)
        self.table = build_parsing_table(self.first, self.follow)

        self.stack = ["EOF", "Program"]
        self.pos = 0
        self.errors = []

        while self.stack:
            top = self.stack.pop()
            tok = self.current_token()
            sym = TOKEN_TO_SYM.get(tok.type, "EOF")

            if top == "EOF":
                if sym == "EOF":
                    break
                else:
                    self.error("Ожидался конец файла, но встречены лишние токены", tok)
                    return 1

            if top in TERMINALS:
                if top == sym:
                    self.advance()
                else:
                    expected = SYMBOL_DISPLAY.get(top, top)
                    self.error(f"Ожидался {expected}", tok)
                    return 1

            elif top in NONTERMINALS:
                if sym in self.table[top]:
                    rule_id = self.table[top][sym]
                    rhs = RULES[rule_id][1]
                    for s in reversed(rhs):
                        if s != "":
                            self.stack.append(s)
                else:
                    expected = self._expected_str(top)
                    self.error(
                        f"При разборе <{top}> ожидался один из: {expected}",
                        tok
                    )
                    return 1
            else:
                self.error(
                    f"Внутренняя ошибка: неизвестный символ стека '{top}'",
                    tok
                )
                return 1

        return 0

    def print_errors(self):
        if self.errors:
            print("=== ОШИБКИ СИНТАКСИЧЕСКОГО АНАЛИЗА ===", file=sys.stderr)
            for e in self.errors:
                print(e, file=sys.stderr)
            print(f"Всего ошибок: {len(self.errors)}", file=sys.stderr)
        else:
            print("=== Ошибок нет ===", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "input.txt"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден", file=sys.stderr)
        print(1)
        return

    lexer = Lexer(source)
    tokens = []
    while True:
        tok = lexer.next_token()
        tokens.append(tok)
        if tok.type == TokenType.EOF:
            break

    parser = Parser(tokens)
    result = parser.parse()

    parser.print_errors()
    print(result)
    sys.exit(result)


if __name__ == "__main__":
    main()