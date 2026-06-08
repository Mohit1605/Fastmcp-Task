import time
from schemas.workflow import WorkflowResult, WorkflowStep
from core.argument_builder import ArgumentBuilder
import traceback
from schemas.tool_log import ToolLog
import json

class AgentExecutor:
    def __init__(self, mcp_client, router, workflows: dict, logger, llm_client):
        self.mcp_client = mcp_client
        self.router = router
        self.workflows = workflows
        self.logger = logger

        self.argument_builder = ArgumentBuilder(llm_client, mcp_client)

    async def execute(self, query: str, context):

        route = await self.router.route(query)
        print("\n===== ROUTE DECISION =====")
        print(route)
        print("==========================\n")
        context.add_metadata("route", route.model_dump())

        if route.workflow:
            return await self._run_workflow(route.workflow, query, context)

        if route.tool:
            return await self._run_tool(route.tool, query, context)

        return {
            "success": False,
            "message": "No route found",
            "route": route.model_dump()
        }

    async def _run_tool(self, tool_name: str, query: str, context):
        start = time.time()
        try:
            tool = self.mcp_client.get_tool_by_name(tool_name)
            print("\n===== TOOL INFO =====")
            print("NAME:", getattr(tool, "name", None))
            print("ARGS_SCHEMA:", getattr(tool, "args_schema", None))
            print("INPUT_SCHEMA:", getattr(tool, "input_schema", None))
            print("=====================\n")
            args = await self.argument_builder.build(tool_name, query)
            print("\n===== MCP INVOCATION =====")
            print("TOOL OBJECT:", tool)
            print("ARGS:", args)
            print("==========================\n")

            result = await tool.ainvoke(args)
            result = self._normalize_result(result)
            latency = int((time.time() - start) * 1000)
           
            log_entry = ToolLog(
                server="job",
                tool=tool_name,
                args=args,
                latency_ms=latency,
                response_size_bytes=len(str(result)),
                success=True
            )

            await self.logger.log(log_entry)

            return {
                "success": True,
                "tool": tool_name,
                "result": result
            }

        except Exception as e:
            return {
                "success": False,
                "tool": tool_name,
                "error": str(e)
            }

    async def _run_workflow(self, workflow_name: str, query: str, context):

        if workflow_name not in self.workflows:
            return {"success": False, "error": "workflow not found"}

        steps = []

        try:
            result = await self.workflows[workflow_name](
                query=query,
                mcp_client=self.mcp_client,
                context=context,
                logger=self.logger,
                steps=steps,
                argument_builder=self.argument_builder
            )

            return WorkflowResult(
                workflow_name=workflow_name,
                steps=steps,
                final_output=result,
                success=True
            )

        except Exception as e:

            return {
                "success": False,
                "workflow": workflow_name,
                "error": str(e)
            }


    def _normalize_result(self, result):

        if (
            isinstance(result, list)
            and len(result) > 0
            and isinstance(result[0], dict)
            and result[0].get("type") == "text"
        ):
            try:
                return json.loads(result[0]["text"])
            except Exception:
                return result

        return result