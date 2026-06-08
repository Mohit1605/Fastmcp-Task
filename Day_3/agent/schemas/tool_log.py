from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime


# class ToolLog(BaseModel):
#     trace_id: Optional[str] = None

#     server: str
#     tool: str

#     args: Dict[str, Any]

#     latency_ms: int
#     response_size_bytes: int

#     success: bool = True
#     error: Optional[str] = None

#     timestamp: datetime = datetime.utcnow()

class ToolLog(BaseModel):
    server: str
    tool: str
    args: dict[str, Any]
    latency_ms: int
    response_size_bytes: int
    success: bool