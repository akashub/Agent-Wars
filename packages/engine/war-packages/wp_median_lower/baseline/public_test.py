from solution import median_lower


def test_even_returns_lower_middle_not_average():
    assert median_lower([1, 2, 3, 4]) == 2      # lower of (2,3); NOT 2.5


def test_odd_unsorted():
    assert median_lower([3, 1, 2]) == 2


def test_empty_returns_none():
    assert median_lower([]) is None
