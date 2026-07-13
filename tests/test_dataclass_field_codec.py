from __future__ import annotations
import json
from dataclasses import asdict, dataclass
from enum import Enum, StrEnum, auto

import pytest

from dataclassdb.dataclass_field_codec import (
    DataclassJsonCodec,
    DataclassPickleCodec,
    EnumCodec,
    IdentityCodec,
    JsonCodec,
    PickleCodec,
    StrEnumCodec,
    bool_codec,
    create_field_codec,
    identity_codec,
    json_codec,
    pickle_codec,
)
from dataclassdb.dataclass_sqlite_table import get_field_codec


@dataclass
class Dataclass1:
    id: int
    name: str
    sibling: Dataclass1 | None = None


@pytest.mark.parametrize(
    "inputs, expected",
    [
        ((Enum, "INTEGER"), EnumCodec),
        ((StrEnum, "TEXT"), StrEnumCodec),
        ((bool, "BLOB"), pickle_codec),
        ((bool, "INTEGER"), bool_codec),
        ((str, "TEXT"), identity_codec),
        ((dict, "BLOB"), pickle_codec),
        ((dict, "TEXT"), json_codec),
        ((list, "TEXT"), json_codec),
        ((Dataclass1, "BLOB"), DataclassPickleCodec),
        ((Dataclass1, "TEXT"), DataclassJsonCodec),
    ],
)
def test_get_field_codec(inputs, expected):
    codec = create_field_codec(*inputs)
    assert codec == expected or isinstance(codec, expected)


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (
            Dataclass1(1, "one", Dataclass1(2, "two", None)),
            '{"id": 1, "name": "one", "sibling": {"id": 2, "name": "two", "sibling": null}}',
        ),
        (Dataclass1(1, "one", None), '{"id": 1, "name": "one", "sibling": null}'),
    ],
)
def test_DataclassCodec(inputs, expected):
    codec = DataclassJsonCodec(Dataclass1)
    encoded = codec.encode(inputs)
    assert encoded == expected

    decoded = codec.decode(expected)
    assert decoded == inputs


@pytest.mark.parametrize(
    "inputs",
    [Dataclass1(1, "one", Dataclass1(2, "two", None)), Dataclass1(1, "one", None)],
)
def test_DataclassCodecBlob(inputs):
    for codec_class, sql_type in [
        (DataclassJsonCodec, "TEXT"),
        (DataclassPickleCodec, "BLOB"),
        (JsonCodec, "TEXT"),
        (PickleCodec, "BLOB"),
    ]:
        codec = codec_class(type(inputs), sql_type)
        encoded = codec.encode(inputs)
        decoded = codec.decode(encoded)
        if codec_class is JsonCodec:
            assert decoded == asdict(inputs)
        else:
            assert decoded == inputs


@pytest.mark.parametrize(
    "inputs",
    [Dataclass1(1, "one", Dataclass1(2, "two", None)), Dataclass1(1, "one", None)],
)
def test_DataclassCodecDictInput(inputs):
    dict_input: dict = asdict(inputs)
    codec = DataclassPickleCodec(type(inputs), "Blob")
    encoded = codec.encode(dict_input)
    decoded = codec.decode(encoded)
    assert decoded == inputs
    assert codec.decode(dict_input) == inputs


@pytest.mark.parametrize(
    "inputs",
    [Dataclass1(1, "one", Dataclass1(2, "two", None)), Dataclass1(1, "one", None)],
)
def test_DataclassCodecBlobInput(inputs):
    dict_input = asdict(inputs)
    codec = DataclassPickleCodec(type(inputs), "Blob")
    encoded = codec.encode(dict_input)
    decoded = codec.decode(encoded)
    assert decoded == inputs


@pytest.mark.parametrize("inputs, expected", [(True, 1), (False, 0)])
def test_BoolCodec(inputs, expected):
    assert bool_codec.encode(inputs) == expected
    assert bool_codec.decode(expected) == inputs


@pytest.mark.parametrize(
    "inputs, expected",
    [(1, 1), (1.0, 1.0), ("one", "one"), (True, True), (None, None), (False, False)],
)
def test_IdentityCodec(inputs, expected):
    codec = IdentityCodec(bool, "")
    assert codec.encode(inputs) == expected
    assert codec.decode(expected) == inputs


class Enum1(Enum):
    A = auto()
    B = auto()
    C = auto()


class StrEnum1(StrEnum):
    A = auto()
    B = auto()
    C = auto()


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (Enum1.A, 1),
        (Enum1.B, 2),
        (Enum1.C, 3),
    ],
)
def test_EnumCodec_encoding(inputs, expected):
    codec = EnumCodec(type(inputs), "INTEGER")
    assert codec.encode(inputs) == expected
    assert codec.decode(expected) == inputs


@pytest.mark.parametrize(
    "inputs, expected", [(StrEnum1.A, "a"), (StrEnum1.B, "b"), (StrEnum1.C, "c")]
)
def test_StrEnumCodec_encoding(inputs, expected):
    codec = StrEnumCodec(type(inputs), "TEXT")
    assert codec.encode(inputs) == expected
    assert codec.decode(expected) == inputs


@pytest.mark.parametrize(
    "field_type, sql_type", [(StrEnum1, "INTEGER"), (Enum1, "TEXT"), (bool, "REAL")]
)
def test_init_exceptions(field_type, sql_type):
    with pytest.raises(ValueError):
        create_field_codec(field_type, sql_type)


def test_json_dataclass_codec(db_mem_connection):
    @dataclass
    class Person:
        name: str
        age: int
        address: "Address"

        @dataclass
        class Address:
            address: str
            town: str
            state: str
            zip: str

    person = Person(
        "stuart", 59, Person.Address("adrr", "test town", "SC", "12345-12345")
    )
    person_dict = asdict(person)
    assert person_dict

    # address_codec = get_
    address_codec = get_field_codec(Person, "address")
    # assert isinstance(address_codec.codec, DataclassJsonCodec)

    encoded = address_codec.encode(person.address)
    assert encoded == address_codec.encode(asdict(person.address))

    decoded = address_codec.codec.decode(encoded)
    assert decoded == address_codec.codec.decode(json.loads(encoded))


@pytest.mark.parametrize(
    "codec",
    [
        identity_codec,
        bool_codec,
        pickle_codec,
        DataclassJsonCodec(Dataclass1),
        DataclassPickleCodec(Dataclass1),
        json_codec,
        StrEnumCodec(StrEnum1),
        EnumCodec(Enum1),
    ],
)
def test_None_Identity(codec):
    codec.encode(None)
    codec.decode(None)
    pass
