
# Hotel Operations API

A REST API for managing hotel maintenance issues, built with Python, FastAPI, PostgreSQL, SQLAlchemy and Docker.

## Features

- Create, view, update and delete maintenance issues
- JWT-based authentication
- PostgreSQL database with SQLAlchemy
- Database migrations using Alembic
- Automated tests using pytest
- Docker Compose for local development
- Automatic database migrations during Docker startup

## Technology Stack

- Python 3.13
- FastAPI
- PostgreSQL 17
- SQLAlchemy
- Alembic
- PyJWT
- Argon2 password hashing
- pytest
- Docker and Docker Compose

## Getting Started

### Prerequisites

- Docker Desktop with Docker Compose
- Git

### 1. Clone the repository

```bash
git clone https://github.com/JJRogueWolf/hotel-operations-api.git
cd hotel-operations-api
```

### 2. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and replace the placeholder credentials.

Generate a JWT secret using Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Generate an Argon2 password hash using the project's Python environment:

```python
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
print(password_hash.hash("your_admin_password"))
```

Set `AUTH_PASSWORD_HASH` to the generated hash. Keep it single-quoted in `.env` so Docker Compose does not interpret the `$` characters.

For Docker Compose, set `DOCKER_DB_PASSWORD` to a strong password.

Never commit `.env` or real credentials.

### 3. Start the application

```bash
docker compose up -d --build
```

Docker Compose will:

1. Start PostgreSQL.
2. Wait for the database to become healthy.
3. Apply Alembic migrations.
4. Start the FastAPI application.

Check container status:

```bash
docker compose ps -a
```

### 4. Access the API

Swagger documentation:

http://localhost:8000/docs

Health check:

http://localhost:8000/health

### 5. Authentication

The issue endpoints require JWT authentication.

In Swagger UI:

1. Click **Authorize**.
2. Enter the username and password configured in `.env`.
3. Confirm authorization.
4. Use the protected `/issues` endpoints.

Calling `/auth/login` directly returns an access token, but does not automatically authorize subsequent Swagger requests.

### 6. API endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/health` | Check API health | No |
| POST | `/auth/login` | Obtain JWT access token | No |
| GET | `/issues` | List maintenance issues | Yes |
| GET | `/issues/{id}` | Retrieve an issue | Yes |
| POST | `/issues` | Create an issue | Yes |
| PATCH | `/issues/{id}` | Update an issue | Yes |
| DELETE | `/issues/{id}` | Delete an issue | Yes |

### 7. Run tests

Tests use a separate PostgreSQL test database and require the local test configuration.

With the Python virtual environment activated and the test database configured:

```bash
pytest -q
```

Do not point the test configuration at a database containing important data.

### 8. Stop the application

```bash
docker compose down
```

This stops and removes the containers while preserving the PostgreSQL named volume.

**Warning:** `docker compose down -v` also removes the named volume and deletes the database data stored in it.

## Project Status

The application is functional and containerized for local development.

Before production deployment, additional configuration is required, including separate database roles for migrations and runtime access, production secrets, and secure deployment settings.
