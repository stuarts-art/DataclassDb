import logging
from dataclasses import dataclass, field, is_dataclass
from typing import Annotated

import pytest

from dataclassdb.builders.query_builder import QueryBuilder
from dataclassdb.dataclass_db import DataclassDb
from dataclassdb.dataclass_sqlite_table import decode_dict
from dataclassdb.db_engine import DbEngine


@dataclass
class Example_Dataclass:
    id: Annotated[int, "PRIMARY KEY"]
    username: Annotated[str, "UNIQUE"]
    score: int = 0
    tags: Annotated[list, "TEXT"] = field(default_factory=list)
    connections: Annotated[dict, "BLOB"] = field(default_factory=dict)
    extras: list[str] | None = None


@dataclass
class XOR_Example_Dataclass:
    pid: Annotated[int, "PRIMARY KEY"]
    name: Annotated[str, "UNIQUE"]
    points: int = 0


@dataclass
class Example_Extended(Example_Dataclass):
    data: str = ""


def test_create_table(db_mem_connection):
    with DataclassDb(Example_Dataclass, db_mem_connection) as db:
        db.sql_create_table()
        pass

    with pytest.raises(ConnectionError):
        with DataclassDb(Example_Dataclass, None) as db:
            pass

    class PlainClass:
        id = 0
        name = ""

    with pytest.raises(TypeError):
        with DataclassDb(PlainClass, None) as db:
            pass


def test_modify_table(db_mem_connection):
    table_name = "test_modify"
    with DataclassDb(Example_Dataclass, db_mem_connection, table_name) as db:
        start_id = 0
        starting_obj = Example_Dataclass(
            start_id, "stuart", tags=["a", "b"], connections={"a": 1}
        )
        db.insert(starting_obj)
        assert start_id in db

        obj_dict = db.get(start_id, as_dict=True)
        assert "data" not in obj_dict

    with DataclassDb(Example_Extended, db_mem_connection, table_name) as db:
        assert start_id in db

        extended_obj_dict = db.get(start_id, as_dict=True)
        assert "data" in extended_obj_dict

        extended_obj = db.get(start_id)
        assert extended_obj != starting_obj
        assert is_dataclass(extended_obj)
        assert isinstance(extended_obj, Example_Extended)

        db.insert(Example_Extended(1, "user", 0, ["a"], {"word": "val"}, "1234"))
        obj1 = db.get(start_id)
        assert is_dataclass(obj1)
        assert isinstance(obj1, Example_Extended)


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

    with DataclassDb(Example_Dataclass, db_mem_connection) as db:
        assert db.get_current_table_query()


def test_multiple_primary(db_mem_connection):
    @dataclass
    class MultipleKeysExample:
        region: Annotated[str, "PRIMARY KEY"]
        eid: Annotated[int, "PRIMARY KEY"]
        username: Annotated[str, "UNIQUE"]
        tag: Annotated[str, "UNIQUE"]
        other: str = ""

    with DataclassDb(MultipleKeysExample, "test_dunno.db") as db:
        test_obj = MultipleKeysExample("na", 0, "test user", "test tag")
        db.insert(test_obj)
        cols = db.get(("na", 0), ["username", "tag"], as_dict=False, as_tuple=True)
        assert cols == ("test user", "test tag")
        cols_dict = db.get(("na", 0), ["username", "tag"], as_dict=True, as_tuple=False)
        assert (cols_dict["username"], cols_dict["tag"]) == ("test user", "test tag")

        with pytest.raises(ValueError):
            db.get("na")

        with pytest.raises(ValueError):
            db.get(("na", 0), ["tag"])

        with pytest.raises(ValueError):
            db.get(("na", 0), as_dict=True, as_tuple=True)

        duplicate_obj = MultipleKeysExample(
            "na", 1, "test user", "test tag", "modified"
        )
        db.insert(duplicate_obj)
        assert ("na", 0) not in db
        assert ("na", 1) in db
        assert db.get(("na", 0)) == db.get(region="na", eid=0)
        assert db.select_query() is None

    with DataclassDb(MultipleKeysExample, db_mem_connection, False) as db:
        assert ("na", 0) not in db
        assert ("na", 1) not in db
        pass


