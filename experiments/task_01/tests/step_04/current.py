import os
from solution import main

def test_main_postfix():
    with open("In.txt", "w") as f:
        f.write("postfix\n3 4 +")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "7"

def test_main_prefix():
    with open("In.txt", "w") as f:
        f.write("prefix\n+ 1 2")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 0
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "3"

def test_main_error_div_zero():
    with open("In.txt", "w") as f:
        f.write("postfix\n5 0 /")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 1
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "Error"

def test_main_error_sqrt_neg():
    with open("In.txt", "w") as f:
        f.write("postfix\n-4 sqrt")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 1
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "Error"

def test_main_no_file():
    if os.path.exists("In.txt"):
        os.remove("In.txt")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 1
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "Error"

def test_main_empty_file():
    with open("In.txt", "w") as f:
        f.write("")
    if os.path.exists("Out.txt"):
        os.remove("Out.txt")
    result = main()
    assert result == 1
    with open("Out.txt", "r") as f:
        assert f.read().strip() == "Error"