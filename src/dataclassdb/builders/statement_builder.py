"""This script creates the getter and setter sql files from strenums."""

__all__ = ['StatementBuilder']

from typing import Self

from dataclassdb.builders.string_builder import StringBuilder
from dataclassdb.constants import SQL


class StatementBuilder(StringBuilder):
    # Generated from scripts/generate_builder_files.py
    @property
    def ABORT(self) -> Self:
        return self.add(SQL.ABORT)

    @property
    def ACTION(self) -> Self:
        return self.add(SQL.ACTION)

    @property
    def ADD(self) -> Self:
        return self.add(SQL.ADD)

    @property
    def AFTER(self) -> Self:
        return self.add(SQL.AFTER)

    @property
    def ALL(self) -> Self:
        return self.add(SQL.ALL)

    @property
    def ALTER(self) -> Self:
        return self.add(SQL.ALTER)

    @property
    def ALWAYS(self) -> Self:
        return self.add(SQL.ALWAYS)

    @property
    def ANALYZE(self) -> Self:
        return self.add(SQL.ANALYZE)

    @property
    def AND(self) -> Self:
        return self.add(SQL.AND)

    @property
    def AS(self) -> Self:
        return self.add(SQL.AS)

    @property
    def ASC(self) -> Self:
        return self.add(SQL.ASC)

    @property
    def ATTACH(self) -> Self:
        return self.add(SQL.ATTACH)

    @property
    def AUTOINCREMENT(self) -> Self:
        return self.add(SQL.AUTOINCREMENT)

    @property
    def BEFORE(self) -> Self:
        return self.add(SQL.BEFORE)

    @property
    def BEGIN(self) -> Self:
        return self.add(SQL.BEGIN)

    @property
    def BETWEEN(self) -> Self:
        return self.add(SQL.BETWEEN)

    @property
    def BY(self) -> Self:
        return self.add(SQL.BY)

    @property
    def CASCADE(self) -> Self:
        return self.add(SQL.CASCADE)

    @property
    def CASE(self) -> Self:
        return self.add(SQL.CASE)

    @property
    def CAST(self) -> Self:
        return self.add(SQL.CAST)

    @property
    def CHECK(self) -> Self:
        return self.add(SQL.CHECK)

    @property
    def COLLATE(self) -> Self:
        return self.add(SQL.COLLATE)

    @property
    def COLUMN(self) -> Self:
        return self.add(SQL.COLUMN)

    @property
    def COMMIT(self) -> Self:
        return self.add(SQL.COMMIT)

    @property
    def CONFLICT(self) -> Self:
        return self.add(SQL.CONFLICT)

    @property
    def CONSTRAINT(self) -> Self:
        return self.add(SQL.CONSTRAINT)

    @property
    def CREATE(self) -> Self:
        return self.add(SQL.CREATE)

    @property
    def CROSS(self) -> Self:
        return self.add(SQL.CROSS)

    @property
    def CURRENT(self) -> Self:
        return self.add(SQL.CURRENT)

    @property
    def CURRENT_DATE(self) -> Self:
        return self.add(SQL.CURRENT_DATE)

    @property
    def CURRENT_TIME(self) -> Self:
        return self.add(SQL.CURRENT_TIME)

    @property
    def CURRENT_TIMESTAMP(self) -> Self:
        return self.add(SQL.CURRENT_TIMESTAMP)

    @property
    def DATABASE(self) -> Self:
        return self.add(SQL.DATABASE)

    @property
    def DEFAULT(self) -> Self:
        return self.add(SQL.DEFAULT)

    @property
    def DEFERRABLE(self) -> Self:
        return self.add(SQL.DEFERRABLE)

    @property
    def DEFERRED(self) -> Self:
        return self.add(SQL.DEFERRED)

    @property
    def DELETE(self) -> Self:
        return self.add(SQL.DELETE)

    @property
    def DESC(self) -> Self:
        return self.add(SQL.DESC)

    @property
    def DETACH(self) -> Self:
        return self.add(SQL.DETACH)

    @property
    def DISTINCT(self) -> Self:
        return self.add(SQL.DISTINCT)

    @property
    def DO(self) -> Self:
        return self.add(SQL.DO)

    @property
    def DROP(self) -> Self:
        return self.add(SQL.DROP)

    @property
    def EACH(self) -> Self:
        return self.add(SQL.EACH)

    @property
    def ELSE(self) -> Self:
        return self.add(SQL.ELSE)

    @property
    def END(self) -> Self:
        return self.add(SQL.END)

    @property
    def ESCAPE(self) -> Self:
        return self.add(SQL.ESCAPE)

    @property
    def EXCEPT(self) -> Self:
        return self.add(SQL.EXCEPT)

    @property
    def EXCLUDE(self) -> Self:
        return self.add(SQL.EXCLUDE)

    @property
    def EXCLUSIVE(self) -> Self:
        return self.add(SQL.EXCLUSIVE)

    @property
    def EXISTS(self) -> Self:
        return self.add(SQL.EXISTS)

    @property
    def EXPLAIN(self) -> Self:
        return self.add(SQL.EXPLAIN)

    @property
    def FAIL(self) -> Self:
        return self.add(SQL.FAIL)

    @property
    def FILTER(self) -> Self:
        return self.add(SQL.FILTER)

    @property
    def FIRST(self) -> Self:
        return self.add(SQL.FIRST)

    @property
    def FOLLOWING(self) -> Self:
        return self.add(SQL.FOLLOWING)

    @property
    def FOR(self) -> Self:
        return self.add(SQL.FOR)

    @property
    def FOREIGN(self) -> Self:
        return self.add(SQL.FOREIGN)

    @property
    def FROM(self) -> Self:
        return self.add(SQL.FROM)

    @property
    def FULL(self) -> Self:
        return self.add(SQL.FULL)

    @property
    def GENERATED(self) -> Self:
        return self.add(SQL.GENERATED)

    @property
    def GLOB(self) -> Self:
        return self.add(SQL.GLOB)

    @property
    def GROUP(self) -> Self:
        return self.add(SQL.GROUP)

    @property
    def GROUPS(self) -> Self:
        return self.add(SQL.GROUPS)

    @property
    def HAVING(self) -> Self:
        return self.add(SQL.HAVING)

    @property
    def IF(self) -> Self:
        return self.add(SQL.IF)

    @property
    def IGNORE(self) -> Self:
        return self.add(SQL.IGNORE)

    @property
    def IMMEDIATE(self) -> Self:
        return self.add(SQL.IMMEDIATE)

    @property
    def IN(self) -> Self:
        return self.add(SQL.IN)

    @property
    def INDEX(self) -> Self:
        return self.add(SQL.INDEX)

    @property
    def INDEXED(self) -> Self:
        return self.add(SQL.INDEXED)

    @property
    def INITIALLY(self) -> Self:
        return self.add(SQL.INITIALLY)

    @property
    def INNER(self) -> Self:
        return self.add(SQL.INNER)

    @property
    def INSERT(self) -> Self:
        return self.add(SQL.INSERT)

    @property
    def INSTEAD(self) -> Self:
        return self.add(SQL.INSTEAD)

    @property
    def INTERSECT(self) -> Self:
        return self.add(SQL.INTERSECT)

    @property
    def INTO(self) -> Self:
        return self.add(SQL.INTO)

    @property
    def IS(self) -> Self:
        return self.add(SQL.IS)

    @property
    def ISNULL(self) -> Self:
        return self.add(SQL.ISNULL)

    @property
    def JOIN(self) -> Self:
        return self.add(SQL.JOIN)

    @property
    def KEY(self) -> Self:
        return self.add(SQL.KEY)

    @property
    def LAST(self) -> Self:
        return self.add(SQL.LAST)

    @property
    def LEFT(self) -> Self:
        return self.add(SQL.LEFT)

    @property
    def LIKE(self) -> Self:
        return self.add(SQL.LIKE)

    @property
    def LIMIT(self) -> Self:
        return self.add(SQL.LIMIT)

    @property
    def MATCH(self) -> Self:
        return self.add(SQL.MATCH)

    @property
    def MATERIALIZED(self) -> Self:
        return self.add(SQL.MATERIALIZED)

    @property
    def NATURAL(self) -> Self:
        return self.add(SQL.NATURAL)

    @property
    def NO(self) -> Self:
        return self.add(SQL.NO)

    @property
    def NOT(self) -> Self:
        return self.add(SQL.NOT)

    @property
    def NOTHING(self) -> Self:
        return self.add(SQL.NOTHING)

    @property
    def NOTNULL(self) -> Self:
        return self.add(SQL.NOTNULL)

    @property
    def NULL(self) -> Self:
        return self.add(SQL.NULL)

    @property
    def NULLS(self) -> Self:
        return self.add(SQL.NULLS)

    @property
    def OF(self) -> Self:
        return self.add(SQL.OF)

    @property
    def OFFSET(self) -> Self:
        return self.add(SQL.OFFSET)

    @property
    def ON(self) -> Self:
        return self.add(SQL.ON)

    @property
    def OR(self) -> Self:
        return self.add(SQL.OR)

    @property
    def ORDER(self) -> Self:
        return self.add(SQL.ORDER)

    @property
    def OTHERS(self) -> Self:
        return self.add(SQL.OTHERS)

    @property
    def OUTER(self) -> Self:
        return self.add(SQL.OUTER)

    @property
    def OVER(self) -> Self:
        return self.add(SQL.OVER)

    @property
    def PARTITION(self) -> Self:
        return self.add(SQL.PARTITION)

    @property
    def PLAN(self) -> Self:
        return self.add(SQL.PLAN)

    @property
    def PRAGMA(self) -> Self:
        return self.add(SQL.PRAGMA)

    @property
    def PRECEDING(self) -> Self:
        return self.add(SQL.PRECEDING)

    @property
    def PRIMARY(self) -> Self:
        return self.add(SQL.PRIMARY)

    @property
    def PRIMARY_KEY(self) -> Self:
        return self.add(SQL.PRIMARY_KEY)

    @property
    def QUERY(self) -> Self:
        return self.add(SQL.QUERY)

    @property
    def RAISE(self) -> Self:
        return self.add(SQL.RAISE)

    @property
    def RANGE(self) -> Self:
        return self.add(SQL.RANGE)

    @property
    def RECURSIVE(self) -> Self:
        return self.add(SQL.RECURSIVE)

    @property
    def REFERENCES(self) -> Self:
        return self.add(SQL.REFERENCES)

    @property
    def REGEXP(self) -> Self:
        return self.add(SQL.REGEXP)

    @property
    def REINDEX(self) -> Self:
        return self.add(SQL.REINDEX)

    @property
    def RELEASE(self) -> Self:
        return self.add(SQL.RELEASE)

    @property
    def RENAME(self) -> Self:
        return self.add(SQL.RENAME)

    @property
    def REPLACE(self) -> Self:
        return self.add(SQL.REPLACE)

    @property
    def RESTRICT(self) -> Self:
        return self.add(SQL.RESTRICT)

    @property
    def RETURNING(self) -> Self:
        return self.add(SQL.RETURNING)

    @property
    def RIGHT(self) -> Self:
        return self.add(SQL.RIGHT)

    @property
    def ROLLBACK(self) -> Self:
        return self.add(SQL.ROLLBACK)

    @property
    def ROW(self) -> Self:
        return self.add(SQL.ROW)

    @property
    def ROWS(self) -> Self:
        return self.add(SQL.ROWS)

    @property
    def SAVEPOINT(self) -> Self:
        return self.add(SQL.SAVEPOINT)

    @property
    def SELECT(self) -> Self:
        return self.add(SQL.SELECT)

    @property
    def SET(self) -> Self:
        return self.add(SQL.SET)

    @property
    def STORED(self) -> Self:
        return self.add(SQL.STORED)

    @property
    def TABLE(self) -> Self:
        return self.add(SQL.TABLE)

    @property
    def TEMP(self) -> Self:
        return self.add(SQL.TEMP)

    @property
    def TEMPORARY(self) -> Self:
        return self.add(SQL.TEMPORARY)

    @property
    def THEN(self) -> Self:
        return self.add(SQL.THEN)

    @property
    def TIES(self) -> Self:
        return self.add(SQL.TIES)

    @property
    def TO(self) -> Self:
        return self.add(SQL.TO)

    @property
    def TRANSACTION(self) -> Self:
        return self.add(SQL.TRANSACTION)

    @property
    def TRIGGER(self) -> Self:
        return self.add(SQL.TRIGGER)

    @property
    def UNBOUNDED(self) -> Self:
        return self.add(SQL.UNBOUNDED)

    @property
    def UNION(self) -> Self:
        return self.add(SQL.UNION)

    @property
    def UNIQUE(self) -> Self:
        return self.add(SQL.UNIQUE)

    @property
    def UPDATE(self) -> Self:
        return self.add(SQL.UPDATE)

    @property
    def USING(self) -> Self:
        return self.add(SQL.USING)

    @property
    def VACUUM(self) -> Self:
        return self.add(SQL.VACUUM)

    @property
    def VALUES(self) -> Self:
        return self.add(SQL.VALUES)

    @property
    def VIEW(self) -> Self:
        return self.add(SQL.VIEW)

    @property
    def VIRTUAL(self) -> Self:
        return self.add(SQL.VIRTUAL)

    @property
    def WHEN(self) -> Self:
        return self.add(SQL.WHEN)

    @property
    def WHERE(self) -> Self:
        return self.add(SQL.WHERE)

    @property
    def WINDOW(self) -> Self:
        return self.add(SQL.WINDOW)

    @property
    def WITH(self) -> Self:
        return self.add(SQL.WITH)

    @property
    def WITHOUT(self) -> Self:
        return self.add(SQL.WITHOUT)

    @property
    def INTEGER(self) -> Self:
        return self.add(SQL.INTEGER)

    @property
    def TEXT(self) -> Self:
        return self.add(SQL.TEXT)

    @property
    def BLOB(self) -> Self:
        return self.add(SQL.BLOB)

    @property
    def REAL(self) -> Self:
        return self.add(SQL.REAL)

    @property
    def NUMERIC(self) -> Self:
        return self.add(SQL.NUMERIC)

    @property
    def ANY(self) -> Self:
        return self.add(SQL.ANY)

    @property
    def OLD(self) -> Self:
        return self.add(SQL.OLD)
