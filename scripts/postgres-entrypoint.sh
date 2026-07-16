#!/bin/bash
# Wrapper script for PostgreSQL to ensure pg_stat_statements is created
# This runs before PostgreSQL starts and handles both fresh and existing databases

set -e

# Start PostgreSQL in the background
exec docker-entrypoint.sh postgres "$@" &
PG_PID=$!

# Wait for PostgreSQL to be ready
until pg_isready -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" 2>/dev/null; do
  if ! kill -0 $PG_PID 2>/dev/null; then
    wait $PG_PID
    exit $?
  fi
  sleep 1
done

echo "PostgreSQL is ready. Ensuring pg_stat_statements extension..."

# Attempt to create the extension using the appropriate password file
if [ -n "$POSTGRES_PASSWORD_FILE" ] && [ -f "$POSTGRES_PASSWORD_FILE" ]; then
  export PGPASSWORD=$(cat "$POSTGRES_PASSWORD_FILE")
elif [ -n "$POSTGRES_PASSWORD" ]; then
  export PGPASSWORD="$POSTGRES_PASSWORD"
fi

psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c "CREATE EXTENSION IF NOT EXISTS pg_stat_statements;" || true

echo "pg_stat_statements extension migration complete."

# Wait for the main PostgreSQL process to finish
wait $PG_PID
