# Health and Info Checks

Set the target once and reuse it in the commands.

Local direct service ports:

```bash
LOCAL_IP="${LOCAL_IP:-127.0.0.1}"
curl -fsS "http://${LOCAL_IP}:8090/health"
curl -fsS "http://${LOCAL_IP}:8081/actuator/health"
curl -fsS "http://${LOCAL_IP}:8081/actuator/info"
curl -fsS "http://${LOCAL_IP}:8083/actuator/health"
curl -fsS "http://${LOCAL_IP}:8083/actuator/info"
curl -fsS "http://${LOCAL_IP}:8002/actuator/health"
curl -fsS "http://${LOCAL_IP}:8002/actuator/info"
curl -fsS "http://${LOCAL_IP}:8082/actuator/health"
curl -fsS "http://${LOCAL_IP}:8082/actuator/info"
```

The frontend exposes `/health` only. Caddy and PostgreSQL do not expose
application-style HTTP `/actuator/info` endpoints.

Local through Caddy, when the `proxy` profile is running. The local Caddyfile
routes only to the frontend:

```bash
LOCAL_IP="${LOCAL_IP:-127.0.0.1}"
CADDY_PORT="${CADDY_PORT:-8088}"
curl -fsS "http://${LOCAL_IP}:${CADDY_PORT}/health"
```

Remote through Kubernetes ingress or production Caddy:

```bash
REMOTE_BASE_URL="${REMOTE_BASE_URL:-http://<ip-or-domain>}"
curl -fsS "${REMOTE_BASE_URL}/health"
curl -fsS "${REMOTE_BASE_URL}/application/actuator/health"
curl -fsS "${REMOTE_BASE_URL}/application/actuator/info"
curl -fsS "${REMOTE_BASE_URL}/chat/actuator/health"
curl -fsS "${REMOTE_BASE_URL}/chat/actuator/info"
curl -fsS "${REMOTE_BASE_URL}/genai/actuator/health"
curl -fsS "${REMOTE_BASE_URL}/genai/actuator/info"
curl -fsS "${REMOTE_BASE_URL}/game-engine/actuator/health"
curl -fsS "${REMOTE_BASE_URL}/game-engine/actuator/info"
```

PostgreSQL containers are checked by Docker/Kubernetes readiness probes, not by
HTTP curl endpoints.
