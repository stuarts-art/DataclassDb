from typing import Annotated

import pytest
from dataclasses import dataclass

from dataclassdb.dataclass_db import DataclassDb



@dataclass
class No_Constraints:
    id: int
    name: str

@dataclass
class Multiple_Unique:
    id: int
    first_name: Annotated[str, "UNIQUE"]
    last_name: Annotated[str, "UNIQUE"]

@dataclass
class Multiple_Primary:
    id: Annotated[int, "PRIMARY KEY"]
    region: Annotated[str, "PRIMARY KEY"]
    name: str
    # first_name: Annotated[str, "UNIQUE"]
    # last_name: Annotated[str, "UNIQUE"]

@dataclass
class Multiple_Primary_and_Unique:
    id: Annotated[int, "PRIMARY KEY"]
    region: Annotated[str, "PRIMARY KEY"]
    first_name: Annotated[str, "UNIQUE"]
    last_name: Annotated[str, "UNIQUE"]

@pytest.mark.parametrize(
    "data_class, field_count", 
    [
        (No_Constraints, 2),
        (Multiple_Unique, 4),
        (Multiple_Primary, 4),
        (Multiple_Primary_and_Unique, 6),
    ],
)
def test_no_constraints(data_class, field_count, db_mem_connection):
    with DataclassDb(data_class, db_mem_connection) as db:
        assert len(db.get_curr_cols(db.data_class)) == field_count
        assert len(db.dataclass_sql_cols()) == field_count

        assert db.get_curr_cols(db.data_class) == db.dataclass_sql_cols()


    






