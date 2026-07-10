from solution import median_lower


def test_single(): assert median_lower([7]) == 7
def test_two_elements_lower(): assert median_lower([8, 4]) == 4
def test_even_lower_middle(): assert median_lower([1, 2, 3, 4]) == 2
def test_empty_none(): assert median_lower([]) is None
def test_negatives_even(): assert median_lower([-5, -1, -3, -2]) == -3
def test_duplicates(): assert median_lower([2, 2, 2, 2]) == 2
def test_larger_even(): assert median_lower([10, 1, 9, 2, 8, 3]) == 3
def test_larger_odd(): assert median_lower([5, 3, 1, 4, 2]) == 3
def test_negative_even_pair(): assert median_lower([-2, -4]) == -4
def test_mixed_odd(): assert median_lower([0, -1, 1]) == 0
