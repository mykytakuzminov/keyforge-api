# Keyforge API

![Python](https://img.shields.io/badge/Python-376996?logo=python&logoColor=fff)
![FastAPI](https://img.shields.io/badge/FastAPI-376996?logo=fastapi&logoColor=fff)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-376996?logo=postgresql&logoColor=fff)
![Alembic](https://img.shields.io/badge/Alembic-376996?logo=postgresql&logoColor=fff)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-376996?logo=sqlalchemy&logoColor=fff)
![Redis](https://img.shields.io/badge/Redis-376996?logo=redis&logoColor=fff)
![Docker](https://img.shields.io/badge/Docker-376996?logo=docker&logoColor=fff)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-376996?logo=github-actions&logoColor=fff)
![Uv](https://img.shields.io/badge/Uv-376996?logo=uv&logoColor=fff)
![Ruff](https://img.shields.io/badge/Ruff-376996?logo=ruff&logoColor=fff)
![Mypy](https://img.shields.io/badge/Mypy-376996?logo=python&logoColor=fff)
![Pytest](https://img.shields.io/badge/Pytest-376996?logo=pytest&logoColor=fff)

> OAuth2 authentication server built with FastAPI, PostgreSQL, and Redis — featuring role-based access control, token management, and modern async toolchain.

## 🗺️ Features

| Feature | Description |
|---|---|
| JWT Authentication | Access token (15 min) + Refresh token (7 days) management |
| Client Management | Full lifecycle control over OAuth2 client applications |
| RBAC | Role-based access control (Admin and Member levels) |
| Security & Safety | Rate limiting on auth endpoints and automatic token invalidation on logout |
| Storage Strategy | PostgreSQL for persistent data, Redis for storage and quick validation of refresh tokens |

## 🛠️ Tech Stack

- **[python](https://www.python.org/)** — core language, 3.14 with async capabilities
- **[fastapi](https://fastapi.tiangolo.com/)** — high-performance async REST API framework
- **[postgresql](https://www.postgresql.org/)** — powerful, open-source object-relational database system
- **[alembic](https://alembic.sqlalchemy.org/)** — database schema migrations management
- **[sqlalchemy](https://www.sqlalchemy.org/)** — robust SQL toolkit and async Object Relational Mapper (ORM)
- **[redis](https://redis.io/)** — high-speed refresh token storage and rate limiting implementation
- **[docker](https://www.docker.com/)** — containerized deployment and environment consistency
- **[github actions](https://github.com/features/actions)** — automated CI/CD pipeline on push and pull requests
- **[uv](https://github.com/astral-sh/uv)** — blazing fast package and environment management
- **[ruff](https://github.com/astral-sh/ruff)** — fast linting and code formatting in one tool
- **[mypy](http://mypy-lang.org/)** — strict static type checking across the entire codebase
- **[pytest](https://docs.pytest.org/)** — async testing ecosystem with testcontainers

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose

### Setup

```bash
git clone [https://github.com/mykytakuzminov/keyforge-api.git](https://github.com/mykytakuzminov/keyforge-api.git)
cd keyforge-api
cp .env.example .env
```

Fill in your values in `.env`, then run:

```bash
docker compose up -d
docker compose exec app .venv/bin/alembic upgrade head
```

API documentation will be available at `http://localhost:8000/docs`

## ⚙️ API Endpoints

### Auth

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | /auth/register | Register new user | — |
| POST | /auth/token | Login, get tokens | — |
| POST | /auth/refresh | Refresh access token | — |
| POST | /auth/logout | Logout | Required |
| GET | /auth/userinfo | Get current user info | Required |

### User

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | /users/ | Get user by email | Admin |
| GET | /users/{id} | Get user by ID | Admin |
| POST | /users/ | Create user | Admin |
| PATCH | /users/{id} | Update user | User |
| DELETE | /users/{id} | Delete user | User |

### Client

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | /clients/ | List all clients | Admin |
| POST | /clients/ | Create client | Admin |
| GET | /clients/{id} | Get client by ID | Admin |
| PATCH | /clients/{id} | Update client | Admin |
| DELETE | /clients/{id} | Delete client | Admin |

## 🔧 Development & Testing

```bash
uv sync
uv run pytest tests/
uv run ruff check
uv run mypy /src
```
