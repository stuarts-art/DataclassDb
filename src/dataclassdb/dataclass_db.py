import logging
import sqlite3
from dataclasses import is_dataclass
from typing import Any, Iterable, TypeVar

from dataclassdb.builders.query_builder import QueryBuilder
from dataclassdb.constants import SQL
from dataclassdb.dataclass_sqlite_table import encode_field, get_class_codec
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
        self.field_names = []
        self.codec = get_class_codec(data_class)
        self.connection_name = ""
        for name, _field in self.codec.class_fields.items():
            self.field_names.append(name)
            if _field.primary_key:
                self.primary_keys.append(name)
            if _field.unique:
                self.unique.append(name)
        self.create_or_update_table()

    def __contains__(self, key: int | str | tuple | dict) -> bool:
        try:
            params = self.parse_constraint_dict(key)
            query = QueryBuilder().SELECT(1).FROM(self.table_name)
            if params:
                query.WHERE(self.where_args(*params.keys())).LIMIT(1)
                result = self.execute_one(
                    *params.values(), sql_str=str(query), as_dict=False
                )
                return result is not None
            elif isinstance(key, int):
                query.WHERE("rowid").eq("?").LIMIT(1)
                result = self.execute_one(key, sql_str=str(query), as_dict=False)
                return result is not None
            else:
                return False
        except Exception:
            return False

    def __setitem__(self, key, value) -> DataclassT:
        self.insert(value)

    def insert_query(self, *field_names, returning=True):
        key = (
            "insert_query",
            field_names,
            returning,
        )
        if key not in self.query_map:
            uniques_in_fields = [x for x in self.unique if x in field_names]
            primaries_in_fields = [x for x in self.primary_keys if x in field_names]

            query = QueryBuilder()
            query.INSERT.INTO(self.table_name).par(*field_names).VALUES.placeholders(
                *field_names
            )

            if self.unique and len(uniques_in_fields) == len(self.unique):
                query.br.ON.CONFLICT(*self.unique, par=True).br
                cols = [col for col in field_names if col not in self.unique]
                if len(cols) > 0:
                    query.DO.UPDATE.SET(*[f"{col} = excluded.{col}" for col in cols])
                elif returning:
                    query.DO.UPDATE.SET(f"{self.unique[0]} = {self.unique[0]}")
                else:
                    query.DO.NOTHING

            if self.primary_keys and len(primaries_in_fields) == len(self.primary_keys):
                query.br.ON.CONFLICT(*self.primary_keys, par=True).br
                cols = [col for col in field_names if col not in self.primary_keys]
                if len(cols) > 0:
                    query.DO.UPDATE.SET(*[f"{col} = excluded.{col}" for col in cols])
                elif returning:
                    query.DO.UPDATE.SET(
                        f"{self.primary_keys[0]} = {self.primary_keys[0]}"
                    )
                else:
                    query.DO.NOTHING
            if returning:
                ret_fields = self.primary_keys if self.primary_keys else ["rowid"]
                query.br.RETURNING(*ret_fields)

            self.query_map[key] = str(query)
        return self.query_map[key]

    def where_args(self, *args):
        return " AND ".join([f"{key} = ?{i}" for i, key in enumerate(args, start=1)])

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

    def insert(self, item: DataclassT):
        params = self.codec.encode(item, as_tuple=False, ignore_none=True)
        field_names = params.keys()
        row = self.execute_one(
            *params.values(), sql_str=self.insert_query(*field_names)
        )
        if row:
            return row[0] if len(self.primary_keys) == 1 else row

    def insert_many(self, items: list[DataclassT]):
        encoded = [
            self.codec.encode(item, as_tuple=True, ignore_none=False) for item in items
        ]
        field_names = self.codec.class_fields.keys()
        return self.execute_many(
            *encoded, sql_str=self.insert_query(*field_names, returning=False)
        )

    def get(
        self,
        key=None,
        select_fields: list[str] = [],
        as_dict=False,
        as_tuple=False,
        single_row=True,
        **kwargs,
    ) -> DataclassT:
        """
        1. establish search
        2. establish select
        """

        if as_dict and as_tuple:
            raise ValueError("as_dict and as _tuple cannot both be true")
        if select_fields and not as_dict and not as_tuple:
            raise ValueError(
                "If select fields are provided either as_dict or as_tuple must be true."
            )

        params = self.parse_constraint_dict(key=key, **kwargs)

        if not params:
            return self.peek(
                key, select_fields=select_fields, as_dict=as_dict, as_tuple=as_tuple
            )

        row_dict = self.select_query(*select_fields, as_dict=True, single_row=single_row, **params)
        if single_row:
            as_obj = not (as_tuple or as_dict)
            decoded = self.codec.decode(row_dict, as_obj=as_obj)
            if as_tuple:
                return tuple(decoded.values())
            else:
                return decoded
        else:
            # row_dict = self.select_query(*select_fields, as_dict=True, single_row=False, **params)
            as_obj = not (as_tuple or as_dict)
            decoded_row = [self.codec.decode(row, as_obj=as_obj) for row in row_dict]
            if as_tuple:
                return [tuple(row.values()) for row in decoded_row]
            else:
                return decoded_row

    def get_all(
        self,
        key=None,
        select_fields: list[str] = [],
        as_dict=False,
        as_tuple=False,
        **kwargs,
    ) -> DataclassT:
        """
        1. establish search
        2. establish select
        """
        return self.get(
            key=key,
            select_fields=select_fields,
            as_dict=as_dict,
            as_tuple=as_tuple,
            single_row=False,
            **kwargs
            
        )



    def parse_constraint_dict(self, key=None, **kwargs):
        params = {}

        for k, v in kwargs.items():
            params[str(k)] = encode_field(self.data_class, k, v)

        if key is not None:
            if isinstance(key, dict):
                params |= key
            elif isinstance(key, Iterable) and not isinstance(key, (str, bytes)):
                kv_zip = zip(self.primary_keys, key, strict=True)
                for k, v in kv_zip:
                    params[str(k)] = encode_field(self.data_class, k, v)
            else:
                if len(self.primary_keys) == 0:
                    pass
                else:
                    if len(self.primary_keys) > 1:
                        raise ValueError(
                            "The number of keys does not match the number of primary keys."
                        )
                    params[str(self.primary_keys[0])] = encode_field(
                        self.data_class, self.primary_keys[0], key
                    )
        return params

    def select_query(self, *args, from_="", as_dict=False, single_row = True, **kwargs):
        """Selects *args columns with **kwargs conditions.

        Returns:
            _type_: _description_
        """
        qb = QueryBuilder(self.connection)
        if not args:
            qb.select("*")
        else:
            qb.select(*args)
        qb.FROM(from_ if from_ else self.table_name)
        if kwargs:
            qb.WHERE(self.where_args(*kwargs.keys()))
            if single_row:
                return qb.execute_one(*kwargs.values(), as_dict=as_dict)
            else:
                return qb.execute(*kwargs.values(), as_dict=as_dict)
        else:
            return None

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
        params = self.parse_constraint_dict(key=key)
        if params:
            query = (
                QueryBuilder()
                .DELETE.FROM(self.table_name)
                .WHERE(self.where_args(*params.keys()))
            )
            self.execute_one(*params.values(), sql_str=str(query))
        elif isinstance(key, int) and not self.primary_keys:
            query = QueryBuilder().DELETE.FROM(self.table_name).WHERE("rowid").eq("?")
            self.execute_one(key, sql_str=str(query))

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
                "Attempting to update table on these overlapping fields %s, %s",
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
