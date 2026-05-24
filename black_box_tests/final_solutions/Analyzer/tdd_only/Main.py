import TokenParser
import Code2IR
import os


def main() -> int:
    result = 0
    if os.path.exists("input.txt"):
        try:
            token_parser = TokenParser.TokenParser("input.txt")
            tokens = token_parser.parse()
            if token_parser.error_flag:
                result = 1
            else:
                ll1 = Code2IR.LL1(tokens)
                result = ll1.run()
        except:
            result = 1
    else:
        result = 1
    
    with open("Out.txt", "w") as outFile:
        outFile.write(str(result))

    print(result)
    return result

if __name__ == "__main__":
    main()