from pprint import pprint

from tools.write_tools import (
    create_job,
    add_technician,
    assign_job,
    close_job,
)

from schemas.job_schemas import (
    CreateJobInput,
    AssignJobInput,
    CloseJobInput,
)

from schemas.technician_schemas import (
    AddTechnicianInput,
)

from schemas.types import JobPriority

from core.state import (
    jobs,
    technicians,
    reset_state,
)

reset_state()


print("\n" + "=" * 60)
print("TEST 1 → CREATE JOB")
print("=" * 60)

job_response = create_job(
    CreateJobInput(
        title="Fix Office Printer",
        description="Printer is not responding to print requests.",
        priority=JobPriority.HIGH,
    )
)

pprint(job_response)

job_id = job_response["job"]["id"]


print("\n" + "=" * 60)
print("TEST 2 → ADD TECHNICIAN")
print("=" * 60)

technician_response = add_technician(
    AddTechnicianInput(
        name="Charlie",
        skill="Hardware",
    )
)

pprint(technician_response)

technician_id = technician_response["technician"]["id"]


print("\n" + "=" * 60)
print("TEST 3 → ASSIGN JOB")
print("=" * 60)

assign_response = assign_job(
    AssignJobInput(
        job_id=job_id,
        technician_id=technician_id,
    )
)

pprint(assign_response)



print("\n" + "=" * 60)
print("TEST 4 → VERIFY STATE AFTER ASSIGNMENT")
print("=" * 60)

print("\nJobs:")
pprint(jobs)

print("\nTechnicians:")
pprint(technicians)


print("\n" + "=" * 60)
print("TEST 5 → CLOSE JOB")
print("=" * 60)

close_response = close_job(
    CloseJobInput(
        job_id=job_id,
    )
)

pprint(close_response)


print("\n" + "=" * 60)
print("TEST 6 → VERIFY FINAL STATE")
print("=" * 60)

print("\nJobs:")
pprint(jobs)

print("\nTechnicians:")
pprint(technicians)



print("\n" + "=" * 60)
print("TEST 7 → ERROR CASE (INVALID JOB)")
print("=" * 60)

invalid_job_response = assign_job(
    AssignJobInput(
        job_id="invalid_job",
        technician_id=technician_id,
    )
)

pprint(invalid_job_response)



print("\n" + "=" * 60)
print("TEST 8 → ERROR CASE (BUSY TECHNICIAN)")
print("=" * 60)

# Create another job
second_job_response = create_job(
    CreateJobInput(
        title="Network Failure",
        description="Internet is down on second floor.",
        priority=JobPriority.MEDIUM,
    )
)

pprint(second_job_response)

second_job_id = second_job_response["job"]["id"]


# Reassign technician before closing
reassign_response = assign_job(
    AssignJobInput(
        job_id=second_job_id,
        technician_id=technician_id,
    )
)

pprint(reassign_response)