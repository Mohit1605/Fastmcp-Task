from langchain_mcp_adapters.client import MultiServerMCPClient
from core.constants import SERVER_CONFIG


class MCPClientManager:
    def __init__(self):
        self.client = None
        self.tools = []
        self.tool_map = {}
        self.is_connected = False

    async def connect(self):
        if not SERVER_CONFIG or not isinstance(SERVER_CONFIG, dict):
            raise ValueError("SERVER_CONFIG is missing or invalid")

        self.client = MultiServerMCPClient(SERVER_CONFIG)
        self.tools = await self.client.get_tools()

        if not self.tools:
            raise RuntimeError("No tools loaded from MCP servers")

        self.tool_map = {t.name: t for t in self.tools}

        self.is_connected = True

        print(f"✅ MCP Connected Successfully")
        print(f"🔧 Total Tools Loaded: {len(self.tools)}")

        return self.tools

    def get_tools(self):
        if not self.is_connected:
            raise RuntimeError("MCP not connected")
        return self.tools

    def get_tool_by_name(self, tool_name: str):
        tool = self.tool_map.get(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found")
        return tool

    def get_tool_schema(self, tool_name: str):
        tool = self.get_tool_by_name(tool_name)

        if hasattr(tool, "args_schema") and tool.args_schema:
            try:
                return tool.args_schema.model_json_schema()
            except:
                return tool.args_schema

        if hasattr(tool, "input_schema"):
            return tool.input_schema

        return {"type": "object", "properties": {}}