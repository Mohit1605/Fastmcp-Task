import json

from schemas.workflow import WorkflowStep


def parse_mcp_result(result):

    if (
        isinstance(result, list)
        and len(result) > 0
        and result[0].get("type") == "text"
    ):
        return json.loads(result[0]["text"])

    return result


async def quality_review(query,mcp_client,context,logger,steps):

    try:

        list_failed_calls_tool = (mcp_client.get_tool_by_name("list_calls_by_status"))

        get_call_tool = (mcp_client.get_tool_by_name("get_call"))

        failed_args = {
            "data": {
                "status": "FAILED",
                "cursor": 0,
                "limit": 10
            }
        }

        failed_result = await (list_failed_calls_tool.ainvoke(failed_args))

        failed_payload = parse_mcp_result(failed_result)

        steps.append(
            WorkflowStep(
                step_name="list_failed_calls",
                input=failed_args,
                output=failed_payload
            )
        )

        if not failed_payload.get("success"):
            raise Exception(f"Failed call lookup failed: {failed_payload}")

        failed_calls = (failed_payload.get("calls", []))

        # -----------------------------
        # STEP 2
        # SORT MOST RECENT
        # -----------------------------

        failed_calls = sorted(
            failed_calls,
            key=lambda x: x.get(
                "created_at",
                ""
            ),
            reverse=True
        )

        recent_calls = failed_calls[:3]

        # -----------------------------
        # STEP 3
        # GET FULL CALL DETAILS fro top 3 failed one
        # -----------------------------

        call_details = []

        for call in recent_calls:

            call_id = call["call_id"]

            get_args = {
                "data": {
                    "call_id": call_id
                }
            }

            call_result = await (get_call_tool.ainvoke(get_args))

            call_payload = parse_mcp_result(call_result)

            steps.append(
                WorkflowStep(
                    step_name="get_call",
                    input=get_args,
                    output=call_payload
                )
            )

            if call_payload.get("success"):

                call_details.append(
                    call_payload["call"]
                )

        # -----------------------------
        # STEP 4
        # BUILD REVIEW PROMPT
        # -----------------------------

        prompt_parts = []

        prompt_parts.append(
            """
                You are a senior Quality Assurance analyst reviewing failed customer support calls.

                For each call analyze:

                1. Root cause of failure
                2. Customer sentiment
                3. Agent performance
                4. Missing troubleshooting steps
                5. Escalation necessity
                6. Recommended improvements

                Return a structured review report.
            """
        )

        for idx, call in enumerate(call_details,start=1):

            prompt_parts.append(
                f"""
                CALL {idx}
                ------------------------

                Call ID:
                {call.get("call_id")}

                Customer:
                {call.get("customer_name")}

                Duration:
                {call.get("duration_seconds")} seconds

                Status:
                {call.get("status")}

                Transcript:
                {call.get("transcript")}

                Notes:
                {call.get("notes")}
                """
            )

        quality_prompt = "\n".join(prompt_parts)
    
        return {
            "success": True,
            "workflow": "quality_review",
            "calls_analyzed": len(
                call_details
            ),
            "call_ids": [
                c["call_id"]
                for c in call_details
            ],
            "quality_review_prompt":
                quality_prompt
        }

    except Exception as e:

        return {
            "success": False,
            "workflow": "quality_review",
            "error": str(e)
        }