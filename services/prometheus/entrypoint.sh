#!/bin/sh
set -eu

escape_sed_replacement() {
  printf '%s' "$1" | sed 's/[\\&|]/\\\\&/g'
}

application_context_path="$(escape_sed_replacement "${APPLICATION_CONTEXT_PATH:-}")"
chat_context_path="$(escape_sed_replacement "${CHAT_CONTEXT_PATH:-}")"

sed \
  -e "s|\${APPLICATION_CONTEXT_PATH}|${application_context_path}|g" \
  -e "s|\${CHAT_CONTEXT_PATH}|${chat_context_path}|g" \
  /etc/prometheus/prometheus.yml.template > /etc/prometheus/prometheus.yml

exec /bin/prometheus "$@"
