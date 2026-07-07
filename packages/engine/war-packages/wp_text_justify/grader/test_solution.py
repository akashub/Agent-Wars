import pytest
from solution import full_justify


def test_example1_basic():
    words = ["This", "is", "an", "example", "of", "text", "justification."]
    result = full_justify(words, 16)
    assert result == ["This    is    an", "example  of text", "justification.  "]


def test_example1_line_widths():
    words = ["This", "is", "an", "example", "of", "text", "justification."]
    for line in full_justify(words, 16):
        assert len(line) == 16


def test_example2_single_word_and_last_line_left_justified():
    # "acknowledgment" is a single word on its line; "shall be" is the last line
    words = ["What", "must", "be", "acknowledgment", "shall", "be"]
    result = full_justify(words, 16)
    assert result == ["What   must   be", "acknowledgment  ", "shall be        "]


def test_example2_line_widths():
    words = ["What", "must", "be", "acknowledgment", "shall", "be"]
    for line in full_justify(words, 16):
        assert len(line) == 16


def test_example3_science():
    words = [
        "Science", "is", "what", "we", "understand", "well", "enough", "to",
        "explain", "to", "a", "computer.", "Art", "is", "everything", "else",
        "we", "do",
    ]
    result = full_justify(words, 20)
    expected = [
        "Science  is  what we",
        "understand      well",
        "enough to explain to",
        "a  computer.  Art is",
        "everything  else  we",
        "do                  ",
    ]
    assert result == expected


def test_example3_line_widths():
    words = [
        "Science", "is", "what", "we", "understand", "well", "enough", "to",
        "explain", "to", "a", "computer.", "Art", "is", "everything", "else",
        "we", "do",
    ]
    for line in full_justify(words, 20):
        assert len(line) == 20


def test_single_word_exactly_fills_width():
    # "hello" at width 5: no padding needed
    assert full_justify(["hello"], 5) == ["hello"]


def test_single_short_word_padded():
    # single word shorter than width: left-justify with trailing spaces
    result = full_justify(["a"], 4)
    assert result == ["a   "]
    assert len(result[0]) == 4


def test_two_words_last_line_left_justified():
    # two words on one line which is also the last line: single space, pad right
    result = full_justify(["ab", "cd"], 10)
    assert result == ["ab cd     "]
    assert len(result[0]) == 10


def test_all_lines_exactly_max_width():
    # paranoia check across all three LeetCode examples combined
    cases = [
        (["This", "is", "an", "example", "of", "text", "justification."], 16),
        (["What", "must", "be", "acknowledgment", "shall", "be"], 16),
        (
            ["Science", "is", "what", "we", "understand", "well", "enough", "to",
             "explain", "to", "a", "computer.", "Art", "is", "everything", "else",
             "we", "do"],
            20,
        ),
    ]
    for words, width in cases:
        for line in full_justify(words, width):
            assert len(line) == width, f"line {line!r} has len {len(line)}, expected {width}"


def test_spaces_distributed_left_heavy():
    # width=10, words=['ab','cde','fg','hi']
    # Line 1 (not last): 'ab','cde','fg' -> 7 chars, 3 spaces over 2 gaps
    #   base=1, extra=1 -> gaps get 2 then 1 -> "ab  cde fg"
    # Line 2 (last): 'hi' -> left-justified + pad -> "hi        "
    result = full_justify(["ab", "cde", "fg", "hi"], 10)
    assert result[0] == "ab  cde fg"
    assert result[1] == "hi        "
    for line in result:
        assert len(line) == 10
