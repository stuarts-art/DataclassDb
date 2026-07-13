# Manually generates statement and function builder files from constants.
#    - DataclassDb\src\dataclassdb\statement_builder.py
#    - DataclassDb\src\dataclassdb\statement_getter.py
#    - DataclassDb\src\dataclassdb\function_builder.py
#    - DataclassDb\src\dataclassdb\function_getter.py

import pathlib

from dataclassdb.constants import SQL, SQL_FUNC, SQL_FUNC_PRAGMA


def main():
    create_builders = True
    create_getters = False

    if create_builders:
        p = pathlib.Path(__file__).resolve().parent.parent
        builder_folder = p / "src" / "dataclassdb" / "builders"

        builder_text = build_builder_file(
            class_name="StatementBuilder", enum_list=[SQL], as_property=True
        )
        file_name = builder_folder / "statement_builder.py"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(builder_text)
        print(f"Created File: {file_name}")

    if create_getters:
        getter_text = build_getter_file([SQL], as_property=True)
        file_name = builder_folder / "statement_getter.py"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(getter_text)
        print(f"Created File: {file_name}")

    if create_builders:
        builder_text = build_builder_file(
            class_name="FunctionBuilder",
            enum_list=[SQL_FUNC, SQL_FUNC_PRAGMA],
            as_property=False,
        )
        file_name = builder_folder / "function_builder.py"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(builder_text)
        print(f"Created File: {file_name}")

    if create_getters:
        getter_text = build_getter_file([SQL_FUNC, SQL_FUNC_PRAGMA], as_property=False)
        file_name = builder_folder / "function_getter.py"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(getter_text)
        print(f"Created File: {file_name}")


def build_builder_file(class_name="", enum_list=[], as_property=True):
    lines = []
    parent = "StringBuilder"
    lines.append(
        '"""This script creates the getter and setter sql files from strenums."""\n'
    )
    lines.append(f"__all__ = ['{class_name}']\n")
    lines.append("from typing import Self\n")
    lines.append(f"from dataclassdb.builders.string_builder import {parent}")
    lines.append(
        f"from dataclassdb.constants import {', '.join([enum.__name__ for enum in enum_list])}\n\n"
    )
    lines.append(f"class {class_name}({parent}):")
    lines.append("    # Generated from scripts/generate_builder_files.py")

    for e in [item for nested in enum_list for item in nested]:
        if as_property:  # Add statements properties
            name = e.name
            lines.append(
                f"    @property\n"
                f"    def {name}(self) -> Self:\n"
                f"        return self.add({e.__class__.__name__}.{e.name})\n"
            )
        else:  # Add Functions as normal functions
            name = e.name.capitalize()
            lines.append(
                f"    def {name}(self, *args) -> Self:\n"
                f"        return self.add_func({e.__class__.__name__}.{e.name}, *args)\n"
            )
    return "\n".join(lines)


def build_getter_file(enum_list=[], as_property=True):
    lines = []
    header = []
    lines.append("from dataclassdb.builders.query_builder import QueryBuilder\n")
    header.append("__all__ = [")
    header_line = "    "

    for e in [item for nested in enum_list for item in nested]:
        if as_property:  # Add statements properties
            name = e.name
            lines.append(
                f"def {e.name}(*args, commas=True, par=False, quotes=False, **kwargs) -> QueryBuilder:"
            )
            lines.append(
                f"   return QueryBuilder().{e.name}(*args, commas=commas, par=par, quotes=quotes, **kwargs)"
            )
            lines.append("")
        else:  # Add Functions as normal functions
            name = e.name.capitalize()
            lines.append(f"def {name}(*args) -> QueryBuilder:")
            lines.append(f"   return QueryBuilder().{name}(*args)")
            lines.append("")

        if len(header_line) + len(name) > 76:
            header.append(header_line)
            header_line = f'    "{name}",'
        else:
            header_line += f' "{name}",'

    header_line = header_line[:-1]
    header.append(header_line)
    header.append("]\n")
    return "\n".join(header + lines)


if __name__ == "__main__":
    main()
