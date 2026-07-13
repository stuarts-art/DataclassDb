from typing import Annotated

from dataclassdb import DataclassDb
from dataclassdb.constants import SQL
from dataclasses import dataclass

@dataclass
class SmokeTestClass:
    id: Annotated[int, SQL.PRIMARY_KEY]
    name: str = ""
    count: int = 0

obj = SmokeTestClass(0, "smoke test obj", 1)

with DataclassDb(SmokeTestClass, ":memory:") as db:
    assert db.get(0) is None
    db.insert(obj)

    gotten_obj = db.get(0)
    assert gotten_obj == obj