def test_multiple_unique(db_mem_connection):
    @dataclass
    class MultipleUnique:
        username: Annotated[str, "UNIQUE"]
        tag: Annotated[str, "UNIQUE"]

    with DataclassDb(MultipleUnique, db_mem_connection) as db:
        db.insert(MultipleUnique("a", "0"))
        db.insert(MultipleUnique("a", "0"))


def test_multiple_unique_one_primary(db_mem_connection):
    logging.basicConfig(level=logging.DEBUG)

    @dataclass
    class MultipleUniqueOnePrimary:
        username: Annotated[str, "UNIQUE"]
        tag: Annotated[str, "UNIQUE"]
        id: Annotated[int | None, "PRIMARY KEY"] = None

    obj = MultipleUniqueOnePrimary("x", "y")
    with DataclassDb(MultipleUniqueOnePrimary, db_mem_connection) as db:
        id_ = db.insert(obj)
        assert id_ == 1

        id_ = db.insert(obj)
        assert id_ == 1

        # Change Primary if uniques are provided
        obj = MultipleUniqueOnePrimary("x", "y", 4)
        assert 1 in db
        id_ = db.insert(obj)
        assert 1 not in db
        assert id_ == 4

        # # Change unique fields if primary provided
        obj = MultipleUniqueOnePrimary("x2", "y", 4)
        db.insert(obj)
        assert db.get(4).username == "x2"

        objs = [
            MultipleUniqueOnePrimary("foo", "f"),
            MultipleUniqueOnePrimary("bar", "b"),
            MultipleUniqueOnePrimary("baz", "ba"),
        ]
        db.insert_many(objs)


def test_decode_dict(db_mem_connection):
    @dataclass
    class Profile:
        email: str
        password: str

    @dataclass
    class Student:
        id: Annotated[int, "PRIMARY KEY"]
        username: Annotated[str, "UNIQUE"]
        credentials: list[str] = field(default_factory=list)
        profile: Profile | None = None
        color: str = ""

    @dataclass
    class Course:
        id: Annotated[int, "PRIMARY KEY"]
        subject: str
        level: int

    @dataclass
    class StudentCourseLink:
        student_id: Annotated[int, "PRIMARY KEY"]
        course_id: Annotated[int, "PRIMARY KEY"]

    profile = Profile("abc@asdfasdfasf.com", "abc")
    student = Student(0, "Stuart A", ["0", "1", "2"], profile=profile, color="blue")
    course = Course(0, "english", 100)

    with DataclassDb(Student, db_mem_connection) as student_db:
        student_db.insert(student)
    with DataclassDb(Course, db_mem_connection) as test_db:
        test_db.insert(course)

    with DataclassDb(StudentCourseLink, db_mem_connection) as link_db:
        link_db.insert(StudentCourseLink(0, 0))

    with QueryBuilder(db_mem_connection) as qb:
        query_output = (
            qb.select(
                "s.username",
                "s.credentials",
                "s.profile",
                "c.subject",
                "c.level",
                "student_id",
                "course_id",
            )
            .comma("s.color as [d.color]")
            .from_(StudentCourseLink)
            .join(Student, "s", "student_id = s.id")
            .join(Course, "c", "course_id = c.id")
            .show.execute_one(as_dict=True)
        )

    decoded = decode_dict(
        query_output, StudentCourseLink, prefix_class_map={"s": Student, "c": Course}
    )

    assert decoded["s.username"] == student.username
    assert decoded["s.credentials"] == student.credentials
    assert decoded["s.profile"] == student.profile
    assert decoded["c.subject"] == course.subject
    assert decoded["c.level"] == course.level
    assert decoded["d.color"] == student.color
    assert decoded["student_id"] == student.id
    assert decoded["course_id"] == course.id

    decoded = decode_dict(
        query_output, None, prefix_class_map={"s": Student, "c": Course}
    )
    assert decoded["s.username"] == student.username
    assert decoded["s.credentials"] == student.credentials
    assert decoded["s.profile"] == student.profile
    assert decoded["c.subject"] == course.subject
    assert decoded["c.level"] == course.level
    assert decoded["d.color"] == student.color
    assert decoded["student_id"] == student.id
    assert decoded["course_id"] == course.id


