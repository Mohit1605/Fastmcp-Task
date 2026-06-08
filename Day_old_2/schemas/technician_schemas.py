from pydantic import BaseModel, Field

class AddTechnicianInput(BaseModel):
  name: str = Field(..., min_length=2, max_length=50)
  skill: str = Field(..., min_length=2, max_length=50)

class CreateTechnicianResponse(BaseModel):
  success: bool = Field(default=False,description="Indicates the technician was create successful or not.")
  message: str | None = Field(default=None,description="Response message describing the result of the technician creation.")
  technician: dict | None = Field(default=None,description="Contains the created technician details.")

  error: str | None = Field(default=None,description="Human readable error message")
  code: str | None = Field(default=None,description="Machine readable error code")
  suggestion: str | None = Field(default=None,description="Suggested resolution")