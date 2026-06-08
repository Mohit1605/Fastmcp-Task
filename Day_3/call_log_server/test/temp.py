from schemas.call_schemas import LogCallInput,GetCallInput
from tools.write_tools import log_call
from core.state import calls
from tools.read_tools import get_call
created = log_call(
    LogCallInput(
        customer_name="John Doe",
        phone_number="9876543210",
        duration_seconds=180,
        transcript="Customer reported washing machine leakage."
    )
)

print(calls)

print(created)
print(type(created))

call_id = created.call.call_id 

result = get_call(
    GetCallInput(
        call_id=call_id
    )
)
print("result",result)

