import sqlite3
from datetime import datetime, timezone
from typing import List, Optional


def connect(db_path: str = "billing.db") -> sqlite3.Connection:
    """Opens a SQLite connection with row access by column name."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Creates the billing tables if they do not exist yet."""
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            currency TEXT NOT NULL DEFAULT 'USD',
            status TEXT NOT NULL DEFAULT 'draft',
            created_at TEXT NOT NULL,
            paid_at TEXT
        );

        CREATE TABLE IF NOT EXISTS invoice_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
            description TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price_cents INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            amount_cents INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_transactions_account_created
            ON transactions (account_id, created_at);
        """
    )
    conn.commit()


def utc_now_iso() -> str:
    """Returns the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def create_invoice(conn: sqlite3.Connection, account_id: int, currency: str = "USD") -> int:
    """Creates a draft invoice for an account."""
    cursor = conn.execute(
        "INSERT INTO invoices (account_id, currency, created_at) VALUES (?, ?, ?)",
        (account_id, currency, utc_now_iso()),
    )
    conn.commit()
    return int(cursor.lastrowid)


def add_line(
    conn: sqlite3.Connection,
    invoice_id: int,
    description: str,
    quantity: int,
    unit_price_cents: int,
) -> int:
    """Adds a line item to a draft invoice."""
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    if unit_price_cents < 0:
        raise ValueError("unit_price_cents must not be negative")
    if not description.strip():
        raise ValueError("description must not be empty")

    cursor = conn.execute(
        "INSERT INTO invoice_lines (invoice_id, description, quantity, unit_price_cents) "
        "VALUES (?, ?, ?, ?)",
        (invoice_id, description.strip(), quantity, unit_price_cents),
    )
    conn.commit()
    return int(cursor.lastrowid)


def list_lines(conn: sqlite3.Connection, invoice_id: int) -> List[sqlite3.Row]:
    """Returns all line items for an invoice in insertion order."""
    return conn.execute(
        "SELECT * FROM invoice_lines WHERE invoice_id = ? ORDER BY id",
        (invoice_id,),
    ).fetchall()


def line_total_cents(line: sqlite3.Row) -> int:
    """Computes the total for a single invoice line, in cents."""
    return int(line["quantity"]) * int(line["unit_price_cents"])


def invoice_subtotal_cents(conn: sqlite3.Connection, invoice_id: int) -> int:
    """Sums all line totals for an invoice, in cents."""
    total = 0
    for line in list_lines(conn, invoice_id):
        total += line_total_cents(line)
    return total


def validate_discount_percent(percent: float) -> float:
    """Ensures a discount percentage is within the allowed range."""
    if percent < 0 or percent > 100:
        raise ValueError("discount percent must be between 0 and 100")
    return percent


def apply_discount(amount_cents: int, percent: float) -> int:
    """Returns the amount in cents after applying a percentage discount."""
    validate_discount_percent(percent)
    return int(round(amount_cents * (1 - percent / 100)))


def validate_tax_percent(percent: float) -> float:
    """Ensures a tax percentage is within the allowed range."""
    if percent < 0 or percent > 100:
        raise ValueError("tax percent must be between 0 and 100")
    return percent


def tax_cents(amount_cents: int, percent: float) -> int:
    """Returns the tax owed on an amount, in cents."""
    validate_tax_percent(percent)
    return int(round(amount_cents * (percent / 100)))


def invoice_total_cents(
    conn: sqlite3.Connection,
    invoice_id: int,
    discount_percent: float = 0,
    tax_percent: float = 0,
) -> int:
    """Computes the invoice total after discount and tax, in cents."""
    subtotal = invoice_subtotal_cents(conn, invoice_id)
    discounted = apply_discount(subtotal, discount_percent)
    return discounted + tax_cents(discounted, tax_percent)


def mark_invoice_paid(conn: sqlite3.Connection, invoice_id: int) -> None:
    """Marks a draft invoice as paid."""
    row = conn.execute(
        "SELECT status FROM invoices WHERE id = ?", (invoice_id,)
    ).fetchone()
    if row is None:
        raise ValueError("invoice not found")
    if row["status"] == "paid":
        return
    if row["status"] != "draft":
        raise ValueError("only draft invoices can be paid")

    conn.execute(
        "UPDATE invoices SET status = 'paid', paid_at = ? WHERE id = ?",
        (utc_now_iso(), invoice_id),
    )
    conn.commit()


def invoice_status(conn: sqlite3.Connection, invoice_id: int) -> str:
    """Returns the status of an invoice."""
    row = conn.execute(
        "SELECT status FROM invoices WHERE id = ?", (invoice_id,)
    ).fetchone()
    if row is None:
        raise ValueError("invoice not found")
    return str(row["status"])


def record_transaction(
    conn: sqlite3.Connection,
    account_id: int,
    amount_cents: int,
    created_at: Optional[str] = None,
) -> int:
    """Records a posted account transaction."""
    if amount_cents == 0:
        raise ValueError("amount_cents must not be zero")

    cursor = conn.execute(
        "INSERT INTO transactions (account_id, amount_cents, created_at) "
        "VALUES (?, ?, ?)",
        (account_id, amount_cents, created_at or utc_now_iso()),
    )
    conn.commit()
    return int(cursor.lastrowid)


def balance_cents(conn: sqlite3.Connection, account_id: int) -> int:
    """Returns the net balance for an account, in cents."""
    row = conn.execute(
        "SELECT COALESCE(SUM(amount_cents), 0) AS balance "
        "FROM transactions WHERE account_id = ?",
        (account_id,),
    ).fetchone()
    return int(row["balance"])


def format_cents(amount_cents: int, currency: str = "USD") -> str:
    """Formats a cent amount as a human-readable currency string."""
    sign = "-" if amount_cents < 0 else ""
    absolute = abs(int(amount_cents))
    whole, fraction = divmod(absolute, 100)
    return f"{sign}{whole}.{fraction:02d} {currency}"


def parse_amount_to_cents(text: str) -> int:
    """Parses a decimal amount such as '12.34' into cents."""
    cleaned = text.strip().replace(",", "")
    if not cleaned:
        raise ValueError("amount must not be empty")
    negative = cleaned.startswith("-")
    if negative:
        cleaned = cleaned[1:]
    if cleaned.count(".") > 1:
        raise ValueError("amount has more than one decimal point")
    whole, _, fraction = cleaned.partition(".")
    fraction = (fraction + "00")[:2]
    cents = int(whole) * 100 + int(fraction)
    return -cents if negative else cents


def statement_rows(
    conn: sqlite3.Connection,
    account_id: int,
    start_date: str,
    end_date: str,
) -> List[sqlite3.Row]:
    """Returns posted transactions between two ISO dates, inclusive."""
    return conn.execute(
        "SELECT id, account_id, amount_cents, created_at FROM transactions "
        "WHERE account_id = ? AND created_at >= ? AND created_at < ? "
        "ORDER BY created_at, id",
        (account_id, start_date, end_date),
    ).fetchall()
