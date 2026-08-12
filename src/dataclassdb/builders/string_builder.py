from dataclasses import is_dataclass
from typing import Self

import dataclassdb.builders.list_utils as lu


class StringBuilder:
    def __init__(self, *args, **kwargs):
        self.query = []

    def __repr__(self) -> str:
        br_query: list[str] = []
        for cur in map(str, self.query):
            if not br_query or not br_query[-1].endswith("\n"):
                br_query.append(cur)
            else:
                br_query[-1] = f"{br_query[-1]}{cur}"
        return " ".join(br_query)

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

    def show(self) -> Self:
        print(self)
        return self

    def br(self) -> Self:
        if self.query:
            self.query[-1] = f"{self.query[-1]}\n"
        else:
            self.query.append("\n")
        return self

    @property
    def clear(self) -> Self:
        self.query = []

    def as_string(self) -> str:
        """Returns the built string and clears the query
        Returns:
            str: _description_
        """
        try:
            return str(self)
        finally:
            self.clear


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
        if newline and params:
            params[0] = f"\n{params[0]}"

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
