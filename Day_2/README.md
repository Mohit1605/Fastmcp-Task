# Day 2 - Job Tracker MCP Server

## Overview

`Day_2` is a FastMCP-based job tracking server built around an in-memory data store. It exposes tools for creating jobs, managing technicians, assigning and closing jobs, plus list tools with cursor-based pagination. The server is organized to support both HTTP and stdio transport modes, with authentication and scope checks applied at the tool-call layer.

The codebase is split into small, focused modules so the server logic stays easy to reason about:

- `core/` contains authentication, authorization, pagination, error handling, middleware, shared state, and startup validation.
- `schemas/` defines the Pydantic input and output models used by tools.
- `tools/` contains the read and write tool implementations.
- `resources/` exposes resource endpoints that return snapshots of the in-memory store.
- `prompts/` provides reusable prompt templates for agent workflows.
- `unit test/` and `test suite/` contain lightweight test scripts for the main flows.

## Folder Structure

```text
Day_2/
├── .env
├── .env-example
├── .gitignore
├── config.py
├── old_server.py
├── requirements.txt
├── server.py
├── core/
│   ├── __init__.py
│   ├── auth.py
│   ├── auth_provider.py
│   ├── errors.py
│   ├── middleware.py
│   ├── pagination.py
│   ├── permissions.py
│   ├── state.py
│   └── validators.py
├── prompts/
│   └── job_prompts.py
├── resources/
│   └── jobs_resources.py
├── schemas/
│   ├── error_schema.py
│   ├── job_schemas.py
│   ├── pagination_schema.py
│   ├── technician_schemas.py
│   └── types.py
├── test suite/
│   ├── test_auth.py
│   ├── test_pagination.py
│   └── test_permission.py
├── tools/
│   ├── read_tools.py
│   └── write_tools.py
└── unit test/
    ├── __init__.py
    ├── test_auth.py
    ├── test_idempotancy.py
    ├── test_pagination.py
    ├── test_permission.py
    ├── test_read_tools.py
    ├── test_state.py
    └── test_write_tools.py
```

## What This Server Does

This server models a simple job tracker with two in-memory collections:

- `jobs`
- `technicians`

Jobs can be created, assigned, listed, and closed. Technicians can be created and listed, and their availability changes as jobs are assigned and closed. Because the storage is in memory, all data is reset when the process restarts.

The server exposes:

- 8 tools
- 3 resources
- 2 prompts

## Runtime Entry Point

The main server bootstrap lives in [`server.py`](./server.py).

At startup, it:

1. Creates a `FastMCP` server instance.
2. Attaches `AuthenticationMiddleware`.
3. Registers each tool with an `output_schema` and strict annotations.
4. Registers resources and prompts.
5. Runs in either `stdio` or `http` mode depending on `TRANSPORT`.

If `TRANSPORT=stdio`, the server runs locally over stdio. If `TRANSPORT=http`, it listens on the configured host and port.

## Configuration

Configuration is loaded in [`config.py`](./config.py) using environment variables.

- `TRANSPORT` controls the transport mode.
- `PORT` sets the HTTP port.
- `.env-example` shows the expected environment variables.

Example:

```env
TRANSPORT=http
PORT=3000
AUTH_TOKEN=writer-token
```

## Authentication

Authentication is implemented manually, without any auth library.

### Token Flow

- [`core/auth_provider.py`](./core/auth_provider.py) extracts the token.
- For HTTP, it reads the `Authorization: Bearer <token>` header.
- For stdio, it reads the `AUTH_TOKEN` environment variable.
- [`core/auth.py`](./core/auth.py) validates the token against a hardcoded registry.
- Valid tokens are stored in `TOKEN_REGISTRY` with scopes and expiry data.

### Scope Checks

Authorization is handled through [`core/permissions.py`](./core/permissions.py).

- Read tools require `read`.
- Write tools require `write`.
- The current auth context is stored with a `ContextVar`, so the permission check can be reused across tool calls.

### Expiry Behavior

Tokens in the registry include `expires_at` values.

- If a token is missing, the server returns an `UNAUTHORIZED` style error.
- If a token is invalid, the server returns `INVALID_TOKEN`.
- If a token is expired, the server returns `TOKEN_EXPIRED` and includes how many seconds ago the token expired.

## Pagination

Cursor-based pagination is implemented in [`core/pagination.py`](./core/pagination.py).

The list tools support:

- `cursor`
- `limit`

The response shape is:

