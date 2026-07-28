from dataclasses import dataclass, field
from typing import Annotated

from dataclassdb.dataclass_db import DataclassDb


@dataclass
class Example_Dataclass:
    id: Annotated[int, "PRIMARY KEY"]
    username: Annotated[str, "UNIQUE"]
    score: int = 0
    tags: Annotated[list, "TEXT"] = field(default_factory=list)
    connections: Annotated[dict, "BLOB"] = field(default_factory=dict)
    extras: list[str] | None = None

def test_CRUD(db_mem_connection):
    with DataclassDb(Example_Dataclass, db_mem_connection) as db:
        assert 0 not in db
        assert db.get_current_table_query()

        test_obj = Example_Dataclass(0, "stuart", tags=["a", "b"], connections={"a": 1})
        db.insert(test_obj)
        assert 0 in db

        assert db.get(0) == test_obj
        assert db.get([0]) == test_obj
        assert db.get((0)) == test_obj
        assert db.dataclass_sql_cols()
        db.delete(0)
        assert 0 not in db

        test_obj.id = 1
        test_obj.username = "user1"
        db[1] = test_obj

def test_delete_multiple(db_mem_connection):
    with DataclassDb(Example_Dataclass, db_mem_connection) as db:
        for i in range(10):
            db.insert(Example_Dataclass(i, f"user_{i}", 1 if i % 2 == 0 else 2))
        
        for i in range(10):
            assert i in db
        assert len(db) == 10
        assert db.length() == 10
        
        db.delete(score = 1)
        assert len(db) == 5
        assert db.length() == 5


def test_empty_len(db_mem_connection):
    with DataclassDb(Example_Dataclass, db_mem_connection) as db:
        db.select_query = lambda *args, **kwargs: None
        assert len(db) == 0