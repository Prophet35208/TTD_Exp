class Token:
    def __init__(self, type, value=None, line=0, col=0):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line={self.line}, col={self.col})"


def tokenize(source):
    tokens = []
    i = 0
    line = 1
    col = 1

    while i < len(source):
        ch = source[i]

        # Пропуск пробелов и переводов строк
        if ch in ' \t':
            i += 1
            col += 1
            continue
        if ch == '\n':
            i += 1
            line += 1
            col = 1
            continue

        # Комментарии //
        if ch == '/' and i + 1 < len(source) and source[i + 1] == '/':
            i += 2
            col += 2
            while i < len(source) and source[i] != '\n':
                i += 1
                col += 1
            continue

        # Составные операторы
        if ch == '<' and i + 1 < len(source) and source[i + 1] == '=':
            tokens.append(Token("LE", line=line, col=col))
            i += 2
            col += 2
            continue
        if ch == '>' and i + 1 < len(source) and source[i + 1] == '=':
            tokens.append(Token("GE", line=line, col=col))
            i += 2
            col += 2
            continue
        if ch == '=' and i + 1 < len(source) and source[i + 1] == '=':
            tokens.append(Token("EQ", line=line, col=col))
            i += 2
            col += 2
            continue
        if ch == '!' and i + 1 < len(source) and source[i + 1] == '=':
            tokens.append(Token("NEQ", line=line, col=col))
            i += 2
            col += 2
            continue

        # Одиночные символы
        if ch == '{':
            tokens.append(Token("LBRACE", line=line, col=col))
            i += 1
            col += 1
            continue
        if ch == '}':
            tokens.append(Token("RBRACE", line=line, col=col))
            i += 1
            col += 1
            continue
        if ch == '(':
            tokens.append(Token("LPAREN", line=line, col=col))
            i += 1
            col += 1
            continue
        if ch == ')':
            tokens.append(Token("RPAREN", line=line, col=col))
            i += 1
            col += 1
            continue
        if ch == ';':
            tokens.append(Token("SEMICOLON", line=line, col=col))
            i += 1
            col += 1
            continue
        if ch == '+':
            tokens.append(Token("PLUS", line=line, col=col))
            i += 1
            col += 1
            continue
        if ch == '-':
            tokens.append(Token("MINUS", line=line, col=col))
            i += 1
            col += 1
            continue
        if ch == '*':
            tokens.append(Token("STAR", line=line, col=col))
            i += 1
            col += 1
            continue
        if ch == '/':
            tokens.append(Token("SLASH", line=line, col=col))
            i += 1
            col += 1
            continue
        if ch == '<':
            tokens.append(Token("LT", line=line, col=col))
            i += 1
            col += 1
            continue
        if ch == '>':
            tokens.append(Token("GT", line=line, col=col))
            i += 1
            col += 1
            continue
        if ch == '=':
            tokens.append(Token("ASSIGN", line=line, col=col))
            i += 1
            col += 1
            continue

        # Числа
        if ch.isdigit():
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
                tokens.append(Token("FLOATCONST", float(num_str), line=line, col=start_col))
            else:
                tokens.append(Token("INTCONST", int(num_str), line=line, col=start_col))
            continue

        # Идентификаторы и ключевые слова
        if ch.isalpha() or ch == '_':
            start_col = col
            ident = ""
            while i < len(source) and (source[i].isalnum() or source[i] == '_'):
                ident += source[i]
                i += 1
                col += 1
            keywords = {
                "int": "INT",
                "double": "DOUBLE",
                "if": "IF",
                "main": "MAIN",
                "return": "RETURN"
            }
            if ident in keywords:
                tokens.append(Token(keywords[ident], line=line, col=start_col))
            else:
                tokens.append(Token("ID", ident, line=line, col=start_col))
            continue

        # Неизвестный символ
        raise ValueError(f"Unexpected character: {ch} at line {line}, col {col}")

    tokens.append(Token("EOF", line=line, col=col))
    return tokens