import asyncio
from router.tool_router import ToolRouter
from core.mcp_client import MCPClientManager
from langchain_google_genai import ChatGoogleGenerativeAI
from schemas.routing_schema import RouteDecision

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite",api_key="AIzaSyA5jGulpClVROSwcJKY8U9irbhsw-opHP4")
llm_sturct = llm.with_structured_output(RouteDecision)

async def test():
    mcp = MCPClientManager()
    tools = await mcp.connect()

    router = ToolRouter(tools=tools, llm_client=llm_sturct)

    query = "create a job for API bug"

    decision = await router.route(query)

    print(decision)

asyncio.run(test())