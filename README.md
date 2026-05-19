# keyforge-api

OAuth2 authentication server built with FastAPI, PostgreSQL, and Redis.

## Stack

- **Python 3.14** + **FastAPI** — async REST API
- **PostgreSQL** + **SQLAlchemy** — database with async ORM
- **Alembic** — database migrations
- **Redis** — refresh token storage and rate limiting
- **JWT** — access and refresh token authentication
- **Docker** + **Docker Compose** — containerization
- **GitHub Actions** — CI/CD pipeline
- **Pytest** — async tests with testcontainers

## Features

- User registration and authentication with JWT tokens
- Access token (15 min) + Refresh token (7 days)
- Role-based access control (admin / member)
- Client management for OAuth2 applications
- Rate limiting on auth endpoints
- Automatic token invalidation on logout

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

```bash
git clone https://github.com/mykytakuzminov/keyforge-api.git
cd keyforge-api
cp .env.example .env
# Fill in .env with your values
docker compose up -d
docker compose exec app .venv/bin/alembic upgrade head
```

API docs available at `http://localhost:8000/docs`

## API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Register new user | — |
| POST | `/auth/token` | Login, get tokens | — |
| POST | `/auth/refresh` | Refresh access token | — |
| POST | `/auth/logout` | Logout | Required |
| GET | `/auth/userinfo` | Get current user info | Required |

### Users
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/users/` | Get user by email | Admin |
| GET | `/users/{id}` | Get user by ID | Admin |
| POST | `/users/` | Create user | Admin |
| PATCH | `/users/{id}` | Update user | User |
| DELETE | `/users/{id}` | Delete user | User |

### Clients
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/clients/` | List all clients | Admin |
| POST | `/clients/` | Create client | Admin |
| GET | `/clients/{id}` | Get client by ID | Admin |
| PATCH | `/clients/{id}` | Update client | Admin |
| DELETE | `/clients/{id}` | Delete client | Admin |

## Project Structure

```
src/keyforge/
├── auth/          # Authentication logic
├── clients/       # OAuth2 client management
├── tokens/        # Token repository
├── users/         # User management
└── core/          # Database, Redis, security utils
```

## Environment Variables

```env
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/dbname
ALEMBIC_DATABASE_URL=postgresql+psycopg2://user:password@db:5432/dbname
REDIS_URL=redis://redis:6379
SECRET_KEY=your-secret-key
POSTGRES_DB=dbname
POSTGRES_USER=user
POSTGRES_PASSWORD=password
```

## Running Tests

```bash
uv run pytest tests/
```
