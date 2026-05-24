import re
from enum import Enum, auto

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

class Token:
    def __init__(self, type, value=None, line=0, col=0):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line={self.line}, col={self.col})"

KEYWORDS = {
    'int': TokenType.INT,
    'double': TokenType.DOUBLE,
    'if': TokenType.IF,
    'main': TokenType.MAIN,
    'return': TokenType.RETURN,
}

TOKEN_SPEC = [
    ('FLOATCONST', r'\d+\.\d+'),
    ('INTCONST', r'\d+'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('LE', r'<='),
    ('GE', r'>='),
    ('EQ', r'=='),
    ('NEQ', r'!='),
    ('LT', r'<'),
    ('GT', r'>'),
    ('ASSIGN', r'='),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('STAR', r'\*'),
    ('SLASH', r'/'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('SEMICOLON', r';'),
    ('SKIP', r'[ \t]+'),
    ('NEWLINE', r'\n'),
    ('COMMENT', r'//[^\n]*'),
]

def tokenize(code):
    tokens = []
    line = 1
    col = 1
    pos = 0
    while pos < len(code):
        match = None
        for token_type, pattern in TOKEN_SPEC:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                text = match.group(0)
                if token_type == 'NEWLINE':
                    line += 1
                    col = 1
                elif token_type == 'SKIP':
                    col += len(text)
                elif token_type == 'COMMENT':
                    col += len(text)
                else:
                    if token_type == 'ID' and text in KEYWORDS:
                        token_type = KEYWORDS[text].name
                        value = None
                    elif token_type == 'INTCONST':
                        value = int(text)
                    elif token_type == 'FLOATCONST':
                        value = float(text)
                    elif token_type == 'ID':
                        value = text
                    else:
                        value = None
                    tokens.append(Token(TokenType[token_type], value, line, col))
                    col += len(text)
                pos = match.end()
                break
        if not match:
            raise SyntaxError(f"Unexpected character: {code[pos]!r} at line {line}, col {col}")
    tokens.append(Token(TokenType.EOF, None, line, col))
    return tokens