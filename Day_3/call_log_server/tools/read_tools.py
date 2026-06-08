from core.state import calls
from schemas.call_schemas import Call,GetCallInput,GetCallResponse,ListCallsInput,ListCallsResponse,ListCallsByStatusInput,ListCallsByStatusResponse,GetStatsInput,GetStatsResponse,GetCallSummaryInput,GetCallSummaryResponse
from schemas.note_schemas import ListNotesForCallInput,ListNotesForCallResponse
from core.pagination import paginate
from fastmcp import Context
from core.permissions import require_scope

def get_call(data: GetCallInput) -> GetCallResponse:
  permission_error = require_scope("read")

  if permission_error == "UNAUTHORIZED":
      return GetCallResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return GetCallResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: read"
      )
  
  try:
    if not data.call_id.strip():
      return GetCallResponse(
        success=False,
        error="Call ID is required.",
        code="INVALID_CALL_ID",
        suggestion="Provide a valid call ID."
      )

    if data.call_id not in calls:
      return GetCallResponse(
        success=False,
        error="Call not found.",
        code="CALL_NOT_FOUND",
        suggestion="Use list_calls to find a valid call ID."
      )

    call = Call(**calls[data.call_id])

    return GetCallResponse(
      success=True,
      call=call.model_dump(mode="json")
    )

  except Exception as e:
    return GetCallResponse(
      success=False,
      error=f"Failed to retrieve call: {str(e)}",
      code="FAILED_TO_GET_CALL",
      suggestion="Verify the call ID and try again."
    )


def list_calls(data: ListCallsInput) -> ListCallsResponse:
    permission_error = require_scope("read")

    if permission_error == "UNAUTHORIZED":
        return ListCallsResponse(
            success=False,
            error="Authentication required",
            code="UNAUTHORIZED",
            suggestion="Authenticate before accessing this tool"
        )

    if permission_error == "FORBIDDEN":
        return ListCallsResponse(
            success=False,
            error="Insufficient permissions",
            code="FORBIDDEN",
            suggestion="Required scope: read"
        )
    try:

        all_calls = list(calls.values())

        pagination_result = paginate(
            items=all_calls,
            cursor=data.cursor,
            limit=data.limit
        )

        if not pagination_result.success:

            return ListCallsResponse(
                success=False,
                error=pagination_result.error,
                code=pagination_result.code,
                suggestion=pagination_result.suggestion
            )

        return ListCallsResponse(
          success=True,
          calls=pagination_result.data,
          count=len(pagination_result.data or []),
          next_cursor=pagination_result.next_cursor,
          has_more=pagination_result.has_more,
          total_count=pagination_result.total_count
        )

    except Exception as e:

        return ListCallsResponse(
            success=False,
            error=f"Failed to list calls: {str(e)}",
            code="FAILED_TO_LIST_CALLS",
            suggestion="Try again or verify pagination inputs."
        )


def list_calls_by_status(data: ListCallsByStatusInput) -> ListCallsByStatusResponse:
  
  permission_error = require_scope("read")

  if permission_error == "UNAUTHORIZED":
      return ListCallsByStatusResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return ListCallsByStatusResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: read"
      )
  try:
    filtered_calls = []
    status_value = (
        data.status.value
        if hasattr(data.status, "value")
        else data.status
    )
    
    filtered_calls = [
            call_data
            for call_data in calls.values()
            if call_data["status"] == status_value
        ]

    pagination_result = paginate(
            items=filtered_calls,
            cursor=data.cursor,
            limit=data.limit
        )

    if not pagination_result.success:
      return ListCallsByStatusResponse(
        success=False,
        error=pagination_result.error,
        code=pagination_result.code,
        suggestion=pagination_result.suggestion
      )

    return ListCallsByStatusResponse(
      success=True,
      calls=pagination_result.data,
      count=len(pagination_result.data),
      next_cursor=pagination_result.next_cursor,
      has_more=pagination_result.has_more,
      total_count=pagination_result.total_count
    )

  except Exception as e:
    return ListCallsByStatusResponse(
      success=False,
      error=f"Failed to list calls by status: {str(e)}",
      code="FAILED_TO_FILTER_CALLS",
      suggestion="Verify the status and try again."
    )
  

def list_notes_for_call(data: ListNotesForCallInput) -> ListNotesForCallResponse:
  
  permission_error = require_scope("read")

  if permission_error == "UNAUTHORIZED":
      return ListNotesForCallResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return ListNotesForCallResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: read"
      )
  try:
    if not data.call_id.strip():
      return ListNotesForCallResponse(
        success=False,
        error="Call ID is required.",
        code="INVALID_CALL_ID",
        suggestion="Provide a valid call ID."
      )

    if data.call_id not in calls:
      return ListNotesForCallResponse(
        success=False,
        error="Call not found.",
        code="CALL_NOT_FOUND",
        suggestion="Use get_call or list_calls to find a valid call ID."
    )

    notes = calls[data.call_id].get("notes", [])

    if not isinstance(notes, list):
            notes = []

    return ListNotesForCallResponse(
      success=True,
      call_id=data.call_id,
      notes=notes,
      total_notes=len(notes)
    )

  except Exception as e:
    return ListNotesForCallResponse(
      success=False,
      error=f"Failed to retrieve notes: {str(e)}",
      code="FAILED_TO_LIST_NOTES",
      suggestion="Verify the call ID and try again."
    )
 
 
def get_stats(data: GetStatsInput) -> GetStatsResponse:
  
  permission_error = require_scope("read")

  if permission_error == "UNAUTHORIZED":
      return GetStatsResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return GetStatsResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: read"
      )
  try:

    status_counts = {}
    outcome_counts = {}

    for call in calls.values():
      status = str(call["status"])

      status_counts[status] = (status_counts.get(status, 0) + 1)

      outcome = call.get("outcome")

      if outcome:
        status = call["status"]
        outcome_counts[outcome] = (outcome_counts.get(outcome, 0) + 1)

    return GetStatsResponse(
      success=True,
      total_calls=len(calls),
      status_counts=status_counts,
      outcome_counts=outcome_counts
    )

  except Exception as e:
    return GetStatsResponse(
      success=False,
      error=f"Failed to generate statistics: {str(e)}",
      code="FAILED_TO_GENERATE_STATS",
      suggestion="Try again after verifying call data."
    )
  

async def get_call_summary(data: GetCallSummaryInput,ctx: Context) -> GetCallSummaryResponse:
  
    permission_error = require_scope("read")

    if permission_error == "UNAUTHORIZED":
        return GetCallSummaryResponse(
            success=False,
            error="Authentication required",
            code="UNAUTHORIZED",
            suggestion="Authenticate before accessing this tool"
        )

    if permission_error == "FORBIDDEN":
        return GetCallSummaryResponse(
            success=False,
            error="Insufficient permissions",
            code="FORBIDDEN",
            suggestion="Required scope: read"
        )
    try:

        # Validate

        if not data.call_id.strip():

            return GetCallSummaryResponse(
                success=False,
                error="Call ID is required.",
                code="INVALID_CALL_ID",
                suggestion="Provide a valid call ID."
            )

        # Check existence

        if data.call_id not in calls:

            return GetCallSummaryResponse(
                success=False,
                error="Call not found.",
                code="CALL_NOT_FOUND",
                suggestion="Use get_call or list_calls to find a valid call ID."
            )

        call = calls[data.call_id]

        transcript = call["transcript"]

        status = str(call.get("status", "UNKNOWN"))
        
        outcome = str(call.get("outcome", "NOT_SET"))

        duration = call["duration_seconds"]

        prompt = f"""
          Summarize the following customer support call.

          Include:
          1. Main issue
          2. Actions taken
          3. Final outcome

          Call Status:
          {status}

          Call Outcome:
          {outcome}

          Duration:
          {duration} seconds

          Transcript:
          {transcript}
          """

        summary = await ctx.sample(prompt.strip())

        return GetCallSummaryResponse(
            success=True,
            call_id=data.call_id,
            summary=str(summary)
        )

    except Exception as e:

        return GetCallSummaryResponse(
            success=False,
            error=f"Failed to generate summary: {str(e)}",
            code="FAILED_TO_GENERATE_SUMMARY",
            suggestion="Verify the call data and try again."
        )