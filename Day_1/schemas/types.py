from enum import Enum
from pydantic import BaseModel


class JobStatus(str, Enum):
  OPEN = "open"
  IN_PROGRESS = "in_progress"
  CLOSED = "closed"


class JobPriority(str, Enum):
  LOW = "low"
  MEDIUM = "medium"
  HIGH = "high"


class TechnicianStatus(str, Enum):
  AVAILABLE = "available"
  BUSY = "busy"


class BaseResponse(BaseModel):
  success: bool
  message: str
  next_action: str | None = None