from dataclasses import dataclass, field
from typing import Annotated

import pytest

from dataclassdb.dataclass_field_codec import identity_codec
from dataclassdb.dataclass_sqlite_field import DataclassSqliteField
from dataclassdb.dataclass_sqlite_table import (
    DataclassTableCodec,
    decode_field,
    encode_field,
    get_class_codec,
    get_field_codec,
)


@dataclass
class Dataclass1:
    id: Annotated[int, "PRIMARY KEY"]
    name: str
    username: Annotated[str, "CONSTRAINT UNIQUE", "DEFAULT ''"]
    links: Annotated[list[str], "TEXT"] = field(default_factory=list)
    socials: Annotated[list[str], "BLOB"] = field(default_factory=list)
    score: int = 0


@pytest.mark.parametrize(
    "field_name, expected_type, expected_sql_type",
    [
        ("id", int, "INTEGER"),
        ("name", str, "TEXT"),
        ("username", str, "TEXT"),
        ("links", list[str], "TEXT"),
        ("socials", list[str], "BLOB"),
    ],
)
def test_field_creation(field_name, expected_type, expected_sql_type):
    for codec_builder in [get_class_codec, DataclassTableCodec]:
        codec = codec_builder(Dataclass1)
        class_field: DataclassSqliteField = codec.class_fields[field_name]
        assert class_field.type == expected_type
        assert class_field.sql_type == expected_sql_type

        assert class_field.sql_col_def()
        assert class_field.sql_col_def(skip_primary=True)
        assert class_field.sql_col_def(skip_unique=True)
        assert class_field.sql_col_def(skip_primary=True, skip_unique=True)
        assert class_field.primary_key is not None
        assert class_field.unique is not None
        assert class_field.notnull is not None
        assert class_field.sql_type is not None


@pytest.mark.parametrize(
    "input",
    [
        Dataclass1(1, "test one", "user_1", [], []),
        Dataclass1(1, "test one", "user_1", ["a", "b"], ["c", "d"]),
    ],
)
def test_missing_key(input):
    codec = get_class_codec(Dataclass1)
    input.missing = 1
    encoded = codec.encode(input, "missing", as_tuple=False)
    encoded["missing"] = 1
    decoded = codec.decode(encoded)
    assert decoded
    with pytest.raises(AttributeError):
        decoded.missing


@pytest.mark.parametrize(
    "input",
    [
        Dataclass1(1, "test one", "user_1", [], []),
        Dataclass1(1, "test one", "user_1", ["a", "b"], ["c", "d"]),
    ],
)
def test_encoding_decoding(input):
    codec = get_class_codec(Dataclass1)
    encoded = codec.encode(input, as_tuple=False)
    decoded = codec.decode(encoded, as_obj=True)
    assert input == decoded

    encoded_tuple = codec.encode(input)
    decoded_dict = codec.decode(encoded, as_obj=False)
    assert isinstance(encoded_tuple, tuple)
    assert isinstance(decoded_dict, dict)


def test_sqlite_codec_errors(db_mem_connection):

    class normal_class:
        name = "test"

    with pytest.raises(ValueError):
        DataclassTableCodec(normal_class)
    assert get_class_codec(normal_class) is None

    assert encode_field(Dataclass1, "links", ["1", "2", "3"]) == '["1", "2", "3"]'
    assert decode_field(Dataclass1, "links", '["1", "2", "3"]') == ["1", "2", "3"]

    assert get_field_codec(normal_class, "name") == identity_codec

    fields = get_class_codec(Dataclass1)
    assert "id" in fields
    assert "name" in fields
    assert "username" in fields
    assert "missing" not in fields


def test_None_identity():
    codec = get_class_codec(Dataclass1)
    assert codec.encode(None) is None
    assert codec.decode(None) is None
