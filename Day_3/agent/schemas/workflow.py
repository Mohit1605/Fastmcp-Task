from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class WorkflowStep(BaseModel):
    step_name: str
    input: Dict[str, Any]
    output: Dict[str, Any]


class WorkflowResult(BaseModel):
    workflow_name: str
    steps: List[WorkflowStep]
    final_output: Dict[str, Any]
    success: bool = True
    error: Optional[str] = None