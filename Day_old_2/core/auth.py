import time
from contextvars import ContextVar
from core.errors import error_response
from typing import Optional

TOKEN_REGISTRY = {
  "reader-token": {
    "scopes": ["read"],
    "expires_at": 1893456000
  },

  "writer-token": {
    "scopes": ["read", "write"],
    "expires_at": 1893456000
  }
}


CURRENT_AUTH: ContextVar[Optional[dict]] = ContextVar("CURRENT_AUTH",default=None)


def validate_token(token: str):
  if not token:
    return error_response(
      error="Authorization token missing",
      code="UNAUTHORIZED",
      suggestion="Provide a valid bearer token"
    )

  token_data = TOKEN_REGISTRY.get(token)

  if not token_data:
    return error_response(
      error="Invalid token",
      code="INVALID_TOKEN",
      suggestion="Provide a registered token"
    )

  current_time = int(time.time())

  expires_at = token_data["expires_at"]

  if current_time > expires_at:
    expired_seconds = current_time - expires_at
    return error_response(
      error=f"Token expired {expired_seconds} seconds ago",
      code="TOKEN_EXPIRED",
      suggestion="Use a valid non-expired token"
    )

  CURRENT_AUTH.set({
    "token": token,
    "scopes": token_data["scopes"],
  })

  # return token_data
  return {
        "success": True,
        "message": "Authentication successful"
    }



def get_current_auth():
  return CURRENT_AUTH.get()