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

## Test

```sh
uv run pytest
```
