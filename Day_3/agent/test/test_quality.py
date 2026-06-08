import asyncio

from core.mcp_client import MCPClientManager
from core.context import AgentContext
from core.executor import AgentExecutor
from router.tool_router import ToolRouter
from workflows.workflow_quality_review import quality_review

from langchain_google_genai import ChatGoogleGenerativeAI


async def seed_failed_calls(mcp):

    log_call_tool = mcp.get_tool_by_name("log_call")

    failed_calls = [
        {
            "data": {
                "customer_name": "John Doe",
                "phone_number": "9999999991",
                "duration_seconds": 120,
                "transcript": "Customer reported login failure. Could not access account.",
                "status": "FAILED"
            }
        },
        {
            "data": {
                "customer_name": "Jane Smith",
                "phone_number": "9999999992",
                "duration_seconds": 180,
                "transcript": "Payment failed during checkout. Customer extremely frustrated.",
                "status": "FAILED"
            }
        }
    ]

    for payload in failed_calls:
        result = await log_call_tool.ainvoke(payload)
        print(result)


async def main():
    llm=ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",api_key="AIzaSyAHwUPPYMQoysAHTyh-3oERowrx22jk3pw"
        )
    mcp = MCPClientManager()

    tools = await mcp.connect()

    print("Connected")

    await seed_failed_calls(mcp)

    print("\nFAILED CALLS CREATED\n")

    router = ToolRouter(tools,llm)

    executor = AgentExecutor(
        mcp_client=mcp,
        router=router,
        workflows={
            "quality_review": quality_review
        },
        logger=None,
        llm_client=None
    )

    context = AgentContext()

    result = await executor.execute(
        "Generate a quality review prompt for the 3 most recent failed calls",
        context
    )

    print("\nWORKFLOW RESULT\n")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())