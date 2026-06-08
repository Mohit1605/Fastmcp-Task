import asyncio
from core.executor import AgentExecutor
from core.context import AgentContext
from core.mcp_client import MCPClientManager
from logger.tool_logger import ToolLogger

async def test():
    mcp = MCPClientManager()
    tools = await mcp.connect()

    executor = AgentExecutor(
        mcp_client=mcp,
        router=None,
        workflows={},
        logger=ToolLogger()
    )

    context = AgentContext()

    result = await executor._run_tool(
        "list_jobs",
        {"cursor": 0, "limit": 2},
        context
    )

    print(result)

asyncio.run(test())