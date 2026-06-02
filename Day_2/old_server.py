from fastmcp import FastMCP
from config import TRANSPORT, PORT
from tools.write_tools import create_job,add_technician,assign_job,close_job
from tools.read_tools import list_jobs,list_open_jobs,list_technicians,list_available_technicians
from resources.jobs_resources import get_all_jobs,get_open_jobs,get_available_technicians
from prompts.job_prompts import triage_job,assign_suggestion
from schemas.job_schemas import CreateCloseJobResponse,AssingJobResponse
from schemas.technician_schemas import CreateTechnicianResponse
from schemas.pagination_schema import PaginationResponse

mcp = FastMCP(name="Job Tracker MCP Server")

mcp.tool(
          output_schema=CreateCloseJobResponse.model_json_schema(),
          annotations={
              "title" : "Create A New Job",
              "readOnlyHint": False,
              "destructiveHint": False,
              "idempotentHint": False,
              "openWorldHint": False
          }
        )(create_job)

mcp.tool(
          output_schema=CreateTechnicianResponse.model_json_schema(),
          annotations={
              "title":"Create A New Technician",
              "readOnlyHint": False,
              "destructiveHint": False,
              "idempotentHint": False,
              "openWorldHint": False
          }
        )(add_technician)

mcp.tool(
          output_schema=AssingJobResponse.model_json_schema(),
          annotations={
              "title":"Assign Open Job to Available Technician",
              "readOnlyHint": False,
              "destructiveHint": False,
              "idempotentHint": True,
              "openWorldHint": False
          }
        )(assign_job)

mcp.tool(
          output_schema=CreateCloseJobResponse.model_json_schema(),
          annotations={
              "title":"Close Job",
              "readOnlyHint": False,
              "destructiveHint": False,
              "idempotentHint": True,
              "openWorldHint": False
          }
        )(close_job)

mcp.tool( 
          output_schema=PaginationResponse.model_json_schema(),
          annotations={
              "title":"List All Jobs",
              "readOnlyHint": True,
              "destructiveHint": False,
              "idempotentHint": True,
              "openWorldHint": False
          }
        )(list_jobs)

mcp.tool(
          output_schema=PaginationResponse.model_json_schema(),
          annotations={
              "title":"List Open Jobs",
              "readOnlyHint": True,
              "destructiveHint": False,
              "idempotentHint": True,
              "openWorldHint": False
          }
        )(list_open_jobs)

mcp.tool(
          output_schema=PaginationResponse.model_json_schema(),
          annotations={
              "title":"List All Technicians",
              "readOnlyHint": True,
              "destructiveHint": False,
              "idempotentHint": True,
              "openWorldHint": False
          }
        )(list_technicians)

mcp.tool(
          output_schema=PaginationResponse.model_json_schema(),
          annotations={
              "title" : "List Available Technicians",
              "readOnlyHint": True,
              "destructiveHint": False,
              "idempotentHint": True,
              "openWorldHint": False
          }
        )(list_available_technicians)


mcp.resource("jobs://all")(get_all_jobs)
mcp.resource("jobs://open")(get_open_jobs)
mcp.resource("technicians://available")(get_available_technicians)


mcp.prompt()(triage_job)
mcp.prompt()(assign_suggestion)


if __name__ == "__main__":

  # print(f"\nStarting MCP server using transport: {TRANSPORT}\n")

  if TRANSPORT == "stdio":
    mcp.run()

  elif TRANSPORT == "http":
    mcp.run(transport="http",host="0.0.0.0",port=PORT)

  else:
    raise ValueError(
      f"Unsupported TRANSPORT '{TRANSPORT}'. "
      f"Use 'stdio' or 'http'."
    )