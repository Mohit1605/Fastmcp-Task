import asyncio

from core.mcp_client import MCPClientManager
from router.tool_router import ToolRouter
from core.executor import AgentExecutor
from core.context import AgentContext
from logger.tool_logger import ToolLogger
from langchain_google_genai import ChatGoogleGenerativeAI
from workflows.create_link import create_link
from workflows.workflow_failed_sync import failed_sync
from workflows.workflow_quality_review import quality_review
from workflows.workflow_escalate_failed_calls import escalate_failed_calls
from workflows.workflow_dashboard_report import dashboard_report

WORKFLOWS = {
    "create_link": create_link,
    "failed_sync":failed_sync,
    "quality_review":quality_review,
    "escalate_failed_calls":escalate_failed_calls,
    "dashboard_report": dashboard_report
}

async def main():

    print("\n🚀 Starting Multi-Server MCP Agent...\n")

    # -----------------------------
    # 1. INIT MCP CLIENT
    # -----------------------------
    mcp = MCPClientManager()

    tools = await mcp.connect()
    print(f"✅ MCP Connected | Tools Loaded: {len(tools)}")

  
    llm_client = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite",api_key="AIzaSyDh23EJUR5azOot0p1ijgXTTnGyA1M7aLY") 

    router = ToolRouter(tools=tools,llm_client=llm_client)

    logger = ToolLogger()

    executor = AgentExecutor(
        mcp_client=mcp,
        router=router,
        workflows=WORKFLOWS,
        logger=logger,
        llm_client=llm_client
    )

    # -----------------------------
    # 5. CREATE CONTEXT
    # -----------------------------
    context = AgentContext()

    print("\n🧠 Agent Ready. Type your queries below:\n")

    # -----------------------------
    # 6. INTERACTIVE LOOP
    # -----------------------------
    while True:

        try:
            query = input("User > ")

            if query.lower() in ["exit", "quit"]:
                print("👋 Shutting down agent...")
                break

            # EXECUTE FULL PIPELINE
            result = await executor.execute(query, context)

            print("\n🤖 RESULT:\n")
            print(result)

            print("\n──────────────────────────────\n")

        except Exception as e:
            print(f"❌ Runtime Error: {str(e)}")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    asyncio.run(main())

