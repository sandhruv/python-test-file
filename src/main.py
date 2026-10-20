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

def safe_divide(a: float, b: float) -> float:
    """Divides a by b, returning 0 on any error.
    BUG: bare except â€” swallows KeyboardInterrupt/SystemExit and hides real bugs.
    """
    try:
        return a / b
    except:
        return 0.0
