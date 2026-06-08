from core.auth import validate_token
from core.auth_provider import extract_token
from fastmcp.server.middleware import Middleware

class AuthenticationMiddleware(Middleware):

    async def on_call_tool(
        self,
        context,
        call_next
    ):

        token = extract_token(context)

        auth_result = validate_token(token)

        if "error" in auth_result:
            raise RuntimeError(
                auth_result["error"]
            )

        return await call_next(context)