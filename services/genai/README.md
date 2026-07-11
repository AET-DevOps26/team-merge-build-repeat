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

## Chat answer endpoint

```text
POST /v1/chat/answer
Authorization: Bearer <token>
```

Request body:

```json
{
  "gameId": "00000000-0000-0000-0000-000000000000",
  "message": "What is the next step?"
}
```

The service retrieves the current board from `GET /games/{gameId}/state` and
the candidates from `GET /games/{gameId}/pencil-marks` on `GAME_SERVICE_URL`.
It reads the existing chat from the chat database service, generates an
assistant answer using the Sudoku MCP tools, then stores the user message and
assistant response.

Configuration:

```text
CHAT_SERVICE_URL=http://localhost:8081
GENAI_MCP_COMMAND=python
GENAI_MCP_ARGS="-m genai_service.mcp_server"
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=smollm2:135m
GAME_SERVICE_URL=http://localhost:8080
```

Before calculating a Sudoku strategy, the service retrieves the solved board
from `GET /games/{gameId}/solution` and the original puzzle template from
`GET /games/{gameId}/template` on `GAME_SERVICE_URL`. `GAME_SERVICE_URL` may
include an Application context path such as `http://application:8080/application`.
Both endpoints receive the caller's `Authorization` header.

Application is the data source for game state, template, and solution. Sudoku
validation for assistant answers is intentionally local to GenAI: the local MCP
server validates the current board and candidates against the loaded solution
before a strategy is selected.

The current Application service returns a raw 9x9 board matrix. GenAI also
accepts object responses for forward compatibility:

```json
{ "gameId": "...", "solution": [[...]] }
```

```json
{ "gameId": "...", "template": [[...]] }
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
Before a strategy runs, the MCP server validates the board against the solution,
then validates candidates against both the board and the solution. Missing
solution candidates are returned as `missing_candidates`.

## Test

```sh
uv run pytest
```
