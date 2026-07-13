"""This script creates the getter and setter sql files from strenums."""

__all__ = ['FunctionBuilder']

from typing import Self

from dataclassdb.builders.string_builder import StringBuilder
from dataclassdb.constants import SQL_FUNC, SQL_FUNC_PRAGMA


class FunctionBuilder(StringBuilder):
    # Generated from scripts/generate_builder_files.py
    def Abs(self, *args) -> Self:
        return self.add_func(SQL_FUNC.ABS, *args)

    def Changes(self, *args) -> Self:
        return self.add_func(SQL_FUNC.CHANGES, *args)

    def Char(self, *args) -> Self:
        return self.add_func(SQL_FUNC.CHAR, *args)

    def Coalesce(self, *args) -> Self:
        return self.add_func(SQL_FUNC.COALESCE, *args)

    def Concat(self, *args) -> Self:
        return self.add_func(SQL_FUNC.CONCAT, *args)

    def Concat_ws(self, *args) -> Self:
        return self.add_func(SQL_FUNC.CONCAT_WS, *args)

    def Format(self, *args) -> Self:
        return self.add_func(SQL_FUNC.FORMAT, *args)

    def Glob(self, *args) -> Self:
        return self.add_func(SQL_FUNC.GLOB, *args)

    def Hex(self, *args) -> Self:
        return self.add_func(SQL_FUNC.HEX, *args)

    def If(self, *args) -> Self:
        return self.add_func(SQL_FUNC.IF, *args)

    def Ifnull(self, *args) -> Self:
        return self.add_func(SQL_FUNC.IFNULL, *args)

    def Iif(self, *args) -> Self:
        return self.add_func(SQL_FUNC.IIF, *args)

    def Instr(self, *args) -> Self:
        return self.add_func(SQL_FUNC.INSTR, *args)

    def Last_insert_rowid(self, *args) -> Self:
        return self.add_func(SQL_FUNC.LAST_INSERT_ROWID, *args)

    def Length(self, *args) -> Self:
        return self.add_func(SQL_FUNC.LENGTH, *args)

    def Like(self, *args) -> Self:
        return self.add_func(SQL_FUNC.LIKE, *args)

    def Likelihood(self, *args) -> Self:
        return self.add_func(SQL_FUNC.LIKELIHOOD, *args)

    def Likely(self, *args) -> Self:
        return self.add_func(SQL_FUNC.LIKELY, *args)

    def Load_extension(self, *args) -> Self:
        return self.add_func(SQL_FUNC.LOAD_EXTENSION, *args)

    def Lower(self, *args) -> Self:
        return self.add_func(SQL_FUNC.LOWER, *args)

    def Ltrim(self, *args) -> Self:
        return self.add_func(SQL_FUNC.LTRIM, *args)

    def Max(self, *args) -> Self:
        return self.add_func(SQL_FUNC.MAX, *args)

    def Min(self, *args) -> Self:
        return self.add_func(SQL_FUNC.MIN, *args)

    def Nullif(self, *args) -> Self:
        return self.add_func(SQL_FUNC.NULLIF, *args)

    def Octet_length(self, *args) -> Self:
        return self.add_func(SQL_FUNC.OCTET_LENGTH, *args)

    def Printf(self, *args) -> Self:
        return self.add_func(SQL_FUNC.PRINTF, *args)

    def Quote(self, *args) -> Self:
        return self.add_func(SQL_FUNC.QUOTE, *args)

    def Random(self, *args) -> Self:
        return self.add_func(SQL_FUNC.RANDOM, *args)

    def Randomblob(self, *args) -> Self:
        return self.add_func(SQL_FUNC.RANDOMBLOB, *args)

    def Replace(self, *args) -> Self:
        return self.add_func(SQL_FUNC.REPLACE, *args)

    def Round(self, *args) -> Self:
        return self.add_func(SQL_FUNC.ROUND, *args)

    def Rtrim(self, *args) -> Self:
        return self.add_func(SQL_FUNC.RTRIM, *args)

    def Sign(self, *args) -> Self:
        return self.add_func(SQL_FUNC.SIGN, *args)

    def Soundex(self, *args) -> Self:
        return self.add_func(SQL_FUNC.SOUNDEX, *args)

    def Sqlite_compileoption_get(self, *args) -> Self:
        return self.add_func(SQL_FUNC.SQLITE_COMPILEOPTION_GET, *args)

    def Sqlite_compileoption_used(self, *args) -> Self:
        return self.add_func(SQL_FUNC.SQLITE_COMPILEOPTION_USED, *args)

    def Sqlite_offset(self, *args) -> Self:
        return self.add_func(SQL_FUNC.SQLITE_OFFSET, *args)

    def Sqlite_source_id(self, *args) -> Self:
        return self.add_func(SQL_FUNC.SQLITE_SOURCE_ID, *args)

    def Sqlite_version(self, *args) -> Self:
        return self.add_func(SQL_FUNC.SQLITE_VERSION, *args)

    def Substr(self, *args) -> Self:
        return self.add_func(SQL_FUNC.SUBSTR, *args)

    def Substring(self, *args) -> Self:
        return self.add_func(SQL_FUNC.SUBSTRING, *args)

    def Total_changes(self, *args) -> Self:
        return self.add_func(SQL_FUNC.TOTAL_CHANGES, *args)

    def Trim(self, *args) -> Self:
        return self.add_func(SQL_FUNC.TRIM, *args)

    def Typeof(self, *args) -> Self:
        return self.add_func(SQL_FUNC.TYPEOF, *args)

    def Unhex(self, *args) -> Self:
        return self.add_func(SQL_FUNC.UNHEX, *args)

    def Unicode(self, *args) -> Self:
        return self.add_func(SQL_FUNC.UNICODE, *args)

    def Unistr(self, *args) -> Self:
        return self.add_func(SQL_FUNC.UNISTR, *args)

    def Unistr_quote(self, *args) -> Self:
        return self.add_func(SQL_FUNC.UNISTR_QUOTE, *args)

    def Unlikely(self, *args) -> Self:
        return self.add_func(SQL_FUNC.UNLIKELY, *args)

    def Upper(self, *args) -> Self:
        return self.add_func(SQL_FUNC.UPPER, *args)

    def Zeroblob(self, *args) -> Self:
        return self.add_func(SQL_FUNC.ZEROBLOB, *args)

    def Avg(self, *args) -> Self:
        return self.add_func(SQL_FUNC.AVG, *args)

    def Group_concat(self, *args) -> Self:
        return self.add_func(SQL_FUNC.GROUP_CONCAT, *args)

    def Median(self, *args) -> Self:
        return self.add_func(SQL_FUNC.MEDIAN, *args)

    def Percentile(self, *args) -> Self:
        return self.add_func(SQL_FUNC.PERCENTILE, *args)

    def Percentile_cont(self, *args) -> Self:
        return self.add_func(SQL_FUNC.PERCENTILE_CONT, *args)

    def Percentile_disc(self, *args) -> Self:
        return self.add_func(SQL_FUNC.PERCENTILE_DISC, *args)

    def String_agg(self, *args) -> Self:
        return self.add_func(SQL_FUNC.STRING_AGG, *args)

    def Sum(self, *args) -> Self:
        return self.add_func(SQL_FUNC.SUM, *args)

    def Total(self, *args) -> Self:
        return self.add_func(SQL_FUNC.TOTAL, *args)

    def Count(self, *args) -> Self:
        return self.add_func(SQL_FUNC.COUNT, *args)

    def Date(self, *args) -> Self:
        return self.add_func(SQL_FUNC.DATE, *args)

    def Time(self, *args) -> Self:
        return self.add_func(SQL_FUNC.TIME, *args)

    def Datetime(self, *args) -> Self:
        return self.add_func(SQL_FUNC.DATETIME, *args)

    def Julianday(self, *args) -> Self:
        return self.add_func(SQL_FUNC.JULIANDAY, *args)

    def Unixepoch(self, *args) -> Self:
        return self.add_func(SQL_FUNC.UNIXEPOCH, *args)

    def Strftime(self, *args) -> Self:
        return self.add_func(SQL_FUNC.STRFTIME, *args)

    def Timediff(self, *args) -> Self:
        return self.add_func(SQL_FUNC.TIMEDIFF, *args)

    def Integer(self, *args) -> Self:
        return self.add_func(SQL_FUNC.INTEGER, *args)

    def Text(self, *args) -> Self:
        return self.add_func(SQL_FUNC.TEXT, *args)

    def Blob(self, *args) -> Self:
        return self.add_func(SQL_FUNC.BLOB, *args)

    def Real(self, *args) -> Self:
        return self.add_func(SQL_FUNC.REAL, *args)

    def Numeric(self, *args) -> Self:
        return self.add_func(SQL_FUNC.NUMERIC, *args)

    def Any(self, *args) -> Self:
        return self.add_func(SQL_FUNC.ANY, *args)

    def Analysis_limit(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.ANALYSIS_LIMIT, *args)

    def Application_id(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.APPLICATION_ID, *args)

    def Auto_vacuum(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.AUTO_VACUUM, *args)

    def Automatic_index(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.AUTOMATIC_INDEX, *args)

    def Busy_timeout(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.BUSY_TIMEOUT, *args)

    def Cache_size(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.CACHE_SIZE, *args)

    def Cache_spill(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.CACHE_SPILL, *args)

    def Cell_size_check(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.CELL_SIZE_CHECK, *args)

    def Checkpoint_fullfsync(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.CHECKPOINT_FULLFSYNC, *args)

    def Collation_list(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.COLLATION_LIST, *args)

    def Compile_options(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.COMPILE_OPTIONS, *args)

    def Data_version(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.DATA_VERSION, *args)

    def Database_list(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.DATABASE_LIST, *args)

    def Defer_foreign_keys(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.DEFER_FOREIGN_KEYS, *args)

    def Encoding(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.ENCODING, *args)

    def Foreign_key_check(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.FOREIGN_KEY_CHECK, *args)

    def Foreign_key_list(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.FOREIGN_KEY_LIST, *args)

    def Foreign_keys(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.FOREIGN_KEYS, *args)

    def Freelist_count(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.FREELIST_COUNT, *args)

    def Fullfsync(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.FULLFSYNC, *args)

    def Function_list(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.FUNCTION_LIST, *args)

    def Hard_heap_limit(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.HARD_HEAP_LIMIT, *args)

    def Ignore_check_constraints(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.IGNORE_CHECK_CONSTRAINTS, *args)

    def Incremental_vacuum(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.INCREMENTAL_VACUUM, *args)

    def Index_info(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.INDEX_INFO, *args)

    def Index_list(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.INDEX_LIST, *args)

    def Index_xinfo(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.INDEX_XINFO, *args)

    def Integrity_check(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.INTEGRITY_CHECK, *args)

    def Journal_mode(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.JOURNAL_MODE, *args)

    def Journal_size_limit(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.JOURNAL_SIZE_LIMIT, *args)

    def Legacy_alter_table(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.LEGACY_ALTER_TABLE, *args)

    def Legacy_file_format(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.LEGACY_FILE_FORMAT, *args)

    def Locking_mode(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.LOCKING_MODE, *args)

    def Max_page_count(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.MAX_PAGE_COUNT, *args)

    def Mmap_size(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.MMAP_SIZE, *args)

    def Module_list(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.MODULE_LIST, *args)

    def Optimize(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.OPTIMIZE, *args)

    def Page_count(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.PAGE_COUNT, *args)

    def Page_size(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.PAGE_SIZE, *args)

    def Pragma_list(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.PRAGMA_LIST, *args)

    def Query_only(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.QUERY_ONLY, *args)

    def Quick_check(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.QUICK_CHECK, *args)

    def Read_uncommitted(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.READ_UNCOMMITTED, *args)

    def Recursive_triggers(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.RECURSIVE_TRIGGERS, *args)

    def Reverse_unordered_selects(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.REVERSE_UNORDERED_SELECTS, *args)

    def Secure_delete(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.SECURE_DELETE, *args)

    def Shrink_memory(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.SHRINK_MEMORY, *args)

    def Soft_heap_limit(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.SOFT_HEAP_LIMIT, *args)

    def Synchronous(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.SYNCHRONOUS, *args)

    def Table_info(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.TABLE_INFO, *args)

    def Table_list(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.TABLE_LIST, *args)

    def Table_xinfo(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.TABLE_XINFO, *args)

    def Temp_store(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.TEMP_STORE, *args)

    def Threads(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.THREADS, *args)

    def Trusted_schema(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.TRUSTED_SCHEMA, *args)

    def User_version(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.USER_VERSION, *args)

    def Wal_autocheckpoint(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.WAL_AUTOCHECKPOINT, *args)

    def Wal_checkpoint(self, *args) -> Self:
        return self.add_func(SQL_FUNC_PRAGMA.WAL_CHECKPOINT, *args)
