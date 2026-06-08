from schemas.error_schema import ErrorResponse

def error_response(error: str,code: str,suggestion: str) -> dict:
  """
  Standardized error response helper.
  """

  return ErrorResponse(
      error=error,
      code=code,
      suggestion=suggestion
  ).model_dump()


def auth_http_error(error: str,hint: str):
    return {
        "error": error,
        "hint": hint
    }