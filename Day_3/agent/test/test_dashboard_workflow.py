import asyncio

from core.mcp_client import MCPClientManager
from workflows.workflow_dashboard_report import dashboard_report


async def seed_calls(mcp_client):

    log_call = mcp_client.get_tool_by_name("log_call")
    update_call_outcome = mcp_client.get_tool_by_name(
        "update_call_outcome"
    )

    created_calls = []

    # --------------------------------
    # COMPLETED CALLS
    # --------------------------------

    for i in range(3):

        result = await log_call.ainvoke(
            {
                "data": {
                    "customer_name": f"Completed Customer {i}",
                    "phone_number": f"99999999{i}",
                    "duration_seconds": 120,
                    "transcript": "Issue resolved",
                    "status": "COMPLETED"
                }
            }
        )

        created_calls.append(result)

    # --------------------------------
    # OPEN CALL
    # --------------------------------

    await log_call.ainvoke(
        {
            "data": {
                "customer_name": "Open Customer",
                "phone_number": "8888888888",
                "duration_seconds": 50,
                "transcript": "Waiting for callback",
                "status": "OPEN"
            }
        }
    )

    # --------------------------------
    # FAILED CALLS
    # --------------------------------

    for i in range(2):

        await log_call.ainvoke(
            {
                "data": {
                    "customer_name": f"Failed Customer {i}",
                    "phone_number": f"77777777{i}",
                    "duration_seconds": 400,
                    "transcript": "Call failed",
                    "status": "FAILED"
                }
            }
        )


async def seed_jobs(mcp_client):

    create_job = mcp_client.get_tool_by_name(
        "create_job"
    )

    close_job = mcp_client.get_tool_by_name(
        "close_job"
    )

    # --------------------------------
    # OPEN JOB 1
    # --------------------------------

    await create_job.ainvoke(
        {
            "data": {
                "title": "Fix Login Bug",
                "description": "Open Job",
                "priority": "high"
            }
        }
    )

    # --------------------------------
    # OPEN JOB 2
    # --------------------------------

    await create_job.ainvoke(
        {
            "data": {
                "title": "Database Issue",
                "description": "Open Job",
                "priority": "medium"
            }
        }
    )

    # --------------------------------
    # CLOSED JOB
    # --------------------------------

    result = await create_job.ainvoke(
        {
            "data": {
                "title": "Printer Issue",
                "description": "Will be closed",
                "priority": "low"
            }
        }
    )

    payload = result

    if isinstance(result, list):
        import json
        payload = json.loads(result[0]["text"])

    job_id = payload["job"]["id"]

    await close_job.ainvoke(
        {
            "data": {
                "job_id": job_id
            }
        }
    )


async def main():

    mcp = MCPClientManager()

    await mcp.connect()

    print("\n=== SEEDING CALLS ===")
    await seed_calls(mcp)

    print("\n=== SEEDING JOBS ===")
    await seed_jobs(mcp)

    print("\n=== RUNNING DASHBOARD WORKFLOW ===")

    result = await dashboard_report(
        query="Generate dashboard",
        mcp_client=mcp,
        context=None,
        logger=None,
        steps=[]
    )

    print("\n=== DASHBOARD RESULT ===")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())