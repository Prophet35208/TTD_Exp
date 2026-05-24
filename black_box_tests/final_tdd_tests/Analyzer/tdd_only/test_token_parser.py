import TokenParser as Pars
import Tokens as tok

def check_tokens(expected, actual):
    assert len(expected) == len(actual), "Parsed terminal count doesn't equal expected terminal count"
    for i in range(len(expected)):
        assert isinstance(actual[i], expected[i]), "Expected token " + str(expected[i]) + "; actual " + str(type(actual[i]))

def test_all_kind_tokens():
    with open("input.txt", "w") as inFile:
        lines = ["int double,if= \n",
                 "}{)(//(\n", 
                 ";123 12. 2.5abc main  +-*%/return\n", 
                 "< = <= > = >= = = == !=\n"]
        inFile.writelines(lines)
    
    parser = Pars.TokenParser("input.txt")
    tokens = parser.parse()
    assert parser.error_flag == False
    expected_tokens = [tok.TermInt, tok.TermDouble, tok.TermComma, tok.TermIf, tok.TermAssignment,
                       tok.TermClosingCurlyBrace, tok.TermOpenCurlyBrace, tok.TermClosingParenthesis, tok.TermOpenParenthesis,
                       tok.TermSemicolon, tok.TermIntLiteral, tok.TermRealLiteral, tok.TermRealLiteral, tok.TermId, tok.TermMain, tok.TermPlus, tok.TermMinus, tok.TermAsterisk, tok.TermPercent, tok.TermSlash, tok.TermReturn,
                       tok.TermLess, tok.TermAssignment, tok.TermLessOrEqual, tok.TermGreater, tok.TermAssignment, tok.TermGreaterOrEqual, tok.TermAssignment, tok.TermAssignment, tok.TermEquation, tok.TermInequality]
    check_tokens(expected_tokens, tokens)
