from enum import Enum, StrEnum
from typing import Annotated

from dataclassdb.utils import (
    get_absolute_origin,
    is_enum_class,
    is_strenum,
    table_exists,
)


class EnumClass(Enum):
    a = 1


class StrEnumClass(StrEnum):
    a = "a"


def test_table_exists(db_mem_connection):
    assert table_exists(db_mem_connection, "testing")
    assert not table_exists(db_mem_connection, "missing")


def test_is_enum(db_mem_connection):
    assert is_enum_class(EnumClass)
    assert is_enum_class(StrEnumClass)

    assert not is_strenum(EnumClass)
    assert is_strenum(StrEnumClass)

    for t in [str, int, list, dict, list[str]]:
        assert not is_enum_class(t)
        assert not is_strenum(t)


def test_get_absolute_origin():
    assert get_absolute_origin(list[str]) is list
    assert get_absolute_origin(list[str] | None) is list
    assert get_absolute_origin(Annotated[list[str], "str"]) is list
    assert get_absolute_origin(Annotated[list[str] | None, "str"]) is list
