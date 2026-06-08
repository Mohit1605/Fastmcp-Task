from schemas.pagination_schema import PaginationResponse
from core.state import jobs, technicians
from schemas.types import JobStatus,TechnicianStatus
from core.errors import error_response
from core.pagination import paginate
from core.permissions import require_scope
from schemas.job_schemas import PaginationInput

def list_jobs(data:PaginationInput):
  permission_error = require_scope("read")

  if permission_error == "UNAUTHORIZED":
      return PaginationResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return PaginationResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: read"
      )
  
  try:
    return paginate(
      items=sorted(list(jobs.values()), key=lambda j: j.get("id", 0)),
      cursor=data.cursor,
      limit=data.limit 
    )

  except Exception as e:
    return PaginationResponse(
      success= False,
      error="Failed to retrieve jobs",
      code="LIST_JOBS_ERROR",
      suggestion="Verify server state and retry."
    )


def list_technicians(data:PaginationInput):
  permission_error = require_scope("read")

  if permission_error == "UNAUTHORIZED":
      return PaginationResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return PaginationResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: read"
      )
  
  try:
    return paginate(
      items=sorted(list(technicians.values()), key=lambda j: j.get("id", 0)),
      cursor=data.cursor,
      limit=data.limit
    )

  except Exception as e:
    return PaginationResponse(
      success= False,
      error =  "Failed to retrieve technicians.",
      code = "LIST_TECHNICIANS_ERROR",
      suggestion = f"Internal Error - {str(e)}"
    )

def list_open_jobs(data:PaginationInput):
  permission_error = require_scope("read")

  if permission_error == "UNAUTHORIZED":
      return PaginationResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return PaginationResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: read"
      )
  
  try:
    open_jobs = [
      job for job in jobs.values() 
      if job["status"] != JobStatus.CLOSED.value
    ]

    return paginate(
      items=open_jobs,
      cursor=data.cursor,
      limit=data.limit
    )

  except Exception as e:
    return PaginationResponse(
      success=False,
      error =  "Failed to retrieve open jobs.",
      code = f"LIST_OPEN_JOB_ERROR - ",
      suggestion = f"Internal Erorr - {str(e)}"
    )



def list_available_technicians(data:PaginationInput):
  permission_error = require_scope("read")

  if permission_error == "UNAUTHORIZED":
      return PaginationResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return PaginationResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: read"
      )
  
  try:
    available_technicians = [
      technician for technician in technicians.values() 
      if technician["status"] == TechnicianStatus.AVAILABLE.value
    ]

    return paginate(
      items=available_technicians,
      cursor=data.cursor,
      limit=data.limit
    )

  except Exception as e:
    return error_response(
      error =  "Failed to retrieve available technicians.",
      code = f"LIST_AVAIL_TECHNICIANS_ERROR - {str(e)}",
      suggestion = "Verify server state and retry."
    )