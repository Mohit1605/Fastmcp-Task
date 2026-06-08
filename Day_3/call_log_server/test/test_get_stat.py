from core.state import reset_state,calls
from tools.write_tools import log_call,update_call_outcome
from tools.read_tools import get_stats
from schemas.call_schemas import LogCallInput,UpdateCallOutcomeInput,GetStatsInput
from schemas.types import CallStatus,CallOutcome

def test_get_stats():

    print("\n===== RESET STATE =====")

    reset_state()

    print("\n===== CREATE CALLS =====")

    call_1 = log_call(
        LogCallInput(
            customer_name="John",
            phone_number="1111111111",
            duration_seconds=60,
            transcript="Call 1",
            status=CallStatus.OPEN
        )
    )

    call_2 = log_call(
        LogCallInput(
            customer_name="Jane",
            phone_number="2222222222",
            duration_seconds=90,
            transcript="Call 2",
            status=CallStatus.OPEN
        )
    )

    call_3 = log_call(
        LogCallInput(
            customer_name="Mike",
            phone_number="3333333333",
            duration_seconds=120,
            transcript="Call 3",
            status=CallStatus.FAILED
        )
    )

    print("\n===== ADD OUTCOMES =====")

    update_call_outcome(
        UpdateCallOutcomeInput(
            call_id=call_1.call.call_id,
            status=CallStatus.COMPLETED,
            outcome=CallOutcome.RESOLVED
        )
    )

    update_call_outcome(
        UpdateCallOutcomeInput(
            call_id=call_2.call.call_id,
            status=CallStatus.COMPLETED,
            outcome=CallOutcome.CALLBACK_REQUESTED
        )
    )
    print(calls)
    print("\n===== GET STATS =====")

    result = get_stats(
        GetStatsInput()
    )

    print(result.model_dump())


    print("\n===== TEST PASSED =====")


if __name__ == "__main__":
    test_get_stats()