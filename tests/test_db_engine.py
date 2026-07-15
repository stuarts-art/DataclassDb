import sqlite3

import pytest

from dataclassdb.db_engine import DbEngine


def test_connector(db_mem_connection):

    db = DbEngine(db_mem_connection)
    assert db.connection
    assert isinstance(db.connection, sqlite3.Connection)


def test_mem_connection():
    with DbEngine(":memory:") as db:
        db.show

    with pytest.raises(ValueError):
        with DbEngine() as db:
            db.show


def test_execute(db_mem_connection):
    table_name = "test_execute"
    with DbEngine(db_mem_connection) as db:
        db.execute(sql_str="SELECT * FROM testing")

        db.execute(
            sql_str=f"CREATE TABLE IF NOT EXISTS {table_name}"
            "(id INTEGER PRIMARY KEY, name TEXT NOT NULL)",
            commit=True,
        )

        row_input = (1, "test entry")
        row_input_dict = {"id": row_input[0], "name": row_input[1]}

        db.execute(
            *row_input,
            sql_str=f"INSERT  INTO {table_name} (id, name) VALUES (?, ?)",
        )

        assert db == ""
        row_output = db.execute_one(
            1, sql_str=f"SELECT * FROM {table_name} WHERE id = ?"
        )
        assert row_input == row_output

        row_output_dict = db.execute_one(
            1, sql_str=f"SELECT * FROM {table_name} WHERE id = ?", as_dict=True
        )
        assert row_input_dict == row_output_dict

        query = [
            "BEGIN TRANSACTION;",
            f"CREATE TABLE IF NOT EXISTS temp_{table_name}",
            "(id INTEGER PRIMARY KEY, name TEXT NOT NULL, color TEXT DEFAULT 'red');",
            f"DROP TABLE IF EXISTS {table_name};",
            f"ALTER TABLE temp_{table_name}",
            f"RENAME TO {table_name};",
        ]
        db.execute_script(" ".join(query), as_dict=True, commit=True)


def test_exception_raise(db_mem_connection):

    with DbEngine(db_mem_connection) as db:
        with pytest.raises(ValueError):
            db.execute()

        with pytest.raises(ValueError):
            db.execute_one(as_dict=True, commit=True)

        with pytest.raises(ValueError):
            db.execute_script()

    with pytest.raises(ValueError):
        with DbEngine(db_mem_connection) as db:
            db.execute()


def test_connector_from_outside(tmp_path):
    file = tmp_path / "test.db"
    with DbEngine(file) as db:
        assert db.connection_name == file
        assert db.connection_owner
        assert db.connection
