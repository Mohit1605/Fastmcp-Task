import json
import re


class ArgumentBuilder:
    def __init__(self, llm_client, mcp_client):
        self.llm = llm_client
        self.mcp = mcp_client

    async def build(self, tool_name: str, query: str):

        schema = self.mcp.get_tool_schema(tool_name)
        print("\n===== TOOL SCHEMA =====")
        print("TOOL:", tool_name)
        print(schema)
        print("=======================\n")
        prompt = self._build_prompt(tool_name, query, schema)

        response = await self.llm.ainvoke(prompt)
        text = response.content
        parsed = self._safe_parse(text)

        if parsed:
            return parsed

        return {"query": query}

    def _build_prompt(self, tool_name: str, query: str, schema: dict):

        return f"""
            Convert user query into JSON matching schema EXACTLY.

            TOOL: {tool_name}

            SCHEMA:
            {json.dumps(schema, indent=2)}

            USER QUERY:
            {query}

            RULES:
            - ONLY JSON
            - NO extra fields
            - match schema strictly

            OUTPUT:
        """

    def _safe_parse(self, text: str):
        try:
            return json.loads(text)
        except:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    return None
        return None