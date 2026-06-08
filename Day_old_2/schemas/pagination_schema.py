from pydantic import BaseModel, Field
from typing import Any

# class PaginationResponse(BaseModel):
#   data: list[Any] = Field(...,description="Paginated response data")
#   next_cursor: int | None = Field(...,description="Cursor for next page")
#   has_more: bool = Field(...,description="Whether more records exist")
#   total_count: int = Field(...,description="Total available records")

class PaginationResponse(BaseModel):
  success : bool = Field(default=False)
  data: list[Any] | None= Field(default=None)
  next_cursor: int | None = Field(default=None)
  has_more: bool = Field(default=False)
  total_count: int | None = Field(default=None)

  error: str | None = Field(default=None)
  code: str | None = Field(default=None)
  suggestion: str | None = Field(default=None)