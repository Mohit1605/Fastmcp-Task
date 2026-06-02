from fastmcp.server.middleware import Middleware
from core.auth import validate_token


class AuthenticationMiddleware(Middleware):

    async def on_call_tool(
        self,
        context,
        call_next
    ):

        request_context = (
            context.fastmcp_context.request_context
        )

        request = getattr(
            request_context,
            "request",
            None
        )

        if request is None:

            raise RuntimeError("Your request is none")

        authorization = request.headers.get(
            "Authorization"
        )

        if not authorization:
            raise RuntimeError("no parameter found authorization")

        if not authorization.startswith("Bearer "):
            raise RuntimeError("Authorization token not start with Bearer")

        token = authorization.replace("Bearer ","",1).strip()

        auth_result = validate_token(token)

        if "error" in auth_result:
            raise RuntimeError("Error occured while authenticate")

        return await call_next(context)
 