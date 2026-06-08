from core.state import jobs, technicians
from schemas.types import JobStatus,TechnicianStatus

def get_all_jobs() -> dict:
    try:
        return {
            "success": True,
            "count": len(jobs),
            "jobs": list(jobs.values()),
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Failed to load all jobs resource.",
            "error": str(e),
            "next_action": "Verify server state and retry.",
        }


def get_open_jobs() -> dict:
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
            "message": "Failed to load open jobs resource.",
            "error": str(e),
            "next_action": "Verify server state and retry.",
        }


def get_available_technicians() -> dict:
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
            "message": "Failed to load available technicians resource.",
            "error": str(e),
            "next_action": "Verify server state and retry.",
        }