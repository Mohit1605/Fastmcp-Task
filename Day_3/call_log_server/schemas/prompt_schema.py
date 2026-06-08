from pydantic import BaseModel

class QualityReviewInput(BaseModel):
  call_id: str