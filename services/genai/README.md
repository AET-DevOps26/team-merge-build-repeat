# GenAI Service

Python FastAPI service for the Sudoku GenAI component.

## Setup

```sh
uv sync
```

## Run

```sh
uv run fastapi dev src/genai_service/main.py
```

The service exposes a Spring Boot Actuator style health endpoint:

```text
GET /actuator/health
```

Expected response:

```json
{ "status": "UP" }
```

## MCP server

The Sudoku library is also exposed as a local MCP server for LangChain tools.
It uses stdio transport:

```sh
uv run python -m genai_service.mcp_server
```

Example LangChain configuration with `langchain-mcp-adapters`:

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "sudoku": {
            "command": "uv",
            "args": ["run", "python", "-m", "genai_service.mcp_server"],
            "transport": "stdio",
        }
    }
)

tools = await client.get_tools()
```

Boards are JSON 9x9 integer grids. Candidate boards are JSON 9x9 grids where
each cell contains a list of candidate integers, for example `[1, 2, 3]`.

## Test

```sh
uv run pytest
```
