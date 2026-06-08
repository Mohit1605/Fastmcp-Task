# Day 1: Job Tracker MCP Server

## Table of Contents
1. [Requirements](#requirements)
2. [Project Folder Structure](#project-folder-structure)
3. [File Overview](#file-overview)
4. [Installation](#installation)
5. [How to Run](#how-to-run)
6. [MCP Inspector Workflow](#mcp-inspector-workflow)
7. [Deep Dive Questions](#deep-dive-questions)
8. [Architecture & Trade-offs](#architecture--trade-offs)

---

## Requirements

Build an MCP server managing a job/task tracker with dual-transport support.

✅ **8 Tools (4 Read + 4 Write)**
- Read: list_jobs, list_open_jobs, list_technicians, list_available_technicians
- Write: create_job, add_technician, assign_job, close_job

✅ **3 Resources** - jobs://all, jobs://open, technicians://available

✅ **2 Prompts** - triage_job, assign_suggestion

✅ **Dual Transport** - STDIO (local) & HTTP:3000 (remote) via TRANSPORT env var

✅ **Type Safe** - Pydantic schemas, no untyped dicts

✅ **Error Guidance** - Every error includes next_action field

✅ **State Mutations** - Full workflows in single Inspector session

---

## Project Folder Structure

```
Day_1/
├── config.py                 # Environment configuration
├── requirements.txt          # Python dependencies
├── server.py               # Main MCP server entry point
├── .env                    # Environment variables (local)
├── .env.example            # Environment template
│
├── core/
│   ├── __init__.py         # Package initialization
│   ├── state.py            # In-memory data store and ID generators
│   └── test_state.py       # Unit tests for state module
│
├── prompts/
│   └── job_prompts.py      # Prompt definitions (triage_job, assign_suggestion)
│
├── resources/
│   └── jobs_resources.py   # Resource handlers (jobs://all, jobs://open, technicians://available)
│
├── schemas/
│   ├── job_schemas.py      # Pydantic schemas for job operations
│   ├── technician_schemas.py # Pydantic schemas for technician operations
│   └── types.py            # Enums and base response models
│
└── tools/
    ├── read_tools.py       # Read-only tool implementations
    ├── write_tools.py      # Mutation tool implementations
    ├── test_read_tools.py  # Unit tests for read tools
    └── test_write_tools.py # Unit tests for write tools
```

## File Overview

| File | Purpose |
|------|---------|
| **config.py** | Load TRANSPORT and PORT from environment |
| **server.py** | Register tools/resources/prompts; start MCP server |
| **core/state.py** | Global dicts for jobs & technicians; ID generators |
| **schemas/types.py** | Enums (JobStatus, JobPriority, TechnicianStatus) |
| **schemas/job_schemas.py** | Pydantic: CreateJobInput, AssignJobInput, CloseJobInput |
| **schemas/technician_schemas.py** | Pydantic: AddTechnicianInput |
| **tools/read_tools.py** | list_jobs, list_open_jobs, list_technicians, list_available_technicians |
| **tools/write_tools.py** | create_job, add_technician, assign_job, close_job |
| **resources/jobs_resources.py** | get_all_jobs, get_open_jobs, get_available_technicians (resources) |
| **prompts/job_prompts.py** | triage_job, assign_suggestion (prompt templates) |

## Installation

```bash
# Create & activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # Windows
source .venv/bin/activate          # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

**Dependencies:** fastmcp, pydantic, python-dotenv

---

## How to Run

**Setup environment:**
```bash
cp .env.example .env
```

**STDIO Mode (local, default):**
```bash
python server.py
# or explicitly: TRANSPORT=stdio python server.py
```

**HTTP Mode (remote access):**
```bash
TRANSPORT=http python server.py  # Port 3000
# Custom port: TRANSPORT=http PORT=8080 python server.py
```

**With MCP Inspector:**
```bash
# STDIO: 
npx @modelcontextprotocol/inspector stdio python server.py

# HTTP:
npx @modelcontextprotocol/inspector http://localhost:3000
```

---

## MCP Inspector Workflow

### Quick Test: Create → List → Assign → Close

**1. Create Job**
```json
{
  "title": "Fix Network Router",
  "description": "Router in building A is down, affecting 50 users",
  "priority": "high"
}
```
Returns: job_id (e.g., job_abc12345)

**2. Add Technician**
```json
{
  "name": "Alice Johnson",
  "skill": "Network Administration"
}
```
Returns: tech_id (e.g., tech_xyz78910)

**3. List Jobs**
Verify job appears in list with status "open"

**4. Assign Job**
```json
{
  "job_id": "job_abc12345",
  "technician_id": "tech_xyz78910"
}
```
Verify: Job status → "in_progress", Technician status → "busy"

**5. Call Triage Prompt**
Input: job_id
Returns: Structured analysis prompt for LLM

**6. Call Assignment Suggestion Prompt**
Input: job_id
Returns: Prompt with available technicians (now empty since Alice is busy)

**7. Close Job**
```json
{
  "job_id": "job_abc12345"
}
```
Verify: Job status → "closed", Technician status → "available" again

**8. List Available Technicians**
Verify: Alice appears in available list

### Error Scenarios

| Scenario | Expected |
|----------|----------|
| Assign non-existent job | ❌ "Job not found" + "use list_jobs" |
| Assign closed job | ❌ "Job already closed" + "create new job" |
| Assign to busy technician | ❌ "Technician busy" + "use list_available_technicians" |
| Invalid title (< 3 chars) | ❌ Pydantic validation error |

## Deep Dive Questions

### 1. Protocol-Level Differences: STDIO vs Streamable HTTP

**STDIO Transport:**
```
Client → stdin: JSON-RPC request
Server ← stdout: JSON-RPC response
```
- One connection per session
- Line-delimited JSON-RPC 2.0
- Synchronous request/response
- Pros: Simple, no network overhead
- Cons: Single connection, local-only, harder to debug

**HTTP/Streamable Transport:**
```
Client → HTTP POST: JSON-RPC request body
Server ← HTTP 200: JSON-RPC response body
```
- Multiple concurrent connections
- Standard HTTP requests/responses
- Each request is independent transaction
- Pros: Remote access, standards-based, debuggable with curl
- Cons: Higher latency, more overhead, needs network binding

### 2. Resource vs Tool: When to Use Each?

**Use RESOURCE when:**
- Providing context snapshots (jobs://all)
- Read-only data (no mutations)
- URI-based addressing (hierarchical)
- Sharing state with LLM before decisions
- Returning large datasets

**Use TOOL when:**
- Performing actions (create, modify, delete)
- Complex input validation needed
- Decision logic depends on parameters
- Need detailed error recovery guidance
- Must mutate state

**In this project:**
- Resources: jobs://all, jobs://open, technicians://available (context)
- Tools: create_job, assign_job, close_job (actions)

### 3. Server Crash Mid-Response (HTTP)

**Scenario:** Client sends request → server crashes → no response

**What Happens:**
1. TCP connection breaks immediately
2. No HTTP status code returned
3. Client receives ConnectionError/Timeout (after 30s)
4. JSON-RPC response never arrives

**Recovery:**
- Client: Retry logic with exponential backoff
- Server: Supervision (systemd, Docker, PM2)
- Production: Graceful shutdown handlers

### 4. Prompts vs Tools: Protocol & Client Behavior

| Aspect | Tool | Prompt |
|--------|------|--------|
| **Purpose** | Do work | Guide LLM reasoning |
| **Input** | Structured schema | String parameter |
| **Output** | JSON result | Prompt text |
| **Mutation** | Yes (tools only) | No |
| **Client Use** | Use result directly | Send to LLM for interpretation |
| **Protocol** | Tool use ID tracking | Text to LLM input |

**Flow:**
- **Tool:** Client calls → MCP executes → returns JSON → client uses data
- **Prompt:** Client calls → MCP returns prompt text → client sends to LLM → LLM responds → client uses LLM output

---

## Architecture & Trade-offs

### Why This Folder Structure?

**Layered Design:**
```
config.py         ← Environment
server.py         ← Transport & registration
core/            ← Data layer
schemas/         ← Validation layer
tools/           ← Action layer (read & write split)
resources/       ← Context layer
prompts/         ← Guidance layer
```

**Benefits:**
- Clear dependency flow
- Single responsibility per module
- Easy to test each layer
- Replaceable components

**Why split tools/read & write?**
- Read tools: Cache-friendly, audit logs separated from mutations
- Write tools: State-changing ops grouped together

### Strengths ✅

- Clean, readable code
- Type-safe (Pydantic)
- Easy to test (unit test files included)
- Extensible (add tools without changing structure)
- Transport-agnostic (same logic, two transports)

### Limitations ⚠️

- In-memory only (session-based, no persistence)
- Single process (no horizontal scaling)
- No authentication (HTTP is open)
- No audit logging
- Synchronous (no async support)

### Production Upgrades 📈

1. Add PostgreSQL/MongoDB for persistence
2. Async/await for I/O operations
3. API key/OAuth authentication
4. Structured audit logs (all mutations)
5. Rate limiting + health checks
6. Multi-tenancy support

---

## Summary

**This MCP server demonstrates:**

✅ **8 Tools** managing jobs/technicians workflow  
✅ **3 Resources** providing context snapshots  
✅ **2 Prompts** guiding LLM decisions  
✅ **Dual Transport** (STDIO ↔ HTTP via env var)  
✅ **Type Safety** throughout (Pydantic schemas)  
✅ **Error Guidance** with next_action fields  
✅ **State Persistence** (mutations visible across calls)  
✅ **Inspector Compatible** (full workflows testable)  

**Key Learning:** MCP abstracts transport details. Same business logic runs in STDIO (local) and HTTP (remote) modes. Resources provide context, Tools perform actions, Prompts guide reasoning.

**Lines of Code:** ~500 lines focused Python across 10 files demonstrating enterprise patterns: layered architecture, separation of concerns, comprehensive error handling, extensible design.

