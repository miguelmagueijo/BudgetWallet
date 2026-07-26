from typing import Any, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")

class ArrayDataResponseModel(BaseModel, Generic[T]):
    data: list[T]
    meta: dict[str, Any] | None = None

class ObjectDataResponseModel(BaseModel, Generic[T]):
    data: T
    meta: dict[str, Any] | None = None