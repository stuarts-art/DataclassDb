from dataclasses import dataclass

import pytest

from dataclassdb.dataclass_db import DataclassDb

@dataclass
class NoPrimary:
    name: str
    height: int
    weight: int


def test_no_primary(db_mem_connection):
    with DataclassDb(NoPrimary, db_mem_connection) as db:
        # db.get(row_id)
        
        for i in range(10):
            obj = NoPrimary("test", i, i)
            row_id = db.insert(obj)[0]
            assert row_id == i + 1

            assert db.peek(row_id) == obj
            assert db.peek() == obj
            print(db.peek())

        with pytest.raises(ValueError):
            db.peek(as_dict=True, as_tuple=True)
        with pytest.raises(ValueError):
            db.peek(select_fields=["name"])

        assert db.peek(select_fields=["name"], as_dict=True) == {"name": "test"}
        assert db.peek(select_fields=["name"], as_tuple=True) == ("test",)
        # assert db.peek() == 
        assert db.peek() == db.get(None)
        for i in range(1,9):
            assert db.peek(i) == db.get(i)




