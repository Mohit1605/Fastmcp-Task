from core.state import jobs, technicians
from schemas.types import TechnicianStatus


def triage_job(job_id: str) -> str:
  
  if job_id not in jobs:
    return (
      f"Job '{job_id}' was not found.\n\n"
      "Suggested next action:\n"
      "- Use list_jobs to view valid jobs."
    )

  job = jobs[job_id]

  return f"""
    You are an IT support triage assistant.

    Analyze the following job and provide:

    1. Urgency level
    2. Required technical skills
    3. Estimated complexity
    4. Recommended resolution approach
    5. Potential risks if delayed

    Job Details:
    - Job ID: {job["id"]}
    - Title: {job["title"]}
    - Description: {job["description"]}
    - Priority: {job["priority"]}
    - Status: {job["status"]}
    - Assigned Technician: {job["assigned_to"]}
  """

def assign_suggestion(job_id: str) -> str:

  if job_id not in jobs:
    return (
      f"Job '{job_id}' was not found.\n\n"
      "Suggested next action:\n"
      "- Use list_jobs to view valid jobs."
    )

  job = jobs[job_id]

  available_technicians = [
        tech for tech in technicians.values()
        if tech["status"] == TechnicianStatus.AVAILABLE.value
    ]

  if not available_technicians:
    return (
      "No available technicians found.\n\n"
      "Suggested next action:\n"
      "- Add new technicians\n"
      "- Or close active jobs to free technicians."
    )

  technician_summary = "\n".join(
    [
            (
                f"- ID: {tech['id']} | "
                f"Name: {tech['name']} | "
                f"Skill: {tech['skill']}"
            )
            for tech in available_technicians
    ]
  )

  return f"""
    You are a job assignment assistant.

    Analyze the following job and determine the BEST technician
    for the task based on skill relevance and availability.

    Job Details:
    - Job ID: {job["id"]}
    - Title: {job["title"]}
    - Description: {job["description"]}
    - Priority: {job["priority"]}

    Available Technicians:
    {technician_summary}

    Instructions:
    1. Select the best technician
    2. Explain WHY they are the best match
    3. Mention any skill gaps or risks
    4. Suggest backup technician if relevant
  """