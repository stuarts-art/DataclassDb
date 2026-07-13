import logging
from dataclasses import dataclass, field
from typing import Annotated

from dataclassdb import DataclassDb

logger = logging.getLogger(__name__)


def main():

    logging.basicConfig(level=logging.INFO)
    with DataclassDb(User, "main.db") as db:
        users = {}
        for i in range(10):
            user = User(
                id=i,
                username=f"Test name {i}",
                data=[1, 2, 3, 4, i],
                items=["a", "b", "C", "D", str(i)],
            )
            users[i] = user
            inserted = db.insert(user)
            if inserted:
                logger.info("User %s was inserted", *inserted)
        # file is closed by the context manager.

    with DataclassDb(User, "main.db") as db:
        for i in range(10):
            user = db.get(i)  # Get using the primary key
            assert user == users[i]


@dataclass
class User:
    """Generated create query for the User class:
    ```
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        data BLOB NOT NULL,
        items TEXT NOT NULL DEFAULT '[]'
    );
    ```

    Note that `data` is being encoded and decoded as a pickle "BLOB",
    while `items` is being encoded and decoded as json list strings.
    """

    id: Annotated[int | None, "PRIMARY KEY"]
    username: Annotated[str, "UNIQUE"]
    data: Annotated[list[int], "BLOB"] = field(default_factory=list)
    items: list[str] = field(default_factory=list)


if __name__ == "__main__":
    main()
