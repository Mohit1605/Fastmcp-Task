from core.state import calls


def quality_review(call_id: str) -> str:

  if call_id not in calls:
    return f"Call '{call_id}' not found."

  call = calls[call_id]
  transcript = call["transcript"]
  duration = call["duration_seconds"]
  status = call["status"]
  outcome = call.get("outcome")

  return f"""
          You are a call quality analyst.

          Review the following customer support call and score it.

          Evaluation Criteria:

          1. Resolution Score (1-10)
          - Was the customer's issue resolved?
          - Were appropriate actions taken?

          2. Clarity Score (1-10)
          - Was communication clear?
          - Were instructions understandable?

          3. Duration Score (1-10)
          - Was the call length appropriate?
          - Was time used efficiently?

          Call Information

          Call ID:
          {call_id}

          Status:
          {status}

          Outcome:
          {outcome}

          Duration:
          {duration} seconds

          Transcript:
          {transcript}

          Return your answer strictly in this format:

          Resolution Score: X/10
          Resolution Feedback: ...

          Clarity Score: X/10
          Clarity Feedback: ...

          Duration Score: X/10
          Duration Feedback: ...

          Overall Score: X/10

          Recommendations:
          - ...
          - ...
  """