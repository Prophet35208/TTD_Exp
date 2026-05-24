import Tokens as tok


class TokenParser:
    def __init__(self, path: str):
        self.error_flag = False
        self.error_msg = ""
        self.path = path

    def parse(self) -> list:
        source_code = []
        with open(self.path, "r") as inFile:
            source_code = inFile.readlines()
        source_code = "".join(source_code)
        
        index = 0
        tokens = []
        self.error_flag = False
        while index < len(source_code) and self.error_flag == False:
            if source_code[index:].startswith("/*"):
                comment_finish = source_code[index:].find("*/")
                if comment_finish != -1:
                    index = comment_finish + 2
                else:
                    self.error_flag = True
                    self.error_msg = "Comment is not finished"
            elif source_code[index:].startswith("//"):
                comment_finish = source_code[index:].find("\n")
                index = index + comment_finish + 1 if comment_finish != -1 else len(source_code)
            elif source_code[index] == "\n" or \
                    source_code[index] == "\t" or \
                    source_code[index] == " ":
                index += 1
            elif source_code[index:].startswith("=="):
                tokens.append(tok.TermEquation())
                index += 2
            elif source_code[index:].startswith("!="):
                tokens.append(tok.TermInequality())
                index += 2
            elif source_code[index:].startswith("<="):
                tokens.append(tok.TermLessOrEqual())
                index += 2
            elif source_code[index:].startswith(">="):
                tokens.append(tok.TermGreaterOrEqual())
                index += 2
            elif source_code[index] == "<":
                tokens.append(tok.TermLess())
                index += 1
            elif source_code[index] == ">":
                tokens.append(tok.TermGreater())
                index += 1
            elif source_code[index] == "=":
                tokens.append(tok.TermAssignment())
                index += 1
            elif source_code[index] == "+":
                tokens.append(tok.TermPlus())
                index += 1
            elif source_code[index] == "-":
                tokens.append(tok.TermMinus())
                index += 1
            elif source_code[index] == "*":
                tokens.append(tok.TermAsterisk())
                index += 1
            elif source_code[index] == "/":
                tokens.append(tok.TermSlash())
                index += 1
            elif source_code[index] == "%":
                tokens.append(tok.TermPercent())
                index += 1
            elif source_code[index] == "(":
                tokens.append(tok.TermOpenParenthesis())
                index += 1
            elif source_code[index] == ")":
                tokens.append(tok.TermClosingParenthesis())
                index += 1
            elif source_code[index] == "{":
                tokens.append(tok.TermOpenCurlyBrace())
                index += 1
            elif source_code[index] == "}":
                tokens.append(tok.TermClosingCurlyBrace())
                index += 1
            elif source_code[index] == ";":
                tokens.append(tok.TermSemicolon())
                index += 1
            elif source_code[index] == ",":
                tokens.append(tok.TermComma())
                index += 1
            elif source_code[index].isalpha() or source_code[index] == "_":
                figure = ""
                while   index < len(source_code) and \
                        (source_code[index].isalpha() or \
                         source_code[index] == "_" or \
                        source_code[index].isdigit()):
                    figure += source_code[index]
                    index += 1
                if figure == "main":
                    tokens.append(tok.TermMain())
                elif figure == "return":
                    tokens.append(tok.TermReturn())
                elif figure == "if":
                    tokens.append(tok.TermIf())
                elif figure == "int":
                    tokens.append(tok.TermInt())
                elif figure == "double":
                    tokens.append(tok.TermDouble())
                else:
                    tokens.append(tok.TermId(figure))
            elif source_code[index].isdigit():
                figure = ""
                is_real = False
                while index < len(source_code) and source_code[index].isdigit():
                    figure += source_code[index]
                    index += 1
                
                if index < len(source_code) and (source_code[index] == "."):
                    is_real = True
                    figure += source_code[index]
                    index += 1
                    while index < len(source_code) and source_code[index].isdigit():
                        figure += source_code[index]
                        index += 1
                if index < len(source_code) and (source_code[index] == "e" or source_code[index] == "E"):
                    is_real = True
                    figure += source_code[index]
                    index += 1
                    if index < len(source_code) and (source_code[index] == "+" or source_code[index] == "-"):
                        figure += source_code[index]
                        index += 1
                    if index < len(source_code) and source_code[index].isdigit():
                        while index < len(source_code) and source_code[index].isdigit():
                            figure += source_code[index]
                            index += 1
                    else:
                        self.error_flag = True
                        self.error_msg = "Expected at least one digit after exponent"
                
                if is_real:
                    tokens.append(tok.TermRealLiteral(figure))
                else:
                    tokens.append(tok.TermIntLiteral(figure))
            elif source_code[index] == ".":
                figure = "."
                index += 1
                if index < len(source_code) and source_code[index].isdigit():
                    while index < len(source_code) and source_code[index].isdigit():
                        figure += source_code[index]
                        index += 1
                else:
                    self.error_flag = True
                    self.error_msg = "Expected at least one digit after '.'"

                if index < len(source_code) and (source_code[index] == "e" or source_code[index] == "E"):
                    is_real = True
                    figure += source_code[index]
                    index += 1
                    if index < len(source_code) and (source_code[index] == "+" or source_code[index] == "-"):
                        figure += source_code[index]
                        index += 1
                    if index < len(source_code) and source_code[index].isdigit():
                        while index < len(source_code) and source_code[index].isdigit():
                            figure += source_code[index]
                            index += 1
                    else:
                        self.error_flag = True
                        self.error_msg = "Expected at least one digit after exponent"
                tokens.append(tok.TermRealLiteral(figure))
            else:
                self.error_flag = True
                self.error_msg = "Unknown symbol '" + source_code[index] + "'"
                index += 1
        
        return tokens
