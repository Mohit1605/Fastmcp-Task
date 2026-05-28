from fastmcp import FastMCP
from config import TRANSPORT, PORT
from tools.write_tools import create_job,add_technician,assign_job,close_job
from tools.read_tools import list_jobs,list_open_jobs,list_technicians,list_available_technicians
from resources.jobs_resources import get_all_jobs,get_open_jobs,get_available_technicians
from prompts.job_prompts import triage_job,assign_suggestion

mcp = FastMCP(name="Job Tracker MCP Server")

mcp.tool()(create_job)
mcp.tool()(add_technician)
mcp.tool()(assign_job)
mcp.tool()(close_job)

mcp.tool()(list_jobs)
mcp.tool()(list_open_jobs)
mcp.tool()(list_technicians)
mcp.tool()(list_available_technicians)


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