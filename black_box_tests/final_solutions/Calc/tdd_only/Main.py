import PostfixCalculation
import PrefixCalculation
import os

def main() -> int:
    with open("Out.txt", "w") as outFile:
        if not os.path.exists("In.txt"):
            outFile.write("Error\n")
            return 1
        with open("In.txt", "r") as inFile:
            task = inFile.readline()
            expr = inFile.readline()
            result = None
            if task == "prefix\n":
                result = PrefixCalculation.PrefixCalculation(expr)
            elif task == "postfix\n":
                result = PostfixCalculation.PostfixCalculation(expr)
            else:
                outFile.write("Error\n")
                return 1
            
            if result is not None:
                if isinstance(result, int):
                    result = str(result)
                elif round(result, 2).is_integer():
                    result = str(int(round(result, 2)))
                else:
                    result = str("{:.2f}".format(result))

                outFile.write(result)
            else:
                outFile.write("Error\n")
                return 1
    return 0

if __name__ == "__main__":
    main()