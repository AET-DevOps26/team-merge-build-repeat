FROM python:3.12-slim AS builder

ARG APP_VERSION=0.0.1-SNAPSHOT

COPY --from=ghcr.io/astral-sh/uv:0.11.15 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev --no-install-project

COPY src ./src

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev --no-editable


FROM python:3.12-slim

ARG APP_VERSION=0.0.1-SNAPSHOT
ARG GIT_COMMIT=unknown

ENV PATH="/app/.venv/bin:$PATH" \
  PYTHONUNBUFFERED=1 \
  APP_VERSION="${APP_VERSION}" \
  GIT_COMMIT="${GIT_COMMIT}"

RUN apt-get update \
  && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/*

RUN groupadd --system app \
  && useradd --system \
  --gid app \
  --home-dir /home/app \
  --create-home \
  --shell /usr/sbin/nologin \
  app

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv

USER app

EXPOSE 8080

CMD ["sh", "-c", "exec uvicorn genai_service.main:app --host 0.0.0.0 --port 8080"]
