from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from typing import Annotated

import pytest

from dataclassdb.dataclass_db import DataclassDb
from dataclassdb.dataclass_field_codec import IdentityCodec, JsonCodec, PickleCodec
from dataclassdb.dataclass_types import CustomCodec


class ExampleEnum(Enum):
    A = auto()
    B = auto()
    C = auto()


class ExampleStrEnum(StrEnum):
    A = auto()
    B = auto()
    C = auto()


custom_codec = CustomCodec(encode=lambda x: x + 1, decode=lambda x: x - 1)


class TestInt:
    @dataclass
    class Dataclass_Int:
        test_00: int
        test_01: int | None
        test_02: Annotated[int, "BLOB"]
        test_03: Annotated[int, "TEXT"]
        test_04: Annotated[int, custom_codec]
        test_10: Annotated[int, "INT"]
        test_11: Annotated[int, "TINYINT"]
        test_12: Annotated[int, "SMALLINT"]
        test_13: Annotated[int, "MEDIUMINT"]
        test_14: Annotated[int, "BIGINT"]
        test_15: Annotated[int, "UNSIGNED BIG INT"]
        test_20: Annotated[int, "VARCHAR(10)"]
        test_21: Annotated[int, "should be ignore"]
        test_22: Annotated[int | None, ["should be ignored"]]

    @pytest.mark.parametrize(
        "input_, expected",
        [
            ("test_00", ("INTEGER", IdentityCodec)),
            ("test_01", ("INTEGER", IdentityCodec)),
            ("test_02", ("BLOB", PickleCodec)),
            ("test_03", ("TEXT", JsonCodec)),
            ("test_04", ("INTEGER", CustomCodec)),
            ("test_10", ("INTEGER", IdentityCodec)),
            ("test_11", ("INTEGER", IdentityCodec)),
            ("test_12", ("INTEGER", IdentityCodec)),
            ("test_13", ("INTEGER", IdentityCodec)),
            ("test_14", ("INTEGER", IdentityCodec)),
            ("test_15", ("INTEGER", IdentityCodec)),
            ("test_20", ("TEXT", JsonCodec)),
            ("test_21", ("INTEGER", IdentityCodec)),
        ],
    )
    def test_annotations(self, input_, expected, db_mem_connection):

        with DataclassDb(self.Dataclass_Int, db_mem_connection) as db:
            sql_type, codec = expected
            assert input_ in db.codec.class_fields
            class_field = db.codec.class_fields[input_]
            assert class_field.sql_type == sql_type
            assert isinstance(class_field.codec, codec)

    def test_custom_codec(self, db_mem_connection):
        with DataclassDb(self.Dataclass_Int, db_mem_connection) as db:
            class_field = db.codec.class_fields["test_04"]
            assert class_field.encode(0) == 1
            assert class_field.decode(1) == 0

    def test_invalid_constraints(self, db_mem_connection):

        @dataclass
        class Dataclass_Test_Ignore:
            test_00: int
            test_01: Annotated[int, "should be ignore"]
            test_02: Annotated[int | None, ["should be ignored"]]

        with DataclassDb(Dataclass_Test_Ignore, db_mem_connection) as db:
            class_field = db.codec.class_fields["test_01"]
            assert class_field.constraints == {"NOT": "NOT NULL"}

            class_field = db.codec.class_fields["test_02"]
            assert class_field.constraints == {}

    @dataclass
    class Failure_Dataclass:
        data: set

    def test_set_fields(self, db_mem_connection):
        with pytest.raises(TypeError):
            with DataclassDb(self.Failure_Dataclass, db_mem_connection) as db:
                db.show

    @dataclass
    class Pass_Set_Dataclass:
        test_0: Annotated[set, "TEXT"]
        test_1: Annotated[set[int], "TEXT"]
        test_2: Annotated[set[str], "TEXT"]
        test_10: list
        test_11: list[str]
        test_20: dict
        test_21: dict[str]

    def test_set_text_fields(self, db_mem_connection):
        with DataclassDb(self.Pass_Set_Dataclass, db_mem_connection) as db:
            assert "test_0" in db.codec.class_fields
            assert "test_1" in db.codec.class_fields
            assert "test_2" in db.codec.class_fields

            assert "test_10" in db.codec.class_fields
            assert "test_11" in db.codec.class_fields

            assert "test_20" in db.codec.class_fields
            assert "test_21" in db.codec.class_fields

        # test_10: TestEnum_0
        # test_11: TestEnum_0 | None
        # test_12: Annotated[TestEnum_0, "BLOB"]


#     expected_type_codecs =
#     [
#         ("test_00", ("INTEGER", IdentityCodec)),
#         ("test_01", ("INTEGER", IdentityCodec)),
#         ("test_02", ("BLOB", PickleCodec)),
#         ("test_03", ("TEXT", JsonCodec)),
#         ("test_10", ("INTEGER", EnumCodec)),
#         ("test_11", ("INTEGER", EnumCodec)),
#         ("test_12", ("BLOB", PickleCodec)),
#     ]

# def test_annotations(db_mem_connection):
#     sql_type, codec = expected


#     @dataclass
#     class TestClass_0:
#         test_00: int
#         test_01: int | None
#         test_02: Annotated[int, "BLOB"]
#         test_03: Annotated[int, "TEXT"]

#         test_10: TestEnum_0
#         test_11: TestEnum_0 | None
#         test_12: Annotated[TestEnum_0, "BLOB"]
#         # test_13: Annotated[TestEnum_0, "TEXT"]

#     expected_type_codecs = {
#         ("test_00", ("INTEGER", IdentityCodec)),
#         ("test_01", ("INTEGER", IdentityCodec)),
#         ("test_02", ("BLOB", PickleCodec)),
#         ("test_03", ("TEXT", JsonCodec)),
#         ("test_10", ("INTEGER", EnumCodec)),
#         ("test_11", ("INTEGER", EnumCodec)),
#         ("test_12", ("BLOB", PickleCodec)),
#     }
#     with DataclassDb(TestClass_0, db_mem_connection) as db:
#         for case, expected in expected_type_codecs.items():
#             sql_type, codec = expected
#             assert case in db.codec.class_fields
#             class_field = db.codec.class_fields[case]
#             assert class_field.sql_type == sql_type
#             assert isinstance(class_field.codec, codec)
