import pytest
from solution import roman_to_int


def test_single_i():
    assert roman_to_int("I") == 1


def test_repeated_i():
    assert roman_to_int("III") == 3


def test_subtractive_iv():
    assert roman_to_int("IV") == 4


def test_subtractive_ix():
    assert roman_to_int("IX") == 9


def test_mixed_lviii():
    assert roman_to_int("LVIII") == 58


def test_subtractive_xl():
    assert roman_to_int("XL") == 40


def test_subtractive_xc():
    assert roman_to_int("XC") == 90


def test_subtractive_cd():
    assert roman_to_int("CD") == 400


def test_subtractive_cm():
    assert roman_to_int("CM") == 900


def test_compound_mcmxciv():
    assert roman_to_int("MCMXCIV") == 1994


def test_max_value():
    assert roman_to_int("MMMCMXCIX") == 3999