- `data`
- `next_cursor`
- `has_more`
- `total_count`

This applies to:

- `list_jobs`
- `list_open_jobs`
- `list_technicians`
- `list_available_technicians`

### Why Cursor Pagination

Cursor-based pagination is preferred over offset pagination because it is more stable when the underlying in-memory store changes between calls. If items are inserted or removed while a client is paging, offsets can skip or duplicate results. A cursor is a better fit for MCP-style tool chains because it preserves the client’s place in a changing dataset.

## Tool Design

The tools are registered in [`server.py`](./server.py) and implemented in the `tools/` directory.

### Write Tools

Defined in [`tools/write_tools.py`](./tools/write_tools.py):

- `create_job`
- `add_technician`
- `assign_job`
- `close_job`

These tools mutate in-memory state and are protected by `write` scope.

### Read Tools

Defined in [`tools/read_tools.py`](./tools/read_tools.py):

- `list_jobs`
- `list_open_jobs`
- `list_technicians`
- `list_available_technicians`

These tools are read-only and protected by `read` scope.

### Tool Output Schemas

Structured outputs are defined in [`schemas/`](./schemas).

- `job_schemas.py` defines job inputs and write-tool responses.
- `technician_schemas.py` defines technician inputs and responses.
- `pagination_schema.py` defines the shared list response format.
- `error_schema.py` defines a standard error payload.

Using `output_schema` for every tool lets clients parse results reliably without depending on free-form text.

## Tool Annotations

Each tool is registered with annotations in [`server.py`](./server.py), including:

- `readOnlyHint`
- `destructiveHint`
- `idempotentHint`
- `openWorldHint`

These hints help an MCP host understand tool behavior and choose safer execution strategies.

### Startup Validation

[`core/validators.py`](./core/validators.py) enforces the rule that a tool cannot be both destructive and idempotent. This check runs before tool registration completes, so bad annotations fail fast.

## Error Handling

Errors are normalized through [`core/errors.py`](./core/errors.py) and [`schemas/error_schema.py`](./schemas/error_schema.py).

The standard error shape is:

```json
{
  "error": "Human readable message",
  "code": "MACHINE_READABLE_CODE",
  "suggestion": "Recommended next step"
}
```

HTTP auth failures also return a compact error payload with `error` and `hint` fields so unauthenticated requests can be rejected cleanly.

## Shared State

[`core/state.py`](./core/state.py) holds the in-memory collections and ID generators.

- `jobs` stores job records.
- `technicians` stores technician records.
- `generate_job_id()` creates unique job IDs.
- `generate_technician_id()` creates unique technician IDs.
- `reset_state()` clears both collections, which is useful for tests.

## Resources

The server exports three resources from [`resources/jobs_resources.py`](./resources/jobs_resources.py):

- `jobs://all`
- `jobs://open`
- `technicians://available`

These resources provide snapshot-style access to the current state of the store.

## Prompts

Reusable prompt templates live in [`prompts/job_prompts.py`](./prompts/job_prompts.py):

- `triage_job(job_id)`
- `assign_suggestion(job_id)`

These prompts use the current in-memory state to generate context-rich instructions for an agent.

## Data Models

Common enums and models are defined in [`schemas/types.py`](./schemas/types.py):

- `JobStatus`
- `JobPriority`
- `TechnicianStatus`

The request and response models in the other schema files use these enums to keep payloads consistent and validated.

## Tests

There are two test folders:

- [`unit test/`](./unit%20test/)
- [`test suite/`](./test%20suite/)

They cover:

- token validation
- permission checks
- pagination edge cases
- state mutation
- read and write tool behavior

The tests are written as small executable Python scripts rather than a single test runner configuration, so they can be run individually while developing.

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies from `requirements.txt`.
3. Copy `.env-example` to `.env` and set the values you need.
4. Run the server with `python server.py`.

## Notes

- The server uses in-memory state, so data is not persistent.
- `old_server.py` is present as a legacy server file and can be kept for reference.
- The folder names `unit test/` and `test suite/` contain spaces, so remember to quote them in shell commands.

## Deep Dive Topics

If you are presenting this project or explaining the design, be ready to discuss:

- Why cursor-based pagination is safer than offset pagination for tool-driven clients.
- How `destructiveHint` should influence host behavior.
- What can break if two clients update the same in-memory record concurrently.
- How `outputSchema` helps chained agent workflows.
- Why stdio transport still needs scope enforcement even though it is local.

