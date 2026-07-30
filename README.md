# AgentWatch — Agent Observability Platform

A focused implementation of an agent tracing, evaluation, and guardrails pipeline built across Go, Python, Kafka, Postgres, and React.

## Architecture & Components

- `sdk-python/`: Python instrumentation SDK for tracing agent calls.
- `ingestion-service/`: High-throughput Go ingestion service for consuming trace events and persisting spans & aggregates.
- `eval-service/`: Python microservice for running trace evaluations and guardrail checks.
- `api-service/`: Go REST API serving aggregated metrics, trace waterfalls, and alerts.
- `dashboard/`: React frontend dashboard.
- `infra/`: Infrastructure components (Docker Compose, Kafka, Postgres).

## Local Development Infrastructure

### Postgres Database
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `agentwatch`
- **Username**: `postgres`
- **Password**: `postgres`

Start Postgres via Docker Compose:
```bash
docker compose -f infra/docker-compose.yml up -d
```

