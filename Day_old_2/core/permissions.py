from core.auth import get_current_auth
from core.errors import error_response


def require_scope(required_scope: str):
    
    auth_data = get_current_auth()

    if not auth_data:
        return "UNAUTHORIZED"

    scopes = auth_data.get("scopes", [])

    if required_scope not in scopes:
        return "FORBIDDEN"

    return None