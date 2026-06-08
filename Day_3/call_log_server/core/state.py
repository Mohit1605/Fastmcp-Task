import uuid

calls: dict[str, dict] = {}

def generate_call_id() -> str:
    return f"call_{uuid.uuid4().hex[:8]}"

def get_call(call_id: str) -> dict | None:
    return calls.get(call_id)

def reset_state():
    calls.clear()