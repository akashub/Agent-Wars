import pytest
from solution import is_match


def test_single_char_no_star_mismatch():
    # "aa" vs "a": pattern too short, must match entire string
    assert is_match("aa", "a") is False


def test_star_zero_or_more_matches_repeated():
    # "aa" vs "a*": 'a*' matches two a's
    assert is_match("aa", "a*") is True


def test_dot_star_matches_anything():
    # "ab" vs ".*": '.*' is zero-or-more of any char
    assert is_match("ab", ".*") is True


def test_star_preceding_different_char_acts_as_zero():
    # "aab" vs "c*a*b": c* matches empty, a* matches "aa", b matches b
    assert is_match("aab", "c*a*b") is True


def test_star_cannot_skip_required_char():
    # "mississippi" vs "mis*is*p*.": classic trap — p* can't cover the extra 'p'
    assert is_match("mississippi", "mis*is*p*.") is False


def test_empty_string_empty_pattern():
    # both empty: trivially matches
    assert is_match("", "") is True


def test_empty_string_star_pattern():
    # "" vs "a*": a* matches zero a's
    assert is_match("", "a*") is True


def test_nonempty_string_empty_pattern():
    # "a" vs "": nothing to consume 'a'
    assert is_match("a", "") is False


def test_dot_star_then_char_fails():
    # "ab" vs ".*c": .* matches "ab" but no 'c' remains
    assert is_match("ab", ".*c") is False


def test_star_allows_extra_repetition():
    # "aaa" vs "a*a": a* takes "aa", remaining 'a' matches last a
    assert is_match("aaa", "a*a") is True


def test_multi_star_segments():
    # "aaa" vs "ab*a*c*a": b*=0, a*="aa", c*=0, final a matches last a
    assert is_match("aaa", "ab*a*c*a") is True


def test_star_after_char_covers_zero():
    # "a" vs "ab*": b* matches zero b's, leaving just 'a' matched
    assert is_match("a", "ab*") is True
