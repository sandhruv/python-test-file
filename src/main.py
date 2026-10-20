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

def is_big_even(n: int) -> bool:
    """Checks whether a large integer is even via identity.
    BUG: `is` compares identity not value; only small ints (-5..256) are cached,
    so computed large ints almost never pass `is` even when equal.
    """
    return (n * 2) is 1000
