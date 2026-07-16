import logging
import sqlite3
from dataclasses import is_dataclass
from typing import Any, TypeVar

from dataclassdb.builders.query_builder import QueryBuilder
from dataclassdb.dataclass_sqlite_table import get_class_codec
from dataclassdb.constants import SQL

from dataclassdb.dataclass_types import IsDataclass
from dataclassdb.utils import table_exists

logger = logging.getLogger(__name__)

DataclassT = TypeVar("DataclassT", bound=IsDataclass)


class DataclassDb(QueryBuilder):
    """DataclassDb provides a context managed interface with sqlite 3 using a dataclass.

    Args:
        QueryBuilder (_type_): _description_
    Returns:
        _type_: _description_
    """
    primary_key_map: dict[Any, list[str]] = {}
    unique_map: dict[Any, list[str]] = {}

    def __init__(
        self,
        data_class: DataclassT,
        connection: str | sqlite3.Connection,
        table_name="",
    ):
        super().__init__(connection=connection)
        if not is_dataclass(data_class):
            raise TypeError(f"Class {data_class.__name__} is not a dataclass")
        if not connection:
            raise ConnectionError("Connection must be set.")
        self.data_class = data_class
        self.table_name = table_name if table_name else data_class.__name__
        self._insert_query = None
        self.query_map = {}
        self.primary_keys = []
        self.unique = []
        self.codec = get_class_codec(data_class)
        self.connection_name = ""
        for name, _field in self.codec.class_fields.items():
            if _field.primary_key:
                self.primary_keys.append(name)
            if _field.unique:
                self.unique.append(name)
        self.create_or_update_table()

    def __contains__(self, key) -> bool:
        try:
            query = (
                QueryBuilder()
                .SELECT(1)
                .FROM(self.table_name)
                .WHERE(self.key_match_str())
                .LIMIT(1)
            )
            result = self.execute_one(
                *self.parse_key(key), sql_str=str(query), as_dict=False
            )
            return result is not None
        finally:
            self.clear

    def __setitem__(self, key, value) -> DataclassT:
        self.insert(value)

    def insert_query(self, *field_names, returning=True):
        key = (
            "insert_query",
            field_names,
            returning,
        )
        if key not in self.query_map:
            query = (
                QueryBuilder()
                .INSERT.INTO(self.table_name)
                .par(*field_names)
                .br.VALUES.placeholders(*field_names)
            )
            if self.primary_keys:
                if len(self.primary_keys) < len(self.codec.class_fields):
                    (
                        query.br.ON.CONFLICT.par(*self.primary_keys).br.DO.UPDATE.SET(
                            *[
                                f"{col} = excluded.{col}"
                                for col in field_names
                                if col not in self.primary_keys
                            ]
                        )
                    )
                else:
                    query.ON.CONFLICT.par(*self.primary_keys).DO.NOTHING
                if returning:
                    query.br.RETURNING(*self.primary_keys)
            else:
                if returning:
                    query.br.RETURNING("rowid")
            self.query_map[key] = str(query)
        return self.query_map[key]

    def key_match_str(self):
        return " AND ".join([f"{key} = ?" for key in self.primary_keys])

    def get_current_table_query(self) -> str:
        row = (
            QueryBuilder(self.connection)
            .SELECT("sql")
            .FROM("sqlite_master")
            .WHERE("type")
            .eq.quote("table")
            .AND("name")
            .eq.quote(self.table_name)
            .end.execute_one(as_dict=False)
        )
        return row[0] if row else ""

    def parse_key(self, key):
        if not isinstance(key, tuple):
            if isinstance(key, list):
                key = tuple(key)
            else:
                key = (key,)
        if len(self.primary_keys) != len(key):
            raise KeyError(
                "Input of (%s) does not match length of primary key (%s)",
                key,
                self.primary_keys,
            )
        return key

    def insert(self, item: DataclassT):
        params = self.codec.encode(item, as_tuple=False, ignore_none=True)
        field_names = params.keys()
        return self.execute_one(
            *params.values(), sql_str=self.insert_query(*field_names)
        )

    def insert_many(self, items: list[DataclassT]):
        encoded = [
            self.codec.encode(item, as_tuple=True, ignore_none=False) for item in items
        ]
        field_names = self.codec.class_fields.keys()
        return self.execute_many(
            *encoded, sql_str=self.insert_query(*field_names, returning=False)
        )

    def get(
        self, key, select_fields: list[str] = None, as_dict=False, as_tuple=False
    ) -> DataclassT:
        if self.primary_keys == []:
            return self.peek(key, select_fields, as_dict, as_tuple)
        if as_dict and as_tuple:
            raise ValueError("as_dict and as _tuple cannot both be true")
        if select_fields and not as_dict and not as_tuple:
            raise ValueError(
                "If select fields are provided either as_dict or as_tuple must be true."
            )
        if not select_fields:
            field_str = "*"
        else:
            field_str = ", ".join(select_fields)
        query = (
            QueryBuilder()
            .SELECT(field_str)
            .FROM(self.table_name)
            .WHERE(self.key_match_str())
        )
        row_dict: dict = self.execute_one(
            *self.parse_key(key),
            sql_str=str(query),
            as_dict=True,
        )
        as_obj = not (as_tuple or as_dict)
        decoded = self.codec.decode(row_dict, as_obj=as_obj)
        if as_tuple:
            return tuple(decoded.values())
        else:
            return decoded

    def peek(
        self, rowid=None, select_fields: list[str] = None, as_dict=False, as_tuple=False
    ):
        if as_dict and as_tuple:
            raise ValueError("as_dict and as _tuple cannot both be true")
        if select_fields and not as_dict and not as_tuple:
            raise ValueError(
                "If select fields are provided either as_dict or as_tuple must be true."
            )
        if not select_fields:
            field_str = "*"
        else:
            field_str = ", ".join(select_fields)
        query = QueryBuilder().SELECT(field_str).FROM(self.table_name)
        if rowid is not None:
            query.WHERE("rowid").eq("?")
        query.ORDER.BY("rowid").DESC
        if rowid:
            row_dict: dict = self.execute_one(
                rowid,
                sql_str=str(query),
                as_dict=True,
            )
        else:
            row_dict: dict = self.execute_one(
                sql_str=str(query),
                as_dict=True,
            )
        as_obj = not (as_tuple or as_dict)
        decoded = self.codec.decode(row_dict, as_obj=as_obj)
        if as_tuple:
            return tuple(decoded.values())
        else:
            return decoded

    def delete(self, key) -> DataclassT:
        query = QueryBuilder().DELETE.FROM(self.table_name).WHERE(self.key_match_str())
        self.execute_one(*self.parse_key(key), sql_str=str(query))

    def create_or_update_table(self):
        logger.info("Creating or updating table %s", self.table_name)
        if not table_exists(self.connection, self.table_name):
            logger.info("Table %s does not exist. Creating table.", self.table_name)
            query = QueryBuilder().add(self.sql_create_table())
            self.execute_one(sql_str=str(query))
            # query.execute_one()

        elif self.get_curr_cols(self.data_class) != self.dataclass_sql_cols():
            logger.info(
                "Table %s does exist but does not match the dataclass. Attempting to update table..",
                self.table_name,
            )
            fields_list = self.get_current_fields(self.table_name)

            curr_fields = {f.name: f for f in fields_list}
            dc_fields = self.codec.class_fields
            overlapping_fields = []
            for dc_field, dc_item in dc_fields.items():
                if curr_fields.get(dc_field, None):
                    overlapping_fields.append(dc_field)
            temp_table = f"temp_{self.table_name}"
            logger.info(
                "Attempting to update table on these overlapping fields",
                self.table_name,
                overlapping_fields,
            )
            if overlapping_fields:
                query = (
                    QueryBuilder()
                    .BEGIN.IMMEDIATE.TRANSACTION.end.br(
                        self.sql_create_table(temp_table)
                    )
                    .br.INSERT.INTO(temp_table)
                    .par(*overlapping_fields)
                    .br.SELECT(*overlapping_fields)
                    .FROM(self.table_name)
                    .end.br.DROP.TABLE.IF.EXISTS(self.table_name)
                    .end.br.ALTER.TABLE(temp_table)
                    .RENAME.TO(self.table_name)
                )
                self.execute_script(sql_script=str(query))
            else:
                logger.warning(
                    "Table for dataclass %s has changed with no overlapping fields. Deleting table and creating a new one.",
                    self.data_class.__name__,
                )
                query = (
                    QueryBuilder()
                    .BEGIN.IMMEDIATE.TRANSACTION.end.br.DROP.TABLE.IF.EXISTS(
                        self.table_name
                    )
                    .end.br(self.sql_create_table())
                    .br
                )
                self.execute_script(sql_script=str(query))
            logger.info(
                "Table creation for %s successful with overlapping fields %s",
                self.table_name,
                overlapping_fields,
            )
        else:
            logger.info("Table has not changed.")

    def sql_create_table(self, table_name=None) -> str:
        table_name = table_name if table_name else self.table_name
        cols_str = ",\n".join(self.dataclass_sql_cols())
        return (
            QueryBuilder()
            .CREATE.TABLE.IF.NOT.EXISTS(table_name)
            .par(f"\n{cols_str}\n")
            .end
        )

    def dataclass_sql_cols(self):
        """Returns a list of SQL columns used in CREATE TABLE"""
        #
        params = []
        for name, f in self.codec.class_fields.items():
            params.append(
                f.sql_col_def(len(self.primary_keys) > 1, len(self.unique) > 1)
            )
        if len(self.primary_keys) > 1:
            params.append(f"{SQL.PRIMARY_KEY}({', '.join(self.primary_keys)})")
        if len(self.unique) > 1:
            params.append(f"{SQL.UNIQUE}({', '.join(self.unique)})")
        return params
