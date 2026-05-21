# Team Merge, Build, Repeat

## Problem Statement

Sudoku learners often know whether a move is right or wrong, but not why.
Many Sudoku applications provide hints or mark mistakes, but they rarely explain the reasoning behind a move or teach the techniques needed to improve over time.

This project addresses that gap by building a Sudoku learning platform with integrated AI support.
The goal is to help users solve puzzles while learning the underlying logic through contextual hints, mistake explanations, and strategy guidance.

## Configuration

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

Create the required database password secret with one of these options.

Option 1: create the secret file manually by editing the file.

Option 2: generate the secret with `secretctl`:

```bash
secretctl
```

`secretctl` is available here:

<https://github.com/DarkbreakerDE/secretctl>

The following secret files are expected:

- `secrets/chat_database_password`

## Run The Project

Start the local stack:

```bash
docker compose up -d --build
```

Check the running services:

```bash
docker compose ps
```

Check the application health endpoints:

```bash
curl http://127.0.0.1:8083/actuator/health
```

The default local endpoints are:

- Chat database service: `http://127.0.0.1:8083`
- Application service: `http://127.0.0.1:8081`
- PostgreSQL chat database: `http://127.0.0.1:5431`
- PostgreSQL application: `http://127.0.0.1:5432`

## Stop The Project

Stop the containers while keeping the database volume:

```bash
docker compose down
```

Stop the containers and delete the local database volume:

```bash
docker compose down -v
```

Use `down -v` only when you intentionally want to reset the local PostgreSQL data.
