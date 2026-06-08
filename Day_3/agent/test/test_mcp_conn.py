import asyncio
from core.mcp_client import MCPClientManager

async def test():
    mcp = MCPClientManager()
    tools = await mcp.connect()

    print("\nTOOLS LOADED:")
    for t in tools:
        print("-", t.name)

asyncio.run(test())