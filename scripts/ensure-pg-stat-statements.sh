#!/bin/bash
# Ensure pg_stat_statements extension is created in all databases
# This script handles both fresh databases (via init-db.d) and existing persistent volumes

set -e

# Wait for PostgreSQL to be ready
until pg_isready -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

echo "PostgreSQL is ready. Creating pg_stat_statements extension..."

# Create extension, using available password secrets
if [ -f "/run/secrets/app_database_password" ]; then
  export PGPASSWORD=$(cat /run/secrets/app_database_password)
elif [ -f "/run/secrets/chat_database_password" ]; then
  export PGPASSWORD=$(cat /run/secrets/chat_database_password)
fi

psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c "CREATE EXTENSION IF NOT EXISTS pg_stat_statements;" || true

echo "pg_stat_statements extension ensured."
