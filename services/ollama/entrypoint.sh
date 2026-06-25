#!/bin/sh
set -eu

ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama server..."
until ollama list >/dev/null 2>&1; do
  sleep 1
done

echo "Pulling model: ${OLLAMA_MODEL}"
ollama pull "${OLLAMA_MODEL}"

echo "Ollama is ready with model: ${OLLAMA_MODEL}"
wait "$OLLAMA_PID"
