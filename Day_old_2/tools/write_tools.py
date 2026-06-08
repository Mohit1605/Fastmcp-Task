from core.state import jobs,technicians,generate_job_id,generate_technician_id
from schemas.job_schemas import CreateJobInput,AssignJobInput,CloseJobInput,CreateCloseJobResponse,AssignJobResponse
from schemas.technician_schemas import AddTechnicianInput,CreateTechnicianResponse
from schemas.types import JobStatus,TechnicianStatus
from core.errors import error_response
from core.permissions import require_scope


def create_job(data: CreateJobInput):  
  permission_error = require_scope("write")

  if permission_error == "UNAUTHORIZED":
      return CreateTechnicianResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return CreateTechnicianResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: write"
      )
    
  try:
    job_id = generate_job_id()

    if job_id in jobs:
      return CreateCloseJobResponse(
        success=False,
        error =  "Failed to create new job",
        code = f"JOB_ID_NOT_FOUND - ID collision detected for Jobs. System state corrupt",
        suggestion = "Verify and debug generated job_id and try again." 
      )
    
    new_job = {
      "id": job_id,
      "title": data.title,
      "description": data.description,
      "priority": data.priority.value,
      "status": JobStatus.OPEN.value,
      "assigned_to": None,
    }

    jobs[job_id] = new_job

    return CreateCloseJobResponse(
      success=True,
      message=f"Job '{job_id}' created successfully.",
      job=new_job
    )
    

  except Exception as e:
    return CreateCloseJobResponse(
        success=False,
        error =  "Failed to create new job",
        code = "JOB_NOT_CREATED",
        suggestion = f"Internal Erorr - {str(e)}"
    )


def add_technician(data: AddTechnicianInput):
  permission_error = require_scope("write")

  if permission_error == "UNAUTHORIZED":
      return CreateTechnicianResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return CreateTechnicianResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: write"
      )
  
  try:
    technician_id = generate_technician_id()
    
    if technician_id in technicians:
      print(technician_id)
      return CreateTechnicianResponse(
        success=False,
        error="Failed to create technician",
        code="TECHNICIAN_ID_COLLISION",
        suggestion="Retry generating technician ID."
      )
    
    new_technician = {
      "id": technician_id,
      "name": data.name,
      "skill": data.skill,
      "status": TechnicianStatus.AVAILABLE.value,
    }

    technicians[technician_id] = new_technician
    
    return CreateTechnicianResponse(
      success=True,
      message=f"Technician '{technician_id}' added successfully.",
      technician=new_technician
    )

  except Exception as e:
    return CreateTechnicianResponse(
      success=False,
      error="Failed to create technician",
      code="TECHNICIAN_CREATION_FAILED",
      suggestion="Verify input data and try again."
    )


def assign_job(data: AssignJobInput):
  permission_error = require_scope("write")

  if permission_error == "UNAUTHORIZED":
      return CreateTechnicianResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return CreateTechnicianResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: write"
      )
  
  try:
    if data.job_id not in jobs:
      return AssignJobResponse(
        success=False,
        error =  "Failed to assign job",
        code = f"FAILED_TO_ASSIGN_JOB - Job '{data.job_id}' does not exist. ",
        suggestion = "Use list_jobs to view valid job IDs."
      )

    if data.technician_id not in technicians:
      return AssignJobResponse(
        success=False,
        error =  "Failed to create assign job",
        code = f"FAILED_TO_ASSIGN_JOB - Technician '{data.technician_id}' does not exist. ",
        suggestion = "Use list_technicians to view valid technician IDs."
      )

    job = jobs[data.job_id]
    technician = technicians[data.technician_id]

    if job["status"] == JobStatus.CLOSED.value:
      return AssignJobResponse(
        success=False,
        error =  "Failed to create assign job",
        code = f"JOB_ALREADY_CLOSE - Job '{data.job_id}' is already closed.",
        suggestion = "Create a new job or assign an open job."
      )
     
    if job["assigned_to"] is not None:
      return AssignJobResponse(
        success=False,
        error =  "Failed to create assign job",
        code = f"JOB_ALREADY_ASSIGNED - Job '{data.job_id}' is already assigned.",
        suggestion = "Close the current assignment or choose another job."
      )

    if technician["status"] != TechnicianStatus.AVAILABLE.value:
      return AssignJobResponse(
        success=False,
        error =  "Failed to create assign job",
        code = f"BUSY_TECHNICIAN - Technician '{data.technician_id}' is currently busy.",
        suggestion = "Use list_available_technicians to find available staff."
      )      

    job["assigned_to"] = data.technician_id
    job["status"] = JobStatus.IN_PROGRESS.value

    technician["status"] = TechnicianStatus.BUSY.value

    return AssignJobResponse(
      success =  True,
      message =  (
        f"Job '{data.job_id}' assigned "
        f"to technician '{data.technician_id}'."
        ),
      job = job,
      technician = technician,
    )

  except Exception as e:
    return AssignJobResponse(
        success=False,
        error =  "Failed to assign job",
        code = f"FAILED_TO_ASSING_JOB",
        suggestion = f"Internal error: {str(e)}"
    ) 


def close_job(data: CloseJobInput):
  permission_error = require_scope("write")

  if permission_error == "UNAUTHORIZED":
      return CreateTechnicianResponse(
          success=False,
          error="Authentication required",
          code="UNAUTHORIZED",
          suggestion="Authenticate before accessing this tool"
      )

  if permission_error == "FORBIDDEN":
      return CreateTechnicianResponse(
          success=False,
          error="Insufficient permissions",
          code="FORBIDDEN",
          suggestion="Required scope: write"
      )
  
  try:
    if data.job_id not in jobs:
      return CreateCloseJobResponse(
          success=False,
          error="Failed to close the job",
          code=f"FAILED_TO_CLOSE_JOB - Job '{data.job_id}' does not exist.",
          suggestion="Use list_jobs to find valid job IDs."
      )

    job = jobs[data.job_id]

    if job["status"] == JobStatus.CLOSED.value:
      return CreateCloseJobResponse(
          success=False,
          error="Failed to close the job",
          code=f"JOB_ALREADY_CLOSE - Job '{data.job_id}' is already closed.",
          suggestion="Use list_open_jobs to find active jobs."
      )

    assigned_technician_id = job["assigned_to"]

    if assigned_technician_id:

      if assigned_technician_id in technicians:
        technicians[assigned_technician_id]["status"] = (TechnicianStatus.AVAILABLE.value)

    job["status"] = JobStatus.CLOSED.value

    return CreateCloseJobResponse(
      success= True,
      message = f"Job '{data.job_id}' closed successfully.",
      job = job,
    )

  except Exception as e:
    return CreateCloseJobResponse(
        success=False,
        error="Failed to close the job",
        code="FAILED_JOB_TO_CLOSE",
        suggestion=f"Internal error: {str(e)}"
    )
  
