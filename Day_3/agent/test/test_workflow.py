import asyncio
from workflows.create_link import create_link
from core.context import AgentContext
from core.mcp_client import MCPClientManager
from logger.tool_logger import ToolLogger

async def test():
    mcp = MCPClientManager()
    await mcp.connect()

    context = AgentContext()
    logger = ToolLogger()

    steps = []

    result = await create_link(
        query="create job and log call for API bug",
        mcp_client=mcp,
        context=context,
        logger=logger,
        steps=steps
    )

    print(result)

asyncio.run(test())