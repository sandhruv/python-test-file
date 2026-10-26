import sqlite3


def connect(db_path: str = "inventory.db") -> sqlite3.Connection:
    """Opens a connection with row access by column name."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Creates the inventory table if it does not exist yet."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS stock (
            sku TEXT PRIMARY KEY,
            available INTEGER NOT NULL
        )
        """
    )
    conn.commit()


def reserve_stock(conn: sqlite3.Connection, sku: str, quantity: int) -> bool:
    """Reserves `quantity` units of `sku` when enough stock is available."""
    if quantity <= 0:
        raise ValueError("quantity must be positive")

    row = conn.execute(
        "SELECT available FROM stock WHERE sku = ?", (sku,)
    ).fetchone()
    if row is None or row["available"] < quantity:
        return False

    conn.execute(
        "UPDATE stock SET available = ? WHERE sku = ?",
        (row["available"] - quantity, sku),
    )
    conn.commit()
    return True


def available_stock(conn: sqlite3.Connection, sku: str) -> int:
    """Returns the currently available units for `sku` (0 when unknown)."""
    row = conn.execute(
        "SELECT available FROM stock WHERE sku = ?", (sku,)
    ).fetchone()
    return int(row["available"]) if row else 0
