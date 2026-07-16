FROM prometheuscommunity/postgres-exporter:latest

COPY --chown=65534:65534 \
    pg_stat_statements_queries.yaml \
    /etc/postgres_exporter/queries.yaml
