from core.state import reset_state

from resources.call_resources import recent_calls,failed_calls

from tools.write_tools import log_call

from schemas.call_schemas import LogCallInput

from schemas.types import CallStatus

def test_recent_calls():

    reset_state()

    for i in range(5):

        log_call(
            LogCallInput(
                customer_name=f"Customer {i}",
                phone_number=f"99999999{i}",
                duration_seconds=60,
                transcript=f"Call {i}"
            )
        )
  
    result = recent_calls(3)

    print([call.call_id for call in result])

    assert len(result) == 3

    print("TEST PASSED")


def test_failed_calls():

    reset_state()

    log_call(
        LogCallInput(
            customer_name="John",
            phone_number="1111111111",
            duration_seconds=60,
            transcript="Failed Call 1",
            status=CallStatus.FAILED
        )
    )

    log_call(
        LogCallInput(
            customer_name="Jane",
            phone_number="2222222222",
            duration_seconds=60,
            transcript="Open Call",
            status=CallStatus.OPEN
        )
    )

    log_call(
        LogCallInput(
            customer_name="Mike",
            phone_number="3333333333",
            duration_seconds=60,
            transcript="Failed Call 2",
            status=CallStatus.FAILED
        )
    )

    result = failed_calls()

    print([call.model_dump() for call in result])

    print("TEST PASSED")

if __name__ == "__main__":
    test_failed_calls()