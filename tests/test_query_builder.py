import sqlite3

import pytest

from dataclassdb.builders.query_builder import (
    QueryBuilder,
)


def test_query_builder():
    builder = QueryBuilder()

    builder("x").eq("2")
    assert builder == "x = 2"
    builder.clear

    builder("x").neq("2")
    assert builder == "x <> 2"
    builder.clear

    builder("x").lpar("2")
    assert builder == "x ( 2"
    builder.clear

    builder("x").rpar("2")
    assert builder == "x ) 2"
    builder.clear

    builder("x").comma("2")
    assert builder == "x, 2"
    builder.clear

    builder("x").end("2")
    assert builder == "x; 2"
    builder.clear

    builder("x").par("2")
    assert builder == "x (2)"
    builder.clear

    builder("x").quote("2")
    assert builder == 'x "2"'
    builder.clear

    builder("x").dot("2")
    assert builder == "x.2"
    builder.clear

    builder("x").placeholders("2")
    assert builder == "x (?1)"
    builder.clear

    builder("x").placeholders("2", par=False)
    assert builder == "x ?1"
    builder.clear

    builder.SELECT("*").FROM("Table")
    assert builder.as_string() == "SELECT * FROM Table"
    assert builder == ""


def test_raise_error_when_connection_not_set():
    builder = QueryBuilder()
    for method in [builder.execute, builder.execute_one, builder.execute_script]:
        with pytest.raises(ValueError):
            method()


def test_connect_to_db(db_mem_connection):
    builder = QueryBuilder(db_mem_connection)
    assert builder.connection
    assert isinstance(builder.connection, sqlite3.Connection)

    table_query = builder.get_curr_cols("testing")
    assert len(table_query) == 2
    assert table_query[0].startswith("id INTEGER PRIMARY KEY")
    assert table_query[1].startswith("name TEXT NOT NULL")

    table_query = builder.get_current_fields("testing")
    assert len(table_query) == 2
    assert table_query[0].name == "id"
    assert table_query[0].pk
    assert table_query[0].type == "INTEGER"

    assert table_query[1].name == "name"
    assert not table_query[1].pk
    assert table_query[1].type == "TEXT"

    assert builder.get_current_fields("missing_table") == []
    assert builder.get_curr_cols("missing_table") == []


def test_join():

    qb = QueryBuilder()
    with pytest.raises(SyntaxError):
        qb.join("table", as_="t2", on="t1.id = t2.id", using_cols=["id"])
    qb.clear

    # test using_cols
    assert (
        qb.join("table", as_="t2", using_cols=["id"]) == "JOIN table AS t2 USING (id)"
    )
    qb.clear

    (
        qb.SELECT("t1.name", "t2.name")
        .from_("Table1", as_="t1")
        .join("Table2", as_="t2", on="t1.id = t2.id", join_type="LEFT")
    )
    assert (
        qb
        == "SELECT t1.name, t2.name FROM Table1 AS t1 LEFT JOIN Table2 AS t2 ON t1.id = t2.id"
    )


def test_edgecases():
    qb = QueryBuilder()
    assert qb.dot() == "."
    qb.clear
    assert qb.dot("x") == ".x"
    qb.clear

    assert qb.comma == ","
    qb.clear
    assert qb.comma("x") == ", x"
    qb.clear

    assert qb.end("x") == "; x"
    qb.clear

    assert qb.from_("Table", as_="t") == "FROM Table AS t"
    qb.clear
    assert qb.from_("Table") == "FROM Table"
    qb.clear
    assert qb.join("Table") == "JOIN Table"
    qb.clear
    assert qb.join("Table", using_cols="id") == "JOIN Table USING (id)"
    qb.clear
    assert qb.join("Table", using_cols=["id", "name"]) == "JOIN Table USING (id, name)"
