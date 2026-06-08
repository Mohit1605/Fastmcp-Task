from pydantic import BaseModel, Field
from typing import Any
from .call_schemas import BaseResponse

class PaginationResponse(BaseResponse):
    data: list[Any] = Field(default_factory=list)

    next_cursor: int | None = Field(default=None)
    has_more: bool = Field(default=False)
    total_count: int = Field(default=0)