from core.auth import validate_token
from core.state import reset_state
from tools.write_tools import create_job, close_job

from schemas.job_schemas import (
    CreateJobInput,
    CloseJobInput
)

from schemas.types import JobPriority


def setup_function():
    reset_state()
    validate_token("writer-token")


def test_close_job_twice():

    created_job = create_job(
        CreateJobInput(
            title="Test Job",
            description="Testing",
            priority=JobPriority.HIGH
        )
    )

    job_id = created_job["job"]["id"]

    first_close = close_job(
        CloseJobInput(
            job_id=job_id
        )
    )

    assert first_close.success is True

    second_close = close_job(
        CloseJobInput(
            job_id=job_id
        )
    )

    assert second_close["code"].startswith(
        "JOB_ALREADY_CLOSE"
    )