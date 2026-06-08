def validate_tool_annotations(tool_name: str,annotations: dict):
    """
    Validate tool annotation rules.
    """

    destructive = annotations.get(
        "destructiveHint",
        False
    )

    idempotent = annotations.get(
        "idempotentHint",
        False
    )

    if destructive and idempotent:

        raise RuntimeError(
            f"""
              Invalid annotation configuration for tool: {tool_name}

              Rule violated:
              A destructive tool cannot be idempotent.

              Current configuration:
              destructiveHint=True
              idempotentHint=True
              """
        )