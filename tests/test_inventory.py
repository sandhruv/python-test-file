import sqlite3

import pytest

from src.inventory import available_stock, init_db, reserve_stock


@pytest.fixture
def conn():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    init_db(connection)
    connection.execute(
        "INSERT INTO stock (sku, available) VALUES (?, ?)", ("SKU-1", 5)
    )
    connection.commit()
    yield connection
    connection.close()


def test_reserve_stock_reduces_available(conn):
    assert reserve_stock(conn, "SKU-1", 2) is True
    assert available_stock(conn, "SKU-1") == 3


def test_reserve_stock_insufficient(conn):
    assert reserve_stock(conn, "SKU-1", 6) is False
    assert available_stock(conn, "SKU-1") == 5


def test_reserve_stock_unknown_sku(conn):
    assert reserve_stock(conn, "SKU-404", 1) is False


def test_reserve_stock_rejects_non_positive(conn):
    with pytest.raises(ValueError):
        reserve_stock(conn, "SKU-1", 0)
