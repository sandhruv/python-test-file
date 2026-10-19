import pytest
from src.main import add, subtract, calculate_discount

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 2) == 3
    assert subtract(0, 5) == -5

def test_calculate_discount():
    assert calculate_discount(100.0, 10.0) == 90.0
    assert calculate_discount(200.0, 50.0) == 100.0

def test_calculate_discount_invalid():
    with pytest.raises(ValueError):
        calculate_discount(100.0, -5.0)
    with pytest.raises(ValueError):
        calculate_discount(100.0, 105.0)
