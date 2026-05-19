# Keyforge API

![Python](https://img.shields.io/badge/Python-24292e?logo=python&logoColor=fff)
![FastAPI](https://img.shields.io/badge/FastAPI-24292e?logo=fastapi&logoColor=fff)
![Pydantic](https://img.shields.io/badge/Pydantic-24292e?logo=pydantic&logoColor=fff)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-24292e?logo=postgresql&logoColor=fff)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-24292e?logo=sqlalchemy&logoColor=fff)
![Alembic](https://img.shields.io/badge/Alembic-24292e?logo=sqlalchemy&logoColor=fff)
![Redis](https://img.shields.io/badge/Redis-24292e?logo=redis&logoColor=fff)
![Docker](https://img.shields.io/badge/Docker-24292e?logo=docker&logoColor=fff)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-24292e?logo=github-actions&logoColor=fff)

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

- **[Python](https://www.python.org/)** — Core language with async/await capabilities.
- **[FastAPI](https://fastapi.tiangolo.com/)** — High-performance async REST API framework.
- **[Pydantic](https://docs.pydantic.dev/)** — Powerful data parsing, validation, and serialization leveraging Python type hints.
- **[PostgreSQL](https://www.postgresql.org/)** — Robust relational database system.
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — Modern async ORM for database interactions.
- **[Alembic](https://alembic.sqlalchemy.org/)** — Lightweight database migration tool for usage with SQLAlchemy.
- **[Redis](https://redis.io/)** — In-memory storage for token lifecycle management and rate-limiting.
- **[Docker](https://www.docker.com/)** — Containerized multi-service environment (App, DB, Cache).
- **[GitHub Actions](https://github.com/features/actions)** — Automated CI/CD pipeline for testing and linting.

## 🏗️ Project Architecture & Design Patterns

The project is built using a highly scalable, modular **Layered Architecture** focused on separation of concerns and maintainability. It leverages **Dependency Injection (DI)** extensively via FastAPI's built-in dependency system, making the codebase loosely coupled and 100% testable.

### 📁 Directory Structure
- `src/keyforge/` — Root package of the application.
  - `core/` — Global configurations, database connections (PostgreSQL, Redis), security/hashing helpers, and central initializations.
  - `auth/`, `users/`, `clients/`, `tokens/` — Independent domain modules (features).
  - `main.py` — Application entry point and router wiring.

### 🧬 The Three-Layer Pattern (Per Feature)
Each domain module (e.g., `users`, `clients`) is strictly decoupled into three architectural layers:

1. **Router Layer (`routers.py`)** — Handles incoming HTTP requests, input data validation via Pydantic schemas, and defines API endpoints.
2. **Service Layer (`services.py`)** — Contains core business logic, orchestrates use cases, handles exceptions, and enforces security constraints.
3. **Repository Layer (`repositories.py`)** — Abstracts data access. Interacts directly with the database via SQLAlchemy async sessions, completely isolating the business logic from raw database queries.

### 💉 Dependency Injection Example
By decoupling layers, dependencies are explicitly injected downward (`Router -> Service -> Repository`). This design pattern ensures that replacing database engines or mocking components during automated testing requires zero changes to the business logic.

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose

### Quick Start

1. Clone the repository and navigate into it:
```bash
git clone https://github.com/mykytakuzminov/keyforge-api.git
cd keyforge-api
```
2. Set up environment variables:
```bash
cp .env.example .env
```

*(Open `.env` and fill in your custom secret keys and credentials).*

3. Run the complete ecosystem via Docker Compose:
```bash
docker compose up -d
```

4. Run database migrations:
```bash
docker compose exec app .venv/bin/alembic upgrade head
```

Once started, the interactive API documentation will be live at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## ⚙️ API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/auth/register` | Register a new system user | — |
| `POST` | `/auth/token` | User login (returns JWT access and refresh tokens) | — |
| `POST` | `/auth/refresh` | Obtain a new access token using a refresh token | — |
| `POST` | `/auth/logout` | Revoke tokens and blacklist current session | Required |
| `GET` | `/auth/userinfo` | Fetch current authenticated user profile | Required |

### User Management
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/users/` | List or search users by email | **Admin** |
| `GET` | `/users/{id}` | Get detailed user profile by ID | **Admin** |
| `POST` | `/users/` | Create a new user manually | **Admin** |
| `PATCH` | `/users/{id}` | Partially update user profile | User / Admin |
| `DELETE` | `/users/{id}` | Soft/Hard delete user account | User / Admin |

### Client Management (OAuth2)
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/clients/` | List all registered client applications | **Admin** |
| `POST` | `/clients/` | Register a new client application | **Admin** |
| `GET` | `/clients/{id}` | Get client details by ID | **Admin** |
| `PATCH` | `/clients/{id}` | Modify client settings or redirect URIs | **Admin** |
| `DELETE` | `/clients/{id}` | Revoke client application credentials | **Admin** |

## 🔧 Development & Code Quality

This project uses `uv` — an ultra-fast Python package installer and resolver.

### Local Installation

Install dependencies into a managed virtualenv

```bash
uv sync
```

### Running Quality Checks Locally

To maintain enterprise-grade code quality, the following tools are integrated and enforced via CI:

* **Testing:** Powered by `pytest` with async support.
```bash
uv run pytest tests/
```

* **Linting & Formatting:** Handled by `ruff` (replaces black, flake8, isort).
```bash
uv run ruff check
```

* **Static Type Checking:** Enforced using `mypy` with strict mode features.
```bash
uv run mypy src/
```
