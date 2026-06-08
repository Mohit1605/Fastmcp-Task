from core.state import reset_state,calls
from tools.write_tools import log_call,delete_call
from schemas.call_schemas import LogCallInput,DeleteCallInput


def test_delete_call():

    reset_state()

    created = log_call(
        LogCallInput(
            customer_name="John Doe",
            phone_number="9999999999",
            duration_seconds=120,
            transcript="Customer requested support."
        )
    )
    log_call(
        LogCallInput(
            customer_name="ROhit S",
            phone_number="1234567890",
            duration_seconds=120,
            transcript="Pipeline leakage"
        )
    )
    call_id = created.call.call_id

    print("\nBEFORE DELETE")
    print(calls)

    result = delete_call(
        DeleteCallInput(
            call_id=call_id
        )
    )

    print(result.model_dump())

    assert result.success is True

    assert call_id not in calls

    print("\nAFTER DELETE")
    print(calls)

    print("TEST PASSED")


if __name__ == "__main__":
    test_delete_call()