def test_single_decode_dict(db_mem_connection):

    with DataclassDb(Example_Dataclass, db_mem_connection) as db:
        example = Example_Dataclass(0, "tet", "score", [1, 3, 5, 7], {"a": 2})
        db.insert(example)

    cols = ["username", "score", "tags", "connections"]
    with QueryBuilder(db_mem_connection) as qb:
        qb.SELECT(*cols).FROM(Example_Dataclass).WHERE("id").eq(0)
        output = qb.execute(as_dict=True)
        # output = db.get(0, ["username", "score", "tags", "connections"], as_dict=True)
        decoded = decode_dict(output, Example_Dataclass)
        assert decoded

    with pytest.raises(ValueError):
        decode_dict(output)


def test_overwrite_table(db_mem_connection):
    table_name = "example"

    with DataclassDb(Example_Dataclass, db_mem_connection, table_name) as db:
        db.insert(Example_Dataclass(0, "abc"))
        assert 0 in db
        pass

    with DataclassDb(XOR_Example_Dataclass, db_mem_connection, table_name) as db:
        assert 0 not in db
        db.insert(XOR_Example_Dataclass(1, "test"))

        pass


def test_None_identity(db_mem_connection):
    assert None is decode_dict(None, Example_Dataclass)


def test_insert_many(db_mem_connection):
    items = []
    for i in range(10):
        items.append(XOR_Example_Dataclass(i, f"name {i}", 5))

    with DataclassDb(XOR_Example_Dataclass, db_mem_connection) as db:
        db.insert_many(items)
        gotten = db.get_all(points=5)
        assert gotten == items

        tuple_rows = db.get_all(points=5, as_tuple=True)
        for row in tuple_rows:
            assert row[2] == 5


def test_insert_many_failure(db_mem_connection):

    with pytest.raises(ConnectionError):
        db = DbEngine()
        db.execute_many()

    with pytest.raises(ValueError):
        db = DbEngine(db_mem_connection)
        db.execute_many()


def test_insert_many_with_no_newline(db_mem_connection):

    with DataclassDb(XOR_Example_Dataclass, db_mem_connection) as db:
        items = []
        for i in range(10):
            items.append(
                (
                    i,
                    f"name {i}",
                    i * i,
                )
            )
        query = "INSERT INTO XOR_Example_Dataclass (pid, name, points) VALUES (?, ?, ?)"
        db.execute_many(*items, sql_str=query)


def test_insert_many_multi_primary_only(db_mem_connection):
    @dataclass
    class PrimaryTest:
        par_1: Annotated[str, "PRIMARY KEY"]
        par_2: Annotated[str, "PRIMARY KEY"]

    student_a = PrimaryTest("A", "a")
    student_b = PrimaryTest("B", "b")
    student_c = PrimaryTest("C", "c")

    with DataclassDb(PrimaryTest, db_mem_connection) as db:
        db.insert(student_a)
        assert ("A", "a") in db
        db.insert(student_b)
        assert ("B", "b") in db
        db.insert(student_c)
        assert ("C", "c") in db

    with DataclassDb(PrimaryTest, db_mem_connection) as db:
        db.insert_many([student_a, student_b, student_c])
        assert ("A", "a") in db
        assert ("B", "b") in db
        assert ("C", "c") in db


def test_insert_many_multi_unique_only(db_mem_connection):
    @dataclass
    class UniqueTest:
        par_1: Annotated[str, "UNIQUE"]
        par_2: Annotated[str, "UNIQUE"]

    test_a = UniqueTest("A", "a")
    test_b = UniqueTest("B", "b")
    test_c = UniqueTest("C", "c")

    with DataclassDb(UniqueTest, db_mem_connection) as db:
        db.insert(test_a)
        assert 1 in db
        assert db.get(1) == test_a

        db.insert(test_b)
        assert 2 in db
        assert db.get(2) == test_b

        db.insert(test_c)
        assert 3 in db
        assert db.get(3) == test_c

    with DataclassDb(UniqueTest, db_mem_connection) as db:
        db.insert_many([test_a, test_b, test_c])
        assert 1 in db
        assert db.get(1) == test_a

        assert 2 in db
        assert db.get(2) == test_b

        assert 3 in db
        assert db.get(3) == test_c
