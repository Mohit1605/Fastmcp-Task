import os

def extract_token(context):

    request_context = (
        context.fastmcp_context.request_context
    )

    request = getattr(
        request_context,
        "request",
        None
    )

    # HTTP Mode
    if request is not None:

        authorization = request.headers.get(
            "Authorization"
        )

        if not authorization:
            raise RuntimeError(
                "Authorization header missing"
            )

        if not authorization.startswith("Bearer "):
            raise RuntimeError(
                "Invalid Authorization format"
            )

        return authorization.replace(
            "Bearer ",
            "",
            1
        ).strip()

    # STDIO Mode
    token = os.getenv("AUTH_TOKEN")

    if not token:
        raise RuntimeError(
            "AUTH_TOKEN environment variable missing"
        )

    return token