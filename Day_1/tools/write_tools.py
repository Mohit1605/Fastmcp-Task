from core.state import jobs,technicians,generate_job_id,generate_technician_id
from schemas.job_schemas import CreateJobInput,AssignJobInput,CloseJobInput
from schemas.technician_schemas import AddTechnicianInput
from schemas.types import JobStatus,TechnicianStatus,BaseResponse

def create_job(data: CreateJobInput) -> dict:
  try:
    job_id = generate_job_id()

    if job_id in jobs:
      print(job_id)
      return {
        "success": False,
        "message": "Failed to create new job",
        "error": "ID collision detected for technicians - system state corrupt",
        "next_action": "Verify and debug generated job_id and try again.",
      }
    
    new_job = {
      "id": job_id,
      "title": data.title,
      "description": data.description,
      "priority": data.priority.value,
      "status": JobStatus.OPEN.value,
      "assigned_to": None,
    }

    jobs[job_id] = new_job

    return {
      "success": True,
      "message": f"Job '{job_id}' created successfully.",
      "job": new_job,
    }

  except Exception as e:
    return {
      "success": False,
      "message": f"Failed to create new job",
      "error": str(e),
      "next_action": "Verify the job input fields and try again.",
    }


def add_technician(data: AddTechnicianInput) -> dict:
  try:
    technician_id = generate_technician_id()
    
    if technician_id in technicians:
      print(technician_id)
      return {
        "success": False,
        "message": "Failed to create new technician",
        "error": "ID collision detected for technicians - system state corrupt",
        "next_action": "Verify and debug generated technician_id and try again.",
      }
    
    new_technician = {
      "id": technician_id,
      "name": data.name,
      "skill": data.skill,
      "status": TechnicianStatus.AVAILABLE.value,
    }

    technicians[technician_id] = new_technician

    return {
      "success": True,
      "message": f"Technician '{technician_id}' added successfully.",
      "technician": new_technician,
    }

  except Exception as e:
    return {
      "success": False,
      "message": f"Failed to add technician",
      "error": str(e),
      "next_action": "Verify technician details and try again.",
    }


def assign_job(data: AssignJobInput) -> dict:
  try:
    if data.job_id not in jobs:
      return {
        "success": False,
        "message": f"Job '{data.job_id}' does not exist.",
        "next_action": "Use list_jobs to view valid job IDs.",
      }

    if data.technician_id not in technicians:
      return {
        "success": False,
        "message": f"Technician '{data.technician_id}' does not exist.",
        "next_action": "Use list_technicians to view valid technician IDs.",
      }

    job = jobs[data.job_id]
    technician = technicians[data.technician_id]

    if job["status"] == JobStatus.CLOSED.value:
      return {
        "success": False,
        "message": f"Job '{data.job_id}' is already closed.",
        "next_action": "Create a new job or assign an open job.",
      }

    if job["assigned_to"] is not None:
      return {
        "success": False,
        "message": f"Job '{data.job_id}' is already assigned.",
        "next_action": "Close the current assignment or choose another job.",
      }

    if technician["status"] != TechnicianStatus.AVAILABLE.value:
      return {
        "success": False,
        "message": f"Technician '{data.technician_id}' is currently busy.",
        "next_action": "Use list_available_technicians to find available staff.",
      }

    job["assigned_to"] = data.technician_id
    job["status"] = JobStatus.IN_PROGRESS.value

    technician["status"] = TechnicianStatus.BUSY.value

    return {
      "success": True,
      "message": (
        f"Job '{data.job_id}' assigned "
        f"to technician '{data.technician_id}'."
        ),
      "job": job,
      "technician": technician,
    }

  except Exception as e:
    return {
      "success": False,
      "message": f"Failed to assign job",
      "error": str(e),
      "next_action": "Verify job and technician IDs, then try again.",
    }


def close_job(data: CloseJobInput) -> dict:
  try:
    if data.job_id not in jobs:
      return {
        "success": False,
        "message": f"Job '{data.job_id}' does not exist.",
        "next_action": "Use list_jobs to find valid job IDs.",
      }

    job = jobs[data.job_id]

    if job["status"] == JobStatus.CLOSED.value:
      return {
        "success": False,
        "message": f"Job '{data.job_id}' is already closed.",
        "next_action": "Use list_open_jobs to find active jobs.",
      }

    assigned_technician_id = job["assigned_to"]

    if assigned_technician_id:

      if assigned_technician_id in technicians:
        technicians[assigned_technician_id]["status"] = (TechnicianStatus.AVAILABLE.value)

    job["status"] = JobStatus.CLOSED.value

    return {
      "success": True,
      "message": f"Job '{data.job_id}' closed successfully.",
      "job": job,
    }

  except Exception as e:
    return {
      "success": False,
      "message": f"Failed to close job",
      "error": str(e),
      "next_action": "Verify the job ID and try again.",
    }