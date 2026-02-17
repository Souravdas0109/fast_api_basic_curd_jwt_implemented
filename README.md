# FastAPI Product API (CRUD + JWT)

Small FastAPI project providing product management for authenticated sellers.

## Features

- JWT-based authentication (`/login/token`) using `python-jose`.
- Seller login and protected product creation that records the authenticated seller's ID.
- SQLite database via SQLAlchemy for lightweight storage.

## Structure

- `Product/` — application package
  - `auth.py` — auth helpers (token creation, current-seller dependency)
  - `database.py` — SQLAlchemy engine and `get_db()`
  - `models.py` — SQLAlchemy models (`Product`, `Seller`)
  - `routers/` — route modules (`product.py`, `seller.py`, `login.py`)
  - `schemas.py` — Pydantic models
- `main.py` — app entry (imports `Product.main` in this project layout)

## Quick start

1. Activate venv (PowerShell):

```powershell
& "venv/Scripts/Activate.ps1"
```

2. Install dependencies:

```powershell
pip install -r requirement.txt
```

3. Run the app:

```powershell
python -m uvicorn Product.main:app --reload
```

## Usage

- Obtain token: `POST /login/token` with JSON `{ "email": "...", "password": "..." }`.
- Create product (authenticated): `POST /products` with `Authorization: Bearer <token>` header.

## Notes

- Replace the `SECRET_KEY` in `Product/auth.py` with a secure environment variable before deploying.
- Plain-text passwords in the DB are re-hashed on first successful login; consider adding a signup path to store hashed passwords immediately.
