-- Initialize pg_stat_statements extension for fresh databases
-- Existing databases will have the extension created by the startup migration script
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
