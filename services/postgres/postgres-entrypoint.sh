#!/bin/bash
# Wrapper script for PostgreSQL to ensure pg_stat_statements is created
# This runs before PostgreSQL starts and handles both fresh and existing databases

set -e

# Start PostgreSQL in the background
docker-entrypoint.sh postgres "$@" &
PG_PID=$!

# Forward signals to PostgreSQL to ensure graceful shutdown
trap 'kill -TERM $PG_PID; wait $PG_PID' SIGTERM SIGINT

# Wait for POSTGRES_USER to be ready — this naturally synchronizes with docker-entrypoint.sh init
until pg_isready -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" 2>/dev/null; do
  if ! kill -0 $PG_PID 2>/dev/null; then
    wait $PG_PID
    exit $?
  fi
  sleep 1
done

echo "PostgreSQL is ready. Ensuring pg_stat_statements extension..."

if [ -n "$POSTGRES_PASSWORD_FILE" ] && [ -f "$POSTGRES_PASSWORD_FILE" ]; then
  export PGPASSWORD=$(cat "$POSTGRES_PASSWORD_FILE")
elif [ -n "$POSTGRES_PASSWORD" ]; then
  export PGPASSWORD="$POSTGRES_PASSWORD"
fi

RETRIES=30
while [ $RETRIES -gt 0 ]; do
  if psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c "CREATE EXTENSION IF NOT EXISTS pg_stat_statements;"; then
    break
  fi
  echo "Database not ready for extension creation, retrying in 2 seconds..."
  sleep 2
  RETRIES=$((RETRIES-1))
done

echo "pg_stat_statements extension migration complete."

# Wait for the main PostgreSQL process to finish
wait $PG_PID
