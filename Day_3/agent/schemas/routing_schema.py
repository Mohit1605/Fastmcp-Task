from pydantic import BaseModel
from typing import Optional, Literal


class RouteDecision(BaseModel):
    server: Literal["job", "call", "both", "workflow"]
    tool: Optional[str] = None
    workflow: Optional[str] = None
    confidence: float
    reason: Optional[str] = None