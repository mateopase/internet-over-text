from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    items: list[T]
    has_more: bool