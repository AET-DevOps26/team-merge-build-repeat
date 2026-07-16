FROM prom/prometheus:latest

USER root

COPY --chown=nobody:nobody prometheus.yml /etc/prometheus/prometheus.yml.template
COPY --chown=nobody:nobody entrypoint.sh /bin/render-prometheus-config

# The Prometheus image runs as nobody. Create the rendered-config target during
# the image build so it can be overwritten at container startup.
RUN touch /etc/prometheus/prometheus.yml \
    && chown nobody:nobody /etc/prometheus/prometheus.yml \
    && chmod 0755 /bin/render-prometheus-config

USER nobody

ENTRYPOINT ["/bin/render-prometheus-config"]
CMD ["--config.file=/etc/prometheus/prometheus.yml", "--storage.tsdb.path=/prometheus"]
