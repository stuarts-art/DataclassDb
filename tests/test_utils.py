from enum import Enum, StrEnum

from dataclassdb.utils import is_enum_class, is_strenum, table_exists


def test_table_exists(db_mem_connection):
    assert table_exists(db_mem_connection, "testing")
    assert not table_exists(db_mem_connection, "missing")


class EnumClass(Enum):
    a = 1


class StrEnumClass(StrEnum):
    a = "a"


def test_is_enum(db_mem_connection):
    # assert table_exists(db_mem_connection, "testing")
    # assert not table_exists(db_mem_connection, "missing")
    assert is_enum_class(EnumClass)
    assert is_enum_class(StrEnumClass)

    assert not is_strenum(EnumClass)
    assert is_strenum(StrEnumClass)

    for t in [str, int, list, dict, list[str]]:
        assert not is_enum_class(t)
        assert not is_strenum(t)
