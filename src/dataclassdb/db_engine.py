import logging
import sqlite3

from dataclassdb.builders.string_builder import StringBuilder
from dataclassdb.utils import dict_factory

logger = logging.getLogger()


class DbEngine(StringBuilder):
    def __init__(
        self,
        connection: sqlite3.Connection | str = "",  # type: ignore
        **kwargs,
    ):
        self.connection: sqlite3.Connection
        self.connection_owner = False
        self.has_connection = False
        self.connection_name = ""

        if connection:
            self.has_connection = True
            if isinstance(connection, sqlite3.Connection):
                self.connection = connection
            else:
                self.connection = sqlite3.Connection(connection)
                self.connection_owner = True
                self.connection_name = connection
                self.enable_wal()
                logger.info("Connection for %s created.", self.connection_name)

        super().__init__(connection=connection, **kwargs)
        # super(DbExecutor, self).__init__()

    def __enter__(self):
        if not self.has_connection:
            raise ValueError("Connection must be set to use context manager")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection_owner and self.has_connection:
            logger.info("Committing DB.")
            self.connection.commit()
            logger.info("Closing DB.")
            self.connection.close()
        return False

    def enable_wal(self) -> None:
        self.execute_script(
            "PRAGMA journal_mode=WAL;\n"
            "PRAGMA synchronous=NORMAL;\n"
            "PRAGMA busy_timeout = 5000;\n"
            "PRAGMA cache_size = -20000;\n"  # 20MB
            "PRAGMA foreign_keys = true;\n"
            "PRAGMA temp_store = memory;"
        )

    def execute_script(self, sql_script=None, as_dict=False, commit=False):
        if not self.has_connection:
            raise ValueError("Connection must be set to use sql commands.")

        try:
            if sql_script is None:
                sql_script = str(self)
            if not sql_script:
                raise ValueError("Query is empty")
            cur = self.connection.cursor()  # type: ignore
            if as_dict:
                cur.row_factory = dict_factory
            output = cur.executescript(sql_script)
            if commit:
                self.connection.commit()  # type: ignore
            return output
        finally:
            self.clear

    def execute_one(self, *args, sql_str=None, commit=False, as_dict=False):
        return self.execute(
            *args, sql_str=sql_str, commit=commit, single_row=True, as_dict=as_dict
        )

    def execute(
        self, *args, sql_str=None, commit=False, single_row=False, as_dict=False
    ):
        if not self.has_connection:
            raise ValueError("Connection must be set to use sql commands.")
        try:
            params = tuple(args) if args else ()
            if sql_str is None:
                query_str = str(self)
            else:
                query_str = str(sql_str)

            if not query_str:
                raise ValueError("Query is empty")

            if not query_str.endswith(";"):
                query_str = f"{query_str};"

            cur = self.connection.cursor()
            if as_dict:
                cur.row_factory = dict_factory

            if "\n" in query_str:
                logger.debug(
                    "Executing Query: \n    %s", query_str.replace("\n", "\n    ")
                )
                logger.debug(
                    "Using Params   :\n    %s", "\n    ".join(map(str, params))
                )
            else:
                logger.debug("Executing Query: %s", query_str)
                logger.debug("Using Params   : %s", params)

            cur.execute(query_str, params)

            if single_row:
                rows = cur.fetchone()
                return rows
            else:
                rows = cur.fetchall()
            if commit:
                self.connection.commit()
            return rows
        finally:
            self.clear
