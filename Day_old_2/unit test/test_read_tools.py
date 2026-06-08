from pprint import pprint

from core.state import reset_state

from tools.write_tools import (
    create_job,
    add_technician,
)

from tools.read_tools import (
    list_jobs,
    list_open_jobs,
    list_technicians,
    list_available_technicians,
)

from schemas.job_schemas import CreateJobInput
from schemas.technician_schemas import AddTechnicianInput
from schemas.types import JobPriority




reset_state()


create_job(
    CreateJobInput(
        title="Fix Printer",
        description="Printer issue in office.",
        priority=JobPriority.HIGH,
    )
)

create_job(
    CreateJobInput(
        title="Install Windows",
        description="Install OS on lab PC.",
        priority=JobPriority.MEDIUM,
    )
)




add_technician(
    AddTechnicianInput(
        name="Alice",
        skill="Hardware",
    )
)

add_technician(
    AddTechnicianInput(
        name="Bob",
        skill="Software",
    )
)



print("\n" + "=" * 60)
print("TEST → LIST ALL JOBS")
print("=" * 60)

pprint(list_jobs())



print("\n" + "=" * 60)
print("TEST → LIST OPEN JOBS")
print("=" * 60)

pprint(list_open_jobs())


print("\n" + "=" * 60)
print("TEST → LIST ALL TECHNICIANS")
print("=" * 60)

pprint(list_technicians())




print("\n" + "=" * 60)
print("TEST → LIST AVAILABLE TECHNICIANS")
print("=" * 60)

pprint(list_available_technicians())