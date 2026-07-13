from dataclassdb.builders.function_builder import FunctionBuilder
from dataclassdb.builders.statement_builder import StatementBuilder
from dataclassdb.constants import SQL, SQL_FUNC, SQL_FUNC_PRAGMA


def test_function_builder():
    builder = FunctionBuilder()
    for e in [SQL_FUNC, SQL_FUNC_PRAGMA]:
        for func in e:
            func_name = str(func).capitalize()
            method = getattr(builder, func_name)
            assert str(method()) == f"{func_name.lower()}()"
            builder.clear



def test_statement_builder():
    builder = StatementBuilder()
    for e in [SQL]:
        for func in e:
            method = getattr(builder, func.name)
            assert method
            assert str(builder) == str(func)
            builder.clear

