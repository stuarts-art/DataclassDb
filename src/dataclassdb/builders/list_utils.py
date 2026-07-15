from dataclasses import is_dataclass

__all__ = ["flatten", "add_commas", "add_parenthesis", "add_quotes", "placeholders"]


def _flatten_generator(*args):
    for arg in args:
        if isinstance(arg, list) | isinstance(arg, tuple):
            yield from _flatten_generator(*arg)
        else:
            yield arg


def flatten(*args):
    return list(_flatten_generator(*args))


def add_commas(*args):
    params = flatten(*args)
    if len(params) > 1:
        params[:-1] = [f"{param}," for param in params[:-1]]
    return params


def add_parenthesis(*args):
    params = flatten(*args)
    params = [item.__name__ if is_dataclass(item) else item for item in params]
    if not params:
        return ["()"]
    elif len(params) == 1:
        params[0] = f"({params[0]})"
    else:
        params[0] = f"({params[0]}"
        params[-1] = f"{params[-1]})"
    return params


def add_quotes(*args):
    params = [f'"{item}"' for item in flatten(*args)]
    return params


def placeholders(*args, count=None):
    if count:
        return ["?"] * count
    else:
        return ["?"] * len(flatten(*args)) if args else []
