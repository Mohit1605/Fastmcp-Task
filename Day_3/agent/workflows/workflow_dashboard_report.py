import json

from schemas.workflow import WorkflowStep


def parse_mcp_result(result):

    if (isinstance(result, list) and len(result) > 0 and result[0].get("type") == "text"):
        return json.loads(result[0]["text"])
    return result


async def dashboard_report(query,mcp_client,context,logger,steps):
    try:

        get_stats_tool = mcp_client.get_tool_by_name("get_stats")

        list_jobs_tool = mcp_client.get_tool_by_name("list_jobs")

        get_stat_args = {
            "data": {}
        }

        stats_result = await get_stats_tool.ainvoke(get_stat_args)

        stats_payload = parse_mcp_result(stats_result)

        steps.append(
            WorkflowStep(
                step_name="get_stats",
                input={},
                output=stats_payload
            )
        )

        if not stats_payload.get("success"):
            raise Exception(f"Failed to get stats: {stats_payload}")

        all_jobs = []
        
        cursor = 0 
        
        page_args = {
            "data": {
                "cursor": cursor,
                "limit": 10
            }
        }

        while True:

            page_result = await list_jobs_tool.ainvoke(page_args)

            page_payload = parse_mcp_result(page_result)

            steps.append(
                WorkflowStep(
                    step_name="list_jobs",
                    input={
                        "data":{
                            "cursor": cursor,
                            "limit": 10
                        }
                        
                    },
                    output=page_payload
                )
            )

            if not page_payload.get("success"):
                raise Exception(f"Failed to load jobs: {page_payload}")

            all_jobs.extend(page_payload.get("data", []))

            if not page_payload.get("has_more"):
                break

            cursor = page_payload.get("next_cursor")


        total_calls = stats_payload.get("total_calls",0)

        status_counts = stats_payload.get("status_counts",{})

        open_calls = status_counts.get("OPEN",0)

        completed_calls = status_counts.get("COMPLETED",0)

        failed_calls = status_counts.get("FAILED",0)

        success_rate = 0

        if total_calls > 0:
            success_rate = round((completed_calls / total_calls) * 100,2)

        total_jobs = len(all_jobs)

        open_jobs = len([job for job in all_jobs if job["status"] != "closed"])

        closed_jobs = len([job for job in all_jobs if job["status"] == "closed"])

        progress_jobs = len([job for job in all_jobs if job["status"] == "in_progress"])


        report_data = {
            "calls": {
                "total": total_calls,
                "open": open_calls,
                "completed": completed_calls,
                "failed": failed_calls,
                "success_rate": success_rate
            },
            "jobs": {
                "total": total_jobs,
                "open": open_jobs,
                "in_progress":progress_jobs,
                "closed": closed_jobs
            }
        }

        return {
            "success": True,
            "workflow": "dashboard_report",
            "dashboard": report_data
        }

    except Exception as e:

        return {
            "success": False,
            "workflow": "dashboard_report",
            "error": str(e)
        }