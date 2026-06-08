import asyncio

from core.mcp_client import MCPClientManager
from core.executor import AgentExecutor
from core.context import AgentContext
from router.tool_router import ToolRouter

from workflows.workflow_escalate_failed_calls import (
    escalate_failed_calls
)

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite",api_key="AIzaSyA33KjWP_HJOKZic38CTYO_EE_OSi5kCjQ")
async def seed_calls(mcp):

    log_call_tool = mcp.get_tool_by_name(
        "log_call"
    )

    print("\n🌱 Seeding failed calls...\n")

    seed_data = [

        # SHOULD BE SKIPPED
        {
            "data": {
                "customer_name": "John",
                "phone_number": "9999999991",
                "duration_seconds": 120,
                "transcript": "Minor login issue",
                "status": "FAILED"
            }
        },

        # SHOULD CREATE JOB
        {
            "data": {
                "customer_name": "Jane",
                "phone_number": "9999999992",
                "duration_seconds": 450,
                "transcript": "Unable to login for several days",
                "status": "FAILED"
            }
        },

        # SHOULD CREATE JOB
        {
            "data": {
                "customer_name": "Robert",
                "phone_number": "9999999993",
                "duration_seconds": 700,
                "transcript": "Payment and account access both failing",
                "status": "FAILED"
            }
        },

        # NOT FAILED
        {
            "data": {
                "customer_name": "Alice",
                "phone_number": "9999999994",
                "duration_seconds": 500,
                "transcript": "Issue resolved",
                "status": "COMPLETED"
            }
        }
    ]

    for payload in seed_data:

        result = await log_call_tool.ainvoke(
            payload
        )

        print(result)


async def main():

    print("\n🚀 Connecting MCP...\n")

    mcp = MCPClientManager()

    tools = await mcp.connect()

    print("✅ Connected")

    # --------------------------------
    # SEED TEST DATA
    # --------------------------------

    await seed_calls(mcp)

    print("\n✅ Seed Complete\n")

    # --------------------------------
    # BUILD EXECUTOR
    # --------------------------------

    router = ToolRouter(tools,llm)

    executor = AgentExecutor(
        mcp_client=mcp,
        router=router,
        workflows={
            "escalate_failed_calls":
                escalate_failed_calls
        },
        logger=None,
        llm_client=llm
    )

    context = AgentContext()

    # --------------------------------
    # RUN WORKFLOW
    # --------------------------------

    print(
        "\n🔥 Running Escalation Workflow...\n"
    )

    result = await executor.execute(
        "Escalate failed calls",
        context
    )

    print("\n==============================")
    print("WORKFLOW RESULT")
    print("==============================\n")

    print(result)


if __name__ == "__main__":
    asyncio.run(main())