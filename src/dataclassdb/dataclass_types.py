from dataclasses import Field
from typing import Mapping, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")
S = TypeVar("S")

@runtime_checkable
class Codec(Protocol):
    def __init__(self, *args, **kwargs): pass
    @staticmethod
    def encode(data: T) -> S:...
    @staticmethod
    def decode(data: S) -> T:...

class CustomCodec(Codec):
    def __init__(self, encode, decode):
        self.encode = encode
        self.decode = decode

@runtime_checkable
class IsDataclass(Protocol):
    __dataclass_fields__: Mapping[str, Field]
