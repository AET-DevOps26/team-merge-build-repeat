FROM postgres:17

COPY --chmod=0755 postgres-entrypoint.sh \
    /usr/local/bin/custom-postgres-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/custom-postgres-entrypoint.sh"]

CMD ["-c", "shared_preload_libraries=pg_stat_statements"]
