import logging
import sqlite3
from dataclasses import dataclass
from enum import Enum, StrEnum
from typing import Any, ClassVar

import dacite

logger = logging.getLogger()


class UpperStrEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[Any]
    ) -> Any:
        return name.upper().replace("_", " ")


def table_exists(connection: sqlite3.Connection, table_name):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_schema WHERE type='table' AND name=?",
        (table_name,),
    )
    result = cursor.fetchone()
    return result is not None


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    row_dict = {}
    for key, value in zip(fields, row):
        row_dict[key] = value
    return row_dict


def is_enum_class(cls):
    try:
        return issubclass(cls, Enum)
    except Exception:
        return False


def is_strenum(cls):
    try:
        return issubclass(cls, Enum) and issubclass(cls, str)
    except Exception:
        return False


@dataclass
class PragmaTableInfo:
    cid: int
    name: str | None
    type: str | None
    notnull: bool | None
    dflt_value: Any
    pk: bool | None

    _config: ClassVar[dacite.Config] = dacite.Config(
        type_hooks={
            bool: lambda x: bool(x),
        }
    )

    @classmethod
    def from_dict(cls, data) -> "PragmaTableInfo":
        return dacite.from_dict(cls, data, cls._config)

    @classmethod
    def from_list(cls, data) -> list["PragmaTableInfo"]:
        cols = [cls.from_dict(col) for col in data]
        return cols
