import json
import re

from schemas.workflow import WorkflowStep


def parse_mcp_result(result):

    if (
        isinstance(result, list)
        and len(result) > 0
        and result[0].get("type") == "text"
    ):
        return json.loads(result[0]["text"])

    return result


async def failed_sync(query,mcp_client,context,logger,steps):
    try:

        list_failed_calls_tool = (
            mcp_client.get_tool_by_name(
                "list_calls_by_status"
            )
        )

        list_notes_tool = (
            mcp_client.get_tool_by_name(
                "list_notes_for_call"
            )
        )

        list_open_jobs_tool = (
            mcp_client.get_tool_by_name(
                "list_open_jobs"
            )
        )

        close_job_tool = (
            mcp_client.get_tool_by_name(
                "close_job"
            )
        )

        failed_args = {
            "data": {
                "status": "FAILED",
                "cursor": 0,
                "limit": 10
            }
        }

        failed_result = await (
            list_failed_calls_tool.ainvoke(
                failed_args
            )
        )

        failed_payload = parse_mcp_result(
            failed_result
        )

        failed_calls = failed_payload.get(
            "calls",
            []
        )

        steps.append(
            WorkflowStep(
                step_name="list_failed_calls",
                input=failed_args,
                output=failed_payload
            )
        )

        linked_job_ids = set()

        for call in failed_calls:

            call_id = call["call_id"]

            note_args = {
                "data": {
                    "call_id": call_id
                }
            }

            notes_result = await (
                list_notes_tool.ainvoke(
                    note_args
                )
            )

            notes_payload = parse_mcp_result(
                notes_result
            )

            steps.append(
                WorkflowStep(
                    step_name="list_notes_for_call",
                    input=note_args,
                    output=notes_payload
                )
            )

            for note in notes_payload.get(
                "notes",
                []
            ):

                match = re.search(
                    r"job_[a-zA-Z0-9]+",
                    note
                )

                if match:
                    linked_job_ids.add(
                        match.group(0)
                    )

        open_jobs_result = await (
            list_open_jobs_tool.ainvoke({})
        )

        open_jobs_payload = parse_mcp_result(
            open_jobs_result
        )

        open_jobs = open_jobs_payload.get(
            "data",
            []
        )

        steps.append(
            WorkflowStep(
                step_name="list_open_jobs",
                input={},
                output=open_jobs_payload
            )
        )

        open_job_map = {
            job["id"]: job
            for job in open_jobs
        }

        closed_jobs = []

        for job_id in linked_job_ids:

            if job_id not in open_job_map:
                continue

            close_args = {
                "data": {
                    "job_id": job_id
                }
            }

            close_result = await (
                close_job_tool.ainvoke(
                    close_args
                )
            )

            close_payload = parse_mcp_result(
                close_result
            )

            steps.append(
                WorkflowStep(
                    step_name="close_job",
                    input=close_args,
                    output=close_payload
                )
            )

            if close_payload.get("success"):
                closed_jobs.append(
                    job_id
                )

        return {
            "success": True,
            "workflow": "failed_sync",
            "failed_calls_found": len(
                failed_calls
            ),
            "linked_jobs_found": list(
                linked_job_ids
            ),
            "closed_jobs": closed_jobs
        }

    except Exception as e:

        return {
            "success": False,
            "workflow": "failed_sync",
            "error": str(e)
        }