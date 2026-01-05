# Testing Guide

This project ships with a minimal, but illustrative, pytest suite that covers two layers: unit behaviour inside models and an end-to-end booking flow. Below summarizes the setup and current coverage so you can extend it further.

## 1. Setup
```bash
source venv/bin/activate
pip install -r requirements.txt  # installs pytest and dependencies
```

## 2. Running Tests
```bash
# Run entire suite
venv/bin/python -m pytest

# Run with verbose output
venv/bin/python -m pytest -v
```

Pytest automatically discovers tests under the `tests/` folder. CI or local scripts can use the same commands.

## 3. Current Coverage
- **Unit Test – `test_shop_available_quantity_only_counts_active`**
  - Uses an in-memory SQLite database so the schema is recreated per test without touching the real PostgreSQL instance.
  - Creates a `Shop` with both active/inactive `Food` records and asserts `Shop.available_quantity` only sums `is_active=True` items. This guards the homepage badge logic.

- **Integration Test – `test_checkout_flow_creates_order_and_updates_inventory`**
  - Spins up the Flask app in testing mode, inserts demo user/shop/food rows, then uses the Flask test client to simulate: login → POST `/cart/add` → POST `/checkout`.
  - After the flow it verifies the database now has one `Order` and that the selected `Food.quantity` decreased by the amount booked. This ensures customer-facing logic hits the database as expected.

## 4. Why SQLite for Tests?
- **Speed & Isolation**: In-memory SQLite starts/stops instantly per test, so test runs remain fast and hermetic.
- **No Side Effects**: PostgreSQL would require cleaning between tests and risks altering dev data. Using SQLite ensures the real database stays untouched.
- **Portability**: CI runners and new contributors can run the suite without configuring PostgreSQL locally.

You can add additional tests (e.g., more order scenarios, admin actions) by following the structure in `tests/test_app.py`. When writing DB-heavy tests, keep using `app.app_context()` and the in-memory URI to keep runs deterministic.
