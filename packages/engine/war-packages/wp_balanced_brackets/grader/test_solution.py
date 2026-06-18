import pytest
from solution import is_balanced


def test_empty_string_is_balanced():
    assert is_balanced("") is True


def test_single_pair_parens():
    assert is_balanced("()") is True


def test_nested_mixed_brackets():
    assert is_balanced("([{}])") is True


def test_mismatched_close():
    assert is_balanced("(]") is False


def test_wrong_nesting_order():
    assert is_balanced("([)]") is False


def test_unclosed_opens():
    assert is_balanced("(((") is False


def test_close_before_open():
    assert is_balanced(")(") is False


def test_non_bracket_chars_ignored():
    assert is_balanced("a(b)c[d]{e}") is True


def test_deeply_nested():
    assert is_balanced("{[()]}") is True


def test_unmatched_close_brace():
    assert is_balanced("}") is False
