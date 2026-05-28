from core.state import jobs, technicians
from schemas.types import JobStatus,TechnicianStatus

def list_jobs() -> dict:
  try:
    return {
      "success": True,
      "count": len(jobs),
      "jobs": list(jobs.values()),
    }

  except Exception as e:
    return {
      "success": False,
      "message": "Failed to retrieve jobs.",
      "error": str(e),
      "next_action": "Verify server state and retry.",
    }


def list_technicians() -> dict:
  try:
    return {
      "success": True,
      "count": len(technicians),
      "technicians": list(technicians.values()),
    }

  except Exception as e:
    return {
      "success": False,
      "message": "Failed to retrieve technicians.",
      "error": str(e),
      "next_action": "Verify server state and retry.",
    }

def list_open_jobs() -> dict:
  try:
    open_jobs = [
      job for job in jobs.values() 
      if job["status"] != JobStatus.CLOSED.value
    ]

    return {
      "success": True,
      "count": len(open_jobs),
      "jobs": open_jobs,
    }

  except Exception as e:
    return {
      "success": False,
      "message": "Failed to retrieve open jobs.",
      "error": str(e),
      "next_action": "Verify server state and retry.",
    }



def list_available_technicians() -> dict:
  try:
    available_technicians = [
      technician for technician in technicians.values() 
      if technician["status"] == TechnicianStatus.AVAILABLE.value
    ]

    return {
      "success": True,
      "count": len(available_technicians),
      "technicians": available_technicians,
    }

  except Exception as e:
    return {
      "success": False,
      "message": "Failed to retrieve available technicians.",
      "error": str(e),
      "next_action": "Verify server state and retry.",
    }