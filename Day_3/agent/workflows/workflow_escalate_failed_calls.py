import json
from schemas.workflow import WorkflowStep


def parse_mcp_result(result):
    """
    Convert MCP response -> dict
    """

    if isinstance(result, list):
        text = result[0]["text"]
        return json.loads(text)

    return result


async def escalate_failed_calls(
    query,
    mcp_client,
    context,
    logger,
    steps
):
    try:

        # ----------------------------------
        # LOAD TOOLS
        # ----------------------------------

        list_failed_calls_tool = mcp_client.get_tool_by_name(
            "list_calls_by_status"
        )

        get_call_tool = mcp_client.get_tool_by_name(
            "get_call"
        )

        list_jobs_tool = mcp_client.get_tool_by_name(
            "list_jobs"
        )

        create_job_tool = mcp_client.get_tool_by_name(
            "create_job"
        )

        # ----------------------------------
        # STEP 1
        # GET FAILED CALLS
        # ----------------------------------

        failed_call_args = {
            "data": {
                "status": "FAILED",
                "cursor": 0,
                "limit": 10
            }
        }

        failed_result = await list_failed_calls_tool.ainvoke(
            failed_call_args
        )

        failed_payload = parse_mcp_result(
            failed_result
        )

        steps.append(
            WorkflowStep(
                step_name="list_failed_calls",
                input=failed_call_args,
                output=failed_payload
            )
        )

        if not failed_payload.get("success"):
            raise Exception(
                f"Failed calls lookup failed: {failed_payload}"
            )

        failed_calls = failed_payload.get(
            "calls",
            []
        )

        # ----------------------------------
        # STEP 2
        # LOAD EXISTING JOBS
        # ----------------------------------

        jobs_result = await list_jobs_tool.ainvoke({})

        jobs_payload = parse_mcp_result(
            jobs_result
        )

        steps.append(
            WorkflowStep(
                step_name="list_jobs",
                input={},
                output=jobs_payload
            )
        )

        existing_jobs = jobs_payload.get(
            "data",
            []
        )

        created_jobs = []
        skipped_calls = []

        # ----------------------------------
        # STEP 3
        # PROCESS FAILED CALLS
        # ----------------------------------

        for call_summary in failed_calls:

            call_id = call_summary.get("call_id")

            if not call_id:
                continue

            # ------------------------------
            # GET FULL CALL
            # ------------------------------

            get_call_args = {
                "data": {
                    "call_id": call_id
                }
            }

            call_result = await get_call_tool.ainvoke(
                get_call_args
            )

            call_payload = parse_mcp_result(
                call_result
            )

            steps.append(
                WorkflowStep(
                    step_name=f"get_call_{call_id}",
                    input=get_call_args,
                    output=call_payload
                )
            )

            if not call_payload.get("success"):
                continue

            call = call_payload["call"]

            duration = call.get(
                "duration_seconds",
                0
            )

            # ------------------------------
            # ONLY ESCALATE LONG CALLS
            # ------------------------------

            if duration <= 300:

                skipped_calls.append(
                    {
                        "call_id": call_id,
                        "reason": "duration_under_threshold"
                    }
                )

                continue

            # ------------------------------
            # DUPLICATE CHECK
            # ------------------------------

            already_escalated = False

            for job in existing_jobs:

                description = job.get(
                    "description",
                    ""
                )

                if f"Call ID: {call_id}" in description:

                    already_escalated = True

                    skipped_calls.append(
                        {
                            "call_id": call_id,
                            "reason": "already_escalated"
                        }
                    )

                    break

            if already_escalated:
                continue

            # ------------------------------
            # CREATE ESCALATION JOB
            # ------------------------------

            customer_name = call.get(
                "customer_name",
                "Unknown"
            )

            transcript = call.get(
                "transcript",
                ""
            )

            create_job_args = {
                "data": {
                    "title":
                        f"Escalation - Failed Call {call_id}",

                    "description":
                        (
                            f"Call ID: {call_id}\n\n"
                            f"Customer: {customer_name}\n"
                            f"Duration: {duration} seconds\n\n"
                            f"Transcript:\n{transcript}"
                        ),

                    "priority": "high"
                }
            }

            job_result = await create_job_tool.ainvoke(
                create_job_args
            )

            job_payload = parse_mcp_result(
                job_result
            )

            steps.append(
                WorkflowStep(
                    step_name=f"create_job_{call_id}",
                    input=create_job_args,
                    output=job_payload
                )
            )

            if not job_payload.get("success"):

                skipped_calls.append(
                    {
                        "call_id": call_id,
                        "reason": "job_creation_failed"
                    }
                )

                continue

            created_job = job_payload["job"]

            created_jobs.append(
                {
                    "call_id": call_id,
                    "job_id": created_job["id"]
                }
            )

            # IMPORTANT:
            # add newly created job to local cache
            # so duplicate check works during same run

            existing_jobs.append(
                created_job
            )

        # ----------------------------------
        # FINAL RESULT
        # ----------------------------------

        return {
            "success": True,
            "workflow": "escalate_failed_calls",
            "failed_calls_checked": len(
                failed_calls
            ),
            "created_jobs": created_jobs,
            "skipped_calls": skipped_calls
        }

    except Exception as e:

        return {
            "success": False,
            "workflow": "escalate_failed_calls",
            "error": str(e)
        }