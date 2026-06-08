from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
  error: str = Field(...,description="Human readable error message")
  code: str = Field(...,description="Machine readable error code")
  suggestion: str = Field(...,description="Suggested resolution for the client")

