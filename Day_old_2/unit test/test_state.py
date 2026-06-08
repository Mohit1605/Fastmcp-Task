from core.state import jobs, generate_job_id

job_id = generate_job_id()

jobs[job_id] = {
    "id": job_id,
    "title": "Fix Printer",
    "status": "open"
}

job_id = generate_job_id()
jobs[job_id] = {
    "id": job_id,
    "title": "Fix Laptop",
    "status": "open"
}

print(type(jobs))