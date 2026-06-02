from fastmcp import FastMCP
from core.middleware import AuthenticationMiddleware
from config import TRANSPORT, PORT
from tools.write_tools import create_job,add_technician,assign_job,close_job
from tools.read_tools import list_jobs,list_open_jobs,list_technicians,list_available_technicians
from resources.jobs_resources import get_all_jobs,get_open_jobs,get_available_technicians
from prompts.job_prompts import triage_job,assign_suggestion
from schemas.job_schemas import CreateCloseJobResponse,AssignJobResponse
from schemas.technician_schemas import CreateTechnicianResponse
from schemas.pagination_schema import PaginationResponse
from schemas.error_schema import ErrorResponse
from core.validators import validate_tool_annotations


mcp = FastMCP(name="Job Tracker MCP Server")
mcp.add_middleware(AuthenticationMiddleware())


TOOLS = [
  {
    "fn": create_job,
    "output_schema": CreateCloseJobResponse, 
    "annotations": {
        "title": "Create A New Job",
        "requiredScope": "write",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
  },

  {
    "fn": add_technician,
    "output_schema": CreateTechnicianResponse,   
    "annotations": {
        "title": "Create A New Technician",
        "requiredScope": "write",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
  },

  {
    "fn": assign_job,
    "output_schema": AssignJobResponse,  
    "annotations": {
        "title": "Assign Open Job To Available Technician",
        "requiredScope": "write",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
  },

  {
    "fn": close_job,
    "output_schema": CreateCloseJobResponse,
    "annotations": {
        "title": "Close Job",
        "requiredScope": "write",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
  },

  {
    "fn": list_jobs,
    "output_schema": PaginationResponse,
    "annotations": {
        "title": "List All Jobs",
        "requiredScope": "read",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
  },

  {
    "fn": list_open_jobs,
    "output_schema": PaginationResponse,
    "annotations": {
        "title": "List Open Jobs",
        "requiredScope": "read",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
  },

  {
    "fn": list_technicians,
    "output_schema": PaginationResponse, 
    "annotations": {
        "title": "List All Technicians",
        "requiredScope": "read",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
  },

  {
    "fn": list_available_technicians,
    "output_schema": PaginationResponse,
    "annotations": {
        "title": "List Available Technicians",
        "requiredScope": "read",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
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


mcp.resource("jobs://all")(get_all_jobs)
mcp.resource("jobs://open")(get_open_jobs)
mcp.resource("technicians://available")(get_available_technicians)


mcp.prompt()(triage_job)
mcp.prompt()(assign_suggestion)


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