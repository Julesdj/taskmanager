# 🏗️ FastAPI Task Management Backend

A clean, async-first task management backend built with **FastAPI**, **SQLAlchemy (async)**, and **PostgreSQL**.

## ✨ Features

-   ✅ User registration & login
-   🔐 JWT-based authentication with access & refresh tokens
-   🔒 Session-aware token revocation
-   👤 Ownership-based task access
-   🔍 Search, filtering, ordering, pagination
-   📦 Clean, layered architecture (API / Services / Repos)

---

## 🧱 Tech Stack

-   ⚡ FastAPI (async-first web framework)
-   🐘 PostgreSQL with SQLAlchemy (async ORM)
-   🔐 JWT via `python-jose`
-   🔑 Password hashing with `passlib` (bcrypt)
-   📚 Alembic for migrations
-   ☁️ Environment-based config with `.env`

---

## 📁 Project Structure

```text
app/
├── api/ # FastAPI routes
├── core/ # Security, settings
├── db/ # DB session, base class
├── models/ # SQLAlchemy models
├── repositories/ # DB queries (data layer)
├── schemas/ # Pydantic models
├── services/ # Business logic
└── main.py # Entry point
```

---

## 🛠️ Setup

### Requirements

-   Python 3.11+
-   PostgreSQL
-   pip or Poetry

### Installation

```bash
# Clone the repo
git clone https://github.com/Julesdj/taskmanager
cd taskmanager

# Create virtualenv
python -m venv venv && source venv/bin/activate

# Install dependencies
pip install -r requirements.txt  # or `poetry install`
```

### Environment

Create a `.env` file in the root:

```bash
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
SECRET_KEY=your_super_secret_key
REFRESH_SECRET_KEY=your_super_refresh_secret_key
```

### ⚙️ Running the App

```bash
alembic upgrade head  # Run DB migrations
fastapi dev           # Start development server
```

For production, consider using `gunicorn` with `uvicorn.workers.UvicornWorker`.

## 🧪 API Overview

### 🔐 Auth

| Method | Endpoint         | Description                                 |
| ------ | ---------------- | ------------------------------------------- |
| POST   | `/auth/login`    | Login user, returns access + refresh tokens |
| POST   | `/auth/logout`   | Logout user (revoke tokens)                 |
| POST   | `/auth/refresh`  | Rotate and return new tokens                |
| GET    | `/auth/sessions` | List active sessions                        |

### 👤 Users

| Method | Endpoint    | Description           |
| ------ | ----------- | --------------------- |
| POST   | `/users`    | Register new user     |
| GET    | `/users/me` | Get current user info |

### 📋 Tasks

| Method | Endpoint      | Description                           |
| ------ | ------------- | ------------------------------------- |
| GET    | `/tasks`      | List tasks (search, filter, paginate) |
| POST   | `/tasks`      | Create task                           |
| PATCH  | `/tasks/{id}` | Update task                           |
| DELETE | `/tasks/{id}` | Delete task                           |

## ✅ Next Steps

-   Add task ownership
-   Add role-based permissions (admin, user, etc.)
-   Write unit & integration tests
-   Add Docker support for deployment
-   CI pipeline (GitHub Actions or similar)
