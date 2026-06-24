FROM ollama/ollama:latest

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV OLLAMA_MODEL=gemma4:e4b

ENTRYPOINT ["/entrypoint.sh"]
