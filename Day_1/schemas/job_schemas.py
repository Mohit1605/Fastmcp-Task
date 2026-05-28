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