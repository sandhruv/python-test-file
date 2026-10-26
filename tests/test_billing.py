import sqlite3

import pytest

from src.billing import (
    add_line,
    apply_discount,
    connect,
    create_invoice,
    format_cents,
    init_db,
    invoice_status,
    invoice_subtotal_cents,
    invoice_total_cents,
    mark_invoice_paid,
    parse_amount_to_cents,
)


@pytest.fixture
def conn():
    connection = connect(":memory:")
    init_db(connection)
    yield connection
    connection.close()


def test_invoice_subtotal(conn):
    invoice_id = create_invoice(conn, 1)
    add_line(conn, invoice_id, "Widget", 3, 250)
    add_line(conn, invoice_id, "Gadget", 1, 1000)
    assert invoice_subtotal_cents(conn, invoice_id) == 1750


def test_invoice_total_with_discount_and_tax(conn):
    invoice_id = create_invoice(conn, 1)
    add_line(conn, invoice_id, "Widget", 2, 1000)
    assert invoice_total_cents(conn, invoice_id, 10, 5) == 1890


def test_apply_discount_rejects_invalid_percent():
    with pytest.raises(ValueError):
        apply_discount(1000, 120)


def test_mark_invoice_paid(conn):
    invoice_id = create_invoice(conn, 1)
    add_line(conn, invoice_id, "Widget", 1, 500)
    mark_invoice_paid(conn, invoice_id)
    assert invoice_status(conn, invoice_id) == "paid"


def test_format_cents():
    assert format_cents(123456) == "1234.56 USD"
    assert format_cents(-500) == "-5.00 USD"


def test_parse_amount_to_cents():
    assert parse_amount_to_cents("1,234.5") == 123450
    assert parse_amount_to_cents("-0.99") == -99
