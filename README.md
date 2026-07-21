# dataclassdb [BETA]

![](https://img.shields.io/pypi/pyversions/dataclassdb.svg)
![](https://img.shields.io/pypi/v/dataclassdb)
[![Downloads](https://pepy.tech/badge/dataclassdb)](https://pepy.tech/project/dataclassdb)
![](https://readthedocs.org/projects/dataclassdb/badge/?version=latest)
![](https://img.shields.io/github/license/stuarts-art/dataclassdb.svg)

This module provides a lightweight sqlite3 ORM for dataclasses.

## Installation

To install dataclassdb, simply use 'pip:

```zsh
pip install dataclassdb
```

## Requirements

Minimum Python version supported by `dataclassdb` is 3.11. The only dependency is [dacite](https://github.com/konradhalas/dacite).

## Quick Start

```python
from dataclassdb import DataclassDb
from types import Annotated
from dataclasses import dataclass, Annotated

@dataclass
class Foo:
    id: Annotated[int, "PRIMARY KEY"]
    bar: str
    baz: list[int]

with DataclassDb(Foo, "example.db") as db:
    # Insert and get
    db.insert(Foo(0, "x", [1, 2, 3]))
    foo = db.get(0)

    # Arbitrary SQL
    db.SELECT("bar").FROM(FOO).WHERE("id").eq("?")
    selection = db.execute_one(0) # Replaces ? with 0
```

## Overview

- Uses `@dataclass` classes to generate and interact with database files using `sqlite3`. No "Model" super class required.
- SQL table columns are inferred by the dataclass field annotation.
- Codecs(Encoder/Decoder) translate Python to SQL and back.
- Build in [QueryBuilder](src/dataclassdb/builders/query_builder.py) with every SQL statement and function for easy query writing
- Built in [DbEngine](src/dataclassdb/db_engine.py) context manager for managing the db connection, creating tables, and executing queries.

## Deeper Dive

- Each `@dataclass` fields' SQL type is inferred by the python type or by override. By default, undefined mapping are set to "TEXT".
- A Codec (Encoder/Decoder) is used to translate between python and SQL. The following are supported:
  - **Basic Types**: `int`, `str`, `float`, `bool`
  - **Enums**: `Enum`, `StrEnum`
  - **Dates**: `datetime -> INTEGER (unix time)`, `datetime -> TEXT (ISO 8601)`
  - **Json**: `list`, `dict`, `@dataclass` (If all elements are json encodable)
  - **Pickle (Bytes)**: Any `python` object. Notably `set`s are not json encodable. Pickle is not safe and should be used with caution**.
  - Any user defined [Codec](src/dataclassdb/dataclass_types.py#8)
- [Constraints](https://www.sqlite.org/syntax/column-constraint.html)
such as `PRIMARY KEY` or `UNIQUE` can be added as `typing.Annotated` metadata without affecting the base type.
- Dataclass field defaults are encoded
- "NOT NULL" field status is inferred by the

Column type is inferred by the python type and SQL type.

- The column type is inferred by the python type but can be overridden as the first annotation.
- This package does not attempt to abstract away SQL behavior. It's simply a lightweight wrapper around sqlite3.

## Motivation

### 1. Easier to write than plaintext

- All sqlite [keywords](src/dataclassdb/sql_statement_builder.py) and [functions](src/dataclassdb/sql_function_builder.py) are supported
- Queries can be written written without filler words.
- Lists and args are handled how you'd expect them to be handled.

### 2. Easier to write than [SqlAlchemy](https://docs.sqlalchemy.org/), [SqlModel](https://sqlmodel.tiangolo.com/features/#editor-support), and other more complex abstractions

- No required imports [QueryBuilder](src/dataclassdb/query_builder.py)
- Minimal package specific syntax or abstractions to learn

### 3. Abstracts away Non-SQL, `sqlite3`, actions

- Creating connection
- Executing the query
- Returning the result as a list or dictionary

## Features

- [DataclassDb](#dataclassdb): Maps dataclass class into a sqlite3 table.
- [QueryBuilder](#query-builder): Specialized StringBuilder with methods for each sqlite3 [keywords](src/dataclassdb/sql_statement_builder.py) and [functions](src/dataclassdb/sql_function_builder.py). Note that DataclassDb inherits from QueryBuilder.
- [DbEngine](src/dataclassdb/db_engine.py):
- [Codec](src/dataclassdb/dataclass_types.py#5): Protocol
  - [CustomCodec](src/dataclassdb/dataclass_types.py#12)

## DataclassDb

### Column Definition

```python
col_name: Annotated(Type, ? [SQL Type], *[Constraints], [Codec])
```

- Type: The python type for the dataclass field
- SQL Type: Override the default mapped SQL type (see next section)
- Constraints: SQL constraints as text
- Codec: Overrides the default codec. Any object that is a [Codec](src/dataclassdb/dataclass_types.py#5) (has an encode and decode method)

Examples:

| Python Field | Sqlite Col Definition |
| --- | --- |
| `id: Annotated[int, "PRIMARY KEY"]` | `id INTEGER PRIMARY KEY NOT NULL` |
| `username: Annotated[str, "UNIQUE"]` | `username TEXT UNIQUE NOT NULL` |
| `email: str = ""` | `email TEXT NOT NULL DEFAULT ""` |

### Python type to SQL type resolution

Because sqlite has a limited amount of supported types: (INTEGER, TEXT, REAL, NUMERICAL, BLOB), we must map between python types and SQL types.

The "easiest" way to do this is by converting our python object into binary using pickle and storing it as a BLOB. However, there are a few issues with this approach.

1. Pickle is unsafe (bad actors can run arbitrary code on decode.)
2. This data cannot be read without decoding.
3. This data cannot be used in queries without decoding.

This package approaches this issue by using Codecs (Encoder/Decoder) to handle the python -> sqlite -> python conversions.
If no SQL type is declared in the Annotated column definition, first checks the below mapping.

If no mapping is found, the column is assumed to be json encodable. This setting can be overridden by either providing a custom Codec or setting the type to "BLOB".

| SQL Type | python type | Codec |
| --- | --- | --- |
| TEXT | datetime | DatetimeTextCodec |
| TEXT | str | IdentityCodec |
| TEXT | default | JsonCodec |
| INTEGER | datetime | DatetimeIntCodec |
| INTEGER | bool | BoolCodec |
| INTEGER | int | IdentityCodec |
| REAL | float | IdentityCodec |
| BLOB | @dataclass | DataclassPickleCodec |
| BLOB | default | PickleCodec |

## Query Builder

```python
qb = QueryBuilder()            # str(qb)
qb.SELECT                      # = SELECT
qb("a", "b").Group_concat("c") # = SELECT a b group_concat(c)
```

- All SQL statement keywords, such as `SELECT`, `FROM`, etc. are available as **chainable** properties of Query builders `query.SELECT` or as standalone variables `db.SELECT`. See [StatementBuilder](src/dataclassdb/statement_builder.py) or [SQL enum](src/dataclassdb/constants.py#L4)
- Similarly, all SQL functions, such as `count`, `sum`, `group_concat` are available as **chainable** functions `query.SELECT.Count("type")` or as standalone functions `db.Count("type")`. See [QueryBuilder](src/dataclassdb/query_builder.py) or [SQL_FUNC enum](src/dataclassdb/constants.py#L161)
- QueryBuilders `__call__` adds provided arguments to the string as a list, with optional quote and parenthesis options.

QueryBuilder is a fancy SQL flavored String Builder which the following goals:

### Convention breaking weirdness

SQL [statements](src/dataclassdb/sql_statement_builder.py) leverage a totally legal but questionable hack. Each statement is a [`@property`](https://docs.python.org/3/library/functions.html#property) that returns self. The
[`__call__`](https://docs.python.org/3/reference/datamodel.html#emulating-callable-objects) handles the case where the object is called directly. Note that SQL functions are **NOT** properties.

So to for the Query `qb.SELECT("a","b")`

1. `qb.SELECT`: Calls the property `SELECT` which adds `"SELECT"` to the string. It returns self.
2. `qb.SELECT("a", "b")` calls `__call__` function instead of `SELECT` function.

### Comparing QueryBuilder, plain sqlite3 and sqlAlchemy

#### QueryBuilder

```python
query = QueryBuilder("example.db").
query.SELECT("name").FROM("sqlite_master").WHERE("name='spam'")
result = query.execute()
```

#### Sqlite3

```python
#sqlite3
con = sqlite3.connect("example.db")
cur = con.cursor()
res = cur.execute("SELECT name FROM sqlite_master WHERE name='spam'")
```

#### sqlAlchemy

```python
engine = create_engine("sqlite:///example.db")
with engine.connect() as conn:
    query = text("SELECT name FROM sqlite_master WHERE name='spam'")
    res = conn.execute(query)
```

### Bonus functions

- `placeholders(n)` adds string "(? ... n)"
- `show()` prints the query at its current state
- `br` newline
- `lpar` "\("
- `rpar` "\)"
- `rpar` "\)"
- `comma` ","
- `execute(*args)`: Executes the command with the provided args replacing the placeholders.

## Created By

Stuart (@stuarts_art)

- Washed dev who now makes furry art
- I branched this out of [ArtRefSync](https://github.com/stuarts-art/ArtRefSync), a pure python desktop ui to sync reference art from SFW and NSFW image boards.
  - It uses client provided api keys to ethically get data while respecting usage rules
  - User defined black list to avoid the scourge of AI art
  - Is not using excessive ram to spy on you (plus memory is expensive)
