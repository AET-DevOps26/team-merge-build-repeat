# API Docs and Swagger Endpoints

## Local

Set the host once:

```bash
LOCAL_IP="${LOCAL_IP:-127.0.0.1}"
```

| Service     | UI                                              | OpenAPI JSON/YAML                      |
| ----------- | ----------------------------------------------- | -------------------------------------- |
| Application | `http://${LOCAL_IP}:8081/swagger-ui/index.html` | `http://${LOCAL_IP}:8081/v3/api-docs`  |
| Chat        | `http://${LOCAL_IP}:8083/swagger-ui/index.html` | `http://${LOCAL_IP}:8083/v3/api-docs`  |
| GenAI       | `http://${LOCAL_IP}:8002/docs`                  | `http://${LOCAL_IP}:8002/openapi.json` |
| Game Engine | `http://${LOCAL_IP}:8082/docs`                  | `http://${LOCAL_IP}:8082/openapi.json` |

FastAPI services also expose ReDoc at `/redoc`.
The frontend, Caddy, and PostgreSQL services do not expose Swagger/OpenAPI
documentation.

## Remote

Remote paths use the ingress/Caddy prefixes:

```bash
REMOTE_BASE_URL="${REMOTE_BASE_URL:-http://<ip-or-domain>}"
```

| Service     | UI                                                     | OpenAPI JSON/YAML                             |
| ----------- | ------------------------------------------------------ | --------------------------------------------- |
| Application | `${REMOTE_BASE_URL}/application/swagger-ui/index.html` | `${REMOTE_BASE_URL}/application/v3/api-docs`  |
| Chat        | `${REMOTE_BASE_URL}/chat/swagger-ui/index.html`        | `${REMOTE_BASE_URL}/chat/v3/api-docs`         |
| GenAI       | `${REMOTE_BASE_URL}/genai/docs`                        | `${REMOTE_BASE_URL}/genai/openapi.json`       |
| Game Engine | `${REMOTE_BASE_URL}/game-engine/docs`                  | `${REMOTE_BASE_URL}/game-engine/openapi.json` |
