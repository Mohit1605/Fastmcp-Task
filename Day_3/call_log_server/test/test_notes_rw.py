from core.state import reset_state
from tools.write_tools import log_call,add_call_note
from tools.read_tools import list_notes_for_call
from schemas.call_schemas import LogCallInput
from schemas.note_schemas  import AddCallNoteInput,ListNotesForCallInput


reset_state()

created = log_call(
    LogCallInput(
        customer_name="John",
        phone_number="9999999999",
        duration_seconds=120,
        transcript="Customer reported issue."
    )
)

call_id = created.call.call_id

add_call_note(
    AddCallNoteInput(
        call_id=call_id,
        note="job_id=job_123"
    )
)

add_call_note(
    AddCallNoteInput(
        call_id=call_id,
        note="customer requested callback"
    )
)

result = list_notes_for_call(
    ListNotesForCallInput(
        call_id=call_id
    )
)

print(result.model_dump())