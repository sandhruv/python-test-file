def add(a: int, b: int) -> int:
    """Adds two integers."""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtracts b from a."""
    return a - b

def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculates discounted price."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)

def find_user(cursor, name: str):
    """Finds a user by name.
    BUG: SQL injection â€” name is interpolated directly into the query string.
    """
    query = f"SELECT * FROM users WHERE name = '{name}'"
    cursor.execute(query)
    return cursor.fetchone()
