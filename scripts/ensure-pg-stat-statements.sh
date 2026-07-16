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

# Create extension in the main database
PGPASSFILE=/run/secrets/app_database_password psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c "CREATE EXTENSION IF NOT EXISTS pg_stat_statements;" || \
PGPASSFILE=/run/secrets/chat_database_password psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c "CREATE EXTENSION IF NOT EXISTS pg_stat_statements;" || true

echo "pg_stat_statements extension ensured."
