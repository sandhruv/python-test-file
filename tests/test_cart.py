import pytest
from src.cart import apply_coupon, cart_subtotal


def test_cart_subtotal():
    items = [
        {"price": 25.0, "quantity": 2},
        {"price": 10.0, "quantity": 1},
    ]
    assert cart_subtotal(items) == 60.0


def test_apply_coupon():
    items = [{"price": 100.0, "quantity": 2}]
    assert apply_coupon(items, 10) == 180.0


def test_apply_coupon_invalid():
    items = [{"price": 50.0, "quantity": 1}]
    with pytest.raises(ValueError):
        apply_coupon(items, -5)
    with pytest.raises(ValueError):
        apply_coupon(items, 75)
