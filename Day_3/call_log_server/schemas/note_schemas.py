from pydantic import BaseModel
from .call_schemas import BaseResponse
from pydantic import Field

class AddCallNoteInput(BaseModel):
  call_id: str
  note: str

class AddCallNoteResponse(BaseResponse):
  call_id: str | None = None
  note: str | None = None
  total_notes: int = 0

class ListNotesForCallInput(BaseModel):
  call_id: str

class ListNotesForCallResponse(BaseResponse):
  call_id: str | None = None
  notes: list[str] = Field(default_factory=list)
  total_notes: int = 0