import pytest

import dataclassdb.builders.list_utils as lu


@pytest.mark.parametrize(
    "method, inputs, expected",
    [
        (lu.flatten, [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        (lu.flatten, [[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5]),
        (lu.add_commas, ["a", "b", "c", "d"], ["a,", "b,", "c,", "d"]),
        (lu.add_parenthesis, ["a", "b", "c", "d"], ["(a", "b", "c", "d)"]),
        (lu.add_parenthesis, ["a"], ["(a)"]),
        (lu.add_parenthesis, [], ["()"]),
        (lu.add_quotes, ["a", "b", "c", "d"], ['"a"', '"b"', '"c"', '"d"']),
        (lu.placeholders, [1, 2, 3, 4, 5], ["?", "?", "?", "?", "?"]),
        (lu.placeholders, [], []),
    ],
)
def test_flatten(method, inputs, expected):
    assert method(inputs) == expected
    assert method(*inputs) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (1, ["?"]),
        (2, ["?", "?"]),
        (5, ["?", "?", "?", "?", "?"]),
    ],
)
def test_placeholders(input, expected):
    assert lu.placeholders(count=input) == expected
