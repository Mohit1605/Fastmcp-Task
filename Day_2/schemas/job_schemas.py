from pydantic import BaseModel, Field
from schemas.types import JobPriority

class CreateJobInput(BaseModel):
  title: str = Field(..., min_length=3, max_length=100)
  description: str = Field(..., min_length=5)
  priority: JobPriority = JobPriority.MEDIUM

class AssignJobInput(BaseModel):
  job_id: str
  technician_id: str

class CloseJobInput(BaseModel):
  job_id: str


class CreateCloseJobResponse(BaseModel):
  success: bool = Field(default=False,description="Indicates the Job was created successful or not.")
  message: str | None = Field(default=None,description="Response message describing the result.")
  job: dict | None = Field(default=None,description="Contains the job details.")
  
  error: str | None = Field(default=None,description="Human readable error message")
  code: str | None = Field(default=None,description="Machine readable error code")
  suggestion: str | None = Field(default=None,description="Suggested resolution")


class AssignJobResponse(BaseModel):
  success: bool = Field(default=False,description="Indicates the Job was assigned successful or not.")
  message: str | None = Field(default=None,description="Response message describing the result of the job assigned.")
  job: dict | None = Field(default=None,description="Contains the assigned job details.")
  technician: dict | None = Field(default=None,description="Contains the assigned technician details.")
  
  error: str | None = Field(default=None,description="Human readable error message")
  code: str | None = Field(default=None,description="Machine readable error code")
  suggestion: str | None = Field(default=None,description="Suggested resolution")


class PaginationInput(BaseModel):
    cursor: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)