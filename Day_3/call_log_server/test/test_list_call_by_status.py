from core.state import reset_state

from tools.write_tools import log_call
from tools.read_tools import list_calls_by_status

from schemas.call_schemas import LogCallInput,ListCallsByStatusInput

from schemas.types import CallStatus


def test_list_calls_by_status():

    reset_state()

    # OPEN

    for i in range(3):

        log_call(
            LogCallInput(
                customer_name=f"Open {i}",
                phone_number=f"11111111{i}",
                duration_seconds=60,
                transcript="Open call",
                status=CallStatus.OPEN
            )
        )

    # FAILED

    for i in range(2):

        log_call(
            LogCallInput(
                customer_name=f"Failed {i}",
                phone_number=f"22222222{i}",
                duration_seconds=60,
                transcript="Failed call",
                status=CallStatus.FAILED
            )
        )

    result = list_calls_by_status(
        ListCallsByStatusInput(
            status=CallStatus.FAILED,
            cursor=0,
            limit=10
        )
    )

    print(result.model_dump())

    print("TEST PASSED")


if __name__ == "__main__":
    test_list_calls_by_status()