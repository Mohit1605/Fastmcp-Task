# core/context.py

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import uuid
import time


@dataclass
class AgentContext:
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    session_id: Optional[str] = None

    start_time: float = field(default_factory=time.time)

    # runtime memory
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_metadata(self, key: str, value: Any):
        self.metadata[key] = value

    def get_latency(self) -> float:
        return time.time() - self.start_time