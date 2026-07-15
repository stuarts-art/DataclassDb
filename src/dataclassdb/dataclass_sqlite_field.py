import inspect
import logging
from dataclasses import MISSING, Field, is_dataclass
from datetime import datetime
from enum import Enum, StrEnum
from types import NoneType, UnionType
from typing import Annotated, get_args, get_origin

from dataclassdb.builders.query_builder import QueryBuilder
from dataclassdb.dataclass_field_codec import create_field_codec
from dataclassdb.dataclass_types import Codec
from dataclassdb.utils import get_absolute_origin

logger = logging.getLogger(__name__)


class DataclassSqliteField:
    """This class reads annotations and determines the provided type, sqlite constraints, and sqlite type
    It also provides an encoder/decoder to and from sqlite.
    """

    _type_map = {
        int: "INTEGER",
        StrEnum: "TEXT",
        Enum: "INTEGER",
        str: "TEXT",
        float: "REAL",
        bool: "INTEGER",
        list: "TEXT",
        dict: "TEXT",
        datetime: "TEXT",
    }

    @property
    def unique(self) -> bool:
        return "UNIQUE" in self.constraints

    @property
    def notnull(self) -> bool:
        return "NOT" in self.constraints

    @property
    def primary_key(self) -> bool:
        return "PRIMARY" in self.constraints

    def encode(self, value):
        return self.codec.encode(value)

    def decode(self, value):
        return self.codec.decode(value)

    def __init__(self, dc_type: type, dc_field: Field, default_sql_type="TEXT"):
        self.name = dc_field.name
        self.type = None
        self.sql_type = default_sql_type
        self.sql_create_type = ""
        self.constraints = {}
        self.codec: Codec = None
        self.type_override = False

        # Handle field outer wrapper
        if is_dataclass(dc_type):
            field_type = dc_type
        if get_origin(dc_type) is Annotated:
            field_type = self.parse_annotated(dc_type)
        else:
            field_type = dc_type

        self.parse_type(field_type)
        if self.codec is None:
            self.codec = create_field_codec(field_type, self.sql_type)

        self.parse_default(dc_field)

    def parse_annotated(self, dataclass_type: type):
        args = get_args(dataclass_type)
        field_type = args[0]
        field_args = args[1:]
        for i, arg in enumerate(field_args):
            if isinstance(arg, Codec):
                logger.info("Overloading codec for field %s", self.name)
                self.codec = arg
                continue
            elif not isinstance(arg, str):
                logger.warning(
                    "Skipping constraint field %i constraint field for %s",
                    i,
                    self.name,
                )
                continue
            split_arg = arg.split(" ")
            key = split_arg[0]
            if key == "CONSTRAINT":
                key = split_arg[1]
                arg = " ".join(split_arg[1:])

            if i == 0:
                no_par_arg = arg.split("(")[0]
                if no_par_arg in QueryBuilder._affinity_map:
                    affinity = QueryBuilder.get_sql_col_affinity(arg)
                    self.type_override = True
                    self.affinity = affinity
                    self.sql_type = affinity
                    self.sql_create_type = arg
                    continue
            if key in [
                "PRIMARY",
                "NOT",
                "UNIQUE",
                "CHECK",
                "DEFAULT",
                "COLLATE",
                "REFERENCES",
                "GENERATED",
                "AS",
                "ON",
            ]:
                self.constraints[key] = arg
            else:
                logger.warning("Skipping annotation field %s", key)
        return field_type

    def parse_type(self, field_type: type):
        # Handle field inner wrapper (e.g. int | None)
        types = (
            get_args(field_type)
            if isinstance(field_type, UnionType)
            else [
                field_type,
            ]
        )
        if "NOT" not in self.constraints and NoneType not in types:
            self.constraints["NOT"] = "NOT NULL"
        self.type = types[0]

        if self.type_override:
            return

        self.origin = get_absolute_origin(field_type)

        if inspect.isclass(self.origin) and issubclass(self.origin, set):
            raise TypeError(
                "Sets cannot be encoded as text. Either override the type to BLOB, "
                "override the codec, or change the datatype."
            )

        for mapped_type in self._type_map:
            if issubclass(self.origin, mapped_type):
                self.sql_type = self._type_map[mapped_type]
                break

    def parse_default(self, dc_field):
        if dc_field.default_factory is not MISSING:
            default = dc_field.default_factory()
        else:
            default = dc_field.default

        if "DEFAULT" in self.constraints or default is None or default is MISSING:
            return

        encoded = self.codec.encode(default)
        if self.sql_type == "TEXT":
            self.constraints["DEFAULT"] = f"DEFAULT '{encoded}'"
        elif self.sql_type == "BLOB":
            self.constraints["DEFAULT"] = f"DEFAULT X'{encoded.hex()}'"
        else:
            self.constraints["DEFAULT"] = f"DEFAULT {encoded}"

    def sql_col_def(self, skip_primary=False, skip_unique=False):
        output = [
            self.name,
            self.sql_create_type if self.sql_create_type else self.sql_type,
        ]
        for key, val in self.constraints.items():
            if key == "PRIMARY" and skip_primary:
                pass
            elif key == "UNIQUE" and skip_unique:
                pass
            else:
                output.append(val)
        return " ".join(output)
