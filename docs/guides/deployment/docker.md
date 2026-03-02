# Docker Deployment Guide

## Local Development

```bash
pnpm docker:up       # Start Postgres + Redis
pnpm dev             # Start all apps
```

## Production (Single Server)

```bash
docker compose -f infra/docker/docker-compose.yml up -d --build
docker compose logs -f api
```

## Updating

```bash
git pull
docker compose -f infra/docker/docker-compose.yml up -d --build --no-deps api
```
