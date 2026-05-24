import Main
import os

def check_result_if_correct_input(input: str, expected_output: str):
    with open("In.txt", "w") as file:
        file.write(input)
    if os.path.exists('Out.txt'):
        os.remove('Out.txt')

    result = Main.main()

    assert result == 0, 'main() has returned the non-zero result: ' + str(result)
    assert os.path.exists("Out.txt"), "Out.txt doesn't exist"
    with open("Out.txt", "r") as file:
        calc_result = file.readlines()
        assert len(calc_result) > 0, 'Out.txt is empty'
        assert len(calc_result) < 2, 'Out.txt contains extra rows'
        calc_result = calc_result[0]
        assert calc_result == expected_output, 'Out.txt contains the wrong result: ' + calc_result

### Prefix ###

def test_prefix_add():
    check_result_if_correct_input("prefix\n+ 1 2", "3")

def test_prefix_add_2():
    check_result_if_correct_input("prefix\n+ 1.25 3.5", "4.75")

def test_prefix_add_3():
    check_result_if_correct_input("prefix\n+ 1.00 0.005", "1")

def test_prefix_sub():
    check_result_if_correct_input("prefix\n- 1 2", "-1")

def test_prefix_sub_2():
    check_result_if_correct_input("prefix\n- 1.25 3.5", "-2.25")

def test_prefix_mult():
    check_result_if_correct_input("prefix\n* 3 4", "12")

def test_prefix_mult_2():
    check_result_if_correct_input("prefix\n* 1.25 3.5", "4.38")

def test_prefix_div():
    check_result_if_correct_input("prefix\n/ 12 4", "3")

def test_prefix_div_2():
    check_result_if_correct_input("prefix\n/ 12.5 0.5", "25")

def test_prefix_div_rem():
    check_result_if_correct_input("prefix\n% 3 4", "3")

def test_prefix_abs():
    check_result_if_correct_input("prefix\nabs -4", "4")

def test_prefix_sqrt():
    check_result_if_correct_input("prefix\nsqrt 25", "5")

def test_prefix_pow():
    check_result_if_correct_input("prefix\n^ 3 4", "81")

### Postfix ###

def test_postfix_add():
    check_result_if_correct_input("postfix\n1 2 +", "3")

def test_postfix_sub():
    check_result_if_correct_input("postfix\n1 2 -", "-1")

def test_postfix_mult():
    check_result_if_correct_input("postfix\n3 4 *", "12")

def test_postfix_div():
    check_result_if_correct_input("postfix\n12 4 /", "3")

def test_postfix_div_rem():
    check_result_if_correct_input("postfix\n3 4 %", "3")

def test_postfix_abs():
    check_result_if_correct_input("postfix\n-4 abs", "4")

def test_postfix_sqrt():
    check_result_if_correct_input("postfix\n25 sqrt", "5")

def test_postfix_pow():
    check_result_if_correct_input("postfix\n3 4 ^", "81")
