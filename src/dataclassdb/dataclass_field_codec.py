import dataclasses
import json
import logging
import pickle
from datetime import datetime, timezone
from typing import Any, TypeVar, Union, get_args, get_origin

import dacite

from dataclassdb.dataclass_types import Codec, IsDataclass
from dataclassdb.utils import is_enum_class, is_strenum

logger = logging.getLogger(__name__)

DataclassT = TypeVar("DataclassT", bound=IsDataclass)
T = TypeVar("T")
def create_field_codec(field_class: T, sql_type: str) -> Codec:
    if origin := get_origin(field_class):
        if origin is Union:
            field_class = get_args(field_class)[0]
        else:
            field_class = origin

    if sql_type == "BLOB":
        if dataclasses.is_dataclass(field_class):
            return DataclassPickleCodec(field_class)
        else:
            return pickle_codec
    elif dataclasses.is_dataclass(field_class):
        return DataclassJsonCodec(field_class)
    elif is_strenum(field_class):
        if sql_type != "TEXT":
            raise ValueError("The SQL type for StrEnum must be TEXT or BLOB")
        return StrEnumCodec(field_class=field_class, sql_type=sql_type)
    elif is_enum_class(field_class):
        if sql_type != "INTEGER":
            raise ValueError("The SQL type for Enums must be INTEGER or BLOB")
        return EnumCodec(field_class=field_class, sql_type=sql_type)
    elif issubclass(field_class, datetime):
        if sql_type == "INTEGER":
            return datetime_int_codec
        else:
            return datetime_text_codec

    elif sql_type == "TEXT":
        if field_class is str:
            return identity_codec
        else:
            return json_codec
    elif field_class is bool:
        if sql_type != "INTEGER":
            raise ValueError("bool fields must be BLOB, TEXT, or INTEGER")
        return bool_codec
    return identity_codec


class DataclassJsonCodec(Codec):
    def __init__(self, field_class, *args, **kwargs):
        self.field_class = field_class

    def encode(self, data: any) -> str:
        if data is None:
            return ""
        data_dict = None
        if isinstance(data, dict):
            data_dict = data
        else:
            data_dict = dataclasses.asdict(data)
        return json.dumps(data_dict)

    def decode(self, data: str | dict):
        if data is None or data == "":
            return None
        if isinstance(data, dict):
            data_dict = data
        else:
            data_dict = json.loads(data)
        return dacite.from_dict(self.field_class, data_dict)


class DataclassPickleCodec(Codec):
    def __init__(self, field_class, *args, **kwargs):
        self.field_class = field_class

    def encode(self, data):
        if data is None:
            return None
        data_dict = None
        if isinstance(data, dict):
            data_dict = data
        else:
            data_dict = dataclasses.asdict(data)
        return pickle.dumps(data_dict)

    def decode(self, data):
        if data is None:
            return None
        data_dict = None
        if isinstance(data, dict):
            data_dict = data
        else:
            data_dict = pickle.loads(data)
        return dacite.from_dict(self.field_class, data_dict)


class StrEnumCodec(Codec):
    def __init__(self, field_class: T, *args, **kwargs):
        self.field_class = field_class

    def encode(self, data: T) -> str | int:
        if data is None:
            return None
        return data.value

    def decode(self, data: str | int) -> T:
        if data is None:
            return None
        return self.field_class(data)


class EnumCodec(Codec):
    def __init__(self, field_class: T, *args, **kwargs):
        self.field_class = field_class

    def encode(self, data: T) -> str | int:
        if data is None:
            return None
        return data.value

    def decode(self, data: str | int) -> T:
        if data is None:
            return None
        return self.field_class(data)


class JsonCodec(Codec):
    def encode(self, data: any) -> str:
        if data is None:
            return None
        if dataclasses.is_dataclass(data):
            return json.dumps(dataclasses.asdict(data))
        return json.dumps(data)

    def decode(self, data: str) -> any:
        if data is None:
            return None
        return json.loads(data)


class PickleCodec(Codec):
    def encode(self, data: Any) -> bytes:
        if data is None:
            return None
        return pickle.dumps(data)

    def decode(self, data: bytes) -> Any:
        if data is None:
            return None
        return pickle.loads(data)


class IdentityCodec(Codec):
    def encode(self, data: T) -> T:
        return data

    def decode(self, data: T) -> T:
        return data


class BoolCodec(Codec):
    def encode(self, data: bool) -> int:
        if data is None:
            return None
        return 1 if data is True else 0

    def decode(self, data: int) -> bool:
        if data is None:
            return None
        return data >= 1


class DatetimeIntCodec(Codec):
    """Converts between python datetime(utc) to sqlite3 INTEGER"""

    def encode(self, data: datetime) -> int:
        if data is None:
            return None
        return int(data.timestamp())

    def decode(self, data: int) -> datetime:
        if data is None:
            return None
        return datetime.fromtimestamp(timestamp=data, tz=timezone.utc)


class DatetimeTextCodec(Codec):
    """Converts between python datetime to sqlite3 TEXT(ISO 8601)"""

    def encode(self, data: datetime) -> int:
        if data is None:
            return None
        return data.isoformat()

    def decode(self, data: int) -> datetime:
        if data is None:
            return None
        return datetime.fromisoformat(data)


# Reusable codecs:
bool_codec = BoolCodec()
identity_codec = IdentityCodec()
json_codec = JsonCodec()
pickle_codec = PickleCodec()
datetime_int_codec = DatetimeIntCodec()
datetime_text_codec = DatetimeTextCodec()
