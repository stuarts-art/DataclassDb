from dataclasses import is_dataclass
from typing import Self

import dataclassdb.builders.list_utils as lu


class StringBuilder:
    def __init__(self, *args, **kwargs):
        self.sep = " "
        self.query = []
        self.br_count = 0

    def __repr__(self):
        query_str = self.sep.join(map(str, self.query))
        return query_str

    def __eq__(self, value: object) -> bool:
        return str(self) == value

    def __call__(
        self, *args, commas=True, par=False, quotes=False, newline=False, **kwargs
    ) -> Self:
        if not args:
            return self
        else:
            return self.add(
                *args, commas=commas, par=par, quotes=quotes, newline=newline
            )

    @property
    def show(self) -> Self:
        print(self)
        return self

    @property
    def br(self) -> Self:
        self.br_count += 1
        return self

    @property
    def clear(self) -> Self:
        self.query = []
        self.br_count = 0
        return self

    def as_string(self) -> str:
        """Returns the built string and clears the query
        Returns:
            str: _description_
        """
        try:
            return str(self)
        finally:
            self.clear

    def set_sep(self, sep: str) -> Self:
        self.sep = sep
        return self

    def add(
        self, *args, commas=True, par=False, quotes=False, newline=False, **kwargs
    ) -> Self:
        params = [
            arg.__name__ if is_dataclass(arg) else arg
            for arg in lu.flatten(*args)  # type: ignore
        ]
        if quotes:
            params = lu.add_quotes(params)
        if commas:
            params = lu.add_commas(params)
        if par:
            params = lu.add_parenthesis(params)
        if newline:
            if params:
                params[0] = f"\n{params[0]}"
        if self.br_count:
            prefix = "\n" * int(self.br_count)
            params[0] = f"{prefix}{params[0]}"
            self.br_count = 0

        for arg in lu.flatten(params):
            if arg is None or arg == "":
                continue
            else:
                self.query.append(arg)
        return self

    def add_func(self, *args) -> Self:
        params = lu.flatten(*args)
        if not params:
            raise ValueError("Function name must be provided")
        elif len(args) == 1:
            self.add(f"{args[0]}()")
        else:
            params[1:] = lu.add_parenthesis(params[1:])
            params[1] = f"{params[0]}{params[1]}"
            self.add(*params[1:])
        return self
