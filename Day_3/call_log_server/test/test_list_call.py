from core.state import reset_state

from tools.write_tools import log_call
from tools.read_tools import list_calls

from schemas.call_schemas import (
    LogCallInput,
    ListCallsInput
)


def test_list_calls():

    print("\n===== RESET STATE =====")
    reset_state()

    print("\n===== CREATE CALLS =====")

    for i in range(7):

        result = log_call(
            LogCallInput(
                customer_name=f"Customer {i}",
                phone_number=f"99999999{i}",
                duration_seconds=120,
                transcript=f"Transcript for call {i}"
            )
        )

        print(
            f"Created -> {result.call.call_id}"
        )

    print("\n===== PAGE 1 =====")

    page_1 = list_calls(
        ListCallsInput(
            cursor=0,
            limit=5
        )
    )

    print(page_1.model_dump())

    assert page_1.success is True
    assert len(page_1.calls) == 5
    assert page_1.next_cursor == 5
    assert page_1.has_more is True
    assert page_1.total_count == 7

    print("\n===== PAGE 2 =====")

    page_2 = list_calls(
        ListCallsInput(
            cursor=page_1.next_cursor,
            limit=5
        )
    )

    print(page_2.model_dump())

    assert page_2.success is True
    assert len(page_2.calls) == 2
    assert page_2.next_cursor is None
    assert page_2.has_more is False
    assert page_2.total_count == 7

    print("\n===== INVALID CURSOR =====")

    invalid_cursor = list_calls(
        ListCallsInput(
            cursor=-1,
            limit=5
        )
    )

    print(invalid_cursor.model_dump())

    assert invalid_cursor.success is False
    assert invalid_cursor.code == "INVALID_CURSOR"

    print("\n===== INVALID LIMIT =====")

    invalid_limit = list_calls(
        ListCallsInput(
            cursor=0,
            limit=50
        )
    )

    print(invalid_limit.model_dump())

    assert invalid_limit.success is False
    assert invalid_limit.code == "LIMIT_EXCEEDED"

    print("\n===== TEST PASSED =====")


if __name__ == "__main__":
    test_list_calls()