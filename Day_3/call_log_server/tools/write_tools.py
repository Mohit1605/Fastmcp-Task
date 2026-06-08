from datetime import datetime
from core.state import calls, generate_call_id
from schemas.call_schemas import Call,LogCallInput,LogCallResponse,UpdateCallOutcomeInput,UpdateCallOutcomeResponse,DeleteCallInput,DeleteCallResponse
from schemas.note_schemas import AddCallNoteInput,AddCallNoteResponse
from core.permissions import require_scope


def log_call(data: LogCallInput) -> LogCallResponse:
  permission_error = require_scope("read")

  if permission_error == "UNAUTHORIZED":
      return LogCallResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return LogCallResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: read"
      )
  
  try:
    if not data.customer_name.strip():
      return LogCallResponse(
        success=False,
        error="Customer name is required.",
        code="INVALID_CUSTOMER_NAME",
        suggestion="Provide a non-empty customer name."
      )

    if not data.phone_number.strip():
      return LogCallResponse(
        success=False,
        error="Phone number is required.",
        code="INVALID_PHONE_NUMBER",
        suggestion="Provide a non-empty phone number."
      )

    if not data.transcript.strip():
      return LogCallResponse(
        success=False,
        error="Transcript is required.",
        code="INVALID_TRANSCRIPT",
        suggestion="Provide a non-empty transcript."
      )

    if data.duration_seconds < 0:
      return LogCallResponse(
        success=False,
        error="Duration cannot be negative.",
        code="INVALID_DURATION",
        suggestion="Provide a duration greater than or equal to 0."
      )


    call_id = generate_call_id()

    now = datetime.utcnow()
    call = Call(
      call_id=call_id,
      customer_name=data.customer_name.strip(),
      phone_number=data.phone_number.strip(),
      status=data.status,
      outcome=None,
      duration_seconds=data.duration_seconds,
      transcript=data.transcript.strip(),
      notes=[],
      created_at=now,
      updated_at=now
    )


    calls[call_id] = call.model_dump(mode="json")

    return LogCallResponse(
      success=True,
      call=call.model_dump(mode="json")
    )

  except Exception as e:
    return LogCallResponse(
      success=False,
      error=f"Failed to create call: {str(e)}",
      code="FAILED_TO_CREATE_CALL",
      suggestion="Verify the call details and try again."
    )


def update_call_outcome(data: UpdateCallOutcomeInput) -> UpdateCallOutcomeResponse:
  
    permission_error = require_scope("read")

    if permission_error == "UNAUTHORIZED":
        return UpdateCallOutcomeResponse(
            success=False,
            error="Authentication required",
            code="UNAUTHORIZED",
            suggestion="Authenticate before accessing this tool"
        )

    if permission_error == "FORBIDDEN":
        return UpdateCallOutcomeResponse(
            success=False,
            error="Insufficient permissions",
            code="FORBIDDEN",
            suggestion="Required scope: read"
        )

    try:
        if not data.call_id.strip():
            return UpdateCallOutcomeResponse(
                success=False,
                error="Call ID is required.",
                code="INVALID_CALL_ID",
                suggestion="Provide a valid call ID."
            )

        if data.call_id not in calls:
            return UpdateCallOutcomeResponse(
                success=False,
                error="Call not found.",
                code="CALL_NOT_FOUND",
                suggestion="Use list_calls to find a valid call ID."
            )

        call = calls[data.call_id]

        status_value = (
            data.status.value
            if hasattr(data.status, "value")
            else data.status
        )

        call["outcome"] = data.outcome
        call["status"] = status_value
        call["updated_at"] = datetime.now().isoformat()

        calls[data.call_id] = call

        return UpdateCallOutcomeResponse(
            success=True,
            call=call   
        )

    except Exception as e:
        return UpdateCallOutcomeResponse(
            success=False,
            error=f"Failed to update call outcome: {str(e)}",
            code="FAILED_TO_UPDATE_CALL",
            suggestion="Verify the call ID and outcome values."
        )
    
def delete_call(data: DeleteCallInput) -> DeleteCallResponse:
  
  permission_error = require_scope("read")

  if permission_error == "UNAUTHORIZED":
      return DeleteCallResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return DeleteCallResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: read"
      )
  try:
    if not data.call_id.strip():
      return DeleteCallResponse(
        success=False,
        error="Call ID is required.",
        code="INVALID_CALL_ID",
        suggestion="Provide a valid call ID."
      )

    if data.call_id not in calls:
      return DeleteCallResponse(
        success=False,
        error="Call not found.",
        code="CALL_NOT_FOUND",
        suggestion="Use list_calls to find a valid call ID."
      )

    del calls[data.call_id]

    return DeleteCallResponse(
            success=True,
            deleted_call_id=data.call_id
        )

  except Exception as e:
    return DeleteCallResponse(
      success=False,
      error=f"Failed to delete call outcome: {str(e)}",
      code="FAILED_TO_DELETE_CALL",
      suggestion="Verify the call ID"
    )


def add_call_note(data: AddCallNoteInput) -> AddCallNoteResponse:
  
  permission_error = require_scope("read")

  if permission_error == "UNAUTHORIZED":
      return AddCallNoteResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return AddCallNoteResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: read"
      )
  try:
    if not data.call_id.strip():
      return AddCallNoteResponse(
        success=False,
        error="Call ID is required.",
        code="INVALID_CALL_ID",
        suggestion="Provide a valid call ID."
      )
    
    if not data.note.strip():
      return AddCallNoteResponse(
        success=False,
        error="Note cannot be empty.",
        code="EMPTY_NOTE",
        suggestion="Provide a non-empty note."
      )

    if data.call_id not in calls:
      return AddCallNoteResponse(
        success=False,
        error="Call not found.",
        code="CALL_NOT_FOUND",
        suggestion="Use get_call or list_calls to find a valid call ID."
      )

    calls[data.call_id]["notes"].append(data.note.strip())
    calls[data.call_id]["updated_at"] = datetime.now().isoformat()

    return AddCallNoteResponse(
      success=True,
      call_id=data.call_id,
      note=data.note.strip(),
      total_notes=len(calls[data.call_id]["notes"])
    )

  except Exception as e:
    return AddCallNoteResponse(
      success=False,
      error=f"Failed to add note: {str(e)}",
      code="FAILED_TO_ADD_NOTE",
      suggestion="Verify the call ID and note content."
    )
  
  