from fastmcp import FastMCP
from config import TRANSPORT, PORT
from core.middleware import AuthenticationMiddleware
from core.validators import validate_tool_annotations

from tools.write_tools import log_call,update_call_outcome,delete_call,add_call_note
from tools.read_tools import get_call,list_calls,list_calls_by_status,list_notes_for_call,get_stats,get_call_summary

from resources.call_resources import recent_calls,failed_calls

from prompts.call_prompts import quality_review

from schemas.call_schemas import LogCallResponse,GetCallResponse,ListCallsResponse,ListCallsByStatusResponse,UpdateCallOutcomeResponse,DeleteCallResponse,GetStatsResponse,GetCallSummaryResponse

from schemas.note_schemas import AddCallNoteResponse,ListNotesForCallResponse

mcp = FastMCP(name="Call Log MCP Server")

mcp.add_middleware(AuthenticationMiddleware())

TOOLS = [

    {
        "fn": log_call,
        "output_schema": LogCallResponse,
        "annotations": {
            "title": "Log A New Call",
            "requiredScope": "write",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False
        }
    },

    {
        "fn": get_call,
        "output_schema": GetCallResponse,
        "annotations": {
            "title": "Get Call By ID",
            "requiredScope": "read",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    },

    {
        "fn": list_calls,
        "output_schema": ListCallsResponse,
        "annotations": {
            "title": "List Calls",
            "requiredScope": "read",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    },

    {
        "fn": list_calls_by_status,
        "output_schema": ListCallsByStatusResponse,
        "annotations": {
            "title": "List Calls By Status",
            "requiredScope": "read",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    },

    {
        "fn": update_call_outcome,
        "output_schema": UpdateCallOutcomeResponse,
        "annotations": {
            "title": "Update Call Outcome",
            "requiredScope": "write",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False
        }
    },

    {
        "fn": delete_call,
        "output_schema": DeleteCallResponse,
        "annotations": {
            "title": "Delete Call",
            "requiredScope": "admin",
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": False,
            "openWorldHint": False
        }
    },

    {
        "fn": add_call_note,
        "output_schema": AddCallNoteResponse,
        "annotations": {
            "title": "Add Call Note",
            "requiredScope": "write",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False
        }
    },

    {
        "fn": list_notes_for_call,
        "output_schema": ListNotesForCallResponse,
        "annotations": {
            "title": "List Call Notes",
            "requiredScope": "read",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    },

    {
        "fn": get_stats,
        "output_schema": GetStatsResponse,
        "annotations": {
            "title": "Get Call Statistics",
            "requiredScope": "read",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    },

    {
        "fn": get_call_summary,
        "output_schema": GetCallSummaryResponse,
        "annotations": {
            "title": "Generate Call Summary",
            "requiredScope": "read",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": True
        }
    }
]

for tool in TOOLS:
  validate_tool_annotations(
    tool_name=tool["fn"].__name__,
    annotations=tool["annotations"]
  )

for tool in TOOLS:
  mcp.tool(
    output_schema=tool["output_schema"].model_json_schema(),
    annotations=tool["annotations"]
  )(tool["fn"])

mcp.resource("calls://recent/{n}")(recent_calls)
mcp.resource("calls://failed")(failed_calls)

mcp.prompt()(quality_review)

if __name__ == "__main__":

  if TRANSPORT == "stdio":
    mcp.run()

  elif TRANSPORT == "http":
    mcp.run(transport="http",host="0.0.0.0",port=PORT)

  else:
    raise ValueError(
            f"Unsupported TRANSPORT '{TRANSPORT}'. "
            f"Use 'stdio' or 'http'."
        )