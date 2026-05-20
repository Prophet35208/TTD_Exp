"""
Step 01: Сложение и вычитание в постфиксной и префиксной нотации.
"""

import sys
import os
from pathlib import Path

# Добавляем путь к solution.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from solution import calculate


# ============================================================
# Тесты: Постфиксная нотация (сложение)
# ============================================================

def test_postfix_addition_simple():
    assert calculate("postfix", "3 4 +") == 7


def test_postfix_addition_commutative():
    assert calculate("postfix", "5 7 +") == 12
    assert calculate("postfix", "7 5 +") == 12


def test_postfix_addition_with_zero():
    assert calculate("postfix", "42 0 +") == 42


def test_postfix_addition_negative():
    assert calculate("postfix", "-3 7 +") == 4


# ============================================================
# Тесты: Постфиксная нотация (вычитание)
# ============================================================

def test_postfix_subtraction_simple():
    assert calculate("postfix", "10 3 -") == 7


def test_postfix_subtraction_non_commutative():
    assert calculate("postfix", "10 3 -") == 7
    assert calculate("postfix", "3 10 -") == -7


def test_postfix_subtraction_zero():
    assert calculate("postfix", "15 0 -") == 15


def test_postfix_subtraction_negative_result():
    assert calculate("postfix", "3 7 -") == -4


# ============================================================
# Тесты: Префиксная нотация (сложение)
# ============================================================

def test_prefix_addition_simple():
    assert calculate("prefix", "+ 3 4") == 7


def test_prefix_addition_commutative():
    assert calculate("prefix", "+ 5 7") == 12
    assert calculate("prefix", "+ 7 5") == 12


def test_prefix_addition_with_zero():
    assert calculate("prefix", "+ 42 0") == 42


# ============================================================
# Тесты: Префиксная нотация (вычитание)
# ============================================================

def test_prefix_subtraction_simple():
    assert calculate("prefix", "- 10 3") == 7


def test_prefix_subtraction_non_commutative():
    assert calculate("prefix", "- 10 3") == 7
    assert calculate("prefix", "- 3 10") == -7


def test_prefix_subtraction_negative_result():
    assert calculate("prefix", "- 3 7") == -4