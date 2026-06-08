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


async def create_link(query,mcp_client,context,logger,steps,argument_builder):

    try:

        # -----------------------------
        # LOAD TOOLS
        # -----------------------------

        create_job_tool = mcp_client.get_tool_by_name("create_job")

        log_call_tool = mcp_client.get_tool_by_name("log_call")

        add_note_tool = mcp_client.get_tool_by_name("add_call_note")

        # =====================================================
        # STEP 1
        # DYNAMIC JOB CREATION (1 LLM CALL)
        # =====================================================

        job_args = await argument_builder.build("create_job",query)

        job_result = await create_job_tool.ainvoke(job_args)

        job_payload = parse_mcp_result(job_result)

        if not job_payload.get("success"):
            raise Exception(f"Create Job Failed: {job_payload}")

        job = job_payload["job"]

        job_id = job["id"]

        steps.append(
            WorkflowStep(
                step_name="create_job",
                input=job_args,
                output=job_payload
            )
        )

        # =====================================================
        # STEP 2
        # CREATE RELATED CALL (NO LLM)
        # =====================================================

        call_args = {
            "data": {
                "customer_name": "Workflow Customer",
                "phone_number": "0000000000",
                "duration_seconds": 60,
                "transcript": (
                    f"Customer reported issue related to "
                    f"job '{job['title']}' "
                    f"({job_id}). "
                    f"{job['description']}"
                ),
                "status": "OPEN"
            }
        }

        call_result = await log_call_tool.ainvoke(call_args)

        call_payload = parse_mcp_result(call_result)

        if not call_payload.get("success"):
            raise Exception(
                f"Log Call Failed: {call_payload}"
            )

        call = call_payload["call"]

        call_id = call["call_id"]

        steps.append(
            WorkflowStep(
                step_name="log_call",
                input=call_args,
                output=call_payload
            )
        )

        # =====================================================
        # STEP 3
        # LINK CALL ↔ JOB
        # =====================================================

        note_args = {
            "data": {
                "call_id": call_id,
                "note": (
                    f"Linked Job: {job_id}"
                )
            }
        }

        note_result = await add_note_tool.ainvoke(note_args)

        note_payload = parse_mcp_result(note_result)

        if not note_payload.get("success"):
            raise Exception(f"Failed To Link: {note_payload}")

        steps.append(
            WorkflowStep(
                step_name="add_call_note",
                input=note_args,
                output=note_payload
            )
        )

        # =====================================================
        # FINAL RESULT
        # =====================================================

        return {
            "success": True,
            "workflow": "create_link",
            "job": job,
            "call": call,
            "link_note": note_payload
        }

    except Exception as e:

        return {
            "success": False,
            "workflow": "create_link",
            "error": str(e)
        }