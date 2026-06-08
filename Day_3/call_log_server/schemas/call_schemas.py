from datetime import datetime
from pydantic import BaseModel,Field
from schemas.types import CallStatus, CallOutcome


class BaseResponse(BaseModel):
    success: bool

    error: str | None = None
    code: str | None = None
    suggestion: str | None = None

class Call(BaseModel):
    call_id: str

    customer_name: str
    phone_number: str

    status: CallStatus
    outcome: CallOutcome | None = None

    duration_seconds: int

    transcript: str

    notes: list[str] = []

    created_at: datetime
    updated_at: datetime


class LogCallInput(BaseModel):
    customer_name: str
    phone_number: str

    duration_seconds: int

    transcript: str

    status: CallStatus = CallStatus.OPEN

class LogCallResponse(BaseResponse):
    call: dict | None = None

class GetCallInput(BaseModel):
    call_id: str
class GetCallResponse(BaseResponse):
    call: dict | None = None




class ListCallsInput(BaseModel):
    cursor: int = 0
    limit: int = 10
class ListCallsResponse(BaseResponse):
    calls: list[dict] = []

    count: int = 0

    next_cursor: int | None = None
    has_more: bool = False

    total_count: int = 0

class ListCallsByStatusInput(BaseModel):
    status: CallStatus

    cursor: int = 0
    limit: int = 10
class ListCallsByStatusResponse(BaseResponse):
    calls: list[dict] = []

    count: int = 0

    next_cursor: int | None = None
    has_more: bool = False
    total_count: int = 0

class UpdateCallOutcomeInput(BaseModel):
    call_id: str

    outcome: CallOutcome
    status: CallStatus
class UpdateCallOutcomeResponse(BaseResponse):
    call: dict | None = None

class DeleteCallInput(BaseModel):
    call_id: str
class DeleteCallResponse(BaseResponse):
    deleted_call_id: str | None = None

class GetStatsInput(BaseModel):
    pass
class GetStatsResponse(BaseResponse):
    total_calls: int = 0
    status_counts: dict[str, int] = Field(default_factory=dict)
    outcome_counts: dict[str, int] = Field(default_factory=dict)

class GetCallSummaryInput(BaseModel):
    call_id: str
class GetCallSummaryResponse(BaseResponse):
    call_id: str | None = None
    summary: str | None = None
