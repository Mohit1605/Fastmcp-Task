from schemas.pagination_schema import PaginationResponse

MAX_LIMIT = 10

def paginate(items: list,cursor: int = 0,limit: int = 5):
  
  if cursor < 0:
    return PaginationResponse(
      success=False,
      error="Invalid cursor",
      code="INVALID_CURSOR",
      suggestion="Cursor must be greater than or equal to 0"
    )

  if limit < 1:
    return PaginationResponse(
      success=False,
      error="Invalid limit",
      code="INVALID_LIMIT",
      suggestion="Limit must be greater than 0"
    )

  if limit > MAX_LIMIT:
    return PaginationResponse(
      success=False,
      error="Limit exceeded",
      code="LIMIT_EXCEEDED",
      suggestion=f"Maximum limit allowed is {MAX_LIMIT}"
    )

  total_count = len(items)

  if cursor > total_count:
    return PaginationResponse(
      success=False,
      error="Cursor out of range",
      code="CURSOR_OUT_OF_RANGE",
      suggestion="Provide a valid cursor value"
    )

  paginated_data = items[cursor: cursor + limit]

  next_cursor = cursor + limit

  has_more = next_cursor < total_count

  if not has_more:
    next_cursor = None

  return PaginationResponse(
    success=True,
    data=paginated_data,
    next_cursor=next_cursor,
    has_more=has_more,
    total_count=total_count
  )