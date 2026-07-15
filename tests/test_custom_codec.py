from dataclasses import dataclass
from typing import Annotated

from dataclassdb.dataclass_db import DataclassDb
from dataclassdb.dataclass_types import CustomCodec


codec = CustomCodec(encode=lambda x: x + 1000, decode=lambda x: x - 1000)


@dataclass
class Example:
    id: Annotated[int | None, "PRIMARY KEY"]
    username: Annotated[str, "UNIQUE"]
    score: Annotated[int, codec] = 0


def test_auto_increment(db_mem_connection):
    with DataclassDb(Example, db_mem_connection) as db:
        for i in range(1, 20):
            assert i not in db
            user = f"user {i}"
            obj = Example(None, user, i)
            db.insert(obj)
            assert i in db
            retrieved = db.get(i)
            assert retrieved.score == obj.score
            assert retrieved.username == obj.username
