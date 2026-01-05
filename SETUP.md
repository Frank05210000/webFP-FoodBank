# Setup Guide

This guide walks through configuring and running the Food Bank Booking System locally.

## Prerequisites
- Python 3.13 (recommended) and `pip`
- PostgreSQL running locally with a database named `final-hw`
- (Optional) `virtualenv`

## 1. Clone & Enter Project
```bash
git clone <repo-url>
cd webFP-FoodBank
```

## 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```
(Windows PowerShell: `venv\Scripts\Activate`)

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Configure Environment
Export any overrides (e.g. use a different PostgreSQL URL):
```bash
export DATABASE_URL=postgresql://<user>:<password>@localhost/<db>
export SECRET_KEY=<your-secret>
```

Default `Config` already points to `postgresql://postgres:shi2xiu1@localhost/final-hw`.

## 5. Initialize Database
```bash
flask --app app.py db upgrade
```

To load demo data:
```bash
python seed.py
```
This resets tables, seeds demo users/shops/foods.

## 6. Run Development Server
```bash
flask --app app.py run --port 5001 --debug
```

Visit `http://localhost:5001/`.

## Demo Accounts
- User: `user@example.com` / `password`
- Shop: `shop1@example.com` / `password`
- Admin: `admin@example.com` / `admin123`

## 7. Useful CLI Commands
- `flask --app app.py db migrate -m "message"`
- `flask --app app.py db downgrade`
- `flask --app app.py init-db` (legacy SQLite helper)

## 8. Tests / Lint
Not included yet. Add your favourite test runner if needed.

## Troubleshooting
- Verify PostgreSQL is running and accessible.
- Delete `migrations/` and recreate if schema drift becomes unmanageable.
- Clear session cookies if login state behaves unexpectedly.
