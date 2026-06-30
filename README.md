<div align="center">

# 🚀 Keyforge API

Authentication server with JWT tokens and role-based access control

[![CI](https://github.com/mykytakuzminov/keyforge-api/actions/workflows/ci.yml/badge.svg)](https://github.com/mykytakuzminov/keyforge-api/actions/workflows/ci.yml)
[![CD](https://github.com/mykytakuzminov/keyforge-api/actions/workflows/cd.yml/badge.svg)](https://github.com/mykytakuzminov/keyforge-api/actions/workflows/cd.yml)
[![Python Version](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=fff)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

[API Docs](http://204.168.173.88:8000/docs)

</div>

---

## Features

- **Auth** - register, login, refresh and logout
- **Users** - get, create, update and delete
- **Clients** - get, create, update and delete

## Tech Highlights

- **Layered Structure** - router, service and repository layers
- **JWT Authentication** - access and refresh token rotation
- **Role-Based Access Control** - admin and member roles to separate features access
- **Rate Limiting** - Fixed Window Counter algorithm to prevent abuse
- **Migrations** - implemented via alembic
- **CI/CD** - automated linting, testing and deploy

## Getting Started

### Prerequisites

- `uv`, `docker` and `docker compose`

### Installation

Set up your `.env` file and run migrations

```bash
git clone https://github.com/mykytakuzminov/keyforge-api.git
cd keyforge-api
cp .env.example .env
docker compose up -d
docker compose exec keyforge-api-app /app/.venv/bin/alembic upgrade head
```

### Development

```bash
uv run tox # run linter, tests
```

## Tech Stack

### Core

- `Python`, `PostgreSQL`, `Redis`, `Docker`, `Docker Compose`, `GitHub Actions`

### Libraries

- `FastAPI`, `SQLAlchemy`, `alembic`, `asyncpg`, `psycopg2-binary`, `Pydantic`

### Dev Tools

- `pytest`, `ruff`, `mypy`, `tox`
