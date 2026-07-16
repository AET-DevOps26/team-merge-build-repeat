FROM ollama/ollama:latest

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV OLLAMA_MODEL=qwen3:4b

ENTRYPOINT ["/entrypoint.sh"]
