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

def percentage(part: float, total: float) -> float:
    """Returns part as a percentage of total.
    BUG: no guard for total == 0 â€” ZeroDivisionError on empty totals.
    """
    return (part / total) * 100
