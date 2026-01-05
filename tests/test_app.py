import os
import sys
from datetime import datetime, timedelta

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import User, Shop, Food, Order


@pytest.fixture
def test_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def create_shop():
    shop = Shop(
        name="Integration Shop",
        manager_email="shop@test.com",
        phone="02-0000-0000",
        address="Test Address",
        opening_time=datetime.strptime("09:00", "%H:%M").time(),
        closing_time=datetime.strptime("23:30", "%H:%M").time(),
        latitude=25.0,
        longitude=121.5
    )
    db.session.add(shop)
    db.session.commit()
    return shop


def test_shop_available_quantity_only_counts_active(test_app):
    with test_app.app_context():
        shop = create_shop()
        food_active = Food(
            shop_id=shop.id,
            name="Active Food",
            quantity=5,
            is_active=True
        )
        food_inactive = Food(
            shop_id=shop.id,
            name="Inactive Food",
            quantity=10,
            is_active=False
        )
        db.session.add_all([food_active, food_inactive])
        db.session.commit()

        assert shop.available_quantity == 5


def test_checkout_flow_creates_order_and_updates_inventory(test_app, client):
    pickup_time = (datetime.now() + timedelta(hours=1)).strftime('%H:%M')

    with test_app.app_context():
        user = User(name="Test User", email="user@test.com", role='user')
        user.set_password('password123')
        shop = create_shop()
        food = Food(
            shop_id=shop.id,
            name="Sandwich",
            quantity=4,
            is_active=True
        )
        db.session.add_all([user, food])
        db.session.commit()
        food_id = food.id

    login_resp = client.post('/login', data={
        'email': 'user@test.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert login_resp.status_code == 200

    add_resp = client.post('/cart/add', data={
        'food_id': food_id,
        'quantity': 2
    }, follow_redirects=True)
    assert add_resp.status_code == 200

    checkout_resp = client.post('/checkout', data={
        'pickup_time': pickup_time
    })
    assert checkout_resp.status_code == 302

    with test_app.app_context():
        assert Order.query.count() == 1
        updated_food = Food.query.get(food_id)
        assert updated_food.quantity == 2
