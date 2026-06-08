from enum import Enum
from pydantic import BaseModel
from schemas.error_schema import ErrorResponse

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
