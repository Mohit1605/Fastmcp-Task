from core.state import calls
from schemas.call_schemas import Call
from typing import List
from schemas.types import CallStatus

def recent_calls(n: int) -> List[Call]:
  sorted_calls = sorted(
        calls.values(),
        key=lambda call: call["created_at"],
        reverse=True
    )

  return [Call(**call) for call in sorted_calls[:n]]


def failed_calls() -> List[Call]:
  results = []

  for call in calls.values():
    status = call["status"]

    if str(status) == CallStatus.FAILED.value:
      results.append(Call(**call))

  return results