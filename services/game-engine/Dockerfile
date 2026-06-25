FROM python:3.12-slim AS builder

ARG APP_VERSION=0.0.1-SNAPSHOT

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && python -m pip install --upgrade pip setuptools wheel \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create virtualenv and install FastAPI with standard extras (includes uvicorn, pydantic, etc.)
RUN python -m venv .venv \
  && .venv/bin/pip install --upgrade pip setuptools wheel \
  && .venv/bin/pip install --no-cache-dir "fastapi[standard]>=0.115.0" "py-sudoku>=2.0.0"

COPY src ./src

FROM python:3.12-slim

ARG APP_VERSION=0.0.1-SNAPSHOT
ARG GIT_COMMIT=unknown

ENV PATH="/app/.venv/bin:$PATH" \
  PYTHONPATH="/app/src:$PYTHONPATH" \
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
COPY --chown=app:app src ./src

USER app
EXPOSE 8080

CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port 8080"]
