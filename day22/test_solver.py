import pytest
from solver import parse, solve1, solve2

TESTDATA = """
1
10
100
2024
"""

TESTDATA2 = """
1
2
3
2024
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    assert solution == 37327623


# PART 2
def test_solve2():
    solution = solve2(parse(TESTDATA2))
    assert solution == 23
