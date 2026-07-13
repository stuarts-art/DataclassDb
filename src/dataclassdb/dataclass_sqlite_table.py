__all__ = [
    "DataclassTableCodec",
    "decode_dict",
    "get_class_codec",
    "get_field_codec",
    "encode_field",
    "decode_field",
]

import functools
import logging
from dataclasses import asdict, fields, is_dataclass
from typing import Any, Literal, TypeVar, get_type_hints, overload

from dacite import from_dict

from dataclassdb.dataclass_field_codec import identity_codec
from dataclassdb.dataclass_sqlite_field import DataclassSqliteField
from dataclassdb.dataclass_types import IsDataclass

logger = logging.getLogger(__name__)


def decode_dict(
    data: dict[str, Any],
    data_class=None,
    prefix_class_map: dict = None,
    remove_prefix=False,
) -> dict[str, Any]:
    if data is None:
        return None

    if data_class is None and prefix_class_map is None:
        raise ValueError("Either a data class or prefix map must be provided")

    if isinstance(data, list):
        output = [
            decode_dict(row, data_class, prefix_class_map, remove_prefix)
            for row in data
        ]
        return output

    output = {}
    for key, val in data.items():
        if "." in key:
            prefix, split_key = key.split(".")
            if mapped_dataclass := prefix_class_map.get(prefix, None):
                decoded = decode_field(mapped_dataclass, split_key, val)
            else:
                decoded = val
            output_key = split_key if remove_prefix else key
            output[output_key] = decoded
        elif data_class:
            field_codec = get_field_codec(data_class, key)
            output[key] = field_codec.decode(val)
        else:
            output[key] = val
    return output


T = TypeVar("T", bound=IsDataclass)
class DataclassTableCodec:
    """This class takes a dataclass and provides encoder and decoder (codec) from and to sqlite."""

    def __contains__(self, item):
        return item in self.class_fields

    def __init__(self, data_class: T) -> None:
        if not data_class or not is_dataclass(data_class):
            raise ValueError(f"Provided class {data_class} is not a dataclass")

        self.data_class: T = data_class
        self.primary_keys = []
        self.class_fields: dict[str, DataclassSqliteField] = {}

        types_map: dict = get_type_hints(data_class, include_extras=True)
        for _field in fields(data_class):
            name = _field.name
            field_type = types_map.get(name, None)
            dc_field = DataclassSqliteField(field_type, _field)
            self.class_fields[name] = dc_field
            if dc_field.primary_key:
                self.primary_keys.append(name)
        self.key_match_str = " AND ".join([f"{key} = ?" for key in self.primary_keys])

    @overload
    def encode(self, obj: T, *cols, as_tuple: Literal[True]) -> tuple: ...
    @overload
    def encode(self, obj: T, *cols, as_tuple: Literal[False]) -> dict: ...
    def encode(
        self, obj: T, *cols, as_tuple: bool = True, ignore_none=True
    ) -> tuple | dict:
        if obj is None:
            return None
        output = {}
        obj_dict = asdict(obj)
        if not cols:
            cols = obj_dict.keys()

        for col in cols:
            v = obj_dict.get(col, None)

            if col in self.class_fields:
                out = self.class_fields[col].encode(v)
            else:
                out = v
            if out is not None or not ignore_none:
                output[col] = out
        return tuple(output.values()) if as_tuple else output

    @overload
    def decode(self, row_dict, as_obj: Literal[True]) -> T: ...
    @overload
    def decode(self, row_dict, as_obj: Literal[False]) -> dict: ...
    def decode(self, row_dict, as_obj: bool = False) -> T | dict:
        if row_dict is None:
            return None
        output = {}
        for k, v in row_dict.items():
            if k in self.class_fields:
                output[k] = self.class_fields[k].decode(v)
            else:
                output[k] = v
        if as_obj:
            return from_dict(self.data_class, output)
        else:
            return output


@functools.lru_cache
def get_class_codec(data_class: IsDataclass) -> DataclassTableCodec:
    if not data_class or not is_dataclass(data_class):
        return None
    else:
        return DataclassTableCodec(data_class)


def get_field_codec(data_class, field_name) -> DataclassSqliteField:
    class_codec = get_class_codec(data_class)
    if not class_codec:
        return identity_codec
    return class_codec.class_fields.get(field_name, identity_codec)


def encode_field(data_class, field_name, data):
    codec = get_field_codec(data_class, field_name)
    return codec.encode(data)


def decode_field(data_class, field_name, data):
    codec = get_field_codec(data_class, field_name)
    return codec.decode(data)
