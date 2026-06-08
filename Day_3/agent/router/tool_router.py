from schemas.routing_schema import RouteDecision
import json


class ToolRouter:
    def __init__(self, tools, llm_client):
        self.tools = tools
        self.llm = llm_client

        self.job_tools = [
            t.name for t in tools
            if t.name in {
                "create_job",
                
                "add_technician",
                "assign_job",
                "close_job",
                "list_jobs",
                "list_open_jobs",
                "list_technicians",
                "list_available_technicians"
            }
        ]
        self.call_tools = [
            t.name for t in tools
            if t.name in {
                "log_call",
                "get_call",
                "list_calls",
                "list_calls_by_status",
                "update_call_outcome",
                "delete_call",
                "add_call_note",
                "list_notes_for_call",
                "get_call_summary",
                "get_stats"
            }
        ]

    async def route(self, query: str) -> RouteDecision:

        prompt = self._build_prompt(query)

        try:
            response = await self.llm.ainvoke(prompt)

            print("\n===== RAW ROUTER RESPONSE =====")
            print(response.content)
            print("===============================\n")

            data = json.loads(response.content)

            tool = data.get("tool")
            workflow = data.get("workflow")
            confidence = data.get("confidence", 0.5)
            reason = data.get("reason", "")
            if workflow:
                return RouteDecision(
                    server="workflow",
                    tool=None,
                    workflow=workflow,
                    confidence=confidence,
                    reason=reason
                )
            server = self._infer_server(tool)

            return RouteDecision(
                server=server,
                tool=tool,
                workflow=workflow,
                confidence=confidence,
                reason=reason
            )

        except Exception as e:
            return RouteDecision(
                server="job",
                tool="list_jobs",
                workflow=None,
                confidence=0.3,
                reason=f"fallback: {str(e)}"
            )

    def _infer_server(self, tool_name: str):
        if tool_name in self.job_tools:
            return "job"
        if tool_name in self.call_tools:
            return "call"
        return None

    def _build_prompt(self, query: str):

        return f"""
            You are an MCP routing engine.

            TOOLS:
            JOB: {self.job_tools}
            CALL: {self.call_tools}

            WORKFLOWS:
            -> create_link -  create a job, log a related call, link them by job_id stored in call notes, 
            failed_sync - etch all failed calls, find the matching open jobs, bulk-update job status, 

            -> escalate_failed_calls - use when the call duration is long and call status is failed the auotomate to the create Job, Call Failed -> Automate the job creation 
            -> quality_review - use this workflow when user ask about the generate quality prompt, review the recent fail, Analyse last failed call
            -> dashboard_report - use this workflow when user ask for the report for the all job and the call acc to thier jobstatus, calloutcome

            Do not give the response in ```json ``` and markdown format. Return ONLY JSON in below format:
            {{
            "tool": "... or null",
            "workflow": "... or null",
            "confidence": 0-1,
            "reason": "..."
            }}

            USER:
            {query}
        """