from dataclasses import dataclass

import pytest

from dataclassdb.builders.string_builder import StringBuilder


@pytest.mark.parametrize(
    "inputs, expected, kwargs",
    [
        ([], "", {}),
        (["a", "b", "c"], "a, b, c", {"commas": True}),
        (["a", "b", "c"], "a b c", {"commas": False}),
        (["a", "b", "c"], "(a, b, c)", {"par": True}),
        (["a", "b", "c"], '"a", "b", "c"', {"quotes": True}),
        (["a", "b", "c"], "\na, b, c", {"newline": True}),
        (["a", "b", "c"], "\na, b, c", {"newline": True, "random": True}),
    ],
)
def test_add(inputs, expected, kwargs):
    builder = StringBuilder()
    builder.add(*inputs, **kwargs)
    assert str(builder) == expected
    builder.clear
    builder(*inputs, **kwargs)
    assert str(builder) == expected


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (("test", 1, 2, 3), "test(1, 2, 3)"),
        (("print", "hello world"), "print(hello world)"),
        (("print",), "print()"),
    ],
)
def test_add_func(inputs, expected):
    builder = StringBuilder()
    builder.add_func(*inputs)
    assert str(builder) == expected


def test_string_builder_call():
    builder = StringBuilder()("Test words")
    assert str(builder) == "Test words"

    builder.clear
    assert str(builder) == ""

    assert str(builder("a", "b", "c")) == "a, b, c"
    builder.clear

    assert str(builder("a", "b", "c", commas=False)) == "a b c"
    builder.clear

    builder()
    assert str(builder) == ""

    assert str(builder("a").br("c", "d")) == "a \nc, d"
    builder.clear

    @dataclass
    class TestDataclass1:
        id: str

    assert str(builder(TestDataclass1)) == "TestDataclass1"
    builder.clear

    assert str(builder(None)) == ""

    builder.clear

    builder = StringBuilder().set_sep("")
    assert str(builder("a", "b", "c", commas=False)) == "abc"

    with pytest.raises(ValueError):
        builder.add_func()

    builder.clear
    builder.add("Hello World", newline=True)
    builder.clear
    builder.add(newline=True)


def test_show(capsys):
    capsys.readouterr()
    StringBuilder()("Test words").show
    assert capsys.readouterr().out == "Test words\n"
