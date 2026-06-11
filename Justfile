base := "-f docker-compose.yaml"
dev_files := base + " -f docker-compose.dev.yaml"
prod_files := base + " -f docker-compose.prod.yaml"

# Show available commands
default:
    just --list

# Forward any docker compose command to the dev compose stack
dev +args:
    docker compose {{dev_files}} {{args}}

# Forward any docker compose command to the prod compose stack
prod +args:
    docker compose {{prod_files}} {{args}}
