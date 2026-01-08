# Testing Guide

This project ships with a minimal pytest suite covering unit and integration behaviour. Extend from here as needed.

## Setup
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Run Tests
```bash
venv/bin/python -m pytest
```
Use `-v` for verbose output.

## Current Coverage
- **Unit:** `Shop.available_quantity` sums only active foods.
- **Integration:** Login → add to cart → checkout → asserts an `Order` is created and `Food.quantity` is decremented.

Both use SQLite in-memory for speed and isolation.

## Why SQLite for Tests
- Fast, hermetic per test run.
- Avoids touching your Postgres data.
- Works out of the box on most CI runners.

When adding DB-heavy tests, keep using `app.app_context()` and the in-memory URI for deterministic runs.
