from pydantic import BaseModel, Field


class AddTechnicianInput(BaseModel):
  name: str = Field(..., min_length=2, max_length=50)
  skill: str = Field(..., min_length=2, max_length=50)