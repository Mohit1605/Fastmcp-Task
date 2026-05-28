import uuid

jobs: dict[str, dict] = {}

technicians: dict[str, dict] = {}


def generate_job_id() -> str:
    return f"job_{uuid.uuid4().hex[:8]}"


def generate_technician_id() -> str:
    return f"tech_{uuid.uuid4().hex[:8]}"

def reset_state():
    jobs.clear()
    technicians.clear()