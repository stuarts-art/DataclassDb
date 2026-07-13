__all__ = ["QueryBuilder"]
from typing import Self

import dataclassdb.builders.list_utils as lu
from dataclassdb.builders.function_builder import FunctionBuilder
from dataclassdb.builders.statement_builder import StatementBuilder
from dataclassdb.db_engine import DbEngine
from dataclassdb.dataclass_types import IsDataclass
from dataclassdb.utils import PragmaTableInfo


class QueryBuilder(DbEngine, StatementBuilder, FunctionBuilder):
    _affinity_map = {
        "INT": "INTEGER",
        "INTEGER": "INTEGER",
        "TINYINT": "INTEGER",
        "SMALLINT": "INTEGER",
        "MEDIUMINT": "INTEGER",
        "BIGINT": "INTEGER",
        "UNSIGNED BIG INT": "INTEGER",
        "INT2": "INTEGER",
        "INT8": "INTEGER",
        "CHARACTER": "TEXT",
        "VARCHAR": "TEXT",
        "VARYING CHARACTER": "TEXT",
        "NCHAR": "TEXT",
        "NVARCHAR": "TEXT",
        "TEXT": "TEXT",
        "CLOB": "TEXT",
        "BLOB": "BLOB",
        "REAL": "REAL",
        "DOUBLE": "REAL",
        "DOUBLE PRECISION": "REAL",
        "FLOAT": "REAL",
        "NUMERIC": "REAL",
        "DECIMAL": "REAL",
        "BOOLEAN": "INTEGER",
        "DATE": "TEXT",  # Overridden
        "DATETIME": "TEXT",  # Overridden
    }

    @property
    def eq(self) -> Self:
        return self.add("=")

    @property
    def neq(self) -> Self:
        return self.add("<>")

    @property
    def lpar(self) -> Self:
        return self.add("(")

    @property
    def rpar(self) -> Self:
        return self.add(")")

    @property
    def comma(self) -> Self:
        if self.query:
            self.query[-1] = f"{self.query[-1]},"
        else:
            self.query.append(",")
        return self

    @property
    def end(self):
        if self.query:
            self.query[-1] = f"{self.query[-1]};"
        else:
            self.query.append(";")
        return self

    def par(self, *args, commas=True, quotes=False) -> Self:
        return self.add(*args, commas=commas, quotes=quotes, par=True)

    def quote(self, *args, commas=True, par=False) -> Self:
        return self.add(*args, commas=commas, quotes=True, par=par)

    def dot(self, rside: str = "") -> Self:
        """Appends `.{rside}` to the right of the last item in the query."""
        dot_str = f".{rside}"
        if self.query:
            self.query[-1] = f"{self.query[-1]}{dot_str}"
        else:
            self.add(dot_str)
        return self

    def placeholders(self, *args, count=None, par=True) -> Self:
        return self.add(lu.placeholders(*args, count=count), par=par)

    def get_current_fields(self, _data_class) -> list[PragmaTableInfo]:
        query = QueryBuilder().PRAGMA.Table_info(_data_class)
        output = self.execute(sql_str=str(query), as_dict=True)
        return PragmaTableInfo.from_list(output)

    def get_curr_cols(self, _data_class) -> list[str]:
        row = (
            QueryBuilder(self.connection)
            .SELECT("sql")
            .FROM("sqlite_schema")
            .WHERE("name")
            .eq.quote(_data_class)
            # .AND("name")
            # .eq.quote(_data_class)
        ).execute_one()
        if not row:
            return []

        cols = row[0].split("(", 1)[-1].rsplit(")", 1)[0].split(",")
        cols = [col.replace("\n", "").strip() for col in cols]
        return cols

    def select(self, *args):
        """This version of select handles the case where dot notation
        is used in a select.
        `SELECT user.id -> SELECT user.id AS [user.id]`
        Without this change sqlite will ignore the prefix when creating
        the output row.
        """
        params = []
        for arg in args:
            if "." in arg:
                params.append(f"{arg} AS [{arg}]")
            else:
                params.append(arg)
        return self.SELECT(*params)

    def from_(self, table: str | IsDataclass, as_=""):
        self.FROM(table)
        if as_:
            self.AS(as_)
        return self

    def join(
        self, table: str | IsDataclass, as_="", on="", using_cols=[], join_type=""
    ):
        if on and using_cols:
            raise SyntaxError("Cannot have both 'ON' and 'USING' statements in a join.")
        if join_type:
            self(join_type)
        self.JOIN(table)
        if as_:
            self.AS(as_)
        if on:
            self.ON(on)
        elif using_cols:
            self.USING(lu.flatten(using_cols), par=True)
        return self

    @staticmethod
    def get_sql_col_affinity(col_name) -> str | None:
        if "(" in col_name:
            col = col_name.split("(")[0]
        else:
            col = col_name

        return QueryBuilder._affinity_map.get(col, None)